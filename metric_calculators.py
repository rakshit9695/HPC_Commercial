"""Functions to calculate various data center metrics with solar integration."""

import numpy as np
import pandas as pd
from datacenter_config import *

def calculate_pue(total_power, it_power):
    """Calculate Power Usage Effectiveness (PUE)."""
    return total_power / it_power

def calculate_dcie(pue):
    """Calculate Data Center Infrastructure Efficiency (DCiE)."""
    return 100 / pue

def calculate_grid_carbon_emissions(grid_power_kw, time_step_hours):
    """Calculate carbon emissions from grid power in kg CO₂."""
    return grid_power_kw * GRID_CARBON_INTENSITY_KG_PER_KWH * time_step_hours

def calculate_solar_offset(data_center_power_kw, solar_power_mw):
    """Calculate percentage of power offset by solar generation."""
    solar_power_kw = solar_power_mw * 1000
    utilized_solar = np.minimum(solar_power_kw, data_center_power_kw)
    
    # Vectorized calculation with division guard
    with np.errstate(divide='ignore', invalid='ignore'):
        offset_pct = (utilized_solar / data_center_power_kw) * 100
        
    # Handle division by zero and invalid values
    if isinstance(offset_pct, pd.Series):
        return offset_pct.fillna(0).replace([np.inf, -np.inf], 0)
    else:
        return 0 if data_center_power_kw == 0 else offset_pct

def calculate_solar_carbon_savings(solar_power_mw, time_step_hours):
    """Calculate carbon savings from solar power in kg CO₂."""
    solar_energy_kwh = solar_power_mw * 1000 * time_step_hours
    return solar_energy_kwh * GRID_CARBON_INTENSITY_KG_PER_KWH

def calculate_required_solar_farms(avg_data_center_power_kw, 
                                  solar_farm_capacity_mw=SOLAR_FARM_CAPACITY_MW,
                                  capacity_factor=SOLAR_CAPACITY_FACTOR):
    """Calculate number of solar farms needed for continuous power supply."""
    avg_dc_power_mw = avg_data_center_power_kw / 1000
    farm_output = solar_farm_capacity_mw * capacity_factor
    return avg_dc_power_mw / farm_output if farm_output > 0 else 0

def calculate_performance_per_watt(compute_work, power_w):
    """Calculate Performance per Watt (GFLOPS/W)."""
    return compute_work / power_w

def calculate_energy_to_solution(power_w, time_step_hours, compute_work):
    """Calculate Energy-to-Solution in Joules per task."""
    energy_joules = power_w * time_step_hours * 3600
    return energy_joules / compute_work if compute_work > 0 else 0

def predict_power_consumption(hour_of_day, max_power, error_level=0.05):
    """Predict power consumption based on time of day."""
    base_pattern = 0.7 * max_power * (1 + 0.2 * np.sin(2 * np.pi * hour_of_day / 24))
    return base_pattern * (1 + np.random.normal(0, error_level, len(hour_of_day)))
