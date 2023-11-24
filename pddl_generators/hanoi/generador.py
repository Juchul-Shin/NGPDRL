import sys
from random import randrange

args = sys.argv


if len(args) != 2:
    print("Uso: <num_disks>")
    exit(-1)

disks = int(args[1])

if disks % 2 == 0:
    disks -= 1

print("(define (problem hanoi)")
print("(:domain hanoi)")
print("(:objects")

print("peg1 peg2 peg3 ")

for i in range(disks):
    print(f"d{i}",end=" ")

print(")")

print("(:init")

for i in range(disks):
    print(f"(smaller peg1 d{i})")
    print(f"(smaller peg2 d{i})")
    print(f"(smaller peg3 d{i})")
    
for i in range(disks):
    for j in range(i+1,disks):
        print(f"(smaller d{j} d{i})")

print("(clear peg2)")
print("(clear peg3)")
print("(clear d0)")

print(f"(on d{disks-1} peg1)")
for i in range(disks-1):
    print(f"(on d{i} d{i+1})")

print(")")

print("(:goal (and")

print(f"(on d{disks-1} peg3)")
for i in range(disks-1):
    print(f"(on d{i} d{i+1})")

print("))")

print(")")
