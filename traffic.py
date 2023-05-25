#### Units ####
# Distance:     m
# Time:         s
# All other units use the precious ones
# Speed:        m/s
# Acceleration: m/s²
######


class Semaphore:
    def __init__(self, green: int, red: int):
        # time in seconds
        self.clock = 0
        self.status = 0 # 0 red, 1 green
        self.red_timer = red
        self.green_timer = green
        self._fn = self.red

    def red(self):
        if self.clock > self.red_timer:
            self.clock = 0
            self.status = 1
            self._fn = self.green
    def green(self):
        if self.clock > self.green_timer:
            self.clock = 0
            self.status = 0
            self._fn = self.red
            
    def tick(self, time=1):
        self.clock += time
        return self._fn()

class Road:
    _id = 0
    car_spacing = 2 # meters
    def __init__(self, semaphore: Semaphore, inverted_semaphore: bool, width: int):
        self.id = Road._id
        Road._id+=1

        self.semaphore = semaphore
        self.inverted_semaphore = inverted_semaphore

        self.cars: list[Car] = [] # Ordered list by distance, by nature
        self.width = width

        self.car_buffer = []

    def __str__(self) -> str:
        n = 1
        road = ["-"] * (self.width // n)
        for car in self.cars:
            road.insert(car.distance_driven // n, 'X')
            road.remove('-')

        return str.join('', road)

    def run(self):
        i = 0
        cars = self.cars[:]
        while(i < len(cars)):
            car = cars[i]
            car.drive(self, i)
            i += 1

    def semaphore_status(self):
        if self.semaphore == None:
            return 1 # Implicit green traffic light
        
        if self.inverted_semaphore:
            return not self.semaphore.status
        return self.semaphore.status

    def available_space(self):
        if self.cars == []:
            return True
        return self.cars[-1].distance_driven > Road.car_spacing
    
    def leave_road(self, car: "Car"):
        self.cars.remove(car)
    def enter_road(self, car: "Car"):
        self.car_buffer.append(car)
    def unbuffer(self):
        self.cars += self.car_buffer
        self.car_buffer = []

class Car:
    def __init__(self, path: Road):
        self.path: list[Road] = path
        self.distance_driven = 0 # Inside a Road
        self.speed = 0
        self.acceleration = 2
        self.max_speed = 40

        self.total_distance_travelled = 0
        self.total_time = 0
        self.done = 0

        self.left_over = 0

    def __repr__(self) -> str:
        return f"<Car: roads_left: {len(self.path)}, distance_moved: {self.distance_driven}>"

    def drive(self, current_road: Road, car_index: int):
        self.total_time += 1
        if car_index > 0: # Another car in front of this one
            infront_car = current_road.cars[car_index - 1]
            distance = infront_car.distance_driven - self.distance_driven
            if distance - Road.car_spacing < self.speed:
                self.speed = max(distance - Road.car_spacing, 0) ## Move just enough, but don't stop just yet
                self.move()
            else:
                self.move()
                self.accelerate()
        else: # First car
            if self.distance_driven + self.speed <= current_road.width: # If it moves, it will still be in the same road
                self.move()
                self.accelerate()
            else: # Would cross the road
                if current_road.semaphore_status() == 0: # Red
                    self.distance_driven = current_road.width
                    self.stop()
                else:
                    if self.path == []:
                        self.distance_driven = None
                        current_road.leave_road(self)
                        self.done = 1
                        return
                    else:
                        next_road = self.path[0]
                        if next_road.available_space():
                            self.path.pop(0)
                            current_road.leave_road(self)
                            ## TODO Bug
                            # Car can offshot on another road and either pass other cars, or not go trough the entire road. The leftover of the bottom equation may be bigger than the road (getting stuck at the end of it instead of passing trough) or smaller and possibly going over cars.
                            # The problem with solving this are road buffers. It won't take into account other cars that also went trough another road. Taking out the buffer may make cars move twice in one turn
                            # Maybe make it so you iterate over cars, rather than roads
                            self.distance_driven = (self.distance_driven + self.speed) - current_road.width
                            next_road.enter_road(self)            

    def stop(self):
        self.speed = 0
    def move(self):
        self.distance_driven += self.speed
        self.total_distance_travelled += self.speed
    def accelerate(self):
        self.speed = min(self.speed+self.acceleration, self.max_speed)

