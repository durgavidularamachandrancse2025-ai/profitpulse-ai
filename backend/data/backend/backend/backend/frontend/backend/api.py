"""
ProfitPulse API

Connects financial analysis, anomaly detection,
investigation, simulation and human approval.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from profit_engine import analyze_business
from anomaly_detector import detect_anomalies
from decision_engine import analyze_anomalies
from ai_investigator import investigate_anomalies
from simulation_engine import ProfitSimulator
from approval_engine import ApprovalEngine


app = FastAPI(
    title="ProfitPulse API",
    description="AI Profit Forensics & Decision Agent",
    version="2.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


DATA_FILE = "../data/sample_transactions.csv"

approval_engine = ApprovalEngine()
simulator = ProfitSimulator()


class SimulationRequest(BaseModel):

    target: str
    reduction_percent: float


@app.get("/")
def home():

    return {
        "application": "ProfitPulse",
        "status": "online",
        "version": "2.0"
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


@app.get("/investigate")
def investigate():

    anomalies_found = detect_anomalies(DATA_FILE)

    investigations = investigate_anomalies(
        anomalies_found
    )

    return {
        "status": "completed",
        "count": len(investigations),
        "investigations": investigations
    }


@app.get("/decisions")
def decisions():

    anomalies_found = detect_anomalies(DATA_FILE)

    return {
        "count": len(anomalies_found),
        "decisions": analyze_anomalies(
            anomalies_found
        )
    }


@app.post("/simulate")
def simulate(request: SimulationRequest):

    df = pd.read_csv(DATA_FILE)

    revenue = df["revenue"].sum()

    product_cost = df["product_cost"].sum()

    operating_cost = df["operating_cost"].sum()

    marketing_cost = df["marketing_cost"].sum()

    result = simulator.simulate(

        revenue=revenue,

        product_cost=product_cost,

        operating_cost=operating_cost,

        marketing_cost=marketing_cost,

        target=request.target,

        reduction_percent=request.reduction_percent
    )

    return result


@app.post("/recommendations")
def create_recommendation():

    anomalies_found = detect_anomalies(DATA_FILE)

    investigations = investigate_anomalies(
        anomalies_found
    )

    if not investigations:

        return {
            "message": "No recommendation required."
        }

    investigation = investigations[0]

    recommendation = approval_engine.create_recommendation(

        problem=investigation["anomaly"],

        root_cause=investigation["root_cause"],

        recommendation=investigation[
            "recommended_action"
        ],

        expected_impact="Requires simulation",

        confidence=investigation["confidence"]
    )

    return recommendation


@app.post("/recommendations/{recommendation_id}/approve")
def approve_recommendation(
    recommendation_id: str
):

    return approval_engine.approve(
        recommendation_id
    )


@app.post("/recommendations/{recommendation_id}/reject")
def reject_recommendation(
    recommendation_id: str
):

    return approval_engine.reject(
        recommendation_id
    )


@app.get("/audit")
def audit():

    return {
        "audit_log":
            approval_engine.get_audit_log()
    }
