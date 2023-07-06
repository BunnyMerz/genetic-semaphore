from traffic import Car, Semaphore, Road
from path import initialize
from random import randint as rng

def run(roads: list[Road], cars: list[Car], sems: list[Semaphore]):
    i = 0
    while(1):
        for car in cars:
            car.drive()
        
        cars = [car for car in cars if not car.done]

        for s in sems:
            s.tick()

        i += 1
        if cars == []:
            break


def best(genes, fitness):
  fitness, genes = (list(t) for t in zip(*sorted(zip(fitness, genes))))
  return genes[-1], fitness[-1]
  
def squish(x, a, y):
   return max(min(a, y), x)

def mix(gene1, fitness1, gene2, fitness2,mutation_rate=70):
  tf = fitness1 + fitness2
  f1 = int(100*fitness1/tf)
  set_size = 3

  new_gene = []
  for i in range(0, len(gene1),set_size):
    if rng(0, 100) < f1:
      g = gene1[i:i+set_size]
    else:
      g = gene2[i:i+set_size]
    for x in range(set_size):
      if rng(0, mutation_rate) == 0:
        d = rng(-30,30)
        g[x] = squish(5, g[x]+d, 60)
    new_gene += g
  return new_gene
      

def get_gene(genes, fitness, tf):
  i = 0
  f = fitness[i]
  while(tf > f and i < len(fitness)):
    tf -= f
    i += 1
    f = fitness[i]
  return i

def reproduce(genes, fitness, tf):
  fitness, genes = (list(t) for t in zip(*sorted(zip(fitness, genes))))

  population_size = len(genes)
  cut = population_size // 4

  new_genes = genes[:cut]
  for _ in range(len(genes) - cut):
    x = get_gene(genes, fitness, rng(0, tf))
    y = get_gene(genes, fitness, rng(0, tf))
    new_genes.append(mix(genes[x], fitness[x], genes[y], fitness[y]))

  return new_genes

def iterate(genes, _rounds, roads_info, matrix, cars_amount):
  history = []
  try:
    for round in range(_rounds):  
      # if round % 5 == 0:
      print("r:",round)
      # print("Round:",round, end=" | ")
      fitness = []
      tf = 0
      _print = []
      for gene in genes:
        cars,roads,sems = initialize(roads_info, matrix, gene, cars_amount)
        # print(end='.')
        run(roads, cars, sems)
        # print(end=', ')
        s = 0
        for x in cars:
            if x.total_time == 0:
                continue
            av = x.total_distance_travelled/x.total_time
            s+=av
        average = s/len(cars)
        tf += int(average)
        fitness.append(int(average))
        # _print.append(f"{s/len(cars)} for gene {gene}")

      # _, _print = (list(t) for t in zip(*sorted(zip(fitness, _print))))
      # print()
      # [print(x) for x in _print[::-1]]
      # print("Reproducing")
      print(best(genes, fitness)[1])
      history.append(best(genes, fitness)[1])
      genes = reproduce(genes, fitness, tf)
      # print("Result:",genes)
  except KeyboardInterrupt:
    pass
  print("|".join([str(x) for x in history]))
  return genes, fitness
