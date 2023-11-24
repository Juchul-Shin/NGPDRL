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
        #dist = [[j+4,j+6],[2*j+4,2*j+7],[j+1,j+2],[8*j+3,8*j+8]]
        dist = [[3,4],[5,6],[3,4],[5,6]]
    if problem == 'gripper':
        dist = [[5,200]]
    if problem == 'ferry':
        #dist = [[8*j+3,8*j+8],[25*j+2,25*j+20]]
        dist = [[15,20],[20,50]]
    if problem == 'depots':
        dist = [[5,6],[5,6],[5,6],[7,9],[7,9],[7,9]]
    if problem == 'ascensor':
        dist = [[8,10],[5,8],[1,2]]
    if problem == 'logpure':
        dist = [[3,7],[2,8]]
    if problem == 'droneworld_simple':
        dist = [[9,10]]
    return dist


def sample_distribution(params):
    out = []
    for par in params:
        out.append(np.random.randint(par[0], par[1], (1,))[0])
    return out


if __name__ == '__main__':
    domains= ['logistics', 'blocks4', 'satellite', 'gripper', 'ferry', 'depots','ascensor','logpure', 'droneworld_simple']
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  
    directory = directory = os.path.dirname(os.path.abspath(__file__))
    
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-domain', choices=domains, default='blocks4')
    argparser.add_argument('-n_history', type=int, default=1)
    argparser.add_argument('-eval_k', type=int, default=100)
    argparser.add_argument('-max_time', type=int, default=600)
    argparser.add_argument('-use_attention', default=False)
    argparser.add_argument('-hid_dim', type=int, default=256)
    argparser.add_argument('-policy_path')
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
    
    print('creating evaluation task files')
    env = environment.Environment(directory)
    for j in range(5):
        dist = get_distribution(problem, j)
        env.initialize(problem, dist, n_history)
        for i in range(N_tasks // 5):
            path = data_path + '/task{}.pddl'.format(5 * j + i)
            params = sample_distribution(dist)
            env.create_task(params, path)
    print('finished creating evaluation task files')
    
    glob_in, node_in, edge_in = env.get_dims()
    model = ACNet(node_in, edge_in, glob_in, args.hid_dim, env.n_history, args.use_attention)

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
    print('cargado GBFS_GNN')
    files = os.listdir(data_path)
    tasks = []
    for file in files:
        if file.find('.soln') == -1:
            tasks.append(os.path.join(data_path, file))

    for i, task in enumerate(tasks):   
        print(i)
        print(args.max_time)
        # evaluate fast-downward
        is_done, runtime, expansions = call_fast_downward(data_path + '/task{}'.format(i), domain_file, task, time_limit=args.max_time)
        fd_expansions.append(expansions)
        fd_times.append(runtime)
        if is_done is False:
            fd_successes.append(0)
        else:
            fd_successes.append(1)
        
        # evaluate gbfs-gnn
        G, actions, reward, done = env.reset_from_file(task)
        solution2, expansions2, runtime2 = search_alg.search(model, env, args.max_time, device)
        gnn_expansions.append(expansions2)
        gnn_times.append(runtime2)
        if solution2 is None:
            gnn_successes.append(0)
        else:
            gnn_successes.append(1)

        print('task: {} / {}'.format(i+1, len(tasks)))
    
    fd_successes = np.array(fd_successes)
    fd_expansions = np.array(fd_expansions)
    fd_times = np.array(fd_times)
    
    gnn_successes = np.array(gnn_successes)
    gnn_expansions = np.array(gnn_expansions)
    gnn_times = np.array(gnn_times)
    
    # plot success rate against time
    plt.subplot(1,2,1)
    fd_sr = []
    gnn_sr = []
    T = list(range(args.max_time))
    for t in T:
        idx = np.argwhere((fd_times < t) & (fd_successes == 1.0))
        fd_sr.append(len(idx)/len(fd_successes))    
        idx = np.argwhere((gnn_times < t) & (gnn_successes == 1.0))
        gnn_sr.append(len(idx)/len(gnn_successes))
    plt.plot(T, gnn_sr, "-b", label="GBFS-GNN")
    plt.plot(T, fd_sr, "-g", label="FD-lama-first")
    plt.legend(loc="lower right")
    plt.xlabel('time [s]')
    plt.ylabel('success rate')
    plt.grid()
    plt.title(problem)
    
    # plot success rate against expanded states
    plt.subplot(1,2,2)
    fd_sr = []
    gnn_sr = []
    max_time = None
    min_time = 1
    fd_fails = fd_expansions[fd_successes == 0.0]
    if fd_fails.shape[0] > 0:
        max_time = max(fd_fails)
        print('entra_fd')
    gnn_fails = fd_expansions[gnn_successes == 0.0]
    if gnn_fails.shape[0] > 0:
        print('entra_gnn')
        if (max_time is None) or (max(gnn_fails) < max_time):
            max_time = max(gnn_fails)
    
    if fd_fails.shape[0] <= 0 and gnn_fails.shape[0] <= 0:
        max_fd = max(fd_expansions[fd_successes == 1.0])
        max_gnn = max(fd_expansions[gnn_successes == 1.0])
        max_time = max(max_fd,max_gnn)
    
    T = list(range(min_time,int(max_time)))
    for t in T:
        idx = np.argwhere((fd_expansions < t) & (fd_successes == 1.0))
        fd_sr.append(len(idx)/len(fd_successes))    
        idx = np.argwhere((gnn_expansions < t) & (gnn_successes == 1.0))
        gnn_sr.append(len(idx)/len(gnn_successes))
    plt.plot(T, gnn_sr, "-b", label="GBFS-GNN")
    plt.plot(T, fd_sr, "-g", label="FD-lama-first")
    plt.legend(loc="lower right")
    plt.xlabel('expanded states')
    plt.ylabel('success rate')
    plt.grid()
    plt.title(problem)
    
    plt.savefig(result_path + '/eval_results_plot.jpg')
    plt.show(block=False)
    
