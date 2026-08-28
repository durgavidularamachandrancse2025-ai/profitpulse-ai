"""
ProfitPulse - Financial Analysis Engine
Stage 1

This engine calculates the financial health of a merchant
using transaction-level data.
"""

import pandas as pd


def load_transactions(file_path):
    """Load transaction data."""
    df = pd.read_csv(file_path)

    required_columns = [
        "date",
        "net_revenue",
        "profit",
        "payment_fee",
        "discount",
        "refund_amount",
        "refunded",
        "product"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df["date"] = pd.to_datetime(df["date"])

    return df


def calculate_summary(df):
    """Calculate overall financial metrics."""

    revenue = df["net_revenue"].sum()
    profit = df["profit"].sum()
    refunds = df["refund_amount"].sum()
    fees = df["payment_fee"].sum()
    discounts = df["discount"].sum()

    orders = len(df)

    margin = 0

    if revenue > 0:
        margin = (profit / revenue) * 100

    return {
        "orders": orders,
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "profit_margin": round(margin, 2),
        "refunds": round(refunds, 2),
        "payment_fees": round(fees, 2),
        "discounts": round(discounts, 2)
    }


def analyze_products(df):
    """Find products affecting profitability."""

    result = (
        df.groupby("product")
        .agg(
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
            refunds=("refund_amount", "sum"),
            orders=("transaction_id", "count")
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["profit"] /
        result["revenue"].replace(0, 1) *
        100
    )

    return result.sort_values("profit")


def detect_profit_risk(df):
    """
    Detect simple financial warning signals.

    These rules form the foundation for the
    future AI investigation agent.
    """

    warnings = []

    total_revenue = df["net_revenue"].sum()

    if total_revenue == 0:
        return ["No revenue detected."]

    refund_rate = (
        df["refunded"].sum() /
        len(df)
    ) * 100

    fee_rate = (
        df["payment_fee"].sum() /
        total_revenue
    ) * 100

    discount_rate = (
        df["discount"].sum() /
        total_revenue
    ) * 100

    profit_margin = (
        df["profit"].sum() /
        total_revenue
    ) * 100

    if refund_rate > 5:
        warnings.append(
            f"High refund rate detected: {refund_rate:.2f}%"
        )

    if fee_rate > 1.5:
        warnings.append(
            f"High payment fee rate detected: {fee_rate:.2f}%"
        )

    if discount_rate > 10:
        warnings.append(
            f"High discount pressure detected: {discount_rate:.2f}%"
        )

    if profit_margin < 15:
        warnings.append(
            f"Low profit margin detected: {profit_margin:.2f}%"
        )

    if not warnings:
        warnings.append(
            "No major profitability risks detected."
        )

    return warnings


def generate_fin
