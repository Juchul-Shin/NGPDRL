

import sys
from random import randrange

args = sys.argv


if len(args) != 3:
    print("Uso: <num_cities> <num_pkgs>")
    exit(-1)

cities = int(args[1])
pkgs = int(args[2])

print("(define (problem logistics-generated)")
print("(:domain logistics)")

##### OBJECTS #####

print("(:objects")

for i in range(cities):
    print("pos{}".format(i), end=" ")
    print("- place")

for i in range(pkgs):
    print("obj{}".format(i),end=" ")
    print("- package")


print(")")


##### INITIAL STATE #####

print("(:init")

print("(load)\n(nfull)\n(att pos{})".format(randrange(cities)))


for i in range(pkgs):
    print(f"(at obj{i} pos{randrange(cities)})")

print(")")

##### GOAL STATE #####

print("(:goal (and")

for i in range(pkgs):
    print(f"(at obj{i} pos{randrange(cities)})")


print("))")


print(")")
