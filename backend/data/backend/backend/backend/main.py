"""
ProfitPulse - Main Application Pipeline
"""

from profit_engine import analyze_business
from anomaly_detector import detect_anomalies
from decision_engine import analyze_anomalies
import pandas as pd


def run_profitpulse():

    file_path = "../data/sample_transactions.csv"

    df = pd.read_csv(file_path)

    # -----------------------------
    # Overall financial analysis
    # -----------------------------

    total_revenue = df["revenue"].sum()

    total_product_cost = df["product_cost"].sum()

    total_operating_cost = df["operating_cost"].sum()

    total_marketing_cost = df["marketing_cost"].sum()

    financial_data = {
        "revenue": total_revenue,
        "product_cost": total_product_cost,
        "operating_cost": total_operating_cost,
        "marketing_cost": total_marketing_cost
    }

    profit_analysis = analyze_business(financial_data)

    # -----------------------------
    # Detect anomalies
    # -----------------------------

    anomalies = detect_anomalies(file_path)

    # -----------------------------
    # Generate decisions
    # -----------------------------

    decisions = analyze_anomalies(anomalies)

    # -----------------------------
    # Final ProfitPulse output
    # -----------------------------

    print("\n================================")
    print("        PROFITPULSE")
    print(" AI PROFIT FORENSICS ENGINE")
    print("================================")

    print("\nFINANCIAL SUMMARY")
    print("------------------")

    print(f"Revenue: ₹{profit_analysis['revenue']:,.2f}")
    print(f"Total Cost: ₹{profit_analysis['total_cost']:,.2f}")
    print(f"Profit: ₹{profit_analysis['profit']:,.2f}")
    print(f"Profit Margin: {profit_analysis['profit_margin']}%")

    print("\nPROFIT DRIVERS")
    print("------------------")

    for driver in profit_analysis["profit_drivers"]:

        print(
            f"{driver['factor']} → "
            f"{driver['impact']}% "
            f"[{driver['severity']}]"
        )

    print("\nANOMALIES DETECTED")
    print("------------------")

    if not anomalies:

        print("No major anomalies detected.")

    else:

        for anomaly in anomalies:

            print(
                f"{anomaly['date']} → "
                f"{anomaly['type']} → "
                f"{anomaly['severity']}"
            )

    print("\nAI DECISIONS")
    print("------------------")

    if not decisions:

        print("No immediate action required.")

    else:

        for decision in decisions:

            print(f"\nDate: {decision['date']}")
            print(f"Problem: {decision['type']}")
            print(f"Severity: {decision['severity']}")
            print(f"Why: {decision['reason']}")
            print(
                f"Action: "
                f"{decision['recommended_action']}"
            )


if __name__ == "__main__":
    run_profitpulse()
