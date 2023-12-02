import environment
import torch
from ppo import PPO

from time import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from torch.utils.tensorboard import SummaryWriter
import argparse





if __name__ == '__main__':
    domains= ['openstacks','openstacks2','floortile','logistics', 'blocks4', 'satellite', 'gripper', 'ferry','depots', 'hanoi', 'grippers', 'ascensor', 'blocksmulti', 
            'rovers','rovers_collect', 'rovers_rock', 'rovers_soil' ,'log', 'log1by1', 'log1forall', 'blockslimited','blocksunstack','kitchen','kitchenbyone','kitchenloadall','logpure', 'droneworld_simple']
    
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-domain', choices=domains, default='blocks4')
    argparser.add_argument('-n_history', type=int, default=1)
    argparser.add_argument('-gamma', type=float, default=0.99)
    argparser.add_argument('-n_episodes', type=int, default=100)
    argparser.add_argument('-save_freq', type=int, default=10)
    argparser.add_argument('-eval_freq', type=int, default=15)
    argparser.add_argument('-eval_k', type=int, default=50)
    argparser.add_argument('-n_iterations', type=int, default=1000)
    argparser.add_argument('-batch_size', type=int, default=300)
    argparser.add_argument('-use_attention', default=0)
    argparser.add_argument('-dense_reward', default='')
    args = argparser.parse_args()
    
    writer = SummaryWriter()
    
    problem = args.domain
    
    # Number of state history steps in observations
    n_history = args.n_history
    dense_reward = args.dense_reward
    
    # Initialize train and eval environments
    directory = directory = os.path.dirname(os.path.abspath(__file__))
    env = environment.Environment(directory)
    eval_env = environment.Environment(directory)
    print(problem)
    if problem == 'satellite':
        env.initialize('satellite',[[1,4],[1,4],[1,4],[1,4],[2,4]],n_history)
        eval_env.initialize('satellite',[[6,7],[6,7],[4,5],[6,7],[12,14]],n_history)
    if problem == 'blocks4':
        env.initialize('blocks4',[[4,5]],n_history)
        eval_env.initialize('blocks4',[[10,11]],n_history)
    if problem == 'blocksmulti':
        env.initialize('blocksmulti',[[5,6]],n_history)
        eval_env.initialize('blocksmulti',[[10,11]],n_history)
    if problem == 'logistics':
        env.initialize('logistics',[[2,4],[2,4],[2,4],[1,3]],n_history, 0.99, dense_reward)
        eval_env.initialize('logistics',[[3,4],[6,7],[3,4],[6,7]],n_history, 0.99, dense_reward)
    if problem == 'gripper':
        env.initialize('gripper',[[3,4]],n_history)
        eval_env.initialize('gripper',[[15,16]],n_history)
    if problem == 'ferry':
        env.initialize('ferry',[[3,5],[2,4]],n_history)
        eval_env.initialize('ferry',[[9,10],[20,21]],n_history)
    if problem == 'depots':
        env.initialize('depots',[[1,2],[2,3],[2,3],[3,5],[2,4],[3,5]],n_history)
        eval_env.initialize('depots',[[5,6],[5,6],[5,6],[5,6],[5,6],[5,6]],n_history)
    if problem == 'hanoi':
        env.initialize('hanoi',[[3,5]],n_history)
        eval_env.initialize('hanoi',[[7,9]],n_history)
    if problem == 'grippers':
        env.initialize('grippers',[[2,4],[2,4],[5,6]],n_history)
        eval_env.initialize('grippers',[[7,8],[7,8],[10,11]],n_history)
    if problem == 'ascensor':
        env.initialize('ascensor',[[6,10],[2,3],[1,2]],n_history)
        eval_env.initialize('ascensor',[[8,12],[5,10],[1,3]],n_history)
    if problem == 'rovers_collect':
        env.initialize('rovers_collect',[[5,10]],n_history)
        eval_env.initialize('rovers_collect',[[10,20]],n_history)
    if problem == 'rovers_rock':
        env.initialize('rovers_rock',[[5,10]],n_history)
        eval_env.initialize('rovers_rock',[[10,20]],n_history)
    if problem == 'rovers_soil':
        env.initialize('rovers_soil',[[5,10]],n_history)
        eval_env.initialize('rovers_soil',[[10,20]],n_history)
    if problem == 'rovers':
        env.initialize('rovers',[[5,10]],n_history)
        eval_env.initialize('rovers',[[10,20]],n_history)
    if problem == 'log1by1':
        env.initialize('log1by1',[[3,7],[2,8]],n_history)
        eval_env.initialize('log1by1',[[3,7],[2,8]],n_history)
    if problem == 'log':
        env.initialize('log',[[3,7],[2,8]],n_history)
        eval_env.initialize('log',[[3,7],[2,8]],n_history)
    if problem == 'log1forall':
        env.initialize('log1forall',[[3,7],[2,8]],n_history)
        eval_env.initialize('log1forall',[[3,7],[2,8]],n_history)
    if problem == 'logpure':
        env.initialize('logpure',[[3,7],[2,8]],n_history)
        eval_env.initialize('logpure',[[9,10],[20,21]],n_history)
    if problem == 'blockslimited':
        env.initialize('blockslimited',[[5,6]],n_history)
        eval_env.initialize('blockslimited',[[5,10]],n_history)
    if problem == 'blocksunstack':
        env.initialize('blocksunstack',[[5,6]],n_history)
        eval_env.initialize('blocksunstack',[[5,10]],n_history)
    if problem == 'kitchenbyone':
        env.initialize('kitchenbyone',[[2,5],[2,4],[1,4]],n_history)
        eval_env.initialize('kitchenbyone',[[2,5],[2,4],[1,4]],n_history)
    if problem == 'kitchenloadall':
        env.initialize('kitchenloadall',[[2,5],[2,4],[1,4]],n_history)
        eval_env.initialize('kitchenloadall',[[2,5],[2,4],[1,4]],n_history)
    if problem == 'kitchen':
        env.initialize('kitchen',[[2,5],[2,4],[1,4]],n_history)
        eval_env.initialize('kitchen',[[2,5],[2,4],[1,4]],n_history)
    if problem == 'floortile':
        env.initialize('floortile',[[1,4],[2,4]],n_history)
        eval_env.initialize('floortile',[[3,6],[3,6]],n_history)
    if problem == 'openstacks':
        env.initialize('openstacks',[[3,10]],n_history)
        eval_env.initialize('openstacks',[[3,10]],n_history)
    if problem == 'openstacks2':
        env.initialize('openstacks2',[[3,10]],n_history)
        eval_env.initialize('openstacks2',[[3,10]],n_history)
    if problem == 'droneworld_simple':
        env.initialize('droneworld_simple',[[4,5]],n_history, args.gamma, dense_reward)
        eval_env.initialize('droneworld_simple',[[7,8]],n_history, args.gamma, dense_reward)
    gamma = args.gamma
    num_episodes = args.n_episodes
    batch_size = args.batch_size
    alg = PPO(env=env, eval_env=eval_env, gamma=gamma, num_episodes=num_episodes, batch_size=batch_size, use_attention=args.use_attention)
    
    
    ### create folder and save model architecture ###
    save_freq = args.save_freq
    eval_freq = args.eval_freq
    eval_K = args.eval_k
    num_iterations = args.n_iterations
    
    now = datetime.now()
    nowstring = now.strftime("%d_%m_%Y__%H_%M_%S")
    if not os.path.exists('saved_models/' + problem):
        os.mkdir('saved_models/' + problem)
    path = 'saved_models/' + problem + '/' + nowstring
    os.mkdir(path)
    
    with open(path + '/architecture.txt', 'w') as file:
        file.write(str(alg.model))
    
    with open(path + '/env_params.txt', 'a') as file:
        file.write('n_history: {} \n'.format(n_history))
        file.write('env params: {} \n'.format(env.params))
        file.write('eval env params: {} \n'.format(eval_env.params))
        file.write('gamma: {} \n'.format(gamma))
        file.write('num_episodes: {} \n'.format(num_episodes))
        file.write('eval_freq: {} \n'.format(eval_freq))
        file.write('eval_K: {} \n'.format(eval_K))
        file.write('batch_size: {} \n'.format(batch_size))
        file.write('use_attention: {} \n'.format(args.use_attention))
    
    best_eval_score = 0
    
    print()
    print('##################################')
    print('Starting training on {}'.format(problem))      
    print('##################################')
    print()
    for i in range(num_iterations):
        t1 = time()
        log_data = alg.run_episode()
        t2 = time()
        
        success_rate = log_data['Iteration_Success_Rate'][-1][0]
        total = log_data['Num_total_actions'][0]

        print('iteration: {}. success rate: {}. Total {}. Time: {}'.format( i, round(success_rate,3),total, round(t2-t1,3)))
        
        for key in log_data.keys():
            items = log_data[key]
            if key != 'Num_parallel_actions' and key != 'Num_total_actions':
                for item in items:
                    writer.add_scalar(key, item[0], item[1])
            else:
                for item in items:
                    writer.add_scalar(key,item)

 
        if i % save_freq == 0:
            torch.save(alg.model.state_dict(),path + '/PPO_model.pt')
        
        if i % eval_freq == 0:
            print('evaluating model:')
            t1 = time()
            mean_return, eval_sr = alg.eval_model(eval_K)
            t2 = time()
            print('evaluation success rate: {}. time: {} mean_return {}'.format(eval_sr,round(t2-t1,3), round(mean_return,3)))
            writer.add_scalar('Eval_Success_Rate', eval_sr, alg.eval_iteration_count - 1)
                        
            if eval_sr > best_eval_score:
                torch.save(alg.model.state_dict(),path + '/PPO_best_eval_model.pt')
                best_eval_score = eval_sr
            elif eval_sr == 1.0:
                now2 = datetime.now()
                nowstring2 = now.strftime("%d_%m_%Y__%H_%M_%S")
                torch.save(alg.model.state_dict(),path + '/PPO_best_eval_model.pt' + nowstring2)
                    
    print()
    print('##################################')
    print('Finished training on {}'.format(problem))      
    print('Best evaluation success rate: {}'.format(round(best_eval_score, 3)))
    print('##################################')
    print()
            
    
