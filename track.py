

from __future__ import division, print_function
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc
from svgpathtools import svg2paths

import logging

import yaml
from yaml.loader import SafeLoader

import numpy as np
import os

class TrackMap:
    def __init__(self, distance_index, x, y) -> None:
        self.d = distance_index
        self.x = x
        self.y = y


    def get_xy_map(self):
        return self.x, self.y

class Track:
    
    def __init__(self, id):
        
        self.id = id
        self.length = 4318
        self.path_length = 0.0
        self.path = None
        self.map = None

        #self.load_svg(self.length)
        self.load_xy_map('./tracks/' + self.id + '/track_profile.npy')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    def get_map(self):
        return self.map.get_xy_map()

    def load_xy_map(self, filename):
        print("Exists:", os.getcwd(), filename, os.path.exists(filename))
        distance_index, mean_speed_profile, mean_x_profile, mean_y_profile = np.load(filename, allow_pickle=True)
        self.map = TrackMap(distance_index, mean_x_profile, mean_y_profile)


    def load_svg(self, real_length):
        filename = "tracks/"+self.id+"/track.svg"
        paths, attributes = svg2paths(filename)
        path = paths[0]
        path_length = sum([l.length() for l in path])

        scale = self.length / path_length

        offset = complex(-75, -411)
        for l in path:
            l.start *= scale
            l.end *= scale
            l.start += offset
            l.end += offset

        self.path = path
        self.path_length = path_length
