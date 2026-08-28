"""
ProfitPulse - Counterfactual Simulation Engine

Simulates financial decisions before they are implemented.
"""


class ProfitSimulator:

    def calculate_profit(
        self,
        revenue,
        product_cost,
        operating_cost,
        marketing_cost
    ):
        total_cost = (
            product_cost
            + operating_cost
            + marketing_cost
        )

        profit = revenue - total_cost

        margin = (
            profit / revenue * 100
            if revenue > 0
            else 0
        )

        return {
            "revenue": round(revenue, 2),
            "total_cost": round(total_cost, 2),
            "profit": round(profit, 2),
            "margin": round(margin, 2)
        }


    def simulate(
        self,
        revenue,
        product_cost,
        operating_cost,
        marketing_cost,
        target,
        reduction_percent
    ):

        current = self.calculate_profit(
            revenue,
            product_cost,
            operating_cost,
            marketing_cost
        )

        reduction = reduction_percent / 100

        new_product_cost = product_cost
        new_operating_cost = operating_cost
        new_marketing_cost = marketing_cost

        if target == "product_cost":

            new_product_cost = (
                product_cost * (1 - reduction)
            )

        elif target == "operating_cost":

            new_operating_cost = (
                operating_cost * (1 - reduction)
            )

        elif target == "marketing_cost":

            new_marketing_cost = (
                marketing_cost * (1 - reduction)
            )

        else:

            return {
                "error":
                    "Invalid target. Use product_cost, "
                    "operating_cost or marketing_cost."
            }

        projected = self.calculate_profit(
            revenue,
            new_product_cost,
            new_operating_cost,
            new_marketing_cost
        )

        profit_improvement = (
            projected["profit"]
            - current["profit"]
        )

        margin_improvement = (
            projected["margin"]
            - current["margin"]
        )

        return {

            "scenario": {
                "target": target,
                "reduction_percent":
                    reduction_percent
            },

            "current": current,

            "projected": projected,

            "impact": {
                "additional_profit":
                    round(profit_improvement, 2),

                "margin_improvement":
                    round(margin_improvement, 2)
            }
        }


if __name__ == "__main__":

    simulator = ProfitSimulator()

    result = simulator.simulate(
        revenue=100000,
        product_cost=40000,
        operating_cost=20000,
        marketing_cost=10000,
        target="operating_cost",
        reduction_percent=10
    )

    print("\n=== PROFITPULSE COUNTERFACTUAL ===")

    print("\nCurrent Profit:")
    print(
        f"₹{result['current']['profit']:,.2f}"
    )

    print("\nProjected Profit:")
    print(
        f"₹{result['projected']['profit']:,.2f}"
    )

    print("\nAdditional Profit:")
    print(
        f"₹{result['impact']['additional_profit']:,.2f}"
    )

    print("\nMargin Improvement:")
    print(
        f"{result['impact']['margin_improvement']:.2f}%"
    )
