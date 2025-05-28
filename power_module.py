"""
power_module.py

Power Calculation Engine for Wind-Powered ASIC HPC Data Center
"""

import numpy as np

def calculate_compute_power(config, utilization):
    """
    Returns a dict of power (in Watts) for each major compute component.
    Utilization: float (0 to 1)
    """
    gpu_nodes = int(config.total_nodes * config.gpu_node_ratio)
    cpu_nodes = int(config.total_nodes * config.cpu_node_ratio)
    asic_units = int((config.total_power_MW * 1_000_000) // config.asic_power_per_unit_W)

    # Compute node power
    gpu_power = gpu_nodes * config.gpu_power_per_node_W * utilization
    cpu_power = cpu_nodes * config.cpu_power_per_node_W * utilization
    asic_power = asic_units * config.asic_power_per_unit_W * utilization

    # Ancillary (storage/network)
    storage_nodes = int(config.total_nodes * config.storage_node_ratio)
    network_nodes = int(config.total_nodes * config.network_node_ratio)
    storage_power = storage_nodes * config.storage_power_per_node_W
    network_power = network_nodes * config.network_power_per_node_W

    return {
        'gpu_power': gpu_power,
        'cpu_power': cpu_power,
        'asic_power': asic_power,
        'storage_power': storage_power,
        'network_power': network_power
    }

def calculate_cooling_power(it_power, config):
    """
    Returns cooling power (Watts) based on IT load and PUE.
    """
    return it_power * (config.design_pue - 1.0)

def calculate_facility_overhead(it_power, config):
    """
    Returns additional facility overhead (UPS, lighting, security, etc.) if modeled.
    """
    # For advanced modeling, add a small overhead (e.g. 2% of IT power)
    return it_power * 0.02

def calculate_total_power(compute_powers, config):
    """
    Returns total facility power (Watts), including cooling and overhead.
    """
    it_power = sum([compute_powers[k] for k in ['gpu_power', 'cpu_power', 'asic_power', 'storage_power', 'network_power']])
    cooling_power = calculate_cooling_power(it_power, config)
    facility_overhead = calculate_facility_overhead(it_power, config)
    total_power = it_power + cooling_power + facility_overhead
    return {
        'it_power': it_power,
        'cooling_power': cooling_power,
        'facility_overhead': facility_overhead,
        'total_power': total_power
    }

def generate_utilization_pattern(config, pattern='constant', peak_hour=14, min_util=0.8, max_util=1.0):
    """
    Returns an array of utilization values for each simulation step.
    pattern: 'constant', 'diurnal', or 'custom'
    """
    steps = config.simulation_steps
    if pattern == 'constant':
        return np.full(steps, max_util)
    elif pattern == 'diurnal':
        # Simulate a daily utilization curve (e.g., higher in the afternoon)
        hours = np.arange(steps) * config.time_step_minutes / 60
        # Sine wave: min at night, max at peak_hour
        util = min_util + (max_util - min_util) * (0.5 + 0.5 * np.sin((hours - peak_hour) / 24 * 2 * np.pi))
        return util
    else:
        # Custom or imported pattern
        return np.full(steps, max_util)

def calculate_grid_and_wind_power(total_power, wind_delivered):
    """
    Returns grid_power (Watts), wind_used (Watts), and deficit (Watts)
    """
    wind_used = min(total_power, wind_delivered)
    grid_power = max(total_power - wind_delivered, 0)
    deficit = max(total_power - (wind_delivered + grid_power), 0)
    return wind_used, grid_power, deficit
