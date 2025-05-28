"""Solar power integration module for HPC data center simulations."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
from datacenter_config import *

def generate_solar_profile(simulation_duration_days=1):
    """Generate time-series solar power data based on Alberta farm profile."""
    # Calculate time parameters
    total_steps = int(simulation_duration_days * 24 * 60 / TIME_STEP_MINUTES)
    timestamps = [datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                 timedelta(minutes=i*TIME_STEP_MINUTES) for i in range(total_steps)]
    
    # Create interpolation function for daily profile
    interp_func = interp1d(SOLAR_HOURS, SOLAR_POWER_MW, 
                          kind='cubic', bounds_error=False, fill_value=0)
    
    # Generate base power values
    hours = [(t.hour + t.minute/60) for t in timestamps]
    solar_power = np.array([interp_func(h % 24) for h in hours])
    
    # Apply seasonal variation
    months = [t.month for t in timestamps]
    for i, month in enumerate(months):
        solar_power[i] *= SOLAR_SEASONAL_FACTORS.get(month, 1.0)
    
    # Add daily variation and ensure non-negative values
    solar_power *= np.random.normal(1, 0.1, len(solar_power))
    solar_power = np.maximum(0, solar_power)
    
    return pd.DataFrame({
        'Timestamp': timestamps,
        'Solar_Power_MW': solar_power
    })

def calculate_solar_farms_required(data_center_load_kw):
    """Calculate number of solar farms needed for continuous power supply."""
    # Convert units and calculate daily energy needs
    daily_energy_demand_mwh = (data_center_load_kw / 1000) * 24
    farm_daily_energy_mwh = SOLAR_FARM_CAPACITY_MW * SOLAR_CAPACITY_FACTOR * 24
    
    if farm_daily_energy_mwh == 0:
        return 0
    return np.ceil(daily_energy_demand_mwh / farm_daily_energy_mwh)

def calculate_solar_contribution(solar_power_mw, data_center_load_kw):
    """Calculate solar's contribution to data center power needs."""
    solar_power_kw = solar_power_mw * 1000
    utilized_solar = np.minimum(solar_power_kw, data_center_load_kw)
    
    return {
        'solar_contribution_kw': utilized_solar,
        'grid_power_kw': data_center_load_kw - utilized_solar,
        'solar_utilization_pct': (utilized_solar / data_center_load_kw) * 100
    }

def calculate_solar_savings(solar_power_mw, time_step_hours):
    """Calculate environmental and financial savings from solar power."""
    energy_kwh = solar_power_mw * 1000 * time_step_hours
    return {
        'carbon_savings_kg': energy_kwh * GRID_CARBON_INTENSITY_KG_PER_KWH,
        'energy_savings_kwh': energy_kwh
    }

# Example usage
if __name__ == "__main__":
    # Test solar profile generation
    solar_data = generate_solar_profile()
    print("Generated solar profile:")
    print(solar_data.head())
    
    # Test farm calculation
    farms_needed = calculate_solar_farms_required(750)  # 750kW load
    print(f"\nFarms needed: {farms_needed}")
    
    # Test contribution analysis
    contribution = calculate_solar_contribution(solar_data['Solar_Power_MW'], 1000)
    print("\nSolar contribution analysis:")
    print(f"Max contribution: {contribution['solar_utilization_pct'].max():.1f}%")
