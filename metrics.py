"""
metrics.py

Comprehensive Power Metrics & Emissions Calculation Module
For Canadian Wind-Powered ASIC HPC Data Center Simulation
"""

class PowerMetrics:
    def __init__(self, config):
        # Energy metrics (in Wh)
        self.metrics = {
            'gpu_energy_wh': 0.0,
            'cpu_energy_wh': 0.0,
            'asic_energy_wh': 0.0,
            'storage_energy_wh': 0.0,
            'network_energy_wh': 0.0,
            'cooling_energy_wh': 0.0,
            'facility_overhead_wh': 0.0,

            'wind_generated_wh': 0.0,
            'wind_delivered_wh': 0.0,
            'grid_energy_wh': 0.0,
            'transmission_losses_wh': 0.0,
            'power_deficit_wh': 0.0,
        }
        # Emissions (in kg CO2)
        self.emissions = {
            'wind_emissions_kg': 0.0,
            'grid_emissions_kg': 0.0,
        }
        # Utilization
        self.utilization_samples = []
        self.config = config

    def update_metrics(self, timestep_data):
        """
        timestep_data keys:
            gpu_power, cpu_power, asic_power, storage_power, network_power, cooling_power, facility_overhead,
            wind_generated, wind_delivered, grid_power, transmission_losses, power_deficit, utilization
        All power values in Watts, duration in seconds.
        """
        duration_h = timestep_data['duration_s'] / 3600.0

        # Component energies
        self.metrics['gpu_energy_wh'] += timestep_data['gpu_power'] * duration_h
        self.metrics['cpu_energy_wh'] += timestep_data['cpu_power'] * duration_h
        self.metrics['asic_energy_wh'] += timestep_data['asic_power'] * duration_h
        self.metrics['storage_energy_wh'] += timestep_data['storage_power'] * duration_h
        self.metrics['network_energy_wh'] += timestep_data['network_power'] * duration_h
        self.metrics['cooling_energy_wh'] += timestep_data['cooling_power'] * duration_h
        self.metrics['facility_overhead_wh'] += timestep_data.get('facility_overhead', 0.0) * duration_h

        # Wind and grid
        self.metrics['wind_generated_wh'] += timestep_data['wind_generated'] * duration_h
        self.metrics['wind_delivered_wh'] += timestep_data['wind_delivered'] * duration_h
        self.metrics['grid_energy_wh'] += timestep_data['grid_power'] * duration_h
        self.metrics['transmission_losses_wh'] += timestep_data['transmission_losses'] * duration_h
        self.metrics['power_deficit_wh'] += timestep_data['power_deficit'] * duration_h

        # Emissions
        self.emissions['wind_emissions_kg'] += (
            timestep_data['wind_delivered'] * duration_h * self.config.wind_emissions_factor_kgco2_mwh / 1000.0
        )
        self.emissions['grid_emissions_kg'] += (
            timestep_data['grid_power'] * duration_h * self.config.grid_emissions_factor_kgco2_mwh / 1000.0
        )

        # Utilization
        self.utilization_samples.append(timestep_data['utilization'])

    def get_summary(self):
        # Convert Wh to kWh for reporting
        summary = {k.replace('_wh', '_kwh'): round(v / 1000.0, 2) for k, v in self.metrics.items()}
        summary.update({
            'wind_emissions_kg': round(self.emissions['wind_emissions_kg'], 2),
            'grid_emissions_kg': round(self.emissions['grid_emissions_kg'], 2),
            'avg_utilization': round(sum(self.utilization_samples) / len(self.utilization_samples), 4) if self.utilization_samples else 0.0,
            'total_energy_kwh': round(sum([v for k, v in summary.items() if k.endswith('_kwh')]), 2)
        })
        return summary

    def get_time_series(self):
        # For future extension: store time series of each metric if needed for plotting
        pass
