"""Main simulation logic for the HPC data center with solar integration."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datacenter_config import *
from power_models import *
from metric_calculators import *

def run_simulation(num_solar_farms=1):
    """Run the HPC data center simulation with solar integration."""
    print("Starting HPC Data Center simulation with solar integration...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Calculate derived parameters
    num_steps = int(SIMULATION_DURATION_HOURS * 60 / TIME_STEP_MINUTES)
    time_step_hours = TIME_STEP_MINUTES / 60
    
    # Create time points
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    time_range = [start_time + timedelta(minutes=t*TIME_STEP_MINUTES) for t in range(num_steps)]
    
    # Calculate derived node counts
    total_nodes = NUM_RACKS * NODES_PER_RACK
    num_gpu_nodes = int(total_nodes * GPU_NODE_PERCENTAGE)
    num_cpu_nodes = total_nodes - num_gpu_nodes
    
    print(f"Simulating {total_nodes} nodes ({num_gpu_nodes} GPU nodes, {num_cpu_nodes} CPU nodes)...")
    print(f"Solar integration: {num_solar_farms} solar farms with {SOLAR_FARM_CAPACITY_MW} MW capacity each")
    
    # Generate utilization pattern
    utilization = generate_utilization_pattern(num_steps)
    
    # Calculate solar power generation
    solar_power_mw = calculate_solar_power(time_range, num_solar_farms)
    
    # Initialize power arrays
    cpu_power = np.zeros(num_steps)
    gpu_power = np.zeros(num_steps)
    storage_power = np.zeros(num_steps)
    network_power = np.zeros(num_steps)
    cooling_power = np.zeros(num_steps)
    other_infra_power = np.zeros(num_steps)
    total_facility_power = np.zeros(num_steps)
    
    # Calculate power consumption over time
    for i, util in enumerate(utilization):
        # Calculate component power
        cpu_power[i] = calculate_cpu_power(util, num_cpu_nodes)
        gpu_power[i] = calculate_gpu_power(util, num_gpu_nodes)
        storage_power[i] = calculate_storage_power(util, total_nodes)
        network_power[i] = calculate_network_power(util, total_nodes)
        
        # Calculate total IT power
        it_power = cpu_power[i] + gpu_power[i] + storage_power[i] + network_power[i]
        
        # Calculate infrastructure power
        cooling_power[i] = calculate_cooling_power(it_power)
        other_infra_power[i] = calculate_other_infra_power(it_power)
        
        # Calculate total facility power
        total_facility_power[i] = it_power + cooling_power[i] + other_infra_power[i]
    
    # Convert solar power to kW and calculate grid power
    solar_power_kw = solar_power_mw * 1000
    grid_power_kw = np.maximum(total_facility_power/1000 - solar_power_kw, 0)
    
    # Create results dataframe
    results = pd.DataFrame({
        'Timestamp': time_range,
        'Utilization': utilization,
        'Total_Power_kW': total_facility_power / 1000,
        'IT_Power_kW': (cpu_power + gpu_power + storage_power + network_power) / 1000,
        'Solar_Power_MW': solar_power_mw,
        'Grid_Power_kW': grid_power_kw,
        'CPU_Power_kW': cpu_power / 1000,
        'GPU_Power_kW': gpu_power / 1000,
        'Storage_Power_kW': storage_power / 1000,
        'Network_Power_kW': network_power / 1000,
        'Cooling_Power_kW': cooling_power / 1000,
        'Other_Infra_Power_kW': other_infra_power / 1000
    })
    
    # Calculate metrics
    results['PUE'] = calculate_pue(results['Total_Power_kW'], results['IT_Power_kW'])
    results['DCiE'] = calculate_dcie(results['PUE'])
    results['Solar_Offset_Pct'] = calculate_solar_offset(results['Total_Power_kW'], results['Solar_Power_MW'])
    results['Carbon_Emissions_kg'] = calculate_grid_carbon_emissions(results['Grid_Power_kW'], time_step_hours)
    results['Solar_Carbon_Savings_kg'] = calculate_solar_carbon_savings(results['Solar_Power_MW'], time_step_hours)
    
    # Calculate infrastructure metrics
    results['Rack_Power_Density_kW'] = results['Total_Power_kW'] / NUM_RACKS
    results['Node_Power_Usage_W'] = results['IT_Power_kW'] * 1000 / total_nodes
    results['Cooling_Efficiency_COP'] = COOLING_EFFICIENCY_COP
    
    # Temperature metrics
    results['Inlet_Temperature_C'] = TARGET_INLET_TEMP_C + np.random.normal(0, 0.5, len(results))
    results['Delta_T_C'] = MAX_DELTA_T_C * (results['IT_Power_kW'] / results['IT_Power_kW'].max())
    results['Outlet_Temperature_C'] = results['Inlet_Temperature_C'] + results['Delta_T_C']
    
    print("All metrics calculated.")
    
    return results
