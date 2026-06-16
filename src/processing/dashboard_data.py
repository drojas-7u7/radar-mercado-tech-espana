from __future__ import annotations

import pandas as pd


def load_job_postings_data(path: str) -> pd.DataFrame:
    """Load and prepare the processed job postings dataset."""
    df = pd.read_csv(path)

    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["technologies_detected"] = df["technologies_detected"].fillna("")

    return df


def load_ine_salary_context_data(path: str) -> pd.DataFrame:
    """Load and prepare INE sector-level salary context data."""
    df = pd.read_csv(path)

    numeric_columns = [
        "year",
        "salary_monthly_gross_eur",
        "national_reference_salary_monthly_gross_eur",
        "difference_vs_national_reference_eur",
        "difference_vs_national_reference_pct",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    boolean_columns = [
        "is_latest_year",
        "is_total_workday_type",
        "is_total_decile",
        "is_relevant_context_branch",
    ]

    for column in boolean_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.lower()
                .map({"true": True, "false": False})
            )

    return df


def load_manfred_salary_reference_data(path: str) -> pd.DataFrame:
    """Load and prepare Manfred tech salary reference data."""
    df = pd.read_csv(path)

    numeric_columns = [
        "reference_year",
        "table_index",
        "row_index",
        "salary_min_eur_year",
        "salary_max_eur_year",
        "salary_midpoint_eur_year",
        "equity_min_pct",
        "equity_max_pct",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "salary_available" in df.columns:
        df["salary_available"] = (
            df["salary_available"]
            .astype(str)
            .str.lower()
            .map({"true": True, "false": False})
        )

    if "has_equity_component" in df.columns:
        df["has_equity_component"] = (
            df["has_equity_component"]
            .astype(str)
            .str.lower()
            .map({"true": True, "false": False})
        )

    return df


def apply_dashboard_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply dashboard filters to the job postings dataset."""
    filtered = df.copy()

    filtered = filtered[
        filtered["source"].isin(filters["sources"])
        & filtered["role_category"].isin(filters["roles"])
        & filtered["work_mode"].isin(filters["work_modes"])
        & filtered["seniority"].isin(filters["seniorities"])
    ]

    date_range = filters["date_range"]

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["date_posted"].dt.date >= start_date)
            & (filtered["date_posted"].dt.date <= end_date)
        ]

    return filtered
