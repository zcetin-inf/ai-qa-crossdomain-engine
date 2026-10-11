import os
import sys
import requests
import streamlit as st

# Ensure Python can find internal modules / Stelle sicher, dass interne Module gefunden werden
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from ai_qa_engine.reporters.html_reporter import HtmlReporter
from ai_qa_engine.reporters.pdf_reporter import REPORTLAB_AVAILABLE, PdfReporter

# Page Configuration / Seitenkonfiguration
st.set_page_config(
    page_title="AI-QA Crossdomain Engine", page_icon="🤖", layout="wide"
)

st.title("🛡️ AI-QA Crossdomain Engine - Dashboard")
st.markdown(
    "Monitor Model Drift, Catastrophic Forgetting, and generate professional"
    " audit reports."
)

API_BASE_URL = "http://127.0.0.1:8000"


# --- FETCH CENTRAL METRICS FROM API / ZENTRALE METRIKEN VON DER API ABRUFEN ---
@st.cache_data(ttl=2)
def fetch_central_metrics():
  """Fetches the latest shared test data from FastAPI central endpoint.

  Ruft die neuesten gemeinsamen Testdaten vom zentralen FastAPI-Endpunkt ab.
  """
  response = requests.get(f"{API_BASE_URL}/metrics/latest")
  response.raise_for_status()  # Fail-fast: Fail if API is unreachable / Fehler direkt auslösen, falls API nicht erreichbar
  return response.json().get("data")


# Load central data strictly / Zentrale Daten streng laden
central_data = fetch_central_metrics()

drift_test_cfg = central_data["drift_test"]
forgetting_test_cfg = central_data["forgetting_test"]

# Extract values strictly without fallback defaults / Werte streng ohne Fallback-Werte extrahieren
def_baseline_data = ", ".join(map(str, drift_test_cfg["baseline_data"]))
def_current_data = ", ".join(map(str, drift_test_cfg["current_data"]))
def_threshold = float(drift_test_cfg["threshold"])

def_baseline_acc = float(forgetting_test_cfg["baseline_accuracy"])
def_current_acc = float(forgetting_test_cfg["current_accuracy"])
def_max_drop = float(forgetting_test_cfg["max_allowed_drop"])

# Sidebar for Navigation / Seitenleiste für Navigation
st.sidebar.header("Navigation")
option = st.sidebar.selectbox(
    "Choose Evaluation Tool / Wähle Evaluierungstool:",
    ["Model Drift Evaluation", "Catastrophic Forgetting Evaluation"],
)

html_reporter = HtmlReporter()
pdf_reporter = PdfReporter() if REPORTLAB_AVAILABLE else None

if option == "Model Drift Evaluation":
  st.header("📊 Model Drift & Data Distribution Shift")
  st.markdown(
      "Compare baseline dataset with current production data to detect"
      " distribution shifts."
  )

  col1, col2 = st.columns(2)
  with col1:
    baseline_input = st.text_area(
        "Baseline Data (comma-separated)", def_baseline_data
    )
  with col2:
    current_input = st.text_area(
        "Current Production Data (comma-separated)", def_current_data
    )

  threshold = st.slider(
      "Drift Threshold / Drift-Schwellenwert", 0.01, 0.5, def_threshold
  )

  if st.button("Evaluate Drift / Drift Auswerten"):
    try:
      baseline_data = [float(x.strip()) for x in baseline_input.split(",")]
      current_data = [float(x.strip()) for x in current_input.split(",")]

      payload = {
          "baseline_data": baseline_data,
          "current_data": current_data,
          "threshold": threshold,
      }

      response = requests.post(f"{API_BASE_URL}/evaluate/drift", json=payload)

      if response.status_code == 200:
        res_json = response.json()
        st.success("Evaluation Completed Successfully!")

        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Drift Score", res_json["drift_score"])
        mcol2.metric("Threshold", res_json["threshold"])
        mcol3.metric("Status", res_json["status"])

        if res_json["drift_detected"]:
          st.warning("⚠️ Warning: Model Drift Detected!")
        else:
          st.info("✅ Status: Data is Stable.")

        # Generate Reports / Berichte generieren
        st.markdown("---")
        st.subheader("📥 Export Audit Reports / Berichte exportieren")

        html_path = html_reporter.generate_report("Model_Drift", res_json)
        with open(html_path, "r", encoding="utf-8") as f:
          st.download_button(
              "Download HTML Report",
              f,
              file_name=os.path.basename(html_path),
              mime="text/html",
          )

        if REPORTLAB_AVAILABLE:
          pdf_path = pdf_reporter.generate_report("Model_Drift", res_json)
          with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
            )
      else:
        st.error(f"API Error: {response.text}")
    except Exception as e:
      st.error(f"Invalid input format or API connection error: {str(e)}")

elif option == "Catastrophic Forgetting Evaluation":
  st.header("🧠 Catastrophic Forgetting & Historical Accuracy")
  st.markdown(
      "Evaluate performance degradation on historical tasks after new model"
      " updates."
  )

  col1, col2 = st.columns(2)
  with col1:
    baseline_acc = st.number_input(
        "Baseline Accuracy (0.0 - 1.0)",
        min_value=0.0,
        max_value=1.0,
        value=def_baseline_acc,
    )
  with col2:
    current_acc = st.number_input(
        "Current Accuracy on Old Tasks (0.0 - 1.0)",
        min_value=0.0,
        max_value=1.0,
        value=def_current_acc,
    )

  max_drop = st.slider(
      "Max Allowed Drop / Maximal zulässiger Abfall", 0.01, 0.2, def_max_drop
  )

  if st.button("Evaluate Forgetting / Unvergessenheit Auswerten"):
    try:
      payload = {
          "baseline_accuracy": baseline_acc,
          "current_accuracy": current_acc,
          "max_allowed_drop": max_drop,
      }

      response = requests.post(
          f"{API_BASE_URL}/evaluate/forgetting", json=payload
      )

      if response.status_code == 200:
        res_json = response.json()
        st.success("Evaluation Completed Successfully!")

        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Accuracy Drop", res_json["accuracy_drop"])
        mcol2.metric("Max Allowed Drop", res_json["max_allowed_drop"])
        mcol3.metric("Status", res_json["status"])

        if res_json["catastrophic_forgetting_detected"]:
          st.error("❌ Failed: Catastrophic Forgetting Detected!")
        else:
          st.success("✅ Passed: No significant forgetting detected.")

        # Generate Reports / Berichte generieren
        st.markdown("---")
        st.subheader("📥 Export Audit Reports / Berichte exportieren")

        html_path = html_reporter.generate_report(
            "Catastrophic_Forgetting", res_json
        )
        with open(html_path, "r", encoding="utf-8") as f:
          st.download_button(
              "Download HTML Report",
              f,
              file_name=os.path.basename(html_path),
              mime="text/html",
          )

        if REPORTLAB_AVAILABLE:
          pdf_path = pdf_reporter.generate_report(
              "Catastrophic_Forgetting", res_json
          )
          with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
            )
      else:
        st.error(f"API Error: {response.text}")
    except Exception as e:
      st.error(f"API connection error: {str(e)}")