
from random import randrange, sample
import sys

args = sys.argv


if len(args) != 2:
    print("Uso: <num_blocks>")
    exit(-1)

nblocks = int(args[1])

# Según he visto en los problemas, tienen lo máximo 5 torres.

print("(define (problem blocks)")

print("(:domain blocks)")

print("(:objects ")

for i in range(nblocks):
    print(f"b{i}",end=" ")

print(")")

print("(:init")

# GENERACIÓN DE LAS TORRES Y DE LAS DISPOSICIONES

if nblocks > 5:
    num_towers = randrange(5) + 1
else:
    num_towers = randrange(nblocks) + 1

blocks = range(nblocks)

arrblocks = sample(blocks,len(blocks))

towers = sample(blocks,num_towers)


for i in towers:
    print(f"(ontable b{i})")
    index = arrblocks.index(i)
    while arrblocks[index-1] not in towers:
        print(f"(on b{arrblocks[index-1]} b{arrblocks[index]})")
        index -= 1
    print(f"(clear b{arrblocks[index]})")
    
print("(handempty)")
print("(stack)")
print("(nbuilding)")

print(")")

print("(:goal (and")

# GENERACIÓN DE LAS TORRES Y DE LAS DISPOSICIONES

if nblocks > 5:
    num_towers = randrange(5) + 1
else:
    num_towers = randrange(nblocks) + 1

blocks = range(nblocks)

arrblocks = sample(blocks,len(blocks))

towers = sample(blocks,num_towers)


for i in towers:
    print(f"(ontable b{i})")
    index = arrblocks.index(i)
    while arrblocks[index-1] not in towers:
        print(f"(on b{arrblocks[index-1]} b{arrblocks[index]})")
        index -= 1
    print(f"(clear b{arrblocks[index]})")
    

print("))")

print(")")
