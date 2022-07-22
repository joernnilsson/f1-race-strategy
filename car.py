

class Car:

    def __init__(self, name, color, number = ""):
        self.name = name
        self.color = color
        self.number = number



class CarRun:

    def __init__(self, car):
        self.car = car
        self.lap = 0
        self.speed = 0.0
        self.distance = 0.0

        self.x = 0.0
        self.y = 0.0
    
        
