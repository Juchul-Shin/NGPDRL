
from random import randrange, sample
import sys

args = sys.argv


# CUPS = TEABAGS

if len(args) != 4:
    print("Uso: <num_teabags> <num_cupboards> <num_pantries>")
    exit(-1)

nteabags   = int(args[1])
ncupboards = int(args[2])
npantries  = int(args[3])

# Según he visto en los problemas, tienen lo máximo 5 torres.

print("(define (problem kitchen)")

print("(:domain kitchen)")

print("(:objects ")

for i in range(nteabags):
    print(f"tea_bag{i}",end=" ")

print("- tea")
print("water - water")

for i in range(nteabags):
    print(f"cup{i}",end=" ")

print("- cup")
print("keetle - keetle")

for i in range(ncupboards):
    print(f"cupboard{i}",end=" ")

for i in range(npantries):
    print(f"pantry{i}",end=" ")

print("sink base - place")

print(")")

print("(:init")

print("(takefood)")
print("(getitem)")
print("(boil)")

for i in range(nteabags):
    print(f"(clean cup{i})")

for i in range(nteabags):
    j = randrange(npantries)
    print(f"(at_food_t tea_bag{i} pantry{j})")

for i in range(nteabags):
    j = randrange(ncupboards)
    print(f"(at_item_c cup{i} cupboard{j})")
    
print(f"(at_item_k keetle cupboard{randrange(ncupboards)})")

print("(at_food_w water sink)")

print(f"(at_robot cupboard{randrange(ncupboards)})")

print(")")

print("(:goal (and")

for i in range(nteabags):
    print(f"(made tea_bag{i})")

print("))")

print(")")
