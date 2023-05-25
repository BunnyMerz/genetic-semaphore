from traffic import *

s1 = Semaphore(7, 7)
s2 = Semaphore(7, 7)
#     a,    b,    c,    d,    e,    f,    g,    h,    i,    j
ss = [s1  , s2  , None, s2  , s1  , None, s1  , None, None, s2]
si = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

roads = [Road(ss[x], si[x], 4) for x in range(10)]
cars = [
    Car([roads[x % 6] for x in range(1,12)]),
    Car([roads[1],roads[2]]),
    Car([roads[4],roads[5]]),
    Car([roads[4],roads[5]]),
    Car([roads[4],roads[5]]),
    Car([roads[4],roads[5]]),
    ]
roads[0].enter_road(cars[0])
# roads[0].enter_road(cars[1])
# roads[3].enter_road(cars[2])
# roads[3].enter_road(cars[3])
# roads[3].enter_road(cars[4])
# roads[3].enter_road(cars[5])

def print_roads(r: list[Road]):
    print()
    print(
        str(r[0])+str(int(r[0].semaphore_status())),'O ',
        str(r[1])+str(int(r[1].semaphore_status())),'O ',
        str(r[2])
    )
    print(
        str(r[5])[::-1],
        ' O',str(int(r[4].semaphore_status()))+str(r[4])[::-1],
        ' O',str(int(r[3].semaphore_status()))+str(r[3])[::-1]
    )

def run(roads: list[Road], cars: list[Car]):
    while(1):
        for road in roads:
            road.run()

        for road in roads:
            road.unbuffer()

        # print_roads(roads)

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