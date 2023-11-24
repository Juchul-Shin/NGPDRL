import environment
import torch
from time import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse
from fast_downward_caller import call_fast_downward
from models import ACNet
from gbfs_gnn import GBFS_GNN



def get_distribution(problem, j):
    if problem == 'blocks4':
        dist = [[5,100]]
    if problem == 'satellite':
        dist = [[2*j+1,3*j+2],[2*j+2,2*j+3],[j+1,j+2],[2*j+2,2*j+7],[j*9+2,j*9+6]]
    if problem == 'logistics':
        dist = [[j+4,j+6],[2*j+4,2*j+7],[j+1,j+2],[8*j+3,8*j+8]]
    if problem == 'gripper':
        dist = [[5,200]]
    if problem == 'ferry':
        dist = [[8*j+3,8*j+8],[25*j+2,25*j+20]]
    if problem == 'depots':
        dist = [[5,6],[5,6],[5,6],[5,6],[5,6],[5,6]]
    if problem == 'ascensor':
        dist = [[15,20],[15,20],[4,5]]
    if problem == 'log1by1':
        dist = [[2,3],[4,5]]
    if problem == 'log1forall':
        dist = [[2,3],[4,5]]
    if problem == 'logpure':
        dist = [[2,3],[4,5]]
    if problem == 'blockslimited':
    	dist = [[2,3]]
    if problem == 'rovers_collect':
    	dist = [[5,10]]
    if problem == 'rovers_rock':
    	dist = [[5,10]]
    if problem == 'rovers_soil':
    	dist = [[5,10]]
    if problem == 'rovers':
        dist = [[5,10]]

    else:
    	dist = [[10,11],[10,11],[10,11],[10,11],[10,11],[10,11],[10,11],[10,11]]
    return dist


def sample_distribution(params):
    out = []
    for par in params:
        out.append(np.random.randint(par[0], par[1], (1,))[0])
    return out


if __name__ == '__main__':
    domains= ['floortile','openstacks','log','blocksunstack','kitchen','rovers','logistics', 'blocks4','blocksmulti', 'satellite', 'gripper', 'ferry', 'depots', 'ascensor', 'rovers_collect', 'rovers_rock','rovers_soil','log1by1', 'log1forall','logpure', 'kitchenbyone', 'kitchenloadall', 'blockslimited']
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  
    directory = directory = os.path.dirname(os.path.abspath(__file__))
    
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-domain', choices=domains, default='blocks4')
    argparser.add_argument('-n_history', type=int, default=1)
    argparser.add_argument('-eval_k', type=int, default=100)
    argparser.add_argument('-max_time', type=int, default=10)
    argparser.add_argument('-use_attention', default=0)
    argparser.add_argument('-hid_dim', type=int, default=256)
    argparser.add_argument('-policy_path')
    argparser.add_argument('-problema', default=0)
    args = argparser.parse_args()
    
    problem = args.domain
    now = datetime.now()
    nowstring = now.strftime("%d_%m_%Y__%H_%M_%S")
    
    target_path = directory + '/data/' + problem + '/eval_' + nowstring
    result_path = target_path + '/results'
    data_path = target_path + '/eval_tasks'
    os.mkdir(target_path)
    os.mkdir(result_path)
    os.mkdir(data_path)
    
    N_tasks = args.eval_k
    n_history = args.n_history
    
    problema = args.problema
    
    

    env = environment.Environment(directory)

    dist = get_distribution(problem, 0)
    env.initialize(problem, dist, n_history)
    
    glob_in, node_in, edge_in = env.get_dims()

    model = ACNet(node_in, edge_in, glob_in, args.hid_dim, 1, args.use_attention)
    
    model.load_state_dict(torch.load(args.policy_path))

    model = model.to(device)

    domain_file = env.domain_file
    
    fd_successes = []
    fd_expansions = []
    fd_times = []
    
    gnn_successes = []
    gnn_expansions = []
    gnn_times = []
    
    search_alg = GBFS_GNN()

    files = os.listdir(data_path)
    tasks = []
    for file in files:
        if file.find('.soln') == -1:
            tasks.append(os.path.join(data_path, file))

    for task in [problema]:   
        
        # evaluate gbfs-gnn
        G, actions, reward, done = env.reset_from_file(task)
        solution2, expansions2, runtime2 = search_alg.search(model, env, 30, device)
        gnn_expansions.append(expansions2)
        gnn_times.append(runtime2)
        if solution2 is None:
            gnn_successes.append(0)

        else:
            gnn_successes.append(1)
            print(solution2)


        
	    
    
    fd_successes = np.array(fd_successes)
    fd_expansions = np.array(fd_expansions)
    fd_times = np.array(fd_times)
    
    gnn_successes = np.array(gnn_successes)
    gnn_expansions = np.array(gnn_expansions)
    gnn_times = np.array(gnn_times)
    

    
