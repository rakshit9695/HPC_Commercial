# data_center_config.py
"""Unified configuration for HPP-powered HPC Data Center"""

# ================== CORE PARAMETERS ==================
SIMULATION_DURATION_HOURS = 24
TIME_STEP_MINUTES = 5
SIMULATION_STEPS = int(SIMULATION_DURATION_HOURS * 60 / TIME_STEP_MINUTES)

# ================== HPC LOAD PROFILE ==================
HPC_BASE_LOAD_MW = 2.0  # 2MW average load
LOAD_VARIATION_RANGE = 0.3  # ±30% diurnal variation
MIN_LOAD_FACTOR = 0.7  # 70% of base load at minimum

# ================== RENEWABLE GENERATION ==================
# Solar parameters
SOLAR_CAPACITY_MW = 5.0
SOLAR_CAPACITY_FACTOR = 0.17  # Alberta average

# Wind parameters 
WIND_CAPACITY_MW = 8.0
WIND_CAPACITY_FACTOR = 0.38  # Alberta winter

# ================== ENERGY STORAGE ==================
BATTERY_CAPACITY_MWH = 15.0
BATTERY_EFFICIENCY = 0.92  # Round-trip
MIN_SOC = 0.2  # 20% minimum state of charge
MAX_CHARGE_RATE_MW = 3.0

# ================== GRID INTERACTION ==================
GRID_MAX_IMPORT_MW = 4.0
GRID_CARBON_INTENSITY = 0.2  # kgCO2/kWh
GRID_ENERGY_PRICE = 0.12  # CAD/kWh

# ================== OPTIMIZATION PARAMETERS ==================
PENALTY_COST_CURTAILMENT = 1000  # CAD/MW (avoid curtailment)
PENALTY_COST_LOAD_SHED = 5000  # CAD/MW (avoid load shedding)

class HPPConfig:
    def __init__(self):
        self.time_params = {
            'duration_hours': SIMULATION_DURATION_HOURS,
            'time_step_mins': TIME_STEP_MINUTES,
            'total_steps': SIMULATION_STEPS
        }
        self.hpc_load = {
            'base_load': HPC_BASE_LOAD_MW,
            'variation': LOAD_VARIATION_RANGE,
            'min_factor': MIN_LOAD_FACTOR
        }
        self.renewables = {
            'solar_capacity': SOLAR_CAPACITY_MW,
            'solar_cf': SOLAR_CAPACITY_FACTOR,
            'wind_capacity': WIND_CAPACITY_MW,
            'wind_cf': WIND_CAPACITY_FACTOR
        }
        self.storage = {
            'capacity': BATTERY_CAPACITY_MWH,
            'efficiency': BATTERY_EFFICIENCY,
            'min_soc': MIN_SOC,
            'max_charge': MAX_CHARGE_RATE_MW
        }
        self.grid = {
            'max_import': GRID_MAX_IMPORT_MW,
            'carbon_intensity': GRID_CARBON_INTENSITY,
            'energy_price': GRID_ENERGY_PRICE
        }
        self.optimization = {
            'curtailment_penalty': PENALTY_COST_CURTAILMENT,
            'load_shed_penalty': PENALTY_COST_LOAD_SHED
        }

CONFIG = HPPConfig()

