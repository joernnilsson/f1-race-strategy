#!/usr/bin/env python3


import sys
import os
import math
import string
import threading
import time

import logging

import track_parser
import track_visualizer

from track_visualizer import MapView
from track import Track
from car import Car, CarRun
from sim_runner import Sim

from session_dev import SessionDev
from session_dev_fastf1 import SessionFastF1

from position_provider_fastf1 import PositionProviderFastF1

def main():

    visualize = True

    track = Track("red_bull_ring")

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
    logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    log = logging.getLogger(__file__)
    log.setLevel(logging.DEBUG)

    log.info(f"info Loaded {track.id}")

    #track_visualizer.draw_track(track.path)

    #session = SessionDev()
    #session = SessionFastF1(2022, 'Canadian Grand Prix')
    session = SessionFastF1(2021, 'Austrian Grand Prix')

    map = MapView(track)
    map.set_cars(session.get_cars())

    position_provider = PositionProviderFastF1(session)

    # Start simulation
    #sim = Sim(session.get_cars(), 0.1, 0.02 if visualize else 0.0)
    #sim.start()
    position_provider.start_playback(5.0)

    # Main gui loop
    if visualize:
        map.show()
        #sim.quit = True
        position_provider.quit = True

    #sim.join()
    position_provider.join()


if __name__ == "__main__":
    main()

    #-289 -227
    #-214 -638