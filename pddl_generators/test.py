import environment
import torch
from time import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse
from fast_downward_caller import call_fast_downward
from models import ACNet
from gbfs_gnn import GBFS_GNN
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from environment import make_batch
import torch.nn.functional as F

ICON_SIZE = 90

class renderer:
    def __init__(self, grid_size, threats, targets, goal, title=''):
        self.path = path
        self.grid_size = grid_size
        self.num_threat = threats
        self.num_target = threats
        self.goal = goal
        self.threats = threats
        self.targets = targets
        self.drone_icon_north = Image.open('img/drone.png').resize((ICON_SIZE, ICON_SIZE))
        self.drone_icon_east = self.drone_icon_north.rotate(270)
        self.drone_icon_south = self.drone_icon_north.rotate(180)
        self.drone_icon_west = self.drone_icon_north.rotate(90)
        self.threat_icon = Image.open('img/threat.png').resize((ICON_SIZE-20, ICON_SIZE-20))
        self.target_icon = Image.open('img/target.png').resize((ICON_SIZE, ICON_SIZE))
        self.scanned_target_icon = Image.open('img/scanned_target.png').resize((ICON_SIZE, ICON_SIZE))
        self.goal_icon = Image.open('img/goal.png').resize((ICON_SIZE, ICON_SIZE))
        self.title = title
    

    def render(self, env_state):
        fig, ax = plt.subplots()

        # 그리드 크기
        grid_width = self.grid_size
        grid_height = self.grid_size

        # 셀 크기
        cell_width = 100
        cell_height = 100

        # 그리드 생성
        #grid = [[None] * grid_width for _ in range(grid_height)]

        # 그래프 객체 생성
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.set_title(self.title)
        # # 축 범위 설정
        ax.set_xlim(0, grid_width * cell_width)
        ax.set_ylim(0, grid_width * cell_height)
        ax.set_xticks([i * cell_width for i in range(grid_width + 1)])
        ax.set_yticks([i * cell_height for i in range(grid_height + 1)])
        ax.set_xticklabels([])  # x축 눈금 수치 없애기
        ax.set_yticklabels([])  # y축 눈금 수치 없애기
        # 그리드 그리기
        ax.grid(True, linestyle='-', linewidth=1, color='black')

        agent_position = next((element for element in env_state if element.startswith('(at drone pos')), None)
        agent_direction = next((element for element in env_state if element.startswith('(drone-to')), None)
        parts = agent_position.split('-')
        drone_at = (int(parts[1]), int(parts[2][:-1]))
        parts = agent_direction.split(' ')
        drone_to = parts[1][:-1]

        # 각 위치에 아이콘 배치
        for x in range(1, grid_width+1):
            for y in range(1, grid_height+1):
                # 셀 중심 좌표 계산
                cell_center_x = (x-1) * cell_width + cell_width / 2
                cell_center_y = (y-1) * cell_height + cell_height / 2

                # 드론 위치에 드론 아이콘 배치
                if (x, y) == drone_at:
                    if (drone_to == 'north'):
                        icon = self.drone_icon_north
                    elif(drone_to == 'east'):
                        icon = self.drone_icon_east
                    elif(drone_to == 'south'):
                        icon = self.drone_icon_south
                    else:
                        icon = self.drone_icon_west
                # 목표 위치에 목표 아이콘 배치
                elif (x, y) == self.goal:
                    icon = self.goal_icon
                # 위협 위치에 위협 아이콘 배치
                elif (x, y) in self.threats:
                    icon = self.threat_icon
                elif (x, y) in self.targets:
                    index = self.targets.index((x,y))
                    str = '(scanned target-{})'.format(index+1)
                    if str in env.state:
                        icon = self.scanned_target_icon
                    else:
                        icon = self.target_icon
                    
                else:
                    continue

                # 아이콘을 그리드의 셀 중심에 배치
                left = cell_center_x - ICON_SIZE / 2
                top = cell_center_y - ICON_SIZE / 2
                ax.imshow(icon, extent=[left, left + ICON_SIZE, top, top + ICON_SIZE])


        # 그림을 이미지 객체로 변환
        canvas = FigureCanvas(fig)
        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image = Image.open(buffer)
        plt.close(fig)

        return image

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
    if problem == 'droneworld':
        dist = [[10,20], [5, 20]]
    if problem == 'droneworld_scan':
        dist = [[9,10], [3,5], [3,5]]
    if problem == 'droneworld_simple':
        dist = [[5,5]]
    return dist

