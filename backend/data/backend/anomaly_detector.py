"""
ProfitPulse - Financial Anomaly Detector

Detects unusual changes in revenue, costs and profit.
"""

import pandas as pd


def detect_anomalies(file_path):
    df = pd.read_csv(file_path)

    df["total_cost"] = (
        df["product_cost"]
        + df["operating_cost"]
        + df["marketing_cost"]
    )

    df["profit"] = df["revenue"] - df["total_cost"]

    anomalies = []

    for i in range(1, len(df)):
        previous_profit = df.loc[i - 1, "profit"]
        current_profit = df.loc[i, "profit"]

        if previous_profit != 0:
            profit_change = (
                (current_profit - previous_profit)
                / abs(previous_profit)
            ) * 100
        else:
            profit_change = 0

        revenue_change = (
            (df.loc[i, "revenue"] - df.loc[i - 1, "revenue"])
            / max(abs(df.loc[i - 1, "revenue"]), 1)
        ) * 100

        cost_change = (
            (df.loc[i, "total_cost"] - df.loc[i - 1, "total_cost"])
            / max(abs(df.loc[i - 1, "total_cost"]), 1)
        ) * 100

        # Profit shock
        if profit_change <= -30:
            anomalies.append({
                "date": df.loc[i, "date"],
                "type": "PROFIT_SHOCK",
                "profit_change": round(profit_change, 2),
                "revenue_change": round(revenue_change, 2),
                "cost_change": round(cost_change, 2),
                "severity": "HIGH"
            })

        # Cost spike
        elif cost_change >= 25:
            anomalies.append({
                "date": df.loc[i, "date"],
                "type": "COST_SPIKE",
                "profit_change": round(profit_change, 2),
                "revenue_change": round(revenue_change, 2),
                "cost_change": round(cost_change, 2),
                "severity": "MEDIUM"
            })

        # Revenue drop
        elif revenue_change <= -25:
            anomalies.append({
                "date": df.loc[i, "date"],
                "type": "REVENUE_DROP",
                "profit_change": round(profit_change, 2),
                "revenue_change": round(revenue_change, 2),
                "cost_change": round(cost_change, 2),
                "severity": "MEDIUM"
            })

    return anomalies


if __name__ == "__main__":

    file_path = "../data/sample_transactions.csv"

    results = detect_anomalies(file_path)

    print("=== ProfitPulse Anomaly Report ===")

    if not results:
        print("No significant anomalies detected.")

    for anomaly in results:
        print("\nAnomaly detected:")
        print(f"Date: {anomaly['date']}")
        print(f"Type: {anomaly['type']}")
        print(f"Severity: {anomaly['severity']}")
        print(f"Profit change: {anomaly['profit_change']}%")
        print(f"Revenue change: {anomaly['revenue_change']}%")
        print(f"Cost change: {anomaly['cost_change']}%")
