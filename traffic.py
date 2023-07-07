#### Units ####
# Distance:     m
# Time:         s
# All other units use the precious ones
# Speed:        m/s
# Acceleration: m/s²
######
class ID:
    _id = 1
    id = None
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.id = cls._id
        cls._id += 1
        return  obj

    def __repr__(self) -> str:
        return f"<{type(self).__name__}[{self.id}]: ?>"

class Semaphore(ID):
    def __init__(self, green: int, red: int, status: int = 0):
        # time in seconds
        self.clock = 0
        self.status = status > 0 # 0 red, 1 green
        self.red_timer = max(red,6)
        self.green_timer = max(green,6)
        self._fn = self.red
    def __repr__(self):
        return f"<{type(self).__name__}[{self.id}]: ({self.green_timer}|{self.red_timer})>"

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

class Road(ID):
    car_spacing = 2 # meters
    def __init__(self, semaphore: Semaphore, inverted_semaphore: bool, width: int):
        self.semaphore = semaphore
        self.inverted_semaphore = inverted_semaphore

        self.cars: list[Car] = [] # Ordered list by distance, by nature
        self.width = width

    def __str__(self) -> str:
        n = 200
        road = ["-"] * (self.width // n)
        for car in self.cars:
            road.insert(car.distance_driven // n, str(car.id))
            try:
                road.remove('-')
            except:
                pass

        return str.join('', road)

    def car_index(self, car: "Car"):
        return self.cars.index(car)

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
        self.cars.append(car)

class Car(ID):
    cache: list["Car"] = None
    def __init__(self, path: Road):
        self.current_road: Road = path.pop(0)
        self.current_road.enter_road(self)
        self.path: list[Road] = path
        self.distance_driven = 0 # Inside a Road
        self.speed = 0
        self.acceleration = 8
        self.max_speed = 60

        self.total_distance_travelled = 0
        self.total_time = 0
        self.wait_time = 0
        self.times_stopped = 0
        self.done = 0

    def __str__(self) -> str:
        return f"<Car[{self.id}]: roads_left: {len(self.path)}, distance_moved: {self.distance_driven}>"
    def __repr__(self):
        return f"<{type(self).__name__}[{self.id}]: ({'|'.join([str(x.id) for x in ([self.current_road]+self.path)])})>"
      
    def drive(self):
        self.total_time += 1
        self.accelerate()
        return self._drive(self.speed)

    def _drive(self, amount_to_drive):
        # if self.id == 1:
        #     print(f"Drive({amount_to_drive})",self)
        current_road = self.current_road
        car_index = current_road.car_index(self)
        if car_index > 0: # Another car in front of this one
            infront_car = current_road.cars[car_index - 1]
            distance = infront_car.distance_driven - self.distance_driven
            if distance - Road.car_spacing < amount_to_drive:
                self.speed = max(distance - Road.car_spacing, 0) ## Move just enough, but don't stop just yet
                self.move(self.speed)
            else:
                self.move(amount_to_drive)
        else: # First car
            if self.distance_driven + amount_to_drive <= current_road.width: # Even if it moves, it will still be in the same road
                self.move(amount_to_drive)
            else: # If it moves, it will cross the road
                if current_road.semaphore_status() == 0: # Red
                    self.move(current_road.width - self.distance_driven)
                    self.wait_time += 1
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
                            current_road.leave_road(self)
                            self.current_road = self.path.pop(0)
                            self.current_road.enter_road(self)
                            if amount_to_drive + self.distance_driven >= current_road.width:
                                delta = current_road.width - self.distance_driven
                                self.move(delta)
                                left_over = amount_to_drive - delta
                                self.distance_driven = 0
                                # print("*", end='')
                                return self._drive(left_over)
                            else:
                                self.move(amount_to_drive)
                        else: # Next road full. Wait as far as you can
                            self.move(current_road.width - self.distance_driven)
                            self.stop()

    def stop(self):
        if self.speed == 0:
            self.times_stopped += 1
        self.speed = 0

    def move(self, amount):
        self.distance_driven += amount
        self.total_distance_travelled += amount
    def accelerate(self):
        self.speed = min(self.speed+self.acceleration, self.max_speed)
