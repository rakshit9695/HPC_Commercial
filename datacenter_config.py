"""Configuration parameters for the HPC data center simulation."""

# ================== HPC PARAMETERS ================== 
# Simulation parameters
SIMULATION_DURATION_HOURS = 24
TIME_STEP_MINUTES = 5

# Utilization parameters (sinusoidal between 60-90%)
MIN_UTILIZATION = 0.6
MAX_UTILIZATION = 0.9
UTILIZATION_NOISE_LEVEL = 0.03  # 3% random noise

# Data center physical parameters (Canadian Power Grid)
MAX_POWER_CAPACITY_KW = 1000  # 1MW
GRID_VOLTAGE = 480  # V

# Rack and node configuration
NUM_RACKS = 50
NODES_PER_RACK = 40

# Node composition
GPU_NODE_PERCENTAGE = 0.7  # 70% GPU nodes (AI-focused)

# Component power consumption
MAX_CPU_POWER_PER_NODE_W = 360  # AMD EPYC 9654 CPU
MAX_GPU_POWER_PER_NODE_W = 1000  # NVIDIA B200 GPU
IDLE_CPU_POWER_FACTOR = 0.3  # CPU uses 30% of max power when idle
IDLE_GPU_POWER_FACTOR = 0.2  # GPU uses 20% of max power when idle
STORAGE_POWER_PER_NODE_W = 50
NETWORK_POWER_PER_NODE_W = 30

# Cooling and infrastructure
DESIGN_PUE = 1.2  # Target PUE
COOLING_EFFICIENCY_COP = 3.5  # Coefficient of Performance
TARGET_INLET_TEMP_C = 24  # Target inlet temperature in Celsius
MAX_DELTA_T_C = 15  # Max temperature difference

# Power distribution
UPS_CAPACITY_HEADROOM = 1.2  # 20% headroom
BREAKER_TRIP_PROBABILITY = 0.001  # 0.1% per time step

# ================== SOLAR PARAMETERS ================== 
# Solar farm specifications (Alberta report data)
SOLAR_FARM_CAPACITY_MW = 38.9  # Rated AC capacity
SOLAR_FARM_PEAK_POWER_MW = 50.6  # Peak DC capacity
SOLAR_FARM_AREA_HA = 71.2  # Land area required
SOLAR_DC_AC_RATIO = 1.30  # DC-to-AC ratio

# Generation profile (extracted from hourly curve)
SOLAR_HOURS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
SOLAR_POWER_MW = [0,0,0,0,0,0,0,9.5,18,25.5,32,36,38.5,38,36,32,25.5,18,9.5,0,0,0,0,0]

# Seasonal adjustment factors (Alberta-specific)
SOLAR_SEASONAL_FACTORS = {
    1:0.28, 2:0.51, 3:0.99, 4:1.35, 5:1.70, 6:1.74,
    7:1.78, 8:1.50, 9:1.01, 10:0.59, 11:0.30, 12:0.21
}

# Operational parameters
SOLAR_CAPACITY_FACTOR = 0.17  # Typical for Alberta
ENABLE_SOLAR_POWER = True

# ================== ADVANCED SETTINGS ================== 
# Battery storage (optional)
BATTERY_STORAGE_ENABLED = False
BATTERY_CAPACITY_MWH = 0
BATTERY_EFFICIENCY = 0.9  # 90% round-trip efficiency

# Carbon metrics
GRID_CARBON_INTENSITY_KG_PER_KWH = 0.2  # Canadian grid average
RENEWABLE_ENERGY_PERCENTAGE = 60  # Grid mix
