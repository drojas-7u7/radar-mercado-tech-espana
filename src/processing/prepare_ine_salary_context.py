"""Prepare official INE salary context data.

This script downloads and processes INE table 66245:
"Salarios medios por tipo de jornada, rama de actividad y decil. EPA".

The resulting dataset is intended only as official sector-level salary context.
It must not be interpreted as salary data by tech role and must not be used
to impute missing salaries in job offers.
"""

from pathlib import Path

import pandas as pd


SOURCE_NAME = "INE - Salarios medios por tipo de jornada, rama de actividad y decil. EPA"
SOURCE_URL = "https://www.ine.es/jaxiT3/files/t/csv_bd/66245.csv"
TABLE_ID = "66245"

OUTPUT_PATH = Path("data/processed/ine_salary_context_processed.csv")

RELEVANT_CONTEXT_BRANCHES = {
    "Total",
    "J Información y comunicaciones",
    "M Actividades profesionales, científicas y técnicas",
    "K Actividades financieras y de seguros",
    "D Suministro de energía eléctrica, gas, vapor y aire acondicionado",
}


def parse_spanish_number(series: pd.Series) -> pd.Series:
    """Convert Spanish-formatted numeric strings into floats.

    Examples:
    - "3.131,9" -> 3131.9
    - "2.385,6" -> 2385.6
    - ".." -> NaN
    """
    cleaned = (
        series.astype("string")
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    return pd.to_numeric(cleaned, errors="coerce")


def load_ine_salary_data(source_url: str = SOURCE_URL) -> pd.DataFrame:
    """Load raw salary data from the official INE CSV endpoint."""
    return pd.read_csv(
        source_url,
        sep="\t",
        encoding="utf-8-sig",
        dtype=str,
    )


def prepare_salary_context(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the complete official INE sector-level salary context dataset."""
    required_columns = {
        "Tipo de jornada",
        "Rama de actividad",
        "Decil",
        "Periodo",
        "Total",
    }

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")

    context = df.copy()

    context = context.rename(
        columns={
            "Tipo de jornada": "workday_type",
            "Rama de actividad": "activity_branch",
            "Decil": "decile",
            "Periodo": "year",
            "Total": "salary_monthly_gross_eur_original",
        }
    )

    context["year"] = pd.to_numeric(context["year"], errors="coerce").astype("Int64")
    context["salary_monthly_gross_eur"] = parse_spanish_number(
        context["salary_monthly_gross_eur_original"]
    )

    latest_year = int(context["year"].max())

    context["is_latest_year"] = context["year"] == latest_year
    context["is_total_workday_type"] = context["workday_type"] == "Total"
    context["is_total_decile"] = context["decile"] == "Total"
    context["is_relevant_context_branch"] = context["activity_branch"].isin(
        RELEVANT_CONTEXT_BRANCHES
    )

    national_reference = context[
        context["activity_branch"] == "Total"
    ][
        ["year", "workday_type", "decile", "salary_monthly_gross_eur"]
    ].rename(
        columns={
            "salary_monthly_gross_eur": "national_reference_salary_monthly_gross_eur"
        }
    )

    context = context.merge(
        national_reference,
        on=["year", "workday_type", "decile"],
        how="left",
    )

    context["difference_vs_national_reference_eur"] = (
        context["salary_monthly_gross_eur"]
        - context["national_reference_salary_monthly_gross_eur"]
    ).round(1)

    context["difference_vs_national_reference_pct"] = (
        (
            context["salary_monthly_gross_eur"]
            / context["national_reference_salary_monthly_gross_eur"]
            - 1
        )
        * 100
    ).round(1)

    context["source_name"] = SOURCE_NAME
    context["source_url"] = SOURCE_URL
    context["table_id"] = TABLE_ID
    context["methodological_note"] = (
        "Official INE sector-level salary context by activity branch, year, "
        "workday type and decile. This is not salary data by tech role and "
        "must not be used to impute missing salaries in job offers."
    )

    output_columns = [
        "source_name",
        "source_url",
        "table_id",
        "year",
        "workday_type",
        "activity_branch",
        "decile",
        "salary_monthly_gross_eur_original",
        "salary_monthly_gross_eur",
        "national_reference_salary_monthly_gross_eur",
        "difference_vs_national_reference_eur",
        "difference_vs_national_reference_pct",
        "is_latest_year",
        "is_total_workday_type",
        "is_total_decile",
        "is_relevant_context_branch",
        "methodological_note",
    ]

    return (
        context[output_columns]
        .sort_values(
            ["year", "workday_type", "decile", "activity_branch"],
            ascending=[False, True, True, True],
        )
        .reset_index(drop=True)
    )


def main() -> None:
    """Download, process and save the INE salary context dataset."""
    raw_df = load_ine_salary_data()
    context_df = prepare_salary_context(raw_df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    context_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved INE salary context dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(context_df)}")
    print(f"Columns: {len(context_df.columns)}")
    print()
    print("Latest year summary for total workday and total decile:")
    latest_summary = context_df[
        (context_df["is_latest_year"])
        & (context_df["is_total_workday_type"])
        & (context_df["is_total_decile"])
        & (context_df["is_relevant_context_branch"])
    ][
        [
            "year",
            "activity_branch",
            "salary_monthly_gross_eur",
            "difference_vs_national_reference_pct",
        ]
    ].sort_values("salary_monthly_gross_eur", ascending=False)

    print(latest_summary.to_string(index=False))


if __name__ == "__main__":
    main()
