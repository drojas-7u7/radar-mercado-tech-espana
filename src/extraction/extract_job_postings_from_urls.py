from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from extract_sample_job_postings import fetch_job_posting


INPUT_PATH = Path("data/interim/sample_job_urls.csv")
OUTPUT_PATH = Path("data/interim/job_postings_sample.csv")
ERRORS_OUTPUT_PATH = Path("data/interim/job_postings_sample_errors.csv")

REQUEST_DELAY_SECONDS = 1.0


def validate_input_columns(df: pd.DataFrame) -> None:
    """Validate that the input URL dataset contains the required columns."""
    required_columns = {"source", "url"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")


def extract_rows_from_urls(df_urls: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract normalized job posting rows from a URL dataset."""
    extracted_rows = []
    error_rows = []

    with requests.Session() as session:
        for index, row in df_urls.iterrows():
            source = str(row["source"])
            url = str(row["url"])

            print(f"[{index + 1}/{len(df_urls)}] Extracting {source}: {url}")

            try:
                extracted_row = fetch_job_posting(session, source, url)
                extracted_rows.append(extracted_row)
            except (requests.RequestException, ValueError) as error:
                error_rows.append(
                    {
                        "source": source,
                        "url": url,
                        "error_type": type(error).__name__,
                        "error_message": str(error),
                    }
                )
                print(f"  ERROR: {type(error).__name__}: {error}")

            time.sleep(REQUEST_DELAY_SECONDS)

    return extracted_rows, error_rows


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_PATH}. "
            "Run src/extraction/collect_sample_job_urls.py first."
        )

    df_urls = pd.read_csv(INPUT_PATH)
    validate_input_columns(df_urls)

    print(f"Loaded URLs: {len(df_urls)}")
    print()

    extracted_rows, error_rows = extract_rows_from_urls(df_urls)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_output = pd.DataFrame(extracted_rows)
    df_output.to_csv(OUTPUT_PATH, index=False)

    df_errors = pd.DataFrame(error_rows)
    df_errors.to_csv(ERRORS_OUTPUT_PATH, index=False)

    print()
    print(f"Extracted rows: {len(df_output)}")
    print(f"Failed rows: {len(df_errors)}")
    print(f"Saved extracted dataset to: {OUTPUT_PATH}")
    print(f"Saved extraction errors to: {ERRORS_OUTPUT_PATH}")

    if not df_output.empty:
        print()
        print("Extracted sample:")
        print(
            df_output[
                [
                    "source",
                    "title",
                    "company",
                    "location_region",
                    "employment_type",
                    "salary_offer_min",
                    "salary_offer_max",
                    "salary_data_type",
                    "date_posted",
                ]
            ]
        )


if __name__ == "__main__":
    main()
