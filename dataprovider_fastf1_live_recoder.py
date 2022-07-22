import fastf1
import fastf1.livetiming
from fastf1.livetiming.client import SignalRClient, messages_from_raw

import os
from os.path import exists

import asyncio

save_path = '/fastf1_cache/recorded'

def save(filename, timeout):
    print("Saving data to", filename)
    client = SignalRClient(filename, filemode='w',  timeout=timeout)

    asyncio.run(client._async_start())


def next_filename():
    i = 0
    while True:
        filename = os.path.join(save_path, "saved_data_"+str(i).rjust(6, "0")+".txt")
        if not exists(filename):
            return filename
        i += 1

if __name__ == "__main__":
    try:
        while True:
            filename = next_filename()
            save(filename, 60)
    except KeyboardInterrupt:
        print("Keyboard interrupt - exiting...")
