"""
ProfitPulse - Human Approval & Audit Engine

Ensures AI recommendations require human approval
before being considered actionable.
"""

from datetime import datetime
import uuid


class ApprovalEngine:

    def __init__(self):
        self.audit_log = []


    def create_recommendation(
        self,
        problem,
        root_cause,
        recommendation,
        expected_impact,
        confidence
    ):

        recommendation_id = (
            "REC-" + str(uuid.uuid4())[:8].upper()
        )

        record = {
            "recommendation_id": recommendation_id,
            "created_at": datetime.now().isoformat(),
            "problem": problem,
            "root_cause": root_cause,
            "recommendation": recommendation,
            "expected_impact": expected_impact,
            "confidence": confidence,
            "status": "PENDING_APPROVAL"
        }

        self.audit_log.append(record)

        return record


    def approve(self, recommendation_id):

        for record in self.audit_log:

            if record["recommendation_id"] == recommendation_id:

                record["status"] = "APPROVED"

                record["approved_at"] = (
                    datetime.now().isoformat()
                )

                return record

        return {
            "error": "Recommendation not found."
        }


    def reject(
        self,
        recommendation_id,
        reason="No reason provided"
    ):

        for record in self.audit_log:

            if record["recommendation_id"] == recommendation_id:

                record["status"] = "REJECTED"

                record["rejection_reason"] = reason

                record["rejected_at"] = (
                    datetime.now().isoformat()
                )

                return record

        return {
            "error": "Recommendation not found."
        }


    def get_audit_log(self):

        return self.audit_log


if __name__ == "__main__":

    engine = ApprovalEngine()

    recommendation = engine.create_recommendation(

        problem="Profit Shock",

        root_cause=(
            "Revenue decreased while "
            "operating costs increased."
        ),

        recommendation=(
            "Reduce avoidable operating "
            "expenses by 10%."
        ),

        expected_impact="+₹13,000 projected profit",

        confidence=92
    )

    print("\n=== PROFITPULSE RECOMMENDATION ===")

    print(
        f"ID: "
        f"{recommendation['recommendation_id']}"
    )

    print(
        f"Status: "
        f"{recommendation['status']}"
    )

    print(
        f"Recommendation: "
        f"{recommendation['recommendation']}"
    )

    print(
        f"Expected Impact: "
        f"{recommendation['expected_impact']}"
    )

    print("\nApproving recommendation...")

    approved = engine.approve(
        recommendation["recommendation_id"]
    )

    print(
        f"Final Status: "
        f"{approved['status']}"
    )
