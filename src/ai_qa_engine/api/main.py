from functools import lru_cache
import json
import logging
import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import modular evaluators / Importiere modulare Evaluatoren
from ai_qa_engine.evaluators.drift import evaluate_model_drift
from ai_qa_engine.evaluators.forgetting import evaluate_catastrophic_forgetting

# Logging configuration / Logging-Konfiguration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-QA Crossdomain Engine API",
    description=(
        "API for Model Drift, Catastrophic Forgetting evaluation, and Quality"
        " Gates."
    ),
    version="1.0.0",
)


# --- DATA ACCESS LAYER / DATENZUGRIFFSSCHICHT ---
#@lru_cache() - without caching for now, as we want to always fetch the latest metrics
def fetch_metrics_from_source():
  """Reads model metrics and test data from the shared JSON file for now.

  In the future, file reading logic can be replaced with database queries.
  Clients remain completely unaffected (Loose Coupling).

  Liest Modellmetriken und Testdaten vorerst aus der gemeinsamen JSON-Datei.
  In Zukunft kann die Dateilogik durch Datenbankabfragen ersetzt werden.
  """
  file_path = os.path.abspath(
      os.path.join(
          os.path.dirname(__file__), "..", "data", "shared_test_data.json"
      )
  )

  # Read and return data if file exists / Datei lesen und zurückgeben, falls sie existiert
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      return json.load(f)

  # Fallback default values if file is missing / Fallback-Standardwerte bei fehlender Datei
  return {
      "drift_test": {
          "baseline_data": [1.0, 1.1, 1.05, 1.02],
          "current_data": [1.01, 1.03, 1.04, 1.02],
          "threshold": 0.15,
      },
      "forgetting_test": {
          "baseline_accuracy": 0.92,
          "current_accuracy": 0.90,
          "max_allowed_drop": 0.05,
      },
  }


# Request schemas using Pydantic / Anfrageschemata mit Pydantic
class DriftRequest(BaseModel):
  baseline_data: List[float] = Field(
      ..., description="Baseline dataset values / Basis-Datensatzwerte"
  )
  current_data: List[float] = Field(
      ..., description="Current production dataset values / Aktuelle Produktionsdaten"
  )
  threshold: float = Field(
      0.15, description="Drift threshold / Drift-Schwellenwert"
  )


class ForgettingRequest(BaseModel):
  baseline_accuracy: float = Field(
      ..., description="Original model accuracy / Ursprüngliche Modellgenauigkeit"
  )
  current_accuracy: float = Field(
      ...,
      description=(
          "Current model accuracy on old tasks / Aktuelle Genauigkeit bei alten"
          " Aufgaben"
      ),
  )
  max_allowed_drop: float = Field(
      0.05, description="Maximum allowed drop / Maximal zulässiger Abfall"
  )


@app.get("/")
def root():
  """Root endpoint / Root-Endpunkt"""
  return {
      "status": "healthy",
      "message": "AI-QA Engine REST API is running successfully!",
  }


@app.get("/metrics/latest")
def get_latest_metrics():
  """Central API endpoint for clients (Streamlit GUI or C# tests)

  to fetch the latest model test metrics.
  Zentraler API-Endpunkt für Clients zum Abrufen der neuesten Modellmetriken.
  """
  logger.info("Fetching latest metrics from shared storage/source.")
  metrics = fetch_metrics_from_source()

  return {
      "status": "success",
      "data_source": (
          "json_artifact"
      ),  # Will change to "postgresql" when migrating to DB
      "data": metrics,
  }


@app.post("/evaluate/drift")
def post_model_drift(request: DriftRequest):
  """API Endpoint for Model Drift Evaluation.

  API-Endpunkt zur Modell-Drift-Auswertung.
  """
  logger.info("Evaluating model drift request received.")
  try:
    result = evaluate_model_drift(
        baseline_data=request.baseline_data,
        current_data=request.current_data,
        threshold=request.threshold,
    )
    return result
  except Exception as e:
    logger.error(f"Error during drift evaluation: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate/forgetting")
def post_catastrophic_forgetting(request: ForgettingRequest):
  """API Endpoint for Catastrophic Forgetting Evaluation.

  API-Endpunkt zur Auswertung von Catastrophic Forgetting.
  """
  logger.info("Evaluating catastrophic forgetting request received.")
  try:
    result = evaluate_catastrophic_forgetting(
        baseline_accuracy=request.baseline_accuracy,
        current_accuracy=request.current_accuracy,
        max_drop=request.max_allowed_drop,
    )
    return result
  except Exception as e:
    logger.error(f"Error during forgetting evaluation: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))