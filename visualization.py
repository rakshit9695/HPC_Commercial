"""
visualization.py

Data Visualization Module for Wind-Powered ASIC HPC Data Center
"""

import os
import matplotlib.pyplot as plt
import numpy as np

def plot_power_requirement_vs_wind(timesteps, power_required, power_delivered, save_path="results/power_requirement_vs_wind_farm.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(timesteps, power_required, label='Power Requirement (HPC Data Center)', color='navy', linewidth=2)
    plt.plot(timesteps, power_delivered, label='Power Delivered by Wind Farm', color='seagreen', linewidth=2)
    plt.fill_between(timesteps, power_delivered, power_required, where=(np.array(power_required) > np.array(power_delivered)),
                     color='red', alpha=0.3, label='Power Deficit')
    plt.xlabel('Time (hours)')
    plt.ylabel('Power (MW)')
    plt.title('Power Requirement vs Power Delivered by Wind Farm')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_power_losses_vs_time(timesteps, power_losses, save_path="results/power_losses_vs_time.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(timesteps, power_losses, label='Power Losses', color='red', linewidth=2)
    plt.xlabel('Time (hours)')
    plt.ylabel('Power Loss (MW)')
    plt.title('Power Losses vs Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_power_losses_vs_distance(distances_km, power_losses, save_path="results/power_losses_vs_distance.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(distances_km, power_losses, label='Power Losses vs Distance', color='darkorange', linewidth=2)
    plt.xlabel('Transmission Distance (km)')
    plt.ylabel('Power Loss (MW)')
    plt.title('Power Losses vs Transmission Distance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_feasibility_index(timesteps, feasibility_index, save_path="results/feasibility_index.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(timesteps, feasibility_index, label='Feasibility Index', color='purple', linewidth=2)
    plt.axhline(y=1.0, color='green', linestyle='--', label='Feasible Threshold')
    plt.xlabel('Time (hours)')
    plt.ylabel('Feasibility Index')
    plt.title('Feasibility Index Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_power_utilization_components(component_labels, component_powers, save_path="results/power_utilization_components.png"):
    plt.figure(figsize=(10, 6))
    plt.bar(component_labels, component_powers, color=['gray', 'purple', 'blue', 'deepskyblue'])
    plt.title('Power Utilization by HPC Data Center Components')
    plt.ylabel('Power (MW)')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def generate_all_plots(timesteps, power_data, metrics, distances_km=None, losses_vs_distance=None):
    os.makedirs("results", exist_ok=True)

    # Extract relevant data
    power_required = [pd['total_power']/1e6 for pd in power_data]  # MW
    power_delivered = [pd['wind_delivered']/1e6 for pd in power_data]  # MW
    power_losses = [pd['transmission_losses']/1e6 for pd in power_data]  # MW

    # Feasibility index: ratio of delivered to required
    feasibility_index = np.array(power_delivered) / np.array(power_required)

    # Power utilization by components
    component_labels = ['Storage', 'Network', 'CPU', 'GPU']
    component_powers = [
        metrics.metrics['storage_energy_wh'] / (metrics.config.simulation_duration_hours),  # MW
        metrics.metrics['network_energy_wh'] / (metrics.config.simulation_duration_hours),
        metrics.metrics['cpu_energy_wh'] / (metrics.config.simulation_duration_hours),
        metrics.metrics['gpu_energy_wh'] / (metrics.config.simulation_duration_hours)
    ]

    # 1. Power Requirement vs Power Delivered by Wind Farm
    plot_power_requirement_vs_wind(timesteps, power_required, power_delivered)

    # 2. Power Losses vs Time
    plot_power_losses_vs_time(timesteps, power_losses)

    # 3. Power Losses vs Distance (if data provided)
    if distances_km is not None and losses_vs_distance is not None:
        plot_power_losses_vs_distance(distances_km, losses_vs_distance)

    # 4. Feasibility Index Calculations
    plot_feasibility_index(timesteps, feasibility_index)

    # 5. Power Utilization by Data Center Components
    plot_power_utilization_components(component_labels, component_powers)
