"""
ProfitPulse API
Connects the financial intelligence engine
to the web dashboard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from profit_engine import analyze_business
from anomaly_detector import detect_anomalies
from decision_engine import analyze_anomalies


app = FastAPI(
    title="ProfitPulse API",
    description="AI Profit Forensics & Decision API",
    version="1.0.0"
)


# Allow the frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


DATA_FILE = "../data/sample_transactions.csv"


@app.get("/")
def home():

    return {
        "application": "ProfitPulse",
        "status": "online",
        "message": "AI Profit Forensics API"
    }


@app.get("/financial-summary")
def financial_summary():

    df = pd.read_csv(DATA_FILE)

    data = {
        "revenue": df["revenue"].sum(),
        "product_cost": df["product_cost"].sum(),
        "operating_cost": df["operating_cost"].sum(),
        "marketing_cost": df["marketing_cost"].sum()
    }

    return analyze_business(data)


@app.get("/anomalies")
def anomalies():

    results = detect_anomalies(DATA_FILE)

    return {
        "count": len(results),
        "anomalies": results
    }


@app.get("/decisions")
def decisions():

    anomalies_found = detect_anomalies(DATA_FILE)

    results = analyze_anomalies(
        anomalies_found
    )

    return {
        "count": len(results),
        "decisions": results
    }


@app.get("/investigate")
def investigate():

    anomalies_found = detect_anomalies(DATA_FILE)

    decisions_found = analyze_anomalies(
        anomalies_found
    )

    return {
        "investigation_status": "completed",
        "anomalies_detected": len(anomalies_found),
        "findings": decisions_found
    }
