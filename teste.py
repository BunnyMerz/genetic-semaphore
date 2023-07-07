from genes import *
from random import randint as rng
from test import *

gene = [rng(0,100) for _ in range(num_sem * 3)]
cars,roads,sems = initialize(roads_info, matrix, gene, 10)
for x in range(1):
    print("--")
    an_run(cars)
    wait_time = 0
    avg = 0
    distance = 0
    time = 0
    for car in cars:
        print(f"Avg of {int(car.total_distance_travelled)}/{int(car.total_time)} = {(car.total_distance_travelled/car.total_time)}")

        avg += (car.total_distance_travelled/car.total_time)**2
        distance += car.total_distance_travelled
        time += car.total_time
        wait_time += car.wait_time

        car: Car
        car.total_distance_travelled = 0
        car.total_time = 0

    print()
    print(f" Wait time of {wait_time}s, avg = {distance/time} or {avg/len(cars)}")