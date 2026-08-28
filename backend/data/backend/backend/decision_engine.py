"""
ProfitPulse - AI Decision Engine

Converts financial anomalies into explanations
and actionable business recommendations.
"""


def generate_decision(anomaly):
    anomaly_type = anomaly["type"]

    profit_change = anomaly["profit_change"]
    revenue_change = anomaly["revenue_change"]
    cost_change = anomaly["cost_change"]

    # Profit shock
    if anomaly_type == "PROFIT_SHOCK":

        if revenue_change < -10 and cost_change > 10:
            reason = (
                "Revenue decreased while total costs increased."
            )

            action = (
                "Investigate falling sales and immediately "
                "review operating and marketing expenses."
            )

        elif cost_change > 10:
            reason = (
                "The major signal is an unusual increase in costs."
            )

            action = (
                "Audit operating and marketing expenses and "
                "identify unnecessary spending."
            )

        elif revenue_change < -10:
            reason = (
                "The major signal is a significant revenue decline."
            )

            action = (
                "Investigate product sales, pricing and customer "
                "demand before increasing expenditure."
            )

        else:
            reason = (
                "Profit declined significantly compared with "
                "the previous period."
            )

            action = (
                "Review both revenue and cost drivers to locate "
                "the source of the decline."
            )

        return {
            "severity": "HIGH",
            "reason": reason,
            "action": action
        }

    # Cost spike
    if anomaly_type == "COST_SPIKE":

        return {
            "severity": "MEDIUM",
            "reason": (
                f"Total cost increased by {cost_change}% "
                "compared with the previous period."
            ),
            "action": (
                "Audit major expense categories and identify "
                "avoidable or abnormal spending."
            )
        }

    # Revenue drop
    if anomaly_type == "REVENUE_DROP":

        return {
            "severity": "MEDIUM",
            "reason": (
                f"Revenue decreased by {abs(revenue_change)}% "
                "compared with the previous period."
            ),
            "action": (
                "Review product-level sales and investigate "
                "pricing, demand and customer conversion."
            )
        }

    return {
        "severity": "LOW",
        "reason": "No major financial issue detected.",
        "action": "Continue monitoring financial trends."
    }


def analyze_anomalies(anomalies):

    decisions = []

    for anomaly in anomalies:

        decision = generate_decision(anomaly)

        decisions.append({
            "date": anomaly["date"],
            "type": anomaly["type"],
            "severity": decision["severity"],
            "reason": decision["reason"],
            "recommended_action": decision["action"]
        })

    return decisions


if __name__ == "__main__":

    sample_anomaly = {
        "date": "2026-01-15",
        "type": "PROFIT_SHOCK",
        "profit_change": -62.5,
        "revenue_change": -61.9,
        "cost_change": 38.5,
        "severity": "HIGH"
    }

    decision = generate_decision(sample_anomaly)

    print("=== ProfitPulse Decision ===")
    print(f"Date: {sample_anomaly['date']}")
    print(f"Severity: {decision['severity']}")
    print(f"Why: {decision['reason']}")
    print(f"Action: {decision['action']}")
