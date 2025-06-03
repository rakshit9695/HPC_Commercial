import pandas as pd
import matplotlib.pyplot as plt
from windpowerlib import WindTurbine, WindFarm, ModelChain
import numpy as np

# Your wind farm data
wind_farm_data = {
    'Name': ['Ardenville', 'Blackspring', 'Blue Trail', 'Box Springs', 'Buffalo', 
             'Bull Creek', 'Castle River', 'Castle Rock', 'Chin Chute', 'Cowley',
             'Cypress', 'Forty Mile', 'Garden Plain', 'Ghost Pine', 'Grizzly Bear',
             'Halkirk', 'Hand Hills', 'Hilda', 'Jenner'],
    'Turbines': [
        [{'capacity': 3e6, 'diameter': 90, 'height': 80, 'count': 23}],
        [{'capacity': 1.8e6, 'diameter': 100, 'height': 80, 'count': 166}],
        [{'capacity': 3e6, 'diameter': 90, 'height': 80, 'count': 22}],
        [{'capacity': 2e6, 'diameter': 90, 'height': 78, 'count': 3}],
        [{'capacity': 4.3125e6, 'diameter': 145, 'height': 95.5, 'count': 8},
         {'capacity': 5.2e6, 'diameter': 145, 'height': 95.5, 'count': 5}],
        [{'capacity': 1.7e6, 'diameter': 103, 'height': 80, 'count': 17}],
        [{'capacity': 6e5, 'diameter': 44, 'height': 40, 'count': 1},
         {'capacity': 6.6e5, 'diameter': 47, 'height': 50, 'count': 59}],
        [{'capacity': 2.31e6, 'diameter': 71, 'height': 64, 'count': 33},
         {'capacity': 4.2e6, 'diameter': 136, 'height': 82, 'count': 7}],
        [{'capacity': 1.5e6, 'diameter': 77, 'height': 65, 'count': 20}],
        [{'capacity': 1.3e6, 'diameter': 60, 'height': 46, 'count': 15}],
        [{'capacity': 5.2e6, 'diameter': 145, 'height': 90, 'count': 48}],
        [{'capacity': 5e6, 'diameter': 145, 'height': 107.5, 'count': 30},
         {'capacity': 5.2e6, 'diameter': 145, 'height': 107.5, 'count': 15}],
        [{'capacity': 5e6, 'diameter': 145, 'height': 102.5, 'count': 26}],
        [{'capacity': 1.6e6, 'diameter': 82.5, 'height': 80, 'count': 51}],
        [{'capacity': 4.5e6, 'diameter': 150, 'height': 120, 'count': 31},
         {'capacity': 4.2e6, 'diameter': 136, 'height': 82, 'count': 3}],
        [{'capacity': 1.8e6, 'diameter': 90, 'height': 80, 'count': 83}],
        [{'capacity': 5e6, 'diameter': 145, 'height': 95.5, 'count': 29}],
        [{'capacity': 5e6, 'diameter': 145, 'height': 95, 'count': 20}],
        [{'capacity': 5.56e6, 'diameter': 160, 'height': 114, 'count': 22},
         {'capacity': 5.49e6, 'diameter': 160, 'height': 114, 'count': 13},
         {'capacity': 5.56e6, 'diameter': 160, 'height': 114, 'count': 20}]
    ]
}

# Create turbine objects and wind farm fleet
farm_fleets = []
for farm in wind_farm_data['Turbines']:
    fleet = []
    for turbine in farm:
        wind_speeds = np.array([0, 3, 4, 5, 7, 10, 12, 15, 25])
        power_values = np.interp(wind_speeds, [0, 12, 25], [0, turbine['capacity'], 0])
        turbine_obj = WindTurbine(
            hub_height=turbine['height'],
            rotor_diameter=turbine['diameter'],
            nominal_power=turbine['capacity'],
            power_curve=pd.DataFrame({
                'wind_speed': wind_speeds,
                'value': power_values
            })
        )
        fleet.append({
            'wind_turbine': turbine_obj,
            'number_of_turbines': turbine['count']
        })
    farm_fleets.append(pd.DataFrame(fleet))

# --- CORRECT WEATHER DATAFRAME: columns MultiIndex, index DatetimeIndex ---
# ...existing code...

# --- CORRECT WEATHER DATAFRAME: columns MultiIndex, index DatetimeIndex ---
times = pd.DatetimeIndex(['2025-06-03 00:00:00'])

# Find all unique hub heights in the fleet
all_heights = set()
for farm in wind_farm_data['Turbines']:
    for turbine in farm:
        all_heights.add(turbine['height'])

# Create weather DataFrame with wind speed for all hub heights
columns = pd.MultiIndex.from_tuples([('wind_speed', h) for h in sorted(all_heights)])
weather = pd.DataFrame([[7.5]*len(all_heights)], index=times, columns=columns)
# --------------------------------------------------------------------------

power_outputs = []

for fleet in farm_fleets:
    farm = WindFarm(wind_turbine_fleet=fleet)
    model = ModelChain(farm).run_model(weather)
    # Output is a pandas Series with DatetimeIndex, get scalar value with .iloc[0]
    power_outputs.append(model.power_output.iloc[0]/1e6)  # Convert to MW

plt.figure(figsize=(12,6))
plt.bar(wind_farm_data['Name'], power_outputs)
plt.xticks(rotation=90)
plt.ylabel('Power Output (MW)')
plt.title('Wind Farm Power Output at 7.5 m/s Wind Speed')
plt.tight_layout()
plt.show()