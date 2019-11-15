#!/usr/bin/python3

import random

r = 16
d = 32
npop = 1000
mut = 0.5
ngen = 50


def rand_f():
    return { i : random.randrange(r)
             for i in range(d) }

target = rand_f()

def score(f):
    return sum([int(f[i] == target[i])
                for i in range(d)])
    
def tourney(f1, f2):
    return max(f1, f2, key=score)

def crossover(f1, f2):
    c = random.randrange(d)
    f = dict()
    for i in range(c):
        f[i] = f1[i]
    for i in range(c, d):
        f[i] = f2[i]
    return f


def mutate(f):
    f[random.randrange(d)] = random.randrange(r)


split = npop // 2

pop = [rand_f() for _ in range(npop)]

for g in range(ngen):
    random.shuffle(pop)
    left = pop[split:]
    right = pop[:split]
    for i in range(split):
        pop[i] = tourney(left[i], right[i])
    for i in range(split, npop):
        left = random.randrange(split)
        right = random.randrange(split)
        pop[i] = crossover(pop[left], pop[right])
        if random.random() < mut:
            mutate(pop[i])
    best = max(*pop, key=score)
    print("gen", g, "score", score(best))

best = max(*pop, key=score)
print("target")
print(target)
print("best")
print(best)
print("score")
print(score(best))
