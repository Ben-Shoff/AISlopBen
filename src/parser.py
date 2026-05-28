import os
import re
import pandas as pd
from wpiutil.log import DataLogReader

def extract_log_data(filepath, key_patterns):
    """
    Extracts time-series data from a WPILOG file for keys matching specific patterns.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None

    try:
        reader = DataLogReader(filepath)
    except Exception as e:
        print(f"Error reading WPILOG: {e}")
        return None

    if not reader:
        print("Invalid WPILOG file.")
        return None

    # Compile regex patterns for fast matching
    regexes = [re.compile(p, re.IGNORECASE) for p in key_patterns]
    
    # First pass: map entry IDs to names that match our string patterns
    entries = {}
    for record in reader:
        if record.isStart():
            start_data = record.getStartData()
            if any(r.match(start_data.name) for r in regexes):
                # For this simple detector, we will only map floating point (double) fields
                if start_data.type == "double":
                    entries[start_data.entry] = start_data.name

    if not entries:
        return {}

    # Initialize data dictionary
    data = {name: {"timestamps": [], "values": []} for name in entries.values()}
    
    # Second pass: extract payloads only for matched entries
    for record in reader:
        if record.getEntry() in entries:
            name = entries[record.getEntry()]
            if record.isControl():
                continue
                
            try:
                # WPILib timestamps are in integer microseconds
                timestamp = record.getTimestamp() / 1_000_000.0 
                value = record.getDouble()
                data[name]['timestamps'].append(timestamp)
                data[name]['values'].append(value)
            except Exception:
                pass # Ignore parsing errors for malformed records

    # Convert lists to Pandas DataFrames for easier analysis
    dfs = {}
    for name, entry_data in data.items():
        if entry_data['timestamps']: # Only save if we have data points
            dfs[name] = pd.DataFrame(entry_data)

    return dfs
