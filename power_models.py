"""Models for power consumption and solar generation."""

import numpy as np
from scipy.interpolate import interp1d
from datacenter_config import *

def calculate_cpu_power(utilization, num_cpu_nodes):
    """Calculate CPU power consumption based on utilization."""
    cpu_node_power = (IDLE_CPU_POWER_FACTOR * MAX_CPU_POWER_PER_NODE_W + 
                     (1 - IDLE_CPU_POWER_FACTOR) * MAX_CPU_POWER_PER_NODE_W * utilization)
    return cpu_node_power * num_cpu_nodes

def calculate_gpu_power(utilization, num_gpu_nodes):
    """Calculate GPU power consumption based on utilization."""
    gpu_node_power = (IDLE_GPU_POWER_FACTOR * MAX_GPU_POWER_PER_NODE_W + 
                     (1 - IDLE_GPU_POWER_FACTOR) * MAX_GPU_POWER_PER_NODE_W * utilization)
    return gpu_node_power * num_gpu_nodes

def calculate_storage_power(utilization, total_nodes):
    """Calculate storage power consumption based on utilization."""
    return STORAGE_POWER_PER_NODE_W * total_nodes * (0.8 + 0.2 * utilization)

def calculate_network_power(utilization, total_nodes):
    """Calculate network power consumption based on utilization."""
    return NETWORK_POWER_PER_NODE_W * total_nodes * (0.7 + 0.3 * utilization)

def calculate_cooling_power(it_power):
    """Calculate cooling power based on IT power and cooling efficiency."""
    return it_power / COOLING_EFFICIENCY_COP

def calculate_other_infra_power(it_power):
    """Calculate power consumption for other infrastructure."""
    return 0.05 * it_power

def generate_utilization_pattern(num_steps):
    """Generate a sinusoidal utilization pattern between MIN_UTILIZATION and MAX_UTILIZATION."""
    time_points = np.linspace(0, SIMULATION_DURATION_HOURS, num_steps)
    amplitude = (MAX_UTILIZATION - MIN_UTILIZATION) / 2
    mean_utilization = (MAX_UTILIZATION + MIN_UTILIZATION) / 2
    utilization = mean_utilization + amplitude * np.sin(2 * np.pi * time_points / SIMULATION_DURATION_HOURS)
    
    # Add random noise and clamp values
    utilization += np.random.normal(0, UTILIZATION_NOISE_LEVEL, len(utilization))
    return np.clip(utilization, MIN_UTILIZATION, MAX_UTILIZATION)

def interpolate_solar_power(hour_of_day):
    """Interpolate solar power based on hour of day using cubic spline."""
    interp_func = interp1d(SOLAR_HOURS, SOLAR_POWER_MW, 
                          kind='cubic', 
                          bounds_error=False, 
                          fill_value=0)
    return interp_func(hour_of_day % 24)

def calculate_solar_power(timestamps, num_farms=1):
    """Calculate solar power output with seasonal adjustments."""
    hours = [(t.hour + t.minute/60) for t in timestamps]
    solar_power = np.array([interpolate_solar_power(h) for h in hours])
    
    # Apply seasonal variation
    months = [t.month for t in timestamps]
    for i, month in enumerate(months):
        solar_power[i] *= SOLAR_SEASONAL_FACTORS.get(month, 1.0)
    
    # Add daily variation and scale by number of farms
    solar_power *= np.random.normal(1, 0.1, len(solar_power)) * num_farms
    return np.maximum(0, solar_power)
