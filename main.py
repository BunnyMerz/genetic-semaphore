from genes import iterate
from random import randint as rng
from test import *
from path import initialize, initi_rotat


for gg in [20]:
  for cars in [40]:
    genes = [[rng(6,60) if x != 3 else rng(0,1) for x in range(num_sem * 3)] for _ in range(gg)]
    print(f"Genes: {gg}, Cars: {cars}, Len genes: {len(genes)}")

    # # print("Simulated")
    # _r, f = iterate(genes, 5, roads_info, matrix, cars, _type="real wait")
    # f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
    # # print("/".join([str(x) for x in r[0]]))
    # # print(f[0])
    # genes = _r
    for retries in range(10):
      print('Round', retries)
      
      # # print("Analitic")
      # _r, f = iterate(genes, 20, roads_info, matrix, cars, _type="test wait")
      # f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
      # # print("/".join([str(x) for x in r[0]]))
      # # print(f[0])
      # genes = _r

      # print("Simulated")
      _r, f = iterate(genes, 30, roads_info, matrix, cars, _type="real wait")
      f, r = (list(t) for t in zip(*sorted(zip(f, _r), reverse=True)))
      # print("/".join([str(x) for x in r[0]]))
      # print(f[0])
      genes = _r
