
from http.client import CannotSendRequest
import threading
import time
import random

class Sim(threading.Thread):
    def __init__(self, cars, step, interval = 0.0):
        threading.Thread.__init__(self)

        self.step = step
        self.interval = interval
        self.time_elapsed = 0.0

        self.cars = cars

        self.quit = False

    def randomize_speed(self):
        
        for c in self.cars:
            c.speed = random.uniform(27, 30)


    def run(self):
        
        print("Staring simulation")
        self.randomize_speed()

        checkerd_flag = False
        while not self.quit and not checkerd_flag:

            # Update positions
            for c in self.cars:
                c.distance += self.step*c.speed
                if c.distance > 4318.0:
                    checkerd_flag = True
            self.time_elapsed += self.step

            if self.interval > 0.0:
                time.sleep(self.interval)
    