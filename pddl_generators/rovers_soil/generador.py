

import sys
from random import randrange, sample, random

args = sys.argv


if len(args) != 2:
    print("Uso: <waypoints>")
    exit(-1)

waypoints = int(args[1])

print("(define (problem rovers-generated)")
print("(:domain rovers)")

##### OBJECTS #####

print("(:objects")

for i in range(waypoints):
    print("waypoint{}".format(i), end=" ")
    print("- waypoint")


print(")")


##### INITIAL STATE #####

print("(:init")

num_events = randrange(waypoints*2//3,waypoints)

there_is_smth = sample(range(waypoints),num_events)
type_sample = [0 for i in range(waypoints)]

for place in there_is_smth:
    rand = random()
    if rand < 0.1:
        print(f"(at_rock_sample waypoint{place})")
        print(f"(at_soil_sample waypoint{place})")
        type_sample[place] = 3
    elif rand < 0.55:
        print(f"(at_rock_sample waypoint{place})")
        type_sample[place] = 2
    else:
        print(f"(at_soil_sample waypoint{place})")
        type_sample[place] = 1

print(f"(at_lander waypoint{randrange(waypoints)})")

print(f"(at waypoint{randrange(waypoints)})")

print(f"(empty)")

print(f"(sended)")

print(f"(ssend)")

print(f"(mode)")

print(")")

##### GOAL STATE #####

print("(:goal (and")

num_comms = randrange(waypoints//2, waypoints*2//3)

need_comm = sample(range(waypoints),num_comms)

for place in need_comm:
    place_type = type_sample[place]
    if place_type == 3:
        rand = random()
        if rand < 0.1:
            print(f"(communicated_image_data waypoint{place})")
        elif rand < 0.55:
            print(f"(communicated_rock_data waypoint{place})")
        else:
            print(f"(communicated_soil_data waypoint{place})")
    elif place_type == 2:
        if random() < 0.1:
            print(f"(communicated_image_data waypoint{place})")
        else:
            print(f"(communicated_rock_data waypoint{place})")
    elif place_type == 1:
        if random() < 0.1:
            print(f"(communicated_image_data waypoint{place})")
        else:
            print(f"(communicated_soil_data waypoint{place})")
    else:
        print(f"(communicated_image_data waypoint{place})")
print("))")


print(")")
