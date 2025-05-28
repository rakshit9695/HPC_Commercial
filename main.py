"""
Main.py

Main Simulation Orchestrator for Canadian Wind-Powered ASIC HPC Data Center
"""

import datetime
import json
import os
import numpy as np

# Import with the exact filename (case-sensitive)
from data_center_config import DataCenterConfig
from metrics import PowerMetrics
from visualization import generate_all_plots
from wind_farm import WindFarm

# First, let's add the missing PowerSystem class to power_module.py
class PowerSystem:
    def __init__(self, distance_km=1000, voltage=240e3):
        self.distance = distance_km
        self.voltage = voltage
        self.rho_cu = 1.68e-8  # Ω·m (copper resistivity)
        self.cable_area = 500e-6  # 500 mm² conductor area
        
    def transmission_loss(self, power_MW):
        """Calculate transmission losses using P = I²R formula"""
        if power_MW <= 0:
            return 0
        R = (self.rho_cu * self.distance * 1000) / self.cable_area
        current = (power_MW * 1e6) / self.voltage
        return (current**2 * R) / 1e6  # MW
    
    def net_power(self, generated_MW):
        """Return net power after transmission losses"""
        loss = self.transmission_loss(generated_MW)
        return max(generated_MW - loss, 0)

# Enhanced simulation class
class EnhancedHybridSimulation:
    def __init__(self, config):
        self.config = config
        self.wind_farm = WindFarm(
            capacity_MW=config.wind_farm_rated_capacity_MW,
            region='Alberta'
        )
        self.power_system = PowerSystem(
            distance_km=config.transmission_distance_km,
            voltage=config.transmission_voltage_kV * 1000
        )
        
        # Import functions from power_module
        from power_module import calculate_compute_power, calculate_total_power, generate_utilization_pattern
        self.calculate_compute_power = calculate_compute_power
        self.calculate_total_power = calculate_total_power
        
        # Generate utilization pattern
        self.utilization = generate_utilization_pattern(
            config, 
            pattern='diurnal',
            min_util=0.85,
            max_util=1.0
        )
        
        # Initialize time parameters
        self.start_time = datetime.datetime(2025, 5, 21)
        self.time_step = datetime.timedelta(minutes=config.time_step_minutes)

    def run(self):
        """Run the simulation and return timesteps and power_data"""
        timesteps = []
        power_data = []
        current_time = self.start_time
        
        print("🔄 Running simulation...")
        
        for step in range(self.config.simulation_steps):
            # Calculate compute power demand
            compute_power = self.calculate_compute_power(self.config, self.utilization[step])
            total_power = self.calculate_total_power(compute_power, self.config)
            
            # Calculate wind power
            wind_generated = self.wind_farm.realistic_output(
                current_time.hour + current_time.minute/60, 
                self.config.transmission_distance_km
            ) * 1e6  # Convert MW to W
            
            wind_delivered = self.power_system.net_power(wind_generated / 1e6) * 1e6  # W
            
            # Calculate grid power need
            grid_power = max(total_power['total_power'] - wind_delivered, 0)
            power_deficit = max(total_power['total_power'] - (wind_delivered + grid_power), 0)
            
            # Store timestep data
            timesteps.append(current_time.isoformat())
            power_data.append({
                'duration_s': self.config.time_step_minutes * 60,
                'total_power': total_power['total_power'],
                'wind_generated': wind_generated,
                'wind_delivered': wind_delivered,
                'grid_power': grid_power,
                'transmission_losses': wind_generated - wind_delivered,
                'power_deficit': power_deficit,
                'utilization': min(1.0, (wind_delivered + grid_power) / total_power['total_power']),
                **compute_power,
                'cooling_power': total_power['cooling_power'],
                'facility_overhead': total_power['facility_overhead']
            })
            
            # Progress indicator
            if step % 48 == 0:  # Every 8 hours
                progress = (step / self.config.simulation_steps) * 100
                print(f"   Progress: {progress:.1f}%")
            
            current_time += self.time_step
        
        return timesteps, power_data

