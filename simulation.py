"""
simulation.py

Core Simulation Engine for Wind-Powered ASIC HPC Data Center
"""

import numpy as np
from datetime import datetime, timedelta
from metrics import PowerMetrics
from power_module import calculate_compute_power, calculate_total_power, generate_utilization_pattern
from wind_farm import WindFarm
from power_module import PowerSystem

class HybridSimulation:
    def __init__(self, config):
        self.config = config
        self.wind_farm = WindFarm(
            capacity_MW=config.wind_farm_rated_capacity_MW,
            cf=config.wind_farm_capacity_factor
        )
        self.power_system = PowerSystem(
            distance_km=config.transmission_distance_km,
            voltage=config.transmission_voltage_kV * 1000  # Convert kV to V
        )
        self.metrics = PowerMetrics(config)
        
        # Initialize time parameters
        self.start_time = datetime(2025, 5, 21)
        self.time_step = timedelta(minutes=config.time_step_minutes)
        
        # Generate utilization pattern
        self.utilization = generate_utilization_pattern(
            config, 
            pattern='diurnal',
            min_util=0.85,
            max_util=1.0
        )

    def run(self):
        current_time = self.start_time
        for step in range(self.config.simulation_steps):
            # Calculate compute power demand
            compute_power = calculate_compute_power(self.config, self.utilization[step])
            total_power = calculate_total_power(compute_power, self.config)
            
            # Calculate wind power with realistic time-based output
            wind_generated = self.wind_farm.realistic_output(current_time.hour + current_time.minute/60)
            wind_delivered = self.power_system.net_power(wind_generated)
            
            # Calculate grid power need and deficit
            grid_power = max(total_power['total_power'] - wind_delivered, 0)
            power_deficit = max(total_power['total_power'] - (wind_delivered + grid_power), 0)
            
            # Calculate utilization percentage
            utilization_ratio = wind_delivered / total_power['total_power'] if total_power['total_power'] > 0 else 0
            
            # Update metrics
            self.metrics.update_metrics({
                'duration_s': self.config.time_step_minutes * 60,
                **compute_power,
                'cooling_power': total_power['cooling_power'],
                'facility_overhead': total_power['facility_overhead'],
                'wind_generated': wind_generated,
                'wind_delivered': wind_delivered,
                'grid_power': grid_power,
                'transmission_losses': wind_generated - wind_delivered,
                'power_deficit': power_deficit,
                'utilization': utilization_ratio
            })
            
            current_time += self.time_step

        return self.metrics.get_summary()

    def get_time_series(self):
        # For integration with visualization module
        return {
            'timestamps': [self.start_time + i*self.time_step 
                          for i in range(self.config.simulation_steps)],
            'utilization': self.utilization
        }
