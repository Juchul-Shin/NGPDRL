import torch
import torch_geometric.utils as U
from environment import make_batch
from models import ACNet
import torch.nn.functional as F
from copy import deepcopy as dc
from collections import deque
import random



def get_returns(rews,gamma=1.0):
    R = torch.zeros(len(rews))
    R[-1] = rews[-1]
    for i in range(1,len(rews)):
        R[-i-1] = rews[-i-1] + (gamma**(i+1))*R[-i]
    return R


class SimpleBuffer:
    def __init__(self,max_len=100000):
        self.max_len = max_len
        if max_len is not None:
            self.init_buffer = deque(maxlen=self.max_len)
        else:
            self.init_buffer = deque()
        self.buffer = dc(self.init_buffer)
        
    def keep(self,memory):
        self.buffer.append(memory)
        
    def sample(self,batch_size):
        K = min([len(self.buffer),batch_size])
        samples = dc(random.sample(self.buffer, K))
        return samples
    
    def clean(self):
        self.buffer = dc(self.init_buffer)
        
        
class Proportional:
    def __init__(self, entropy_flag=False):
        self.entropy_flag = entropy_flag
        
    def sample(self,pi):
        pi = F.softmax(pi.squeeze(),dim=0)
        dist = torch.distributions.categorical.Categorical(pi.squeeze())
        action = dist.sample().item()
        if self.entropy_flag == True:
            entropy = dist.entropy()
            return action, pi, entropy
        else:
            return action, pi


