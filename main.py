from genes import iterate
from random import randint as rng
from test import *
from path import initialize, initi_rotat
from ant_colony_opt import ant_optimization
import time

total_genes = 40
cars = 15
ANT = True
ANALITIC = True
SIMULATED = True

genes = [[rng(6,60) if x != 3 else rng(0,1) for x in range(num_sem * 3)] for _ in range(total_genes)]
og_genes = [gene.copy() for gene in genes]
print(f"Genes: {total_genes}, Cars: {cars}, Len genes: {len(genes)}")

# Pre-compute
_r, f = iterate(genes, 5, roads_info, matrix, cars, _type="real wait")
f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
genes = _r

start = time.time()
for retries in range(10):
  print('Round', retries)
  print("time",time.time() - start)
  # print("Analitic")

  if ANALITIC:
    print(";")
    _r, f = iterate(genes, 15, roads_info, matrix, cars, _type="test wait")
    f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
    genes = _r
    print("$")


  if SIMULATED:
    _r, f = iterate(genes, 15, roads_info, matrix, cars, _type="real wait")
    f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
    genes = _r

  if ANT:
    print("Opt gene 0")
    genes[-1] = ant_optimization(r[0], cars//2)
    print("Opt gene 1")
    genes[-2] = ant_optimization(r[0], cars//2)
    print("Opt gene 2")
    genes[-3] = ant_optimization(r[0], cars//2)
    print("Opt gene 3")
    genes[-4] = ant_optimization(r[0], cars//2)
    print("Opt gene 4")
    genes[-5] = ant_optimization(r[0], cars//2)
    print("Opt gene 5")
    genes[-6] = ant_optimization(r[0], cars//2)

  if SIMULATED:
    _r, f = iterate(genes, 15, roads_info, matrix, cars, _type="real wait")
    f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
    genes = _r