#!/usr/bin/python3

import random

# Range of function: for each input
# output a value in 0..r-1.
r = 32
# Domain of function: input must be in the range 0..d-1.
d = 32
# Size of population. Should be even.
npop = 1000
# Mutation rate.
mut = 0.01
# Retention rate.
retained = 0.5
# Maximum number of generations to run the simulation.
# (Will stop early on a perfect score.)
ngen = 500
# Show progress iff True.
trace = True

# Construct a random integer function with the given domain
# and range. Functions are represented as dictionaries for
# easy manipulation.
def rand_f():
    return { i : random.randrange(r)
             for i in range(d) }

# Pick a random target function.
target = rand_f()

# Score of a function f in matching the
# target is the number of domain values
# on which the outputs are equal.
def score(f):
    return sum([int(f[i] == target[i])
                for i in range(d)])
    
# Given two functions f1 and f2, return
# the one that scores higher when matched
# against the target.
def tourney(i1, f1, i2, f2):
    if score(f1) > score(f2):
        return i2
    else:
        return i1

# Pick a random "split point" in the genome. Construct a new
# function by picking genes from f1 up to the splitpoint,
# and genes from f2 after.
def crossover(f1, f2):
    c = random.randrange(d)
    f = dict()
    for i in range(c):
        f[i] = f1[i]
    for i in range(c, d):
        f[i] = f2[i]
    return f


# For each gene in f, change it to a new random value with
# probability mut.
def mutate(f):
    for i in range(d):
        if random.random() < mut:
            f[i] = random.randrange(r)

# Construct an initial random population.
pop = [rand_f() for _ in range(npop)]

# Run the GA loop.
for g in range(ngen):
    # Shuffle the population up.
    random.shuffle(pop)

    # Run the tournament.
    split = int(npop * retained)
    surviving = npop
    while surviving > split:
        i = random.randrange(surviving)
        j = random.randrange(surviving)
        if i == j:
            continue
        remove = tourney(i, pop[i], j, pop[j])
        del pop[remove]
        surviving -= 1
        
    # Replace the losers with combinations
    # of random pairs of winners.
    for i in range(split, npop):
        left = random.randrange(split)
        right = random.randrange(split)
        pop.append(crossover(pop[left], pop[right]))
        # This test is strictly an efficiency hack.
        if mut > 0:
            mutate(pop[-1])
    assert len(pop) == npop

    # Find the best score achieved and stop if it is
    # perfect.
    best = score(max(*pop, key=score))
    if best == d:
        break

    # If tracing, show best and worst scores for this
    # generation.
    if trace:
        worst = score(min(*pop, key=score))
        print("gen", g, "best", best, "worst", worst)

# Show final results.
best = max(*pop, key=score)
print("target")
print(target)
print("best")
print(best)
print("score")
print(score(best))
