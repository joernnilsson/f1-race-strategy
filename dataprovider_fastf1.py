import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
import os


def main():
    #os.makedirs("/fastf1_cache", exist_ok=True)

    plotting.setup_mpl()

    fastf1.Cache.enable_cache('/fastf1_cache/api')  # optional but recommended

    #schedule = fastf1.get_event_schedule(2022)
    #print(schedule)
    #return

    race = fastf1.get_session(2022, 'Canadian Grand Prix', 'R')
    race.load()

    lec = race.laps.pick_driver('LEC')
    ham = race.laps.pick_driver('HAM')


    fig, ax = plt.subplots()
    ax.plot(lec['LapNumber'], lec['LapTime'], color='red')
    ax.plot(ham['LapNumber'], ham['LapTime'], color='cyan')
    ax.set_title("LEC vs HAM")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    plt.show()


if __name__ == "__main__":
    main()