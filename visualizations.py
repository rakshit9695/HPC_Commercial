import matplotlib.pyplot as plt
import numpy as np

class HPPVisualizer:
    def __init__(self, metrics, simulation_data):
        self.metrics = metrics
        self.data = simulation_data

    def plot_power_flow(self):
        time = np.arange(len(self.data))
        plt.figure(figsize=(14, 6))
        plt.stackplot(
            time,
            [d['solar_used'] for d in self.data],
            [d['wind_used'] for d in self.data],
            [d['grid'] for d in self.data],
            labels=['Solar', 'Wind', 'Grid'],
            colors=['#FFD700', '#00BFFF', '#A9A9A9']
        )
        plt.title('How the HPP Powers the Data Center: Real-Time Source Split')
        plt.xlabel('Time Step (15 min intervals)')
        plt.ylabel('Power Delivered (MW)')
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_battery_soc(self):
        soc = [d['soc'] for d in self.data]
        plt.figure(figsize=(14, 4))
        plt.plot(soc, color='#8A2BE2', linewidth=2)
        plt.title('Battery State of Charge: Enabling Flexibility and Reliability')
        plt.xlabel('Time Step (15 min intervals)')
        plt.ylabel('SOC (MWh)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_comparison_metrics(self):
        metrics = self.metrics.finalize_metrics()
        # Comparative bar chart: HPP vs. "Grid-Only" scenario (for illustration)
        grid_only_cost = metrics['total_grid_import'] * self.metrics.config.grid['energy_price'] * 1000
        grid_only_renewable = 0  # All grid, no renewables
        grid_only_curtailment = 0
        grid_only_soc = 0

        labels = ['Renewable Penetration (%)', 'Grid Import (MWh)', 'Curtailment (MWh)', 'Energy Cost (CAD)', 'Avg Battery SOC (MWh)']
        hpp_values = [
            metrics['renewable_penetration'] * 100,
            metrics['total_grid_import'],
            metrics['total_curtailment'],
            metrics['total_cost'],
            metrics['avg_soc']
        ]
        grid_only_values = [
            grid_only_renewable,
            sum([d['wind_used'] + d['solar_used'] + d['grid'] for d in self.data]) * self.metrics.config.time_params['time_step_mins'] / 60.0,
            grid_only_curtailment,
            grid_only_cost,
            grid_only_soc
        ]

        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(15, 7))
        bars1 = ax.bar(x - width/2, hpp_values, width, label='Hybrid Power Plant', color='#228B22')
        bars2 = ax.bar(x + width/2, grid_only_values, width, label='Grid-Only (Conventional)', color='#B22222', alpha=0.7)

        ax.set_ylabel('Value')
        ax.set_title('HPP vs. Grid-Only: Key Performance Metrics')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        # Annotate bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.show()

    def narrate_story(self):
        metrics = self.metrics.finalize_metrics()
        narration = f"""
        === Investor Presentation Narrative ===

        The Hybrid Power Plant (HPP) solution is a leap forward in sustainable, reliable, and cost-effective data center operations.

        1. **Sustainability at Scale:** With renewable penetration reaching {metrics['renewable_penetration']*100:.1f}%, the HPP slashes dependency on fossil-based grid electricity, directly reducing carbon emissions and supporting ESG goals.

        2. **Cost Leadership:** Through smart integration of solar, wind, and storage, the total energy cost is just ${metrics['total_cost']:.2f}, far below what a grid-only approach would require for the same workload.

        3. **Maximized Resource Use:** Curtailment is kept to just {metrics['total_curtailment']:.1f} MWh, meaning nearly all renewable generation is actually used, not wasted.

        4. **Resilient Operations:** The battery system maintains an average state of charge of {metrics['avg_soc']:.2f} MWh, providing a buffer against renewable variability and grid outages.

        5. **Grid Relief:** Grid import is minimized to {metrics['total_grid_import']:.1f} MWh, freeing up capacity for other users and shielding the operation from price spikes.

        **Conclusion:** The HPP architecture is not just a technical upgrade—it's a strategic asset. It delivers sustainability, resilience, and economic value, making it a compelling investment for the future of digital infrastructure.
        """
        print(narration)

    def show_all(self):
        print("\n--- Hybrid Power Plant Performance Story ---\n")
        self.plot_power_flow()
        self.plot_battery_soc()
        self.plot_comparison_metrics()
        self.narrate_story()

