import sys
from random import randrange

args = sys.argv


if len(args) != 4:
    print("Uso: <num_plantas> <num_personas> <num_bloques>")
    exit(-1)

plantas = int(args[1])
personas = int(args[2])
bloques = int(args[3])

ascensores = bloques + bloques//3

# Generacion del problema

print("(define (problem ascensor)")
print("(:domain ascensor)")
print("(:objects")

for i in range(personas):
    print("\tPE" + str(i) + ' - persona')

for i in range(plantas):
    print("\tPL" + str(i) + ' - planta')

for i in range(bloques):
    print("\tBL" + str(i) + " - bloque")

print("\tBLR - bloque")

for i in range(ascensores):
    print("\tAS" + str(i) + " - ascensor")

print("\tASR - ascensor")

print(")")

print("(:init")

for i in range(personas):
    print("\t(at_persona PE" + str(i) + " PL" + str(randrange(plantas)) + ")")

print("")

num_plantas_bloque = plantas // bloques

for i in range(bloques):
    if i != bloques-1:
        for j in range(num_plantas_bloque*i,num_plantas_bloque*(i+1) + 1):
            print("\t(corresponde PL"+str(j)+" BL"+str(i)+")")
    else:
        for j in range(num_plantas_bloque*i,num_plantas_bloque*(i+1)):
            print("\t(corresponde PL"+str(j)+" BL"+str(i)+")")
            
for i in range(0,plantas,2):
    print("\t(corresponde PL"+str(i)+" BLR)")

print("")

bloq_asc = dict()

for i in range(bloques):
    bloq_asc[i] = i
    print(f"\t(pertenece AS{i} BL{i})")

for i in range(bloques//3):
    bloq_asc[i+bloques] = randrange(bloques)
    print(f"\t(pertenece AS{i+bloques} BL{bloq_asc[i+bloques]})")

print("\t(pertenece ASR BLR)")


print("")

for i in range(ascensores):
    print(f"\t(at_ascensor AS{i} PL{bloq_asc[i]*num_plantas_bloque})")

print(")")

print("(:goal (and")

for p in range(personas):
    print("\t(at_persona PE" + str(p) + " PL" + str(randrange(plantas)) + ")")


print("))")

print(")")
