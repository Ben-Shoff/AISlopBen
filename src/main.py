import argparse
import sys
from parser import extract_log_data
from heuristics import get_heuristics
from analyzer import analyze_data

def main():
    parser = argparse.ArgumentParser(description="FRC Match Log Anomaly Detector")
    parser.add_argument("logfile", help="Path to the .wpilog file")
    parser.add_argument("--problem", required=True, help="Problem to analyze (e.g., high_power, voltage_drop)")
    args = parser.parse_args()

    heuristics = get_heuristics(args.problem)
    if not heuristics:
        print(f"Unknown problem category: {args.problem}")
        sys.exit(1)
    
    print(f"Analyzing {args.logfile} for '{args.problem}' ({heuristics['description']})...")
    
    # Extract only the data matching the telemetry keys
    data = extract_log_data(args.logfile, heuristics['keys'])
    
    if not data:
        print("No relevant data found for the specified problem telemetry keys.")
        sys.exit(0)

    # Analyze extracted data based on threshold conditions
    results = analyze_data(data, heuristics['conditions'])
    
    # Print reporting results
    if not results:
        print("No anomalies detected.")
    else:
        print("\n=== Anomalies Detected ===")
        for res in results:
            print(f"Subsystem/Metric: {res['metric']}")
            print(f"Time Window:      {res['start_time']:.2f}s to {res['end_time']:.2f}s")
            print(f"Duration:         {res['end_time'] - res['start_time']:.2f}s")
            print(f"Peak Value:       {res['peak_value']:.2f}")
            print("-" * 30)

if __name__ == "__main__":
    main()