def generate_distance_analysis(config):
    """Generate power losses vs distance analysis"""
    distances_km = np.linspace(100, 2000, 20)
    wind_farm = WindFarm(capacity_MW=config.wind_farm_rated_capacity_MW)
    
    # Get average wind output (noon, no transmission losses)
    avg_wind_output = wind_farm._turbine_power(8.0) * (config.wind_farm_rated_capacity_MW / wind_farm._turbine_power(11.5))
    
    losses_vs_distance = []
    for distance in distances_km:
        power_system_temp = PowerSystem(distance_km=distance)
        loss = power_system_temp.transmission_loss(avg_wind_output)
        losses_vs_distance.append(loss)
    
    return distances_km, losses_vs_distance

def main():
    """Main execution function"""
    print("Canadian Wind-Powered ASIC HPC Data Center Simulation")
    print("=" * 60)
    
    # Initialize configuration
    config = DataCenterConfig()
    
    print(f"Data Center: {config.total_power_MW} MW")
    print(f"Wind Farm: {config.wind_farm_rated_capacity_MW} MW")
    print(f"Transmission Distance: {config.transmission_distance_km} km")
    print(f"Simulation Duration: {config.simulation_duration_hours} hours")
    
    # Run simulation
    simulation = EnhancedHybridSimulation(config)
    timesteps, power_data = simulation.run()
    
    # Calculate metrics
    print("Calculating metrics...")
    metrics = PowerMetrics(config)
    for ts in power_data:
        metrics.update_metrics(ts)
    
    # Generate distance analysis
    print("Generating distance analysis...")
    distances_km, losses_vs_distance = generate_distance_analysis(config)
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    # Save results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    results_data = {
        "configuration": {
            "total_power_MW": config.total_power_MW,
            "wind_capacity_MW": config.wind_farm_rated_capacity_MW,
            "transmission_distance_km": config.transmission_distance_km,
            "simulation_duration_hours": config.simulation_duration_hours,
            "time_step_minutes": config.time_step_minutes
        },
        "timesteps": timesteps,
        "power_data": power_data,
        "metrics": metrics.get_summary(),
        "distance_analysis": {
            "distances_km": distances_km.tolist(),
            "losses_MW": losses_vs_distance
        }
    }
    
    with open(f"results/simulation_{timestamp}.json", "w") as f:
        json.dump(results_data, f, indent=2)
    
    print(f"Results saved to: simulation_{timestamp}.json")
    
    # Generate visualizations
    print("Generating visualizations...")
    generate_all_plots(timesteps, power_data, metrics, distances_km, losses_vs_distance)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    summary = metrics.get_summary()
    
    total_energy = summary.get('total_energy_kwh', 0)
    wind_energy = summary.get('wind_delivered_kwh', 0)
    grid_energy = summary.get('grid_energy_kwh', 0)
    
    print(f"Total Energy Consumption: {total_energy:.2f} kWh")
    print(f"Wind Energy Used: {wind_energy:.2f} kWh")
    print(f"Grid Energy Used: {grid_energy:.2f} kWh")
    print(f"Total CO₂ Emissions: {summary.get('wind_emissions_kg', 0) + summary.get('grid_emissions_kg', 0):.1f} kg")
    print(f"Average Utilization: {summary.get('avg_utilization', 0)*100:.1f}%")
    
    if total_energy > 0:
        wind_percentage = (wind_energy / total_energy) * 100
        print(f"Wind Power Contribution: {wind_percentage:.1f}%")
        
        # Calculate cost savings
        grid_cost = grid_energy * 0.08  # $0.08/kWh
        wind_cost = wind_energy * 0.02  # $0.02/kWh
        total_cost = grid_cost + wind_cost
        grid_only_cost = total_energy * 0.08
        savings = grid_only_cost - total_cost
        
        print(f"Estimated Cost: ${total_cost:.2f}")
        print(f"Grid-Only Cost: ${grid_only_cost:.2f}")
        print(f"Cost Savings: ${savings:.2f}")
    
    print("\nSimulation completed successfully!")
    print(f"Results and visualizations saved in 'results/' directory")

if __name__ == "__main__":
    main()
