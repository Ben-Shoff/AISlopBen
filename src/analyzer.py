def analyze_data(data_dict, conditions):
    """
    Analyzes telemetry DataFrames to find timestamp windows where threshold conditions are violated.
    """
    results = []
    
    cond_type = conditions.get('type')
    operator = conditions.get('operator')
    threshold = conditions.get('value')
    min_duration = conditions.get('min_duration', 0.0)
    
    if cond_type != 'threshold':
        # Extend here for edge detection, rate-of-change, etc.
        return results

    for metric_name, df in data_dict.items():
        # Identify point-in-time violations
        if operator == '>':
            violations = df['values'] > threshold
        elif operator == '<':
            violations = df['values'] < threshold
        elif operator == '==':
            violations = df['values'] == threshold
        else:
            continue

        # Find contiguous intervals of violations
        df['is_violation'] = violations
        # Create a grouping key that changes whenever 'is_violation' toggles
        df['group'] = (df['is_violation'] != df['is_violation'].shift()).cumsum()
        
        # Filter down to only the rows that are violations, grouped by contiguous segments
        violation_groups = df[df['is_violation']].groupby('group')
        
        for _, group in violation_groups:
            start_time = group['timestamps'].iloc[0]
            end_time = group['timestamps'].iloc[-1]
            duration = end_time - start_time
            
            # Check if duration meets heuristic requiremens
            if duration >= min_duration:
                peak = group['values'].max() if operator == '>' else group['values'].min()
                
                results.append({
                    'metric': metric_name,
                    'start_time': start_time,
                    'end_time': end_time,
                    'peak_value': peak
                })
                
    return results
