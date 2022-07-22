
import utils

import fastf1
import matplotlib.pyplot as plt
import fastf1.plotting
import numpy as np
import sys
import os
import yaml
from yaml.loader import SafeLoader

def main(track):

    if not os.path.exists('tracks/' + track):
        raise ValueError("track does not exist")


    with open('tracks/' + track + '/track.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)

    print(config)

    fastf1.plotting.setup_mpl()

    fastf1.Cache.enable_cache('/fastf1_cache/api')  # optional but recommended

    session = fastf1.get_session(config["latest_session"]["year"], config["grand_prix_name"], config["latest_session"]["type"])
    session.load(telemetry = True, laps = True, messages = True, weather = True)

    fig, ax = plt.subplots()

    # Find track length
    #track_length = config["length"]
    track_length = 0.0
    for d in session.drivers:
        info = session.get_driver(d)
        lap = session.laps.pick_driver(info['Abbreviation']).pick_fastest()
        try:
            tel = lap.get_car_data().add_distance()
        except:
            print("Error for:", info['Abbreviation'])
            continue
        if tel['Distance'].iat[-1] > track_length:
            track_length = tel['Distance'].iat[-1]

    # Distribute interpoation points
    distance_step = 10.0
    distance_index = np.arange(0, track_length, distance_step)
    speed_profiles = [] #np.zeros(distance_index.shape)
    position_profiles_x = []
    position_profiles_y = []

    for d in session.drivers:
        info = session.get_driver(d)
        lap = session.laps.pick_driver(info['Abbreviation']).pick_fastest()

        try:
            tel = lap.get_car_data()
            tel_pos = lap.get_pos_data()
            
            tel_merged = tel.merge_channels(tel_pos).add_distance()
            

        except:
            print("Error for:", info['Abbreviation'])
            continue

        # Interpolate speed
        speed_profile = np.interp(distance_index, tel_merged['Distance'].to_numpy(), tel_merged['Speed'].to_numpy())
        #print(tel_pos)
        x_profile = np.interp(distance_index, tel_merged['Distance'].to_numpy(), tel_merged['X'].to_numpy())
        y_profile = np.interp(distance_index, tel_merged['Distance'].to_numpy(), tel_merged['Y'].to_numpy())
        speed_profiles.append(speed_profile)
        position_profiles_x.append(x_profile)
        position_profiles_y.append(y_profile)

        #ax.plot(tel['Distance'], tel['Speed'], label=info['Abbreviation'])

    speed_profiles_np = np.array(speed_profiles)
    position_profiles_x_np = np.array(position_profiles_x)
    position_profiles_y_np = np.array(position_profiles_y)

    mean_speed_profile = np.mean(speed_profiles_np, axis=0)
    mean_x_profile = np.mean(position_profiles_x_np, axis=0)*0.1
    mean_y_profile = np.mean(position_profiles_y_np, axis=0)*0.1

    ax.plot(distance_index, mean_x_profile)
    ax.plot(distance_index, mean_y_profile)

    #ax.set_xlabel('Distance in m')
    #ax.set_ylabel('Speed in km/h')

    np.save('tracks/' + track + '/track_profile.npy', [distance_index, mean_speed_profile, mean_x_profile, mean_y_profile])
    
    measured_length = track_length.item()
    config["length_measured"] = measured_length
    with open('tracks/' + track + '/track.yaml', 'w') as f:
        yaml.dump(config, f, sort_keys=False)

    #plt.show()



if __name__ == "__main__":
    tracks = []
    if sys.argv[1] == "all":
        rootdir = './tracks'
        for file in os.listdir(rootdir):
            d = os.path.join(rootdir, file)
            if os.path.isdir(d):
                tracks.append(os.path.basename(d))
    else:
        tracks.append(sys.argv[1])
    print(tracks)

    for t in tracks:
        main(t)