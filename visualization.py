"""Functions for generating visualizations of data center metrics with solar integration."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_power_distribution(results):
    """Plot the distribution of power consumption by component over time."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    components = [
        ('CPU_Power_kW', 'CPU'),
        ('GPU_Power_kW', 'GPU'),
        ('Storage_Power_kW', 'Storage'),
        ('Network_Power_kW', 'Network'),
        ('Cooling_Power_kW', 'Cooling'),
        ('Other_Infra_Power_kW', 'Other Infrastructure')
    ]
    
    bottom = np.zeros(len(results))
    for col, label in components:
        ax.fill_between(results['Timestamp'], bottom, bottom + results[col], 
                       label=label, alpha=0.7)
        bottom += results[col]
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Power Consumption (kW)')
    ax.set_title('Power Distribution Over Time')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig, ax

def plot_utilization_vs_power(results):
    """Plot the relationship between server utilization and power consumption."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(results['Utilization'], results['Total_Power_kW'], alpha=0.6)
    ax.set_xlabel('Server Utilization')
    ax.set_ylabel('Total Power Consumption (kW)')
    ax.set_title('Server Utilization vs. Power Consumption')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    z = np.polyfit(results['Utilization'], results['Total_Power_kW'], 1)
    p = np.poly1d(z)
    ax.plot(np.sort(results['Utilization']), p(np.sort(results['Utilization'])), 
           "r--", alpha=0.8, label=f'Fit: y={z[0]:.2f}x+{z[1]:.2f}')
    ax.legend()
    return fig, ax

def plot_pue_and_efficiency(results):
    """Plot PUE and DCiE over time."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
    
    ax1.plot(results['Timestamp'], results['PUE'], label='PUE', color='blue')
    ax1.set_ylabel('Power Usage Effectiveness (PUE)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2.plot(results['Timestamp'], results['DCiE'], label='DCiE', color='green')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Data Center Infrastructure Efficiency (%)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    return fig, (ax1, ax2)

def plot_temperature_metrics(results):
    """Plot temperature metrics over time."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    ax.plot(results['Timestamp'], results['Inlet_Temperature_C'], label='Inlet', color='blue')
    ax.plot(results['Timestamp'], results['Outlet_Temperature_C'], label='Outlet', color='red')
    ax.fill_between(results['Timestamp'], results['Inlet_Temperature_C'], 
                   results['Outlet_Temperature_C'], color='orange', alpha=0.3, label='ΔT')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Metrics')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig, ax

def plot_solar_power_generation(results):
    """Plot solar power generation over time."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    ax.plot(results['Timestamp'], results['Solar_Power_MW'], 
           label='Solar Generation', color='orange')
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW)')
    ax.set_title('Solar Power Generation')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig, ax

def plot_power_sources(results):
    """Plot data center power sources (grid vs solar) over time."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    total_power_mw = results['Total_Power_kW'] / 1000
    solar_utilized = np.minimum(results['Solar_Power_MW'], total_power_mw)
    grid_power = total_power_mw - solar_utilized
    
    ax.fill_between(results['Timestamp'], 0, solar_utilized, 
                   label='Solar Utilized', color='orange', alpha=0.7)
    ax.fill_between(results['Timestamp'], solar_utilized, total_power_mw, 
                   label='Grid Power', color='gray', alpha=0.7)
    
    ax.plot(results['Timestamp'], total_power_mw, label='Total Power', 
           color='blue', linestyle='--')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW)')
    ax.set_title('Power Sources Breakdown')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig, ax

def generate_summary_report(results):
    """Generate a summary report of key metrics."""
    return pd.Series({
        'Average_Total_Power_kW': results['Total_Power_kW'].mean(),
        'Peak_Power_kW': results['Total_Power_kW'].max(),
        'Average_PUE': results['PUE'].mean(),
        'Average_DCiE_pct': results['DCiE'].mean(),
        'Average_Solar_Offset_pct': results['Solar_Offset_Pct'].mean(),
        'Peak_Solar_Offset_pct': results['Solar_Offset_Pct'].max(),
        'Total_Carbon_Emissions_kg': results['Carbon_Emissions_kg'].sum(),
        'Total_Solar_Savings_kg': results['Solar_Carbon_Savings_kg'].sum(),
        'Average_Rack_Density_kW': results['Rack_Power_Density_kW'].mean(),
        'Average_Node_Power_W': results['Node_Power_Usage_W'].mean()
    })

def save_all_visualizations(results):
    """Generate and save all visualizations."""
    print("Generating visualizations...")
    
    plots = [
        plot_power_distribution(results),
        plot_utilization_vs_power(results),
        plot_temperature_metrics(results),
        plot_solar_power_generation(results),
        plot_power_sources(results)
    ]
    
    filenames = [
        'power_distribution.png',
        'utilization_vs_power.png',
        'temperature_metrics.png',
        'solar_generation.png',
        'power_sources.png'
    ]
    
    for (fig, _), filename in zip(plots, filenames):
        fig.savefig(filename)
        plt.close(fig)
    
    print("Visualizations saved as PNG files.")
