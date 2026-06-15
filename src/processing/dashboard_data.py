from __future__ import annotations

import pandas as pd


def load_job_postings_data(path: str) -> pd.DataFrame:
    """Load and prepare the processed job postings dataset."""
    df = pd.read_csv(path)

    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["technologies_detected"] = df["technologies_detected"].fillna("")

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
