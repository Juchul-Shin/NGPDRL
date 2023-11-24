

import sys
from random import randrange, sample, random

args = sys.argv


if len(args) != 2:
    print("Uso: <orders>")
    exit(-1)

count = int(args[1])

print("(define (problem openstacks)")
print("(:domain openstacks)")

##### OBJECTS #####

print("(:objects")

for i in range(count+1):
    print(f"n{i}", end=" ")
print("- count")

for i in range(count):
    print(f"o{i+1}",end=" ")
print("- order")

for i in range(count):
    print(f"p{i+1}",end=" ")
print("- product")

print(")")


##### INITIAL STATE #####

print("(:init")
print("(nada1)")
for i in range(count):
    print(f"(next n{i} n{i+1})")


for i in range(count):
    print(f"(order-started p{i+1} n0)")

for i in range(count):
    print(f"(verified o{i+1} n0)")

make = [0 for i in range(count)]


for i in range(count):
    print(f"(waiting o{i+1})")
    num = random()
    if num > 0.9:
        nprod = 3
    elif num > 0.2:
        nprod = 1
    else:
        nprod = 2
    for j in sample(range(count),nprod):
        print(f"(includes o{i+1} p{j+1})")
        make[j] += 1
    print(f"(necessary-to-ship o{i+1} n{nprod})")

for i in range(count):
    print(f"(not-made p{i+1})")

for i in range(count):
    print(f"(necessary-to-make p{i+1} n{make[i]})")

print(")")

##### GOAL STATE #####

print("(:goal (and")

for i in range(count):
    print(f"(shipped o{i+1})")

print("))")


print(")")
