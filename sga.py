#!/usr/bin/python3

import random

r = 32
d = 32
npop = 1000
mut = 0.01
ngen = 500
trace = True

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
    for i in range(d):
        if random.random() < mut:
            f[i] = random.randrange(r)


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
        if mut > 0:
            mutate(pop[i])
    best = score(max(*pop, key=score))
    if best == d:
        break
    if trace:
        worst = score(min(*pop, key=score))
        print("gen", g, "best", best, "worst", worst)

best = max(*pop, key=score)
print("target")
print(target)
print("best")
print(best)
print("score")
print(score(best))
