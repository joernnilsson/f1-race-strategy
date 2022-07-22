import matplotlib.pyplot as plt

import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl()


def plot(y, t=None):
    # fig = plt.figure()
    # ax = fig.gca()
    # if time is not None:
    #     plt.plot(time, y)
    # else:
    #     plt.plot(y)
    # plt.show()

    fig, ax = plt.subplots()
    ax.plot(t, y, label='Fast')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed [Km/h]')
    ax.legend()
    plt.show()
