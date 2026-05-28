HEURISTICS = {
    "high_power": {
        "description": "High power consumption (current spikes)",
        # Regex mappings for datalog keys
        "keys": [r".*Current.*", r"/PDH/.*"], 
        "conditions": {
            "type": "threshold",
            "operator": ">",
            "value": 40.0, # Amps
            "min_duration": 0.5 # Seconds sustained
        }
    },
    "voltage_drop": {
        "description": "Battery voltage dropping significantly",
        "keys": [r".*Voltage.*", r"/PDH/Voltage"],
        "conditions": {
            "type": "threshold",
            "operator": "<",
            "value": 9.0, # Volts
            "min_duration": 0.2
        }
    }
}

def get_heuristics(problem_name):
    return HEURISTICS.get(problem_name)