class PPO:
    def __init__(self, env, eval_env, gamma, num_episodes, batch_size, use_attention):
        self.env = env
        self.eval_env = eval_env
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   
        print('device == {}'.format(self.device))
        hid = 256
        glob_in, node_in, edge_in = env.get_dims()


        self.total_actions = set()
        
        self.model = ACNet(node_in, edge_in, glob_in, hid, env.n_history, use_attention).to(self.device)
        self.old_model = ACNet(node_in, edge_in, glob_in, hid, env.n_history, use_attention).to(self.device)
        
        self.model.load_state_dict(self.model.state_dict())
        
        self.old_model.load_state_dict(self.model.state_dict())
        self.n_updates = 20
        self.eps_clip = 0.2
        self.target_kl = 0.01
        self.gamma = gamma
        self.batch_size = batch_size
        self.optimizer = torch.optim.Adam(self.model.parameters(),lr=0.0001,weight_decay=1e-5)
        self.scheduler = torch.optim.lr_scheduler.ExponentialLR(self.optimizer, gamma = 0.9945)
        self.num_episodes = num_episodes
        self.buffer = SimpleBuffer()
        self.sampler = Proportional(entropy_flag=True)
        self.iteration_count = 0
        self.eval_iteration_count = 0
        self.episode_count = 0
        self.eval_episode_count = 0
        self.step_count = 0
        
        
    def run_episode_(self):
        self.old_model.eval()
        G, actions, reward, done = self.env.reset()
        self.total_actions = self.total_actions.union(set(actions))

        sum_r = 0
        rews = []
        vals = []
        data_list = []
        mean_h = 0
        success = 0
        for t in range(self.env.max_time):
            X = make_batch([G.clone()]).to(self.device)
            pi, val = self.old_model(X)

            PI = F.softmax(pi,dim=0).view(pi.numel())
            if PI.numel() == 1:
                action, prob, H = 0,PI[0].view(1),0
            else:
                action, prob, H = self.sampler.sample(pi.detach())
                H = H.detach().cpu().item()
            new_G, actions, reward, done = self.env.fast_step(action)
            self.total_actions = self.total_actions.union(set(actions))

            mean_h = mean_h/(t+1) + H/(t+2)
            sum_r = sum_r + reward
            rews.append(reward)
            vals.append(val.detach().cpu().item())
            data_list.append([G.clone(), action, reward, 0.0, prob[action].detach().cpu().item()])
            
            G = new_G.clone()
            self.step_count += 1
            if done:
                success += 1
                break
        
        R = get_returns(rews, self.gamma)
        for i in range(len(data_list)):
            data_list[i][3] = R[i]
            self.buffer.keep(data_list[i])
        
        self.log_data['Mean_Episode_Entropy'].append((mean_h, self.episode_count))
        self.log_data['Episode_Return'].append((sum_r, self.episode_count))
        self.log_data['Num_total_actions'].append(len(self.total_actions))

        self.episode_count += 1
        return sum_r, success
                
    
    def eval_model_(self):
        self.old_model.eval()
        G, actions, reward, done = self.eval_env.reset()
        sum_r = 0
        steps = 0
        success = 0
        for t in range(self.eval_env.max_time):
            X = make_batch([G.clone()]).to(self.device)
            
            pi, val = self.old_model(X)
            PI = F.softmax(pi,dim=0).view(pi.numel())
            if PI.numel() == 1:
                action,prob,H = 0,PI[0].view(1),0
            else:
                action,prob,H = self.sampler.sample(pi.detach()); H = H.detach().cpu().item()
            new_G, actions, reward, done = self.eval_env.fast_step(action)
            sum_r += reward
            G = new_G.clone()
            steps += 1
            if done:
                success += 1
                break
        self.eval_episode_count += 1
        return sum_r, steps, success
    
    
    def eval_model(self,K):
        total_return = 0.0
        total_success = 0
        eval_steps = 0
        for i in range(K):
            ret, steps, success = self.eval_model_()
            total_return += ret
            eval_steps += steps
            total_success += success
        success_rate = success_rate/K
        self.eval_iteration_count += 1
        return success_rate/K, eval_steps, success_rate
    
    
    def update_model(self):
        self.model.train()
        
        # Exract data from buffer
        N = len(self.buffer.buffer)
        states, actions, _, returns, old_policy = zip(*self.buffer.buffer)
        returns = torch.tensor(returns, dtype=torch.float).view(len(returns), -1)
        old_policy = torch.tensor(old_policy, dtype=torch.float).view(len(old_policy), -1)
        num_batches = N // self.batch_size
        

        # Preorganize data as batches
        if N % self.batch_size > 0:
            num_batches += 1
        batches = []
        data_count = 0
        for i in range(num_batches):        
            K = min(self.batch_size,N - data_count)
            state_batch = states[data_count:(data_count+K)]
            action_batch = actions[data_count:(data_count+K)]
            
            state_batch = make_batch(state_batch, action_batch)
            return_batch = returns[data_count:(data_count+K)]
            return_batch = return_batch.view(return_batch.numel())
            old_policy_batch = old_policy[data_count:(data_count+K)]
            old_policy_batch = old_policy_batch.view(old_policy_batch.numel())
            batches.append([state_batch, return_batch, old_policy_batch])
            data_count += K
                
        for j in range(self.n_updates): 
            self.optimizer.zero_grad()
            mean_approx_kl = 0.0
            indices = list(range(num_batches))
            for i in range(num_batches):
                # Load data to device
                state_batch, return_batch, old_policy_batch = batches[indices[i]]
                state_batch = state_batch.to(self.device)
                return_batch = return_batch.to(self.device)
                old_policy_batch = old_policy_batch.to(self.device)
                
                # Evaluate current policy
                [pi,val] = self.model(state_batch)

                pi = U.softmax(pi.squeeze(),state_batch.glob_action_batch)

                pi = pi[state_batch.action].view(state_batch.action.numel())

                pi = pi.view(pi.numel())

                # Compute advantages
                adv = (return_batch.squeeze() - val.squeeze()).detach()
                adv = adv.view(adv.numel())
                
                # Compute losses
                ratio = torch.exp(pi.log() - old_policy_batch.log())
                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip) * adv
                loss_pi = -torch.min(surr1, surr2).mean()
                loss_v = torch.pow(val.squeeze() - return_batch.squeeze(),2).mean()
                loss_entropy = -pi.log().mean()
                loss = loss_pi + loss_v - 0.01*loss_entropy
                
                # Backward and accumulate gradients over all data
                loss.backward()
                data_count += K
                approx_kl = torch.mean(old_policy_batch.log() - pi.log())
                mean_approx_kl += approx_kl.detach().cpu().item()
            
            # Update policy parameters over all data
            self.optimizer.step()   
            
            # Early stopping
            mean_approx_kl = mean_approx_kl/num_batches
            if mean_approx_kl > 1.5*self.target_kl:
                break
        self.old_model.load_state_dict(self.model.state_dict())
        self.log_data['Mean_TD_Error'].append((loss_v.detach().cpu().item(), self.iteration_count))
        num_iters = j + 1
        return num_iters
    
        
    def run_episode(self):
        self.log_data = dict(Mean_Episode_Entropy=[], 
                             Success_Rate=[],
                             Episode_Return=[],
                             Num_Optimization_Steps=[],
                             Mean_TD_Error=[],
                             Num_total_actions=[]
                             )
        
        # Run episodes
        self.buffer.clean()
        self.step_count = 0
        mean_return = 0.0
        for i in range(self.num_episodes):
            tot_return, num_success = self.run_episode_()
            mean_return = mean_return + tot_return                
        mean_return = mean_return/float(self.num_episodes)
        success_rate = num_success/float(self.num_episodes)
        
        # Update policy
        num_opt_iters = self.update_model()
        self.scheduler.step()
        
        self.log_data['Success_Rate'].append((success_rate, self.iteration_count))
        self.log_data['Num_Optimization_Steps'].append((num_opt_iters, self.iteration_count))

        self.iteration_count += 1
        
        return self.log_data, self.step_count
