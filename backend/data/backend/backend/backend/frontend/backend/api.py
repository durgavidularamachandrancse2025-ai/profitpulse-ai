"""
ProfitPulse API

Connects financial analysis, anomaly detection,
AI investigation, simulation and human approval.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

from profit_engine import analyze_business
from anomaly_detector import detect_anomalies
from decision_engine import analyze_anomalies
from ai_investigator import investigate_anomalies
from simulation_engine import ProfitSimulator
from approval_engine import ApprovalEngine


# ==========================================
# APPLICATION
# ==========================================

app = FastAPI(
    title="ProfitPulse API",
    description="AI Profit Forensics & Decision Agent",
    version="2.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# DATASET PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "sample_transactions.csv"
)


# ==========================================
# ENGINES
# ==========================================

approval_engine = ApprovalEngine()

simulator = ProfitSimulator()


# ==========================================
# REQUEST MODEL
# ==========================================

class SimulationRequest(BaseModel):

    target: str

    reduction_percent: float


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "application": "ProfitPulse",
        "status": "online",
        "version": "2.0",
        "
