
from session import Session
from car import Car, CarRun
from constants import TEAM_COLORS
import utils

import fastf1


class SessionFastF1(Session):

    def __init__(self, year, event):
        Session.__init__(self)

        fastf1.Cache.enable_cache('/fastf1_cache/api')  # optional but recommended

        self.race: fastf1.core.Session = fastf1.get_session(year, event, 'R')
        self.race.load(telemetry = True, laps = True, messages = True, weather = True)

        self.cars = []
        for d in self.race.drivers:
            info: fastf1.core.Driver = self.race.get_driver(d)

            abbr = info["Abbreviation"]
            number = info["DriverNumber"]

            # Determine color
            if number in fastf1._DRIVER_TEAM_MAPPING:
                team = fastf1._DRIVER_TEAM_MAPPING[number]["TeamName"]
                color = TEAM_COLORS[team]
            else:
                color = "black"

            self.cars.append(CarRun(Car(abbr, color, number = number)))

        # utils.plot(self.race.pos_data['33'].X, t=self.race.pos_data['33'].Time)
        # utils.plot(self.race.pos_data['33'].Y)
        # utils.plot(self.race.pos_data['33'].Z)

    def get_cars(self):

        return self.cars