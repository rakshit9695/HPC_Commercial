"""Entry point for the HPC data center simulation application."""

import argparse
from simulation import run_simulation
from visualization import save_all_visualizations, generate_summary_report

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Simulate an HPC Data Center with Solar Integration')
    
    parser.add_argument('--output', default='hpc_results.csv',
                       help='Output CSV file for simulation results')
    parser.add_argument('--summary', default='hpc_summary.csv',
                       help='Output CSV file for summary report')
    parser.add_argument('--no-plots', action='store_true',
                       help='Disable generation of plots')
    parser.add_argument('--solar-farms', type=int, default=1,
                       help='Number of solar farms to simulate')
    
    return parser.parse_args()

def main():
    """Run the simulation and output results."""
    args = parse_arguments()
    
    # Run the simulation
    results = run_simulation(num_solar_farms=args.solar_farms)
    
    # Save results
    results.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")
    
    # Generate summary
    summary = generate_summary_report(results)
    summary.to_csv(args.summary)
    print(f"Summary report saved to {args.summary}")
    
    # Generate visualizations
    if not args.no_plots:
        save_all_visualizations(results)
    
    # Print summary
    print("\n=== Simulation Summary ===")
    print(f"Average Total Power: {summary['Average_Total_Power_kW']:.1f} kW")
    print(f"Peak Power: {summary['Peak_Power_kW']:.1f} kW")
    print(f"Average Solar Offset: {summary['Average_Solar_Offset_pct']:.1f}%")
    print(f"Peak Solar Offset: {summary['Peak_Solar_Offset_pct']:.1f}%")
    print(f"Total Carbon Emissions: {summary['Total_Carbon_Emissions_kg']:.0f} kg CO₂")
    print(f"Carbon Savings from Solar: {summary['Total_Solar_Savings_kg']:.0f} kg CO₂")
    
    print("\nSimulation completed successfully.")

if __name__ == "__main__":
    main()
