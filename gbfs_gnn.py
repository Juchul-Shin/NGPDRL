import sys
import os
from random import randint
from environment import make_batch
import torch
import torch.nn.functional as F
import numpy as np
from time import time
import heapq



def aggregate_random(models,state,device='cuda'):
    K = len(models)
    idx = np.random.randint(0,K,(1,))[0]
    [pi,val] = models[idx](state)
    pi = F.softmax(pi,dim=0).view(pi.numel())
    return pi, val

class Edge:
    def __init__(self, state, actions, action_idx, graph, value, entropy, policy, depth):
        self.state = state
        self.actions = actions
        self.action_idx = action_idx
        self.graph = graph
        self.value = value
        self.entropy = entropy
        self.Q = - (value / (1 + entropy)) * policy
        self.policy = policy
        self.depth = depth
    
    def __lt__(self, other):
        return self.Q < other.Q
    
    
class GBFS_GNN:   
     
    def search(self, gnn, env, max_time, device):
        self.device = device
        self.env = env
        self.gnn = gnn
        t1 = time()
        
        init_state = env.state
        init_graph = env.g
        init_actions = env.actions

        plan = []
        plan_length = None
        timeout = False
        
        openlist = []
        expanded = 0
        
        X = make_batch([env.g.clone()]).to(self.device)    
        pi, val = self.gnn(X)
        pi = torch.softmax(pi.view(pi.numel()), dim=0)
        H = -(pi*pi.log()).sum().detach().cpu().item()
        for i in range(len(env.actions)):
            edge = Edge(self.env.state, self.env.actions, i, env.g.clone(), val.detach().cpu().item(), H, pi.detach().cpu()[i].item(), self.env.depth)
            heapq.heappush(openlist, edge)
        while (True):
            ## get best edge in greedy manner
            edge = heapq.heappop(openlist)
            self.env.replace_state(edge.state, edge.graph, edge.actions, edge.depth)
            
            #print('greedy')
            G, actions, reward, done = env.fast_step(edge.action_idx)
            
            if done == True:
                break
            
            G = env.g
            X = make_batch([G.clone()]).to(self.device)    
            pi, val = self.gnn(X)
                                
            if pi.numel() == 1:
                action = 0
            else:
                pi = F.softmax(pi.view(pi.numel()),dim=0)
                dist = torch.distributions.categorical.Categorical(pi)
                action = dist.sample().item()
            
            H = -(pi*pi.log()).sum().detach().cpu().item()
            for i in range(len(env.actions)):
                edge = Edge(self.env.state, self.env.actions, i, env.g.clone(), val.detach().cpu().item(), H, pi.detach().cpu()[i].item(), self.env.depth)
                heapq.heappush(openlist, edge)
            
            depth = env.depth
            ## perform roll-out with GNN
            for t in range(depth, 300):
                expanded += 1
                if t > depth:
                    G = env.g
                    X = make_batch([G.clone()]).to(self.device)    
                    pi, val = self.gnn(X)
                                        
                    if pi.numel() == 1:
                        action = 0
                    else:
                        pi = F.softmax(pi.view(pi.numel()),dim=0)
                        dist = torch.distributions.categorical.Categorical(pi)
                        action = dist.sample().item()
                
                G, actions, reward, done = env.fast_step(action)

                if done:
                    plan_length = self.env.depth
                    #print('done')
                    break

                if time() - t1 >= max_time:
                    timeout = True
                    #print('timeout')
                    break
                

            if (timeout is True) or (done is True):
                break
        
        dtime = time() - t1
        return plan_length, expanded, dtime
            