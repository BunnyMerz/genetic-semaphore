from random import randint as rng
from traffic import Car, Road, Semaphore



def path(matrix, number_matrix, roads, dest, path_stack, cost):
  if matrix[path_stack[-1]][dest] == 1:
    return [path_stack+[dest, str(cost)]]

  paths = []
  for option in number_matrix[path_stack[-1]]:
    if option not in path_stack:
      paths += path(
        matrix, number_matrix, roads,
        dest,
        path_stack + [option], cost + roads[option].width
      )
  return paths
def path_finding(matrix, number_matrix, roads, source, dest):
  paths = path(matrix, number_matrix, roads, dest, [source], roads[source].width)
  if paths == []: return None
  best_cost = int(paths[0][-1])
  best_path = paths.pop(0)[:-1]

  for other in paths:
    cost = int(other[-1])
    if cost < best_cost:
      best_cost = cost
      best_path = other[:-1]
  return best_path

def generate_car(roads, matrix):
  number_matrix = [[x for x in range(len(road)) if road[x]] for road in matrix]
  c = roads[:]
  source = roads.index(c.pop(rng(0, len(c)-1)))
  dest = roads.index(c.pop(rng(0, len(c)-1)))

  _path = path_finding(matrix, number_matrix, roads, source, dest)
  return Car([roads[x] for x in _path])

def initialize(roads_info, matrix, gene, car_amount):
  Semaphore._id = 0
  Car._id = 0
  Road._id = 0
  sems = [Semaphore(gene[x], gene[x+1], gene[x+2]) for x in range(0, len(gene), 3)]

  roads = []
  for x in range(len(roads_info)):
    width, sem_id, invert = roads_info[x]
    if sem_id == None:
      sem = None
    else:
      sem = sems[sem_id]
    roads.append(Road(sem, invert, width))

  cars = []
  for x in range(car_amount):
    car = generate_car(roads, matrix)
    cars.append(car)

  return cars, roads, sems