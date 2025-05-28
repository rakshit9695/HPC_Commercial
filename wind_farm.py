"""
wind_farm.py

Advanced Wind Farm Simulation Module (Canadian Context)
Implements IEC 61400-12-1 Power Curve Modeling with Transmission Losses
"""

import numpy as np
from scipy.interpolate import interp1d

class WindFarm:
    def __init__(self, capacity_MW=57, rotor_radius_m=75, hub_height_m=120,
                 region='Alberta', converter_type='DFIG', transmission_voltage_kV=500):
        """
        Initialize wind farm with Canadian operational parameters
        
        Args:
            capacity_MW: Total installed capacity (MW)
            rotor_radius_m: Turbine rotor radius (m)
            hub_height_m: Hub height (m)
            region: 'Alberta', 'Ontario', or 'Quebec'
            converter_type: 'DFIG' or 'FullPower'
            transmission_voltage_kV: Transmission line voltage (kV)
        """
        self.capacity_MW = capacity_MW
        self.rotor_radius = rotor_radius_m
        self.hub_height = hub_height_m
        self.region = region
        self.transmission_voltage = transmission_voltage_kV * 1000  # Convert to V
        
        # Region-specific parameters
        self.capacity_factors = {
            'Alberta': 0.345,
            'Ontario': 0.26,
            'Quebec': 0.32
        }
        self.cf = self.capacity_factors.get(region, 0.30)
        
        # Technical parameters
        self.air_density = 1.225  # kg/m³
        self.betz_limit = 0.593
        self.mechanical_efficiency = 0.95
        self.converter_efficiencies = {
            'DFIG': 0.98,
            'FullPower': 0.99
        }
        self.converter_eff = self.converter_efficiencies[converter_type]
        
        # Transmission parameters
        self.conductor_resistivity = 1.68e-8  # Copper (Ω·m)
        self.conductor_area = 500e-6  # 500 mm²
        
        # Wind speed profile (Alberta example)
        self.base_wind_speeds = np.array([
            6.5, 6.7, 6.8, 6.7, 6.5, 6.3, 6.0, 6.2, 6.8, 7.5, 8.0, 8.3,
            8.5, 8.7, 8.8, 8.7, 8.4, 8.1, 7.8, 7.4, 7.0, 6.7, 6.5, 6.4
        ])
        self.wind_speed_interp = interp1d(
            np.linspace(0, 24, 24),
            self.base_wind_speeds,
            kind='cubic'
        )
        
    def _transmission_loss(self, power_MW, distance_km):
        """Calculate transmission losses using P = I²R formula"""
        current = (power_MW * 1e6) / (self.transmission_voltage * np.sqrt(3))
        resistance = (self.conductor_resistivity * distance_km * 1000) / self.conductor_area
        return 3 * (current ** 2) * resistance / 1e6  # 3-phase, return MW loss
        
    def _turbine_power(self, wind_speed):
        """Calculate single turbine output using IEC power curve model"""
        swept_area = np.pi * self.rotor_radius ** 2
        theoretical_power = 0.5 * self.air_density * swept_area * wind_speed **3
        
        # Apply efficiency factors
        return (theoretical_power * self.betz_limit 
                * self.mechanical_efficiency 
                * self.converter_eff) / 1e6  # MW

    def realistic_output(self, time_h, distance_km=1000):
        """
        Calculate wind farm output with realistic temporal variations
        
        Args:
            time_h: Simulation time in hours
            distance_km: Transmission distance in km
            
        Returns:
            delivered_power_MW: Net power delivered to grid
        """
        # Base wind speed with diurnal variation
        base_speed = self.wind_speed_interp(time_h % 24)
        
        # Add turbulence (Kaimal spectrum simplified)
        turbulence_intensity = 0.1  # IEC Class B
        speed_variation = base_speed * turbulence_intensity * np.sin(2*np.pi*time_h/12)
        effective_speed = max(base_speed + speed_variation, 0)
        
        # Calculate raw power
        turbine_power = self._turbine_power(effective_speed)
        num_turbines = self.capacity_MW / (self._turbine_power(11.5))  # Rated at 11.5 m/s
        raw_power = turbine_power * num_turbines
        
        # Apply capacity factor constraint
        cf_limit = self.capacity_MW * self.cf
        limited_power = min(raw_power, cf_limit)
        
        # Calculate transmission losses
        losses = self._transmission_loss(limited_power, distance_km)
        
        return max(limited_power - losses, 0)
    
    def annual_energy_production(self):
        """Calculate estimated annual energy production (GWh)"""
        return self.capacity_MW * self.cf * 8760 / 1000

# Example usage:
if __name__ == "__main__":
    alberta_farm = WindFarm(capacity_MW=5715, region='Alberta')
    print(f"Annual Production: {alberta_farm.annual_energy_production():.1f} GWh")
    
    quebec_farm = WindFarm(capacity_MW=4072, region='Quebec')
    print(f"Quebec Farm @ 8m/s: {quebec_farm._turbine_power(8):.2f} MW/turbine")
