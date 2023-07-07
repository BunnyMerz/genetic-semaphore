from traffic import Car, Semaphore, Road
from path import initialize, initi_rotat
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

def an_run(cars: list[Car]):
    # print("//")
    k = 0
    tw = 0
    for car in cars:
      # print("Car",k)
      k += 1
      total_time_taken = 0
      total_wait_time = 0
      travelled = 0
      speed = car.speed
      max_speed = car.max_speed
      accel = car.acceleration
      times_stopped = 0

      complete_path = [car.current_road] + car.path
      i = 0
      for road in complete_path:
        # print(" Road",i)
        # print(f"  Width of {road.width}m, Car speed at {int(speed)}/{max_speed}")
        i+=1
        total_distance = road.width

        if accel != 0:
          ## If you can increase speed
          if speed < max_speed:
            distance_until_max_speed = (max_speed**2 - speed**2)/(2*accel)
            # print(f"  Not at max speed.")

            # print(f"  {distance_until_max_speed}m until max speed out of {total_distance}m")
            if distance_until_max_speed <= total_distance: # Move until max speed
              # print(f"  % Road big enough. Distance of {distance_until_max_speed}m")
              time_taken = -speed/accel + (speed**2 + 2*accel*distance_until_max_speed)**(1/2)
              total_distance -= distance_until_max_speed
              ## Effect
              total_time_taken += time_taken
              travelled += distance_until_max_speed
              speed = max_speed
            else: # Move as far as you can, while increasing speed
              time_taken = ((speed**2 + 2*accel*total_distance)**(1/2) - speed)/accel
              # Effect
              travelled += total_distance 
              total_distance -= total_distance
              total_time_taken += time_taken
              # print(f"  $ Road not big enough. Speed went from {speed} -> {speed + time_taken*accel}")
              speed += time_taken*accel
        
        ## If this loop is ran, max speed reached but haven't travelled enough
        if total_distance > 0:
          # print(f"  # Driving rest of {total_distance}m at max speed")
          time_taken = total_distance/speed

          total_time_taken += time_taken
          travelled += total_distance
          total_distance = 0
        # else: print("  Already covered the whole road.")

        ## Check if lights are red
        sem = road.semaphore
        if sem != None:
          sem_status = int(not(sem.status)) if road.inverted_semaphore else sem.status
          if road.inverted_semaphore:
            sem_red_timer = sem.green_timer
            sem_green_timer = sem.red_timer
          else:
            sem_red_timer = sem.red_timer
            sem_green_timer = sem.green_timer

          _time = sem_red_timer + sem_green_timer
          # print(f"  Status {sem_status}")
          # if sem_status: print(f"  G{sem_green_timer}, R{sem_red_timer}, T{total_time_taken}, _T{(total_time_taken) % _time}")
          # else: print(f"  R{sem_red_timer}, G{sem_green_timer}, T{total_time_taken}, _T{(total_time_taken) % _time}")

          got_red = False
          wait_time = 0
          if sem_status == 0: # red -> green
            if int(total_time_taken) % _time <= sem_red_timer:
              got_red = True
              wait_time = sem_red_timer - (int(total_time_taken) % _time)
          else: # green -> red
            if int(total_time_taken) % _time > sem_green_timer:
              got_red = True
              wait_time = sem_red_timer - ((int(total_time_taken) % _time) - sem_green_timer)

          if got_red:
            # print(f"   -!Stopped at a red light and lost {wait_time+1}s")
            speed = 0
            total_time_taken += wait_time + 3 ## +1 to avoid going too fast as soon as the lights are green
            total_wait_time += wait_time + 3
            times_stopped += 1

      car.total_distance_travelled = travelled
      car.total_time = total_time_taken
      car.wait_time = total_wait_time
      car.times_stopped = times_stopped
      tw += times_stopped


def best(genes, fitness):
  fitness, genes = (list(t) for t in zip(*sorted(zip(fitness, genes))))
  return genes[-1], fitness[-1]
  
def squish(x, a, y):
   return max(min(a, y), x)

def mix(gene1, fitness1, gene2, fitness2,mutation_rate=20):
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
      if x < 2: # g or r
        if rng(0, mutation_rate) == 0:
          d = rng(-10,10)
          g[x] = squish(6, g[x]+d, 60)
        else:
          g[x] = squish(6, g[x], 60)
      else: # status
        if rng(0, mutation_rate) == 0:
          d = rng(-5,5)
          g[x] = squish(0, g[x]+d, 1)
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
  fitness, genes = (list(t) for t in zip(*sorted(zip(fitness, genes), reverse=True)))

  population_size = len(genes)
  cut = population_size // 5

  new_genes = genes[:cut]
  for _ in range(len(genes) - cut):
    x = get_gene(genes, fitness, rng(0, tf))
    y = get_gene(genes, fitness, rng(0, tf))
    new_genes.append(mix(genes[x], fitness[x], genes[y], fitness[y]))

  return new_genes

def iterate(genes, _rounds, roads_info, matrix, cars_amount, _type, initializing=initialize):
  history = []
  try:
    for round in range(_rounds):  
      # if round % 5 == 0:
      # print("r:",round)
      # print("Round:",round, end=" | ")
      fitness = []
      tf = 0
      _print = []
      for gene in genes:
        cars,roads,sems = initializing(roads_info, matrix, gene, cars_amount)
        # print(end='.')
        if "real" in _type:
          run(roads, cars, sems)
        if "test" in _type:
          an_run(cars)
        # print(end=', ')
        s = 0
        avg_speed = 0
        times_stopped = 0
        for x in cars:
            x: Car
            s += x.wait_time
            avg_speed += x.total_distance_travelled/x.total_time
            times_stopped += x.times_stopped
        avg_speed /= len(cars)

        if "speed" in _type:
          s = avg_speed
          # print(f"  {s} points; {int(avg_speed)}m/s; {times_stopped}; - {gene}")
          tf += int(s)
          fitness.append(int(s))
        if "wait" in _type:
          s = (1/(s+1)) * 10000000
          # print(f"  {s} points; {int(avg_speed)}m/s; {times_stopped}; - {gene}")
          tf += int(s)
          fitness.append(int(s))

        # average = s/len(cars)
        # tf += int(average)
        # fitness.append(int(average))
        # _print.append(f"{s/len(cars)} for gene {gene}")

      # _, _print = (list(t) for t in zip(*sorted(zip(fitness, _print))))
      # print()
      # [print(x) for x in _print[::-1]]
      # print("Reproducing")
      if "wait" in _type:
        # print("",10000000/best(genes, fitness)[1] - 1, best(genes, fitness)[1], best(genes, fitness)[0])
        print(["a","s"]["real" in _type],int(10000000/best(genes, fitness)[1] - 1))
        history.append(10000000/best(genes, fitness)[1] - 1)
      if "speed" in _type:
        print("",best(genes, fitness)[1], best(genes, fitness)[0])
        history.append(best(genes, fitness)[1])
      
      if _rounds == round+1:
        break
      genes = reproduce(genes, fitness, tf)
      # print("Result:",genes)
  except KeyboardInterrupt:
    pass
  # print("|".join([str(x) for x in history]))
  return genes, fitness
