from subprocess import call
import sys
import os
import subprocess

directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directory + '/pyperplan/pyperplan')  


from search import searchspace
from heuristics.relaxation import hFFHeuristic
from planner import _parse, _ground
import numpy as np
import torch
import torch_geometric.utils as U
from torch_geometric.data import Batch
import networkx as nx
from random import randint
#from pddl_generators.droneworld_simple.generator import ProblemGeneratorSimple



def fast_edge_id(S,R,num_nodes):
    I = S
    J = R
    J[J > I] -=1
    return (num_nodes - 1)*I + J

def parse_pred(pred):
    pred = pred[1:-1].split(' ')
    name = pred[0]; args = pred[1:]
    return name, args

def get_preds(domain):
    glob_preds = []; glob_predicates = dict()
    node_preds = []; node_predicates = dict()
    edge_preds = []; edge_predicates = dict()
    for idx,key in enumerate(domain.types.keys()):
        node_preds.append(str(domain.types[key]))
    for key in domain.predicates.keys():
        pred = domain.predicates[key]
        if len(pred.signature) == 0:
            glob_preds.append(key)
        if len(pred.signature) == 1:
            node_preds.append(key)
        if len(pred.signature) == 2:
            edge_preds.append(key)
        if len(pred.signature) > 2:
            raise Exception('predicate ' + key + ' is of arity greater than 2')
    glob_preds.sort()
    for i in range(len(glob_preds)): glob_predicates[glob_preds[i]] = i
    node_preds.sort()
    for i in range(len(node_preds)): node_predicates[node_preds[i]] = i
    edge_preds.sort()
    for i in range(len(edge_preds)): edge_predicates[edge_preds[i]] = i
    return glob_predicates, node_predicates, edge_predicates

def make_batch(graph_list,actions=None):

    batch = []; counter = 0
    counter = 0
    sum_actions = 0
    sum_effects = 0
    sum_nodes = 0
    sum_edges = 0
    for idx,S in enumerate(graph_list):
        S.U += idx; S.UA += sum_effects; S.V += sum_nodes; S.VA += sum_effects; S.E += sum_edges; S.EA += sum_effects
        Na = S.actions_batch[-1] + 1
        S.actions_batch += sum_actions

        S.num_actions = torch.ones((1)).fill_(Na).long()
        S.glob_action_batch = torch.ones(Na).long().fill_(counter)
        if actions is not None:
            S.action = torch.ones((1)).fill_(actions[idx] + sum_actions).long()
        Ne = S.edge_index.shape[1]
        counter += 1
        sum_actions += Na
        sum_edges += Ne
        sum_nodes += S.num_nodes
        sum_effects += S.num_effects
    batch = Batch.from_data_list(graph_list)

    return batch

