# HPP.py
"""Hybrid Power Plant Core Optimization Engine"""
import pulp
from datacenter_config import CONFIG

class HybridPowerPlant:
    def __init__(self, solar_profile, wind_profile):
        self.solar = solar_profile
        self.wind = wind_profile
        self.battery_soc = CONFIG.storage['capacity'] * 0.5  # Start at 50%
        self.soc_history = []

    def optimize_dispatch(self, hpc_demand, current_step):
        prob = pulp.LpProblem("HPP_Optimization", pulp.LpMinimize)

        # Decision Variables
        grid_import = pulp.LpVariable('grid_import', 0, CONFIG.grid['max_import'])
        wind_used = pulp.LpVariable('wind_used', 0, self.wind[current_step])
        solar_used = pulp.LpVariable('solar_used', 0, self.solar[current_step])
        battery_charge = pulp.LpVariable('battery_charge', 0, CONFIG.storage['max_charge'])
        battery_discharge = pulp.LpVariable('battery_discharge', 0, CONFIG.storage['max_charge'])

        # Curtailment
        wind_curtail = self.wind[current_step] - wind_used
        solar_curtail = self.solar[current_step] - solar_used

        # Objective Function
        cost = (grid_import * CONFIG.grid['energy_price'] * 1000 +
                wind_curtail * CONFIG.optimization['curtailment_penalty'] +
                solar_curtail * CONFIG.optimization['curtailment_penalty'])
        prob += cost

        # Power balance constraint
        prob += (grid_import + wind_used + solar_used + battery_discharge - battery_charge >= hpc_demand)

        # Battery SOC update (fix: multiply, not divide)
        timestep_hr = CONFIG.time_params['time_step_mins'] / 60.0
        new_soc = self.battery_soc + (battery_charge * CONFIG.storage['efficiency'] - battery_discharge * (1.0 / CONFIG.storage['efficiency'])) * timestep_hr
        prob += new_soc <= CONFIG.storage['capacity']
        prob += new_soc >= CONFIG.storage['min_soc'] * CONFIG.storage['capacity']

        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        # Update battery SOC for next step
        self.battery_soc = pulp.value(new_soc)
        self.soc_history.append(self.battery_soc)

        return {
            'grid': pulp.value(grid_import),
            'wind_used': pulp.value(wind_used),
            'solar_used': pulp.value(solar_used),
            'battery_charge': pulp.value(battery_charge),
            'battery_discharge': pulp.value(battery_discharge),
            'soc': self.battery_soc,
            'wind_curtail': pulp.value(wind_curtail),
            'solar_curtail': pulp.value(solar_curtail)
        }
