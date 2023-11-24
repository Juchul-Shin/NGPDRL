from subprocess import call
import sys
import subprocess
import os



def call_fast_downward(data_out_path, domain, task, time_limit):
    directory = os.path.dirname(os.path.abspath(__file__))
          
    solver_path = directory + '/../downward'
    sys.path.append(solver_path)
    generator_command = './fast-downward.py --alias lama-first --search-time-limit {}s {} {}'.format(time_limit, domain, task)
    status = call(generator_command + ' >' + data_out_path ,cwd=solver_path, shell=True)
    with open(data_out_path) as file:
        text = file.read()
    is_done = text.find('Solution found.') > -1
    if is_done == True:
        str_tar = 'Search time: '
        s = text.find(str_tar)  + len(str_tar)
        search_time = float(text[s : s + text[s:].find('s')])
        
        str_tar = 'Evaluated '
        s = text.find(str_tar) + len(str_tar)
        evaluated_states = int(text[s : s + text[s:].find(' state(s).')])
    else:
        search_time = time_limit
        
        idx1 = text.rfind(' evaluated, ')
        if idx1 == -1:
            evaluated_states = 0
        else:
            str_tar = ', '
            idx2 = text[0:idx1].rfind(str_tar) + len(str_tar)
            evaluated_states = int(text[idx2:idx1])
    
    return is_done, search_time, evaluated_states
    
    
