
from session import Session
from car import Car, CarRun

class SessionDev(Session):

    def __init__(self):
        Session.__init__(self)

        car_a = CarRun(Car("HAM", "#00D2BE"))
        car_a.speed = 30

        car_b = CarRun(Car("VER", "#1E41FF"))
        car_b.speed = 28

        self.cars = [car_a, car_b]

    def get_cars(self):

        return self.cars