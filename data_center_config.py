"""
HPC_Data_Configuration.py

Canadian Wind-Powered ASIC HPC Data Center Configuration
1-Day Realistic Simulation Parameters
"""

# ================== SIMULATION PARAMETERS ==================
SIMULATION_DURATION_HOURS = 24         # 1-day simulation
TIME_STEP_MINUTES = 5                # 15-minute granularity
SIMULATION_STEPS = int(SIMULATION_DURATION_HOURS * 60 / TIME_STEP_MINUTES)  # 96 steps

# ================== HPC INFRASTRUCTURE ==================
DATA_CENTER_TOTAL_POWER_MW = 2.0       # 2 MW medium-scale facility
GRID_VOLTAGE_V = 13800                 # 13.8 kV medium voltage distribution

NUM_RACKS = 40                         
NODES_PER_RACK = 50                    # Optimized rack density
TOTAL_NODES = NUM_RACKS * NODES_PER_RACK  # 2,000 nodes

# Workload distribution (AI/Compute focus)
GPU_NODE_RATIO = 0.75                  # 75% GPU nodes
CPU_NODE_RATIO = 0.20                  # 20% CPU nodes
ASIC_NODE_RATIO = 0.05                 # 5% ASIC nodes

# Power specifications (modern hardware)
GPU_POWER_PER_NODE_W = 2000            # NVIDIA A100 equivalents
CPU_POWER_PER_NODE_W = 600             # AMD EPYC processors
ASIC_POWER_PER_UNIT_W = 3200           # Latest Bitcoin ASICs

# Realistic idle power factors
IDLE_GPU_POWER_FACTOR = 0.25           # GPU idle consumption
IDLE_CPU_POWER_FACTOR = 0.15           # CPU idle consumption

# ================== ANCILLARY LOADS ==================
STORAGE_POWER_PER_NODE_W = 150         # NVMe storage arrays
NETWORK_POWER_PER_NODE_W = 100         # 100G networking
STORAGE_NODE_RATIO = 0.08              # 8% storage nodes
NETWORK_NODE_RATIO = 0.06              # 6% network infrastructure

# ================== COOLING & FACILITY ==================
DESIGN_PUE = 1.22                      # Realistic Canadian climate PUE
COOLING_COP = 5.5                      # High-efficiency cooling
TARGET_INLET_TEMP_C = 18               # Cold climate optimization
MAX_DELTA_T_C = 12
THERMAL_THROTTLING_THRESHOLD_C = 30    #Throttle servers if inlet           #NEW
                                       #temp exceeds this      

# ================== WIND INTEGRATION ==================
WIND_FARM_RATED_CAPACITY_MW = 3.5      # 3.5 MW wind farm (realistic ratio)
WIND_FARM_CAPACITY_FACTOR = 0.38       # Alberta winter average
TRANSMISSION_DISTANCE_KM = 1000          # Local wind farm proximity
TRANSMISSION_VOLTAGE_KV = 34.5         # Standard distribution voltage
TRANSMISSION_LOSS_PER_1000KM = 0.035   # 3.5% loss per 1000km

# ================== BATTERY AND STORAGE ==================                 #NEW
BATTERY_CAPACITY_MWH = 1.5             # Energy storage in MWh
BATTERY_CHARGE_EFFICIENCY = 0.95
BATTERY_DISCHARGE_EFFICIENCY = 0.95
UPS_BACKUP_DURATION_MINUTES = 15       # Emergency backup time

# ================== EMISSIONS FACTORS ==================
GRID_EMISSIONS_FACTOR_KGCO2_MWH = 420  # Actual Alberta grid mix
WIND_EMISSIONS_FACTOR_KGCO2_MWH = 11   # Lifecycle emissions

# ================== SYSTEM UTILIZATION ==================
DATA_CENTER_UTILIZATION = 0.85         # 85% average utilization

# ================== SERVER DEGRADATION & AGING ==================            #NEW
SERVER_AGE_YEARS = 2.0                    # Average node life
PERFORMANCE_DEGRADATION_RATE = 0.01       # 1% loss in performance per year


# ================== CONFIGURATION CLASS ==================
class DataCenterConfig:
    def __init__(self):
        # Time parameters
        self.simulation_duration_hours = SIMULATION_DURATION_HOURS
        self.time_step_minutes = TIME_STEP_MINUTES
        self.simulation_steps = SIMULATION_STEPS

        # Power system
        self.total_power_MW = DATA_CENTER_TOTAL_POWER_MW
        self.grid_voltage_V = GRID_VOLTAGE_V

        # Hardware configuration
        self.num_racks = NUM_RACKS
        self.nodes_per_rack = NODES_PER_RACK
        self.total_nodes = TOTAL_NODES
        self.gpu_node_ratio = GPU_NODE_RATIO
        self.cpu_node_ratio = CPU_NODE_RATIO
        self.asic_node_ratio = ASIC_NODE_RATIO

        # Power characteristics
        self.gpu_power_per_node_W = GPU_POWER_PER_NODE_W
        self.cpu_power_per_node_W = CPU_POWER_PER_NODE_W
        self.asic_power_per_unit_W = ASIC_POWER_PER_UNIT_W
        self.idle_gpu_power_factor = IDLE_GPU_POWER_FACTOR
        self.idle_cpu_power_factor = IDLE_CPU_POWER_FACTOR

        # Ancillary systems
        self.storage_power_per_node_W = STORAGE_POWER_PER_NODE_W
        self.network_power_per_node_W = NETWORK_POWER_PER_NODE_W
        self.storage_node_ratio = STORAGE_NODE_RATIO
        self.network_node_ratio = NETWORK_NODE_RATIO

        # Cooling system
        self.design_pue = DESIGN_PUE
        self.cooling_cop = COOLING_COP
        self.target_inlet_temp_C = TARGET_INLET_TEMP_C
        self.max_delta_T_C = MAX_DELTA_T_C
         self.thermal_throttling_threshold_C = THERMAL_THROTTLING_THRESHOLD_C

        # Battery
        self.battery_capacity_MWh = BATTERY_CAPACITY_MWH
        self.battery_charge_efficiency = BATTERY_CHARGE_EFFICIENCY
        self.battery_discharge_efficiency = BATTERY_DISCHARGE_EFFICIENCY
        self.ups_backup_duration_minutes = UPS_BACKUP_DURATION_MINUTES

        # Renewable integration
        self.wind_farm_rated_capacity_MW = WIND_FARM_RATED_CAPACITY_MW
        self.wind_farm_capacity_factor = WIND_FARM_CAPACITY_FACTOR
        self.transmission_distance_km = TRANSMISSION_DISTANCE_KM
        self.transmission_voltage_kV = TRANSMISSION_VOLTAGE_KV
        self.transmission_loss_per_1000km = TRANSMISSION_LOSS_PER_1000KM

        # Sustainability metrics
        self.grid_emissions_factor_kgco2_mwh = GRID_EMISSIONS_FACTOR_KGCO2_MWH
        self.wind_emissions_factor_kgco2_mwh = WIND_EMISSIONS_FACTOR_KGCO2_MWH

        # Degradation
        self.server_age_years = SERVER_AGE_YEARS
        self.performance_degradation_rate = PERFORMANCE_DEGRADATION_RATE

        # Operational parameters
        self.data_center_utilization = DATA_CENTER_UTILIZATION

CONFIG = DataCenterConfig()
