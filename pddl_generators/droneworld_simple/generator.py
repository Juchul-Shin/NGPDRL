import random
from random import randint
import time
import sys

INITIAL_FIXED_POSITON = '\t\tdrone-at pos-3-1\n'
INITIAL_FIXED_DIRECTION = 't\t drone-to east\n'

DIR_LIST = ['north', 'east', 'south', 'west']
HEADING_LIST = ['right', 'left']





class ProblemGeneratorSimple():
    def __init__(self, grid_size):
        seed = int(time.time())
        random.seed(seed)
        self.domain_name = 'droneworld_simple'
        self.grid_size = grid_size
        self.problem_size = 1
        self.problem_number = 0
        self.occupied = []
        self.threats = []
        self.targets = []


    def random_agent(self):
        while True:
            retry = False
            self.init_x = randint(1, self.grid_size)
            self.init_y = randint(1, self.grid_size)

            for thing in self.occupied:
                if (self.init_x == thing[0]) and (self.init_y == thing[1]):
                    retry = True
                    break
            if not retry :
                self.occupied.append((self.init_x, self.init_y))
                break
       

    def generate_problem(self):
        self.goal_x = randint(1, self.grid_size)
        self.goal_y = randint(1, self.grid_size)
        self.occupied = [(self.goal_x, self.goal_y)]


        print('(define (problem drone)(:domain droneworld_simple)\n')
        print(self.generate_objects())
        print(self.generate_init())
        print(self.generate_goal())
        print(')')
        

    def generate_objects(self):
        objects_string = '\t(:objects\n'
        objects_string += '\t\tdrone - unit\n'
        for x in range(1, self.grid_size + 1):
            for y in range(1, self.grid_size + 1):
                objects_string += '\t\t'
                objects_string += 'pos-{0}-{1} - position\n'.format(x, y)
        objects_string += '\t)\n'
        return objects_string

    def generate_init(self):
        init_string = '\t(:init\n'

        self.random_agent()
        init_string += '\t\t(at drone pos-{0}-{1})\n'.format(self.init_x, self.init_y)

        init_string += self.generate_static_predicates()
        init_string += '\t)\n'
        return init_string

    def generate_static_predicates(self):
        static_predicates = ''
        for x in range(1, self.grid_size + 1):
            for y in range(1, self.grid_size + 1):
                for dir in DIR_LIST:
                    movable, new_x, new_y = self.is_adjacent(x, y, dir)
                    if (movable):
                        static_predicates += '\t\t(adjacent pos-{0}-{1} pos-{2}-{3})\n'.format(x, y, new_x, new_y)
        return static_predicates

    def is_adjacent(self, x, y, dir):
        if (dir == 'north'):
            if (y+1 > self.grid_size):
                return False, None, None
            else:
                return True, x, y+1
        elif (dir == 'east'):
            if (x+1 > self.grid_size):
                return False, None, None
            else:
                return True, x+1, y
        elif (dir == 'south'):
            if (y-1 < 1):
                return False, None, None
            else:
                return True, x, y-1
        elif (dir == 'west'):
            if (x-1 < 1):
                return False, None, None
            else:
                return True, x-1, y
        else:
            return False, None, None

    def generate_goal(self):
        goal_string = '\t(:goal (and\n\t\t(at drone pos-{}-{})\n'.format(self.goal_x, self.goal_y)

        goal_string += '\t)\n\t)'
        return goal_string



args = sys.argv


if len(args) != 2:
    print("Args: <num_grid>")
    exit(-1)

size_of_grid = int(args[1])

generator = ProblemGeneratorSimple(size_of_grid)
generator.generate_problem()




