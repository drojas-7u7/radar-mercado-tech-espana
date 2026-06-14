from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; radar-mercado-tech-espana/0.1; educational project)"
    )
}

SAMPLE_URLS = {
    "Tecnoempleo": "https://www.tecnoempleo.com/senior-data-engineer-ust/tableau-python/rf-065a1b7b922f93526b42",
    "Ticjob": "https://ticjob.es/esp/trabajo/java-developer-microservicios-ingles-alto-remoto/70577",
}

OUTPUT_PATH = Path("data/interim/sample_job_postings.csv")


def clean_text(value: Any) -> str:
    """Clean HTML entities and repeated whitespace from a text value."""
    if value is None:
        return ""

    text = html.unescape(str(value))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_json_ld(raw_text: str) -> dict[str, Any]:
    """Parse JSON-LD using a tolerant JSON decoder."""
    decoder = json.JSONDecoder(strict=False)
    return decoder.decode(raw_text)


def find_job_posting_json_ld(soup: BeautifulSoup) -> dict[str, Any] | None:
    """Find the first JSON-LD block with @type JobPosting."""
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})

    for script in scripts:
        raw_text = script.get_text(strip=True)

        try:
            data = parse_json_ld(raw_text)
        except json.JSONDecodeError:
            continue

        items = data if isinstance(data, list) else [data]

        for item in items:
            if isinstance(item, dict) and item.get("@type") == "JobPosting":
                return item

    return None


def parse_salary_number(value: str) -> int:
    """Convert salary text like 34.000 into integer 34000."""
    return int(value.replace(".", "").replace(",", "").strip())


def extract_salary_from_description(description: str) -> tuple[int | None, int | None, float | None, str]:
    """Extract explicit salary ranges from the job description when available."""
    patterns = [
        r"salario:\s*(\d{1,3}(?:\.\d{3})*)\s*(?:EUR|€)\s*-\s*(\d{1,3}(?:\.\d{3})*)\s*(?:EUR|€)",
        r"(\d{1,3}(?:\.\d{3})*)\s*(?:EUR|€)\s*-\s*(\d{1,3}(?:\.\d{3})*)\s*(?:EUR|€)",
        r"(\d{1,3}(?:\.\d{3})*)\s*-\s*(\d{1,3}(?:\.\d{3})*)\s*(?:EUR|€)",
    ]

    for pattern in patterns:
        match = re.search(pattern, description, flags=re.IGNORECASE)

        if match:
            salary_min = parse_salary_number(match.group(1))
            salary_max = parse_salary_number(match.group(2))
            salary_avg = round((salary_min + salary_max) / 2, 2)
            return salary_min, salary_max, salary_avg, "published_in_offer"

    return None, None, None, "unavailable"


def extract_company(data: dict[str, Any]) -> str:
    """Extract company name from hiringOrganization."""
    organization = data.get("hiringOrganization")

    if isinstance(organization, dict):
        return clean_text(organization.get("name"))

    return clean_text(organization)


def extract_location_fields(data: dict[str, Any]) -> dict[str, str]:
    """Extract normalized location fields from jobLocation."""
    location = data.get("jobLocation")

    if isinstance(location, list) and location:
        location = location[0]

    if not isinstance(location, dict):
        return {
            "location_locality": "",
            "location_region": "",
            "location_country": "",
        }

    address = location.get("address", {})

    if not isinstance(address, dict):
        return {
            "location_locality": "",
            "location_region": "",
            "location_country": "",
        }

    return {
        "location_locality": clean_text(address.get("addressLocality")),
        "location_region": clean_text(address.get("addressRegion")),
        "location_country": clean_text(address.get("addressCountry")),
    }


def normalize_job_posting(source: str, url: str, data: dict[str, Any]) -> dict[str, Any]:
    """Convert one JobPosting JSON-LD object into a normalized row."""
    description = clean_text(data.get("description"))
    salary_min, salary_max, salary_avg, salary_data_type = extract_salary_from_description(description)
    location_fields = extract_location_fields(data)

    return {
        "source": source,
        "url": url,
        "title": clean_text(data.get("title")),
        "company": extract_company(data),
        "date_posted": clean_text(data.get("datePosted")),
        "valid_through": clean_text(data.get("validThrough")),
        "employment_type": clean_text(data.get("employmentType")),
        "salary_offer_min": salary_min,
        "salary_offer_max": salary_max,
        "salary_offer_avg": salary_avg,
        "salary_data_type": salary_data_type,
        "description_length": len(description),
        "description": description,
        **location_fields,
    }


def fetch_job_posting(session: requests.Session, source: str, url: str) -> dict[str, Any]:
    """Fetch and normalize one job posting URL."""
    response = session.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    job_posting = find_job_posting_json_ld(soup)

    if job_posting is None:
        raise ValueError(f"No JobPosting JSON-LD found for {url}")

    return normalize_job_posting(source, url, job_posting)


def main() -> None:
    rows = []

    with requests.Session() as session:
        for source, url in SAMPLE_URLS.items():
            print(f"Extracting sample job from {source}...")
            row = fetch_job_posting(session, source, url)
            rows.append(row)

    df = pd.DataFrame(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print()
    print("Extracted rows:")
    print(
        df[
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

    print()
    print(f"Saved sample dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
