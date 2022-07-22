
from threading import Thread
import time
import pandas

class PositionProviderFastF1(Thread):

    def __init__(self, session):
        Thread.__init__(self)
        self.quit = False
        self.speedup = 1.0

        self.session = session


    def start_playback(self, speedup = 1.0):
        self.speedup = speedup
        self.start()

    def run(self):

        print("Playing back race")

        playback_time = 0.0

        for index, row in self.session.race.session_status.iterrows():
            if row.Status == "Finalised":
                session_end = row.Time
        session_start = self.session.race.session_start_time
        print(session_start, session_end)

        i = 20000
        playback_time = self.session.race.pos_data[self.session.cars[0].car.number].SessionTime[i].total_seconds()
        while not self.quit:

            # Update positions
            for c in self.session.cars:
                c.distance += 0.01*c.speed

            for c in self.session.cars:
                data = self.session.race.pos_data[c.car.number]#.slice_by_time(start, end)
                c.x = data.X[i]/10.0
                c.y = data.Y[i]/10.0

            last_playback_time = playback_time
            playback_time = self.session.race.pos_data[self.session.cars[0].car.number].SessionTime[i].total_seconds()
            sleep_time = playback_time - last_playback_time
            time.sleep(sleep_time/self.speedup)
            i += 1
