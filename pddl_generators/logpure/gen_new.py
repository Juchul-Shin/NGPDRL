

import sys
from random import randrange

args = sys.argv


if len(args) != 2:
    print("Uso: <num_pkgs>")
    exit(-1)

pkgs = int(args[1])

cities_inf = pkgs//2 + 1

cities_sup = pkgs*2 

cities = randrange(cities_inf,cities_sup)

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

#chain = []
#for i in range(pkgs+1):
#    chain.append(randrange(cities))

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
