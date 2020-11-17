# Random function workbench

import random

d = 5
r = 10
def rand_f():
    return { i : random.randrange(r)
             for i in range(d) }

def eval(f, i):
    return f[i]
