


from __future__ import division, print_function

from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc

from svgpathtools import svg2paths

def get_track(filename):
    paths, attributes = svg2paths(filename)
    return paths
