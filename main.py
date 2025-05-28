# main.py
import numpy as np
from HPP import HybridPowerPlant
from metrics import HPPMetrics
from simulation import HPCSimulation
from visualizations import HPPVisualizer
from datacenter_config import CONFIG

# Generate synthetic renewable profiles
np.random.seed(42)
solar_profile = np.clip(
    np.random.normal(CONFIG.renewables['solar_capacity'] * CONFIG.renewables['solar_cf'],
                     0.2 * CONFIG.renewables['solar_capacity'],
                     CONFIG.time_params['total_steps']),
    0, CONFIG.renewables['solar_capacity']
)
wind_profile = np.clip(
    np.random.normal(CONFIG.renewables['wind_capacity'] * CONFIG.renewables['wind_cf'],
                     0.25 * CONFIG.renewables['wind_capacity'],
                     CONFIG.time_params['total_steps']),
    0, CONFIG.renewables['wind_capacity']
)

# Initialize system components
hpp = HybridPowerPlant(solar_profile, wind_profile)
metrics = HPPMetrics(CONFIG)
simulator = HPCSimulation(hpp, metrics)

# Run simulation
results = simulator.run()

# Visualize results with complete story and comparisons
visualizer = HPPVisualizer(metrics, results)
visualizer.show_all()  # This one call triggers all visualizations and narrative
