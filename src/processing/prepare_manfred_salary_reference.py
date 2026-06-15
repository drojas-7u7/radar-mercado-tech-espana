"""Prepare Manfred 2026 tech salary reference data.

This script downloads and processes the public Manfred salary guide:
"Guía Salarial 2026 - Salarios en tecnología [España]".

The resulting dataset is intended only as a complementary tech salary
reference by role and experience range. It must not be interpreted as
observed salaries from job postings and must not be used to impute missing
salaries in job offers.
"""

from __future__ import annotations

import re
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


SOURCE_NAME = "Manfred - Guía Salarial 2026 - Salarios en tecnología [España]"
SOURCE_URL = "https://www.getmanfred.com/blog/guia-salarial-2026-salarios-en-tecnologia-espana-manfred/"
OUTPUT_PATH = Path("data/processed/manfred_salary_reference_processed.csv")

SECTION_HEADINGS = {
    "Salarios Sistema e Infraestructura",
    "Salarios Data",
    "Salarios liderazgo técnico",
    "Salarios Producto",
    "Salarios ciberseguridad",
}


def normalize_role_name(heading: str) -> str:
    """Normalize Manfred heading into a role name."""
    role = heading.strip()
    role = role.removeprefix("Salarios ").strip()
    return role


def find_previous_headings(table) -> list[str]:
    """Find nearby headings before a salary table."""
    previous_headings: list[str] = []
    current = table

    while current:
        current = current.find_previous(["h2", "h3", "h4"])
        if current:
            text = current.get_text(" ", strip=True)
            if text not in previous_headings:
                previous_headings.append(text)
        if len(previous_headings) >= 5:
            break

    return previous_headings


def detect_role_group(previous_headings: list[str]) -> str | None:
    """Detect a broad role group from nearby section headings."""
    for heading in previous_headings:
        if heading in SECTION_HEADINGS:
            return heading.removeprefix("Salarios ").strip()
    return None


def parse_salary_range(salary_text: str) -> dict[str, float | str | bool | None]:
    """Parse salary ranges such as '€20–30K' or '€110-150K + 0.2/1.0%'."""
    original = str(salary_text).strip()

    result: dict[str, float | str | bool | None] = {
        "salary_reference_raw": original,
        "salary_available": True,
        "salary_min_eur_year": None,
        "salary_max_eur_year": None,
        "salary_midpoint_eur_year": None,
        "equity_min_pct": None,
        "equity_max_pct": None,
        "has_equity_component": False,
    }

    if original in {"∅", "", "nan", "None"}:
        result["salary_available"] = False
        return result

    normalized = (
        original.replace("–", "-")
        .replace("—", "-")
        .replace("€", "")
        .replace(" ", "")
        .upper()
    )

    salary_match = re.search(r"(\d+(?:[.,]\d+)?)-(\d+(?:[.,]\d+)?)K", normalized)
    if salary_match:
        salary_min = float(salary_match.group(1).replace(",", ".")) * 1000
        salary_max = float(salary_match.group(2).replace(",", ".")) * 1000

        result["salary_min_eur_year"] = salary_min
        result["salary_max_eur_year"] = salary_max
        result["salary_midpoint_eur_year"] = round((salary_min + salary_max) / 2, 1)

    equity_match = re.search(
        r"\+(\d+(?:[.,]\d+)?)/(\d+(?:[.,]\d+)?)%",
        normalized,
    )
    if equity_match:
        result["has_equity_component"] = True
        result["equity_min_pct"] = float(equity_match.group(1).replace(",", "."))
        result["equity_max_pct"] = float(equity_match.group(2).replace(",", "."))

    return result


def load_page(source_url: str = SOURCE_URL) -> str:
    """Download Manfred salary guide HTML."""
    response = requests.get(source_url, timeout=20)
    response.raise_for_status()
    return response.text


def prepare_manfred_salary_reference(html: str) -> pd.DataFrame:
    """Extract and normalize all salary tables available in the Manfred guide."""
    soup = BeautifulSoup(html, "html.parser")
    html_tables = soup.find_all("table")
    pandas_tables = pd.read_html(StringIO(html))

    if len(html_tables) != len(pandas_tables):
        raise ValueError(
            f"HTML table count ({len(html_tables)}) does not match pandas table count "
            f"({len(pandas_tables)})."
        )

    records = []

    for table_index, (html_table, table_df) in enumerate(
        zip(html_tables, pandas_tables),
        start=1,
    ):
        previous_headings = find_previous_headings(html_table)
        role_heading = previous_headings[0] if previous_headings else f"Table {table_index}"
        role_name = normalize_role_name(role_heading)
        role_group = detect_role_group(previous_headings)

        expected_columns = {"Experiencia", "Salarios"}
        if not expected_columns.issubset(set(table_df.columns)):
            raise ValueError(
                f"Unexpected columns in table {table_index}: {list(table_df.columns)}"
            )

        for row_index, row in table_df.iterrows():
            salary_parts = parse_salary_range(row["Salarios"])

            records.append(
                {
                    "source_name": SOURCE_NAME,
                    "source_url": SOURCE_URL,
                    "reference_year": 2026,
                    "table_index": table_index,
                    "row_index": row_index + 1,
                    "role_name": role_name,
                    "role_heading_raw": role_heading,
                    "role_group": role_group,
                    "previous_headings": " | ".join(previous_headings),
                    "experience_range": str(row["Experiencia"]).strip(),
                    **salary_parts,
                    "methodological_note": (
                        "Complementary tech salary reference by role and experience. "
                        "This is not observed job-posting salary data and must not be "
                        "used to impute missing salaries in job offers."
                    ),
                }
            )

    return pd.DataFrame(records)


def main() -> None:
    """Download, process and save the Manfred salary reference dataset."""
    html = load_page()
    salary_reference_df = prepare_manfred_salary_reference(html)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    salary_reference_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved Manfred salary reference dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(salary_reference_df)}")
    print(f"Columns: {len(salary_reference_df.columns)}")
    print()
    print("Rows by role:")
    print(
        salary_reference_df["role_name"]
        .value_counts()
        .sort_index()
        .to_string()
    )
    print()
    print("Preview:")
    print(
        salary_reference_df[
            [
                "role_name",
                "role_group",
                "experience_range",
                "salary_reference_raw",
                "salary_min_eur_year",
                "salary_max_eur_year",
                "salary_midpoint_eur_year",
                "has_equity_component",
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
