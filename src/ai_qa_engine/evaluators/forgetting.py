from typing import Dict, Any

def evaluate_catastrophic_forgetting(baseline_accuracy: float, current_accuracy: float, max_drop: float = 0.05) -> Dict[str, Any]:
    """
    Evaluates performance degradation on historical/baseline tasks.
    Bewertet den Leistungsabfall bei historischen/Baseline-Aufgaben.
    """
    accuracy_drop = baseline_accuracy - current_accuracy
    is_forgotten = accuracy_drop > max_drop

    return {
        "baseline_accuracy": baseline_accuracy,
        "current_accuracy": current_accuracy,
        "accuracy_drop": round(float(accuracy_drop), 4),
        "max_allowed_drop": max_drop,
        "catastrophic_forgetting_detected": bool(is_forgotten),
        "status": "FAILED" if is_forgotten else "PASSED"
    }