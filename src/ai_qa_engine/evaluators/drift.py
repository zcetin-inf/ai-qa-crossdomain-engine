import numpy as np
from typing import Dict, Any, List

def evaluate_model_drift(baseline_data: List[float], current_data: List[float], threshold: float = 0.15) -> Dict[str, Any]:
    """
    Calculates data distribution shift between baseline and current production data.
    Berechnet die Datenverteilungsverschiebung zwischen Baseline- und aktuellen Produktionsdaten.
    """
    base_mean = np.mean(baseline_data) if baseline_data else 0.0
    curr_mean = np.mean(current_data) if current_data else 0.0
    
    drift_score = abs(base_mean - curr_mean) / (abs(base_mean) + 1e-8)
    is_drift_detected = drift_score > threshold

    return {
        "drift_score": round(float(drift_score), 4),
        "threshold": threshold,
        "drift_detected": bool(is_drift_detected),
        "status": "WARNING" if is_drift_detected else "STABLE"
    }