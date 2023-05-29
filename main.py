from _main import iterate
from random import randint as rng
from test import *
for gg in [250]:
  for cars in [50]:
    for retries in range(1):
      print('-')
      print(f"{retries},{gg},{cars}")
      genes = [[rng(0,100) for _ in range(num_sem * 3)] for _ in range(gg)]
      
      r, f = iterate(genes, 100, roads_info, matrix, cars)
      f, r = (list(t) for t in zip(*sorted(zip(f, r), reverse=True)))
      print("|".join([str(x) for x in r[0]]))
      print(f[0])



  
  

  