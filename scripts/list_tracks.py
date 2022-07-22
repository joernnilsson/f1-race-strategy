import matplotlib.pyplot as plt
import fastf1.plotting
import fastf1
import os
import yaml
from unidecode import unidecode

fastf1.Cache.enable_cache('/fastf1_cache/api')  # optional but recommended


sched = fastf1.get_event_schedule(2021, include_testing=False)

for index, row in sched.iterrows():
    

    folder = unidecode(row['Location'].lower().replace(' ', '_'))
    print(folder)

    data = {
        'name': row['Location'],
        'grand_prix_name': row['EventName'],
        'length': 5000,
        'laps': 50,
        'latest_session': {
            'year': 2021,
            'type': 'R'
        }
    }

    os.makedirs("tracks/"+folder, exist_ok=True)
    with open("tracks/"+folder+"/track.yaml", 'w') as outfile:
        yaml.dump(data, outfile, sort_keys=False)


