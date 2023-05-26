from traffic import *

def create_cars(paths, roads):
    cars = []
    for path in paths:
        _roads = path.split(',')
        cars.append(Car([roads[int(x)] for x in _roads]))
    return cars

s1 = Semaphore(7, 1)
s2 = Semaphore(7, 1)
#     a,    b,    c,    d,    e,    f,    g,    h,    i,    j
ss = [s1  , s2  , None, s2  , s1  , None, s1  , None, None, s2]
si = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

roads = [Road(ss[x], si[x], 200) for x in range(10)]
cars = create_cars(['1,2,3'] * 2, roads)

def print_roads(r: list[Road]):
    print()
    print(
        "|"+str(r[0])+str(["R","G"][int(r[0].semaphore_status())]),'O ',
        str(r[1])+str(["R","G"][int(r[1].semaphore_status())]),'O ',
        str(r[2])+"|"
    )
    print(
        "|"+str(r[5])[::-1],
        ' O',str(["R","G"][int(r[4].semaphore_status())])+str(r[4])[::-1],
        ' O',str(["R","G"][int(r[3].semaphore_status())])+str(r[3])[::-1]+"|"
    )

def run(roads: list[Road], cars: list[Car]):
    while(1):
        for car in cars:
            car.drive()
        
        cars = [car for car in cars if not car.done]

        print_roads(roads)
        a = 1 + 1

        for s in [s1,s2]:
            s.tick()

        if sum([len(x.cars) for x in roads]) == 0:
            break

run(roads, cars)
for x in cars: print(x)
print()
s = 0
for x in cars:
    if x.total_time == 0:
        continue
    av = x.total_distance_travelled/x.total_time
    print(f'Average: {av}')
    s+=av

print()
print(f"Cars average: {s/len(cars)}")