class Environment:
    def __init__(self, directory):
        self.env_names = ['logistics', 'blocks4', 'satellite', 'gripper', 'ferry', 'droneworld_simple']
        self.params_info = {'logistics': ['number of airplanes','number of cities','number of locations within cities','number of packages'],
                           'blocks4': ['number of blocks'],
                           'satellite': ['number of satellites', 'max instruments per satellite', 'number of modes', 'number of targets', 'number of observations'],
                           'gripper': ['number of balls'],
                           'ferry': ['number of locations','number of cars'],
                           'droneworld_simple' : ['size of grid']}
        self.directory = directory
        
    def initialize(self, name, params, n_history, gamma, dense_reward = None, idx=0):
        self.n_history = n_history
        self.params = params
        self.dense_reward = dense_reward
        self.gamma = gamma
        if name == 'openstacks':
            self.domain_file = self.directory + '/pddl_generators/openstacks/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/openstacks/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {}'.format(params[0])
            self.data_path = self.directory + '/data/openstacks/train_tasks/task{}.pddl'.format(idx)
        elif name == 'openstacks2':
            self.domain_file = self.directory + '/pddl_generators/openstacks2/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/openstacks2/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {}'.format(params[0])
            self.data_path = self.directory + '/data/openstacks2/train_tasks/task{}.pddl'.format(idx)
        elif name == 'logistics':
            self.domain_file = self.directory + '/pddl_generators/logistics/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/logistics/'
            self.generator_command = lambda params: './logistics -a {} -c {} -s {} -p {} >task.pddl'.format(params[0],params[1],params[2],params[3])
            self.eval_generator_command = lambda params: './logistics -a {} -c {} -s {} -p {}'.format(params[0],params[1],params[2],params[3])
            self.data_path = self.directory + '/data/logistics/train_tasks/task{}.pddl'.format(idx)
        elif name == 'blocks4':
            self.domain_file = self.directory + '/pddl_generators/blocksworld/4ops/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/blocksworld/'
            self.generator_command = lambda params: './blocksworld 4 {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: './blocksworld 4 {}'.format(params[0])
            self.data_path = self.directory + '/data/blocks4/train_tasks/task{}.pddl'.format(idx)
        elif name == 'blocksmulti':
            self.domain_file = self.directory + '/pddl_generators/blocksmulti/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/blocksmulti/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generaldor.py {}'.format(params[0])
            self.data_path = self.directory + '/data/blocksmulti/train_tasks/task{}.pddl'.format(idx)
        elif name == 'hanoi':
            self.domain_file = self.directory + '/pddl_generators/hanoi/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/hanoi/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/hanoi/train_tasks/task{}.pddl'.format(idx)
        elif name == 'satellite':
            self.domain_file = self.directory + '/pddl_generators/satellite/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/satellite/'
            self.generator_command = lambda params: './satgen {} {} {} {} {} {} >task.pddl'.format(randint(0,sys.maxsize-1),params[0],params[1],params[2],params[3],params[4])
            self.eval_generator_command = lambda params: './satgen {} {} {} {} {} {}'.format(randint(0,sys.maxsize-1),params[0],params[1],params[2],params[3],params[4])
            self.data_path = self.directory + '/data/satellite/train_tasks/task{}.pddl'.format(idx)
        elif name == 'gripper':
            self.domain_file = self.directory + '/pddl_generators/gripper/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/gripper/'
            self.generator_command = lambda params: './gripper -n {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: './gripper -n {}'.format(params[0])
            self.data_path = self.directory + '/data/gripper/train_tasks/task{}.pddl'.format(idx)
        elif name == 'grippers':
            self.domain_file = self.directory + '/pddl_generators/grippers/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/grippers/'
            self.generator_command = lambda params: './grippers -n {} -r {} -o {} >task.pddl'.format(params[0],params[1],params[2])
            self.eval_generator_command = lambda params: './grippers -n {} -r {} -o {}'.format(params[0],params[1],params[2])
            self.data_path = self.directory + '/data/grippers/train_tasks/task{}.pddl'.format(idx)
        elif name == 'ferry':
            self.domain_file = self.directory + '/pddl_generators/ferry/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/ferry/'
            self.generator_command = lambda params: './ferry -l {} -c {} -s {} >task.pddl'.format(params[0],params[1],randint(0,sys.maxsize-1))
            self.eval_generator_command = lambda params: './ferry -l {} -c {} -s {}'.format(params[0],params[1],randint(0,sys.maxsize-1))
            self.data_path = self.directory + '/data/ferry/train_tasks/task{}.pddl'.format(idx)
        elif name == 'ascensor':
            self.domain_file = self.directory + '/pddl_generators/ascensor/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/ascensor/'
            self.generator_command = lambda params: 'python ascensor.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.eval_generator_command = lambda params: 'python ascensor.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.data_path = self.directory + '/data/ascensor/train_tasks/task{}.pddl'.format(idx)       
        elif name == 'log1by1':
            self.domain_file = self.directory + '/pddl_generators/log1by1/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/log1by1/'
            self.generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.eval_generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.data_path = self.directory + '/data/log1by1/train_tasks/task{}.pddl'.format(idx)
        elif name == 'log':
            self.domain_file = self.directory + '/pddl_generators/log/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/log/'
            self.generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.eval_generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.data_path = self.directory + '/data/log/train_tasks/task{}.pddl'.format(idx)
        elif name == 'logpure':
            self.domain_file = self.directory + '/pddl_generators/logpure/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/logpure/'
            self.generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.eval_generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.data_path = self.directory + '/data/logpure/train_tasks/task{}.pddl'.format(idx)           
        elif name == 'log1forall':
            self.domain_file = self.directory + '/pddl_generators/log1forall/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/log1forall/'
            self.generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.eval_generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.data_path = self.directory + '/data/log1forall/train_tasks/task{}.pddl'.format(idx)           
        elif name == 'depots':
            self.domain_file = self.directory + '/pddl_generators/depots/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/depots/'
            self.generator_command = lambda params: './depots -e {} -i {} -t {} -p {} -c {} -h {} >task.pddl'.format(params[0],params[1],params[2],params[3],params[4],params[5],randint(0,sys.maxsize-1))
            self.eval_generator_command = lambda params: './depots -e {} -i {} -t {} -p {} -c {} -h {}'.format(params[0],params[1],params[2],params[3],params[4],params[5],randint(0,sys.maxsize-1))
            self.data_path = self.directory + '/data/depots/train_tasks/task{}.pddl'.format(idx)
        elif name == 'rovers_collect':
            self.domain_file = self.directory + '/pddl_generators/rovers_collect/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/rovers_collect/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/rovers_collect/train_tasks/task{}.pddl'.format(idx)
        elif name == 'rovers_rock':
            self.domain_file = self.directory + '/pddl_generators/rovers_rock/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/rovers_rock/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/rovers_rock/train_tasks/task{}.pddl'.format(idx)
        elif name == 'rovers':
            self.domain_file = self.directory + '/pddl_generators/rovers/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/rovers/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/rovers/train_tasks/task{}.pddl'.format(idx)
        elif name == 'rovers_soil':
            self.domain_file = self.directory + '/pddl_generators/rovers_soil/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/rovers_soil/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/rovers_rock/train_tasks/task{}.pddl'.format(idx)
        elif name == 'blockslimited':
            self.domain_file = self.directory + '/pddl_generators/blockslimited/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/blockslimited/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/blockslimited/train_tasks/task{}.pddl'.format(idx)
        elif name == 'blocksunstack':
            self.domain_file = self.directory + '/pddl_generators/blocksunstack/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/blocksunstack/'
            self.generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generador.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/blocksunstack/train_tasks/task{}.pddl'.format(idx)
        elif name == 'kitchen':
            self.domain_file = self.directory + '/pddl_generators/kitchen/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/kitchen/'
            self.generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.eval_generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.data_path = self.directory + '/data/kitchen/train_tasks/task{}.pddl'.format(idx)
        elif name == 'kitchenbyone':
            self.domain_file = self.directory + '/pddl_generators/kitchenbyone/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/kitchenbyone/'
            self.generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.eval_generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.data_path = self.directory + '/data/kitchenbyone/train_tasks/task{}.pddl'.format(idx)
        elif name == 'kitchenloadall':
            self.domain_file = self.directory + '/pddl_generators/kitchenloadall/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/kitchenloadall/'
            self.generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.eval_generator_command = lambda params: 'python generador.py {} {} {} >task.pddl'.format(params[0],params[1],params[2])
            self.data_path = self.directory + '/data/kitchenloadall/train_tasks/task{}.pddl'.format(idx)
        elif name == 'floortile':
            self.domain_file = self.directory + '/pddl_generators/floortile/domain.pddl'
            self.generator_path = self.directory + '/pddl_generators/floortile/'
            self.generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.eval_generator_command = lambda params: 'python generador.py {} {} >task.pddl'.format(params[0],params[1])
            self.data_path = self.directory + '/data/floortile/train_tasks/task{}.pddl'.format(idx)
        elif name == 'droneworld_simple':
            self.domain_file = self.directory + '/droneworld_simple.pddl'
            self.generator_path = self.directory + '/pddl_generators/droneworld_simple/'
            self.generator_command = lambda params: 'python generator.py {} >task.pddl'.format(params[0])
            self.eval_generator_command = lambda params: 'python generator.py {} >task.pddl'.format(params[0])
            self.data_path = self.directory + '/data/droneworld_simple/train_tasks/task{}.pddl'.format(idx)
        else:
             raise ValueError('enviornment <' + name + '> does not exist!')
         
        pars = [np.random.randint(self.params[i][0],self.params[i][1],(1,))[0] for i in range(len(self.params))]

        status = call(self.generator_command(pars) + ' >' + self.data_path ,cwd=self.generator_path, shell=True)
        # generator = ProblemGeneratorSimple(4)
        # generator.generate_problem()
        self.problem = _parse(self.domain_file, self.data_path)

        self.glob_preds, self.node_preds, self.edge_preds = get_preds(self.problem.domain)
    
    def get_dims(self):    
        return (2 + self.n_history)*max(len(self.glob_preds),1), (2 + self.n_history)*max(len(self.node_preds),1) + 1, (2 + self.n_history)*max(len(self.edge_preds),1) + 1
     
    def reset(self):
        while True:
            pars = [np.random.randint(self.params[i][0],self.params[i][1],(1,))[0] for i in range(len(self.params))]
            status = call(self.generator_command(pars) + ' >' + self.data_path ,cwd=self.generator_path, shell=True)
            self.problem = _parse(self.domain_file, self.data_path)
            self.task = _ground(self.problem, remove_statics_from_initial_state=False)
            self.heuristic_task = _ground(self.problem, remove_statics_from_initial_state=True)
            self.state = self.task.initial_state
            G = self.state2graph()
            reward = 0; done = self.task.goal_reached(self.state)
            if done == False:
                break
        self.actions = [x for x,y in self.task.get_successor_states(self.state)]
        
        heuristic = hFFHeuristic(self.heuristic_task)
        (rh, rplan) = heuristic.calc_h_with_plan(searchspace.make_root_node(self.heuristic_task.initial_state))
        if rh == float('inf'):
            rh = 50
        self.max_time = int(rh*5)
        
        self.objects = dict()
        for i, name in enumerate(self.problem.objects.keys()):
            self.objects[name] = i
        G = self.get_actions(G)     # 현재 상태에 적용 가능한 Action을 Tensor로 
        G = self.repeat_state(G)    # hist 만큼 확장
        self.g = G.clone()
        self.depth = 0
        return G, self.actions, reward, done
    
    def create_task(self, params, path):
        while True:
            status = call(self.eval_generator_command(params) + ' >' + path ,cwd=self.generator_path, shell=True)
            problem = _parse(self.domain_file, path)
            task = _ground(problem, remove_statics_from_initial_state=False)
            done = task.goal_reached(task.initial_state)
            if done == False:
                break
        return None
    
    def reset_from_file(self, path):
        self.problem = _parse(self.domain_file, path)
        self.task = _ground(self.problem, remove_statics_from_initial_state=False)
        self.heuristic_task = _ground(self.problem, remove_statics_from_initial_state=True)
        self.state = self.task.initial_state
        G = self.state2graph()
        reward = 0; done = self.task.goal_reached(self.state)
        self.actions = [x for x,y in self.task.get_successor_states(self.state)]
        heuristic = hFFHeuristic(self.heuristic_task)
        (rh, rplan) = heuristic.calc_h_with_plan(searchspace.make_root_node(self.heuristic_task.initial_state))
        if rh == float('inf'):
            rh = 50
        self.max_time = int(rh*5)
        self.objects = dict()
        for i, name in enumerate(self.problem.objects.keys()):
            self.objects[name] = i
        G = self.get_actions(G)
        G = self.repeat_state(G)
        self.g = G.clone()
        self.depth = 0
        return G, self.actions, reward, done
    
    def repeat_state(self,g):
        u_dim, v_dim, e_dim = 2*max(len(self.glob_preds),1), 2*max(len(self.node_preds),1) + 1, 2*max(len(self.edge_preds),1) + 1
        u_dim = u_dim//2; v_dim = (v_dim-1)//2; e_dim = (e_dim-1)//2
        u_hist = g.glob[0,0:u_dim].unsqueeze(0); v_hist = g.x[:,0:v_dim]; e_hist = g.edge_attr[:,0:e_dim]
        for i in range(self.n_history):
            g.glob = torch.cat([u_hist,g.glob],dim=1)
            g.x = torch.cat([v_hist,g.x],dim=1)
            g.edge_attr = torch.cat([e_hist,g.edge_attr],dim=1)
        return g
    
    def replace_state(self, state, g, actions, depth):
        self.state = state
        self.g = g
        self.actions = actions
        self.depth = depth
    
    def fast_step(self, action):
        self.state = [y for x,y in self.task.get_successor_states(self.state) if x == self.actions[action]][0]

        u_dim, v_dim, e_dim = 2*max(len(self.glob_preds),1), 2*max(len(self.node_preds),1) + 1, 2*max(len(self.edge_preds),1) + 1
        u_dim = u_dim//2; v_dim = (v_dim-1)//2; e_dim = (e_dim-1)//2
        u_hist = self.g.glob[0,u_dim:-u_dim].unsqueeze(0); v_hist = self.g.x[:,v_dim:-v_dim-1]; e_hist = self.g.edge_attr[:,e_dim:-e_dim-1]
        G = self.g.clone()
        G.glob = G.glob[0,-2*u_dim:].view(1,2*u_dim); G.x = G.x[:,-2*v_dim-1:]; G.edge_attr = G.edge_attr[:,-2*e_dim-1:]
        G = self.update_graph(G, self.actions[action])
        G.glob = torch.cat([u_hist,G.glob],dim=1)
        G.x = torch.cat([v_hist,G.x],dim=1)
        G.edge_attr = torch.cat([e_hist,G.edge_attr],dim=1)
        reward = 0; done = self.task.goal_reached(self.state)
        self.actions = [x for x,y in self.task.get_successor_states(self.state)]
        G = self.get_actions(G)
        self.g = G.clone()
        self.depth += 1
        if self.dense_reward is None:
            if done == True:
                reward = 0.0
            else:
                reward = -1.0
        else:
            if done == True:
                reward = 0.0
            else:
                if (self.dense_reward == 'hFF'):
                    heuristic = hFFHeuristic(self.task)
                    h, _ = heuristic.calc_h_with_plan(searchspace.make_root_node(self.state & self.task.facts))
                    #h = heuristic.calc_goal_h()
                    reward = (self.gamma ** h - 1)/(1-self.gamma)


        return G, self.actions, reward, done

    def update_graph(self, G, action):
        for effect in list(action.add_effects):
            name, pred_args = parse_pred(effect)
            pred_args = [p for p in pred_args if p != '']
            if len(pred_args) == 0:
                G.glob[0,self.glob_preds[name]] = 1.0
            if len(pred_args) == 1:
                G.x[self.objects[pred_args[0]], self.node_preds[name]] = 1.0
            if len(pred_args) == 2:
                e_id = fast_edge_id(torch.Tensor([self.objects[pred_args[0]]]).long().view(1), torch.Tensor([self.objects[pred_args[1]]]).long().view(1), G.num_nodes)
                G.edge_attr[e_id, self.edge_preds[name]] = 1.0
        for effect in list(action.del_effects):
            name, pred_args = parse_pred(effect)
            pred_args = [p for p in pred_args if p != '']
            if len(pred_args) == 0:
                G.glob[0,self.glob_preds[name]] = 0.0
            if len(pred_args) == 1:
                G.x[self.objects[pred_args[0]], self.node_preds[name]] = 0.0
            if len(pred_args) == 2:
                e_id = fast_edge_id(torch.Tensor([self.objects[pred_args[0]]]).long().view(1), torch.Tensor([self.objects[pred_args[1]]]).long().view(1), G.num_nodes)
                G.edge_attr[e_id, self.edge_preds[name]] = 0.0
        return G

        
    def state2graph(self):
        state = list(self.state); GI = []; N = []; NI = []; S = []; R = []; EI = []
        GIg = []; Ng = []; NIg = []; Sg = []; Rg = []; EIg = []
        
        # State
        objects = dict()
        for i, name in enumerate(self.problem.objects.keys()):
            objects[name] = i
            N.append(i); NI.append(self.node_preds[str(self.problem.objects[name])])    #N Object 인덱스 #NI Object 타입
        for pred in state:
            name, pred_args = parse_pred(pred)
            pred_args = [p for p in pred_args if p != '']
            if len(pred_args) == 0:
                GI.append(self.glob_preds[name])
            if len(pred_args) == 1:
                N.append(objects[pred_args[0]]); NI.append(self.node_preds[name])  # N : 1-Ary Predicate의 Object 인덱스, #NI Object 타입
            if len(pred_args) == 2:
                S.append(objects[pred_args[0]]); R.append(objects[pred_args[1]]); EI.append(self.edge_preds[name])   # S : Source  # R : Receiver # EI : Predicate
                
        
        # Soals
        goals = list(self.task.goals)
        for pred in goals:
            name, pred_args = parse_pred(pred)
            pred_args = [p for p in pred_args if p != '']
            if len(pred_args) == 0:
                GIg.append(len(self.glob_preds) + self.glob_preds[name])
            if len(pred_args) == 1:
                Ng.append(objects[pred_args[0]]); NIg.append(len(self.node_preds) + self.node_preds[name])
                Ng.append(objects[pred_args[0]]); NIg.append(-1)
            if len(pred_args) == 2:
                Sg.append(objects[pred_args[0]]); Rg.append(objects[pred_args[1]]); EIg.append(len(self.edge_preds) + self.edge_preds[name])    
                Sg.append(objects[pred_args[0]]); Rg.append(objects[pred_args[1]]); EIg.append(-1)    
        
        # Graph creation
        g = nx.complete_graph(len(objects)).to_directed()   #Complete Graph 만들기
        g = U.from_networkx(g); g.num_nodes = len(objects)  
        x = torch.zeros(len(objects), 2*len(self.node_preds) + 1); x[N,NI] = 1.0; x[Ng,NIg] = 1.0  # Node Feature에 대한 초기화
        g.x = x
        edge_attr = torch.zeros(g.num_edges, 2*len(self.edge_preds) + 1);
        e_ids = fast_edge_id(torch.Tensor(S).long(), torch.Tensor(R).long(), g.num_nodes)
        edge_attr[e_ids, torch.Tensor(EI).long()] = 1.0     # 상태의 Edge Feature
        e_ids = fast_edge_id(torch.Tensor(Sg).long(), torch.Tensor(Rg).long(), g.num_nodes)
        edge_attr[e_ids, torch.Tensor(EIg).long()] = 1.0    # Goal의 Edge Feature
        g.edge_attr = edge_attr
        g.glob = torch.zeros(1,2*max(len(self.glob_preds),1)); g.glob[0,GI] = 1.0; g.glob[0,GIg] = 1.0  ## Global의 상태와 Goal Feature
        return g
    
    def get_actions(self,G):
        U = []; UI = []; US = []; UA = []
        V = []; VI = []; VS = []; VA = []
        E = []; EI = []; ES = []; S = []; R = []; EA = []
        batch = []; counter = 0
        for idx,action in enumerate(self.actions):
            for effect in list(action.add_effects):
                batch.append(idx)
                name, pred_args = parse_pred(effect)
                pred_args = [p for p in pred_args if p != '']
                if len(pred_args) == 0:
                    U.append(0); UI.append(self.glob_preds[name]); US.append(1.0); UA.append(counter)
                if len(pred_args) == 1:
                    V.append(self.objects[pred_args[0]]); VI.append(self.node_preds[name]); VS.append(1.0); VA.append(counter)
                if len(pred_args) == 2:
                    S.append(self.objects[pred_args[0]]); R.append(self.objects[pred_args[1]]); EI.append(self.edge_preds[name]); ES.append(1.0); EA.append(counter)
                counter += 1
            for effect in list(action.del_effects):
                batch.append(idx)
                name, pred_args = parse_pred(effect)
                pred_args = [p for p in pred_args if p != '']
                if len(pred_args) == 0:
                    U.append(0); UI.append(self.glob_preds[name]); US.append(-1.0); UA.append(counter)
                if len(pred_args) == 1:
                    V.append(self.objects[pred_args[0]]); VI.append(self.node_preds[name]); VS.append(-1.0); VA.append(counter)
                if len(pred_args) == 2:
                    S.append(self.objects[pred_args[0]]); R.append(self.objects[pred_args[1]]); EI.append(self.edge_preds[name]); ES.append(-1.0); EA.append(counter)
                counter += 1
                
        G.action_globs = torch.zeros(len(U),len(self.glob_preds)); G.action_globs[list(range(len(U))),[UI]] = torch.Tensor(US)
        G.action_nodes = torch.zeros(len(V),len(self.node_preds)); G.action_nodes[list(range(len(V))),[VI]] = torch.Tensor(VS)
        G.action_edges = torch.zeros(len(S),len(self.edge_preds)); G.action_edges[list(range(len(S))),[EI]] = torch.Tensor(ES)
        E = fast_edge_id(torch.Tensor(S).long(), torch.Tensor(R).long(), G.num_nodes)
        G.U = torch.Tensor(U).long(); G.V = torch.Tensor(V).long(); G.E = E; G.actions_batch = torch.Tensor(batch).long()
        G.UA = torch.Tensor(UA).long(); G.VA = torch.Tensor(VA).long(); G.EA = torch.Tensor(EA).long()
        G.num_effects = torch.Tensor([counter]).long()
        return G
    
    def check_goals(self):
        count = 0
        for goal in self.task.goals:
            if goal in self.state:
                count += 1
        return count, len(self.task.goals)

    def get_state(self):
        return self.state
            
    
