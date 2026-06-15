from __future__ import annotations

from dataclasses import dataclass
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

RAW_DIR = Path("data/raw")
INTERIM_DIR = Path("data/interim")
COMBINED_OUTPUT_PATH = INTERIM_DIR / "job_urls.csv"


PRIORITY_KEYWORDS = [
    "data",
    "python",
    "sql",
    "java",
    "developer",
    "engineer",
    "analyst",
    "remoto",
    "remote",
    "hibrido",
    "hybrid",
]


@dataclass(frozen=True)
class SourceConfig:
    name: str
    slug: str
    sitemap_url: str
    job_url_marker: str


SOURCES = [
    SourceConfig(
        name="Tecnoempleo",
        slug="tecnoempleo",
        sitemap_url="https://www.tecnoempleo.com/sitemap.xml",
        job_url_marker="rf-",
    ),
    SourceConfig(
        name="Ticjob",
        slug="ticjob",
        sitemap_url="https://www.ticjob.es/esp/sitemap.xml",
        job_url_marker="/esp/trabajo/",
    ),
]


def fetch_sitemap_urls(session: requests.Session, sitemap_url: str) -> list[str]:
    """Fetch URLs from a sitemap."""
    response = session.get(sitemap_url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")
    return [loc.get_text(strip=True) for loc in soup.find_all("loc")]


def is_likely_job_url(url: str, source: SourceConfig) -> bool:
    """Check whether a URL looks like an individual job posting."""
    return source.job_url_marker in url.lower()


def get_matched_keywords(url: str) -> list[str]:
    """Detect priority keywords contained in the URL."""
    lower_url = url.lower()
    return [keyword for keyword in PRIORITY_KEYWORDS if keyword in lower_url]


def build_candidate_rows(source: SourceConfig, urls: list[str]) -> list[dict[str, Any]]:
    """Build all candidate job URL rows from sitemap URLs."""
    rows = []

    for position, url in enumerate(urls, start=1):
        if not is_likely_job_url(url, source):
            continue

        matched_keywords = get_matched_keywords(url)

        rows.append(
            {
                "source": source.name,
                "source_slug": source.slug,
                "url": url,
                "sitemap_url": source.sitemap_url,
                "sitemap_position": position,
                "matched_keywords": ", ".join(matched_keywords),
                "keyword_score": len(matched_keywords),
            }
        )

    return rows


def save_source_raw_urls(source: SourceConfig, rows: list[dict[str, Any]]) -> Path:
    """Save raw candidate URL inventory for one source."""
    output_path = RAW_DIR / f"{source.slug}_candidate_urls.csv"

    df_source = pd.DataFrame(rows)
    df_source.to_csv(output_path, index=False)

    return output_path


def main() -> None:
    all_candidate_rows = []

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    with requests.Session() as session:
        for source in SOURCES:
            print("=" * 80)
            print(f"Source: {source.name}")
            print(f"Sitemap: {source.sitemap_url}")

            urls = fetch_sitemap_urls(session, source.sitemap_url)
            candidate_rows = build_candidate_rows(source, urls)

            raw_output_path = save_source_raw_urls(source, candidate_rows)

            print(f"Total sitemap URLs: {len(urls)}")
            print(f"Likely job URLs: {len(candidate_rows)}")
            print(f"Saved raw candidate URLs to: {raw_output_path}")

            all_candidate_rows.extend(candidate_rows)

    df_combined = pd.DataFrame(all_candidate_rows)

    if not df_combined.empty:
        df_combined = df_combined.sort_values(
            by=["source", "keyword_score", "sitemap_position"],
            ascending=[True, False, True],
        )

    df_combined.to_csv(COMBINED_OUTPUT_PATH, index=False)

    print()
    print(f"Total candidate job URLs: {len(df_combined)}")
    print(f"Saved combined candidate URLs to: {COMBINED_OUTPUT_PATH}")

    if not df_combined.empty:
        print()
        print("Candidate URLs by source:")
        print(df_combined["source"].value_counts())
        print()
        print("Preview:")
        print(df_combined[["source", "url", "matched_keywords", "keyword_score"]].head(20))


if __name__ == "__main__":
    main()