def find_action(actions, action_str):
    for idx, action in enumerate(actions):
        s = action.name.replace("(", "").replace(")", "")
        if s in action_str:
            return idx


def sample_distribution(params):
    out = []
    for par in params:
        out.append(np.random.randint(par[0], par[1], (1,))[0])
    return out



if __name__ == '__main__':
    domains= ['logistics', 'blocks4', 'satellite', 'gripper', 'ferry', 'droneworld', 'droneworld_scan']
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  
    #device = torch.device('cuda' if torch.cuda.is_available() else 'mps')  #for M1 mac
    directory = directory = os.path.dirname(os.path.abspath(__file__))
    
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-domain', choices=domains, default='droneworld_scan')
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
    fd_render_path = target_path + '/results/fd'
    pol_render_path = target_path + '/results/pol'
    data_path = target_path + '/eval_tasks'
    
    os.mkdir(target_path)
    os.mkdir(result_path)
    os.mkdir(data_path)
    os.mkdir(fd_render_path)
    os.mkdir(pol_render_path)

    
    N_tasks = args.eval_k
    n_history = args.n_history 
    
    print('creating evaluation task files')
    env = environment.Environment(directory)
    dist = get_distribution(problem, 1)
    env.initialize(problem, dist, n_history)
    path = data_path + '/task.pddl'
    params = sample_distribution(dist)
    grid_size, threats, targets, goal = env.create_task(dist, path)

    print('finished creating test task files')
    
    glob_in, node_in, edge_in = env.get_dims()
    model = ACNet(node_in, edge_in, glob_in, args.hid_dim, env.n_history, use_attention=False)
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

    is_done, runtime, expansions, solution_lines = call_fast_downward(data_path + '/task', domain_file, path, time_limit=args.max_time)
    #fd_expansions.append(expansions)
    #fd_times.append(runtime)
    if is_done is False:
        print("FD failed to find a solution")
    else:
        print("FD found a solution. The solution has {} steps".format(len(solution_lines)-1))
        
    # rendering the result of FD
    G, actions, reward, done = env.reset_from_file(path)
    title = 'Fastdownward Plan - {} steps'.format(len(solution_lines)-1)
    renderer = renderer(grid_size, threats, targets, goal, title)
    frames = []
    frame = renderer.render(env.state)
    frames.append(frame)   
    for line in solution_lines:
        action = find_action(actions, line)
        if (action is None) :
            break
        new_G, actions, reward, done = env.fast_step(action)
        frame = renderer.render(env.state)
        frames.append(frame)
    frames[0].save(fd_render_path + '/animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)

    G, actions, reward, done = env.reset_from_file(path)
    title = 'Roll-out policy'
    renderer.title = title
    frames = []
    frame = renderer.render(env.state)
    frames.append(frame)
    done = False
    step = 0
    while (not done):
        step += 1

        X = make_batch([G.clone()]).to(device)    
        pi, val = model(X)
                            
        if pi.numel() == 1:
            action = 0
        else:
            pi = F.softmax(pi.view(pi.numel()),dim=0)
            dist = torch.distributions.categorical.Categorical(pi)
            action = dist.sample().item()

        G, actions, reward, done = env.fast_step(action)
        frame = renderer.render(env.state)
        frames.append(frame)

        if (actions is None):  #action이 없는 terminal state이면 다시 pop
            print("Agent reached terminal state.")
            break
        if done:
            print("Policy Rolled out {} steps to reach the goal".format(step))
            break

    frames[0].save(pol_render_path + '/animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)

