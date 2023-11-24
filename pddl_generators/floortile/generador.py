
from random import randrange, sample
import sys

args = sys.argv


if len(args) != 3:
    print("Uso: <num_filas> <num_columnas>")
    exit(-1)

nrow = int(args[1]) + 1
ncol = int(args[2])


print("(define (problem floor-tile)")

print("(:domain floor-tile)")

print("(:objects ")

for i in range(nrow):
    for j in range(ncol):
        print(f"tile_{i}-{j+1}",end=" ")
    if i == nrow-1:
        print("- tile")
    else: print()


print("robot1 robot2 - robot")
print("white black - color")

print(")")

print("(:init")

x_r1 = randrange(nrow)
y_r1 = randrange(ncol)
print(f"(robot-at robot1 tile_{x_r1}-{y_r1+1})")
print("(robot-has robot1 white)")

x_r2 = randrange(nrow)
y_r2 = randrange(ncol)
while x_r1 == x_r2 and y_r1 == y_r2:
    x_r2 = randrange(nrow)
    y_r2 = randrange(ncol)


print(f"(robot-at robot2 tile_{x_r2}-{y_r2+1})")
print("(robot-has robot2 black)")

print("(available-color white)")
print("(available-color black)")
print("(nada1)")


for i in range(nrow):
    for j in range(ncol):
        if (x_r1 == i and y_r1 == j) or (x_r2 == i and y_r2 == j):
            pass
        else:
            print(f"(clear tile_{i}-{j+1})")

for i in range(1,nrow):
    for j in range(ncol):
        print(f"(up tile_{i}-{j+1} tile_{i-1}-{j+1})")

for i in range(nrow-1):
    for j in range(ncol):
        print(f"(down tile_{i}-{j+1} tile_{i+1}-{j+1})")

for i in range(nrow):
    for j in range(1,ncol):
        print(f"(right tile_{i}-{j+1} tile_{i}-{j})")

for i in range(nrow):
    for j in range(ncol-1):
        print(f"(left tile_{i}-{j+1} tile_{i}-{j+2})")

print(")")

print("(:goal (and")

for i in range(1,nrow):
    for j in range(1,ncol+1):
        if (i+j)%2 == 0:
            print(f"(painted tile_{i}-{j} white)")
        else:
            print(f"(painted tile_{i}-{j} black)")

    

print("))")

print(")")
