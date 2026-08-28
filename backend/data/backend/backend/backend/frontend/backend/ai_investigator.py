"""
ProfitPulse - AI Investigation Engine

Turns financial anomalies into evidence-backed
root-cause investigations.
"""

from datetime import datetime


class ProfitInvestigator:

    def __init__(self):
        self.name = "ProfitPulse Investigator"

    def investigate(self, anomaly):

        anomaly_type = anomaly.get("type")
        profit_change = anomaly.get("profit_change", 0)
        revenue_change = anomaly.get("revenue_change", 0)
        cost_change = anomaly.get("cost_change", 0)

        evidence = []

        # Evidence 1: Revenue
        if revenue_change < -10:

            evidence.append({
                "metric": "Revenue",
                "change": f"{revenue_change}%",
                "signal": "NEGATIVE",
                "explanation":
                    "Revenue decreased significantly."
            })

        # Evidence 2: Costs
        if cost_change > 10:

            evidence.append({
                "metric": "Total Cost",
                "change": f"+{cost_change}%",
                "signal": "NEGATIVE",
                "explanation":
                    "Total costs increased significantly."
            })

        # Root cause
        if revenue_change < -10 and cost_change > 10:

            root_cause = (
                "Profit deterioration is driven by a "
                "combination of falling revenue and "
                "rising costs."
            )

            confidence = 0.92

        elif cost_change > 10:

            root_cause = (
                "The strongest observed contributor is "
                "an abnormal increase in total costs."
            )

            confidence = 0.86

        elif revenue_change < -10:

            root_cause = (
                "The strongest observed contributor is "
                "a significant decline in revenue."
            )

            confidence = 0.84

        else:

            root_cause = (
                "A significant profit change was detected, "
                "but the available evidence does not identify "
                "a single dominant driver."
            )

            confidence = 0.65

        # Recommendation
        if cost_change > 10:

            recommendation = (
                "Audit operating and marketing expenses, "
                "identify abnormal spending, and reduce "
                "avoidable costs."
            )

        elif revenue_change < -10:

            recommendation = (
                "Investigate product-level demand, "
                "pricing and customer conversion."
            )

        else:

            recommendation = (
                "Continue monitoring the affected financial "
                "metrics and collect additional evidence."
            )

        return {

            "investigation_id":
                f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",

            "anomaly": anomaly_type,

            "root_cause": root_cause,

            "confidence":
                round(confidence * 100, 1),

            "evidence": evidence,

            "recommended_action":
                recommendation,

            "status":
                "READY_FOR_REVIEW"
        }


def investigate_anomalies(anomalies):

    investigator = ProfitInvestigator()

    results = []

    for anomaly in anomalies:

        results.append(
            investigator.investigate(anomaly)
        )

    return results


if __name__ == "__main__":

    sample = {

        "type": "PROFIT_SHOCK",

        "profit_change": -62.5,

        "revenue_change": -61.9,

        "cost_change": 38.5

    }

    investigator = ProfitInvestigator()

    result = investigator.investigate(sample)

    print("\n=== PROFITPULSE INVESTIGATION ===")

    print("\nRoot Cause:")
    print(result["root_cause"])

    print(
        f"\nConfidence: "
        f"{result['confidence']}%"
    )

    print("\nEvidence:")

    for item in result["evidence"]:

        print(
            f"- {item['metric']}: "
            f"{item['change']}"
        )

    print("\nRecommended Action:")
    print(result["recommended_action"])
