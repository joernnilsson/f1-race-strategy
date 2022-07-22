
from turtle import width
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc
import matplotlib
matplotlib.use( 'tkagg')
import matplotlib.pyplot as plt
from matplotlib import pyplot, transforms
from matplotlib.animation import FuncAnimation
import logging
import time
import sys
from track import Track
import numpy as np

CAR = 'car'
PLOTS = 'plots'

log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

class MapView():

    def __init__(self, track):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.ax.axis('equal')
        self.cars = []
        self.track = track
        self.ani = None

        self.draw_track()

    def draw_track_(self):
        for line in self.track.path:
            plt.plot([line.start.real, line.end.real], [-line.start.imag, -line.end.imag], color = 'r', marker = 'o')


    def draw_track(self):
        x, y = self.track.get_map()

        # Track
        plt.plot(x, y, color = 'k', linewidth = 10)

        # Start/finish
        p_0 = np.array([x[0], y[0]])
        p_1 = np.array([x[10], y[10]])

        p_diff = p_1 - p_0
        print(p_diff, np.linalg.norm(p_diff))
        track_direction = (p_diff) / np.linalg.norm(p_diff)
        orthogonal = np.array([track_direction[1], -track_direction[0]])

        p_2 = (p_0 + orthogonal*40)
        p_3 = (p_0 - orthogonal*40)

        plt.plot([p_0[0], p_2[0]], [p_0[1], p_2[1]], color = 'k', linewidth = 2)
        plt.plot([p_0[0], p_3[0]], [p_0[1], p_3[1]], color = 'k', linewidth = 2)


    def set_cars(self, cars):
        for c in cars:
            marker, = plt.plot([], [], color = c.car.color, marker = 'o')
            name = matplotlib.pyplot.text(0, 0, c.car.name)
            self.cars.append({
                CAR: c,
                PLOTS: [marker, name]
            })

    def update_pos(self, i=0):
        for c in self.cars: 
            c[PLOTS][0].set_data(c[CAR].x, c[CAR].y)
            c[PLOTS][1].set_position([c[CAR].x, c[CAR].y])
            
    def update_dist(self, i=0):
        for c in self.cars: 
            lap_distance = c[CAR].distance % self.track.length

            acc_dist = 0
            for line in self.track.path:
                line_end = acc_dist + line.length()
                if lap_distance < line_end:
                    line_distance = lap_distance - acc_dist
                    pos = line.start + (line.end - line.start) * line_distance / line.length()
                    c[PLOTS][0].set_data(pos.real, -pos.imag)
                    c[PLOTS][1].set_position([pos.real +5, -pos.imag-5])
                    break
                acc_dist = line_end

    def show(self):

        self.ani = FuncAnimation(self.fig, self.update_pos, interval=0.01)
        plt.show(block=True)

if __name__ == "__main__":
    track = Track(sys.argv[1])
    MapView(track)
    plt.show()