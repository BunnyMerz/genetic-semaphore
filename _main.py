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
  
def mix(gene1, fitness1, gene2, fitness2,mutation_rate=50):
  tf = fitness1 + fitness2
  f1 = int(100*fitness1/tf)
  f2 = 100 - f1

  new_gene = []
  for i in range(len(gene1)):
    if rng(0, 100) < f1:
      g = gene1[i]
    else:
      g = gene2[i]
    if rng(0, mutation_rate) == 0:
      if i % 3 != 2: # green, red
        d = rng(-30,30)
        g = max(min(g+d, 60), 5)
      # elif rng(0,1000) == 0: # status
      #   g = int(not g)
    new_gene.append(g)
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

  new_genes = []
  for _ in range(len(genes)):
    x = get_gene(genes, fitness, rng(0, tf))
    y = get_gene(genes, fitness, rng(0, tf))
    new_genes.append(mix(genes[x], fitness[x], genes[y], fitness[y]))

  return new_genes

def iterate(genes, _rounds, roads_info, matrix, cars_amount):
  history = []
  for round in range(_rounds):
    if round % 5 == 0:
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
    history.append(best(genes, fitness)[1])
    genes = reproduce(genes, fitness, tf)
    # print("Result:",genes)
  print("|".join([str(x) for x in history]))
  return genes, fitness
