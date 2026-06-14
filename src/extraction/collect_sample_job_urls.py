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

OUTPUT_PATH = Path("data/interim/sample_job_urls.csv")

MAX_URLS_PER_SOURCE = 10

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
    sitemap_url: str
    job_url_marker: str


SOURCES = [
    SourceConfig(
        name="Tecnoempleo",
        sitemap_url="https://www.tecnoempleo.com/sitemap.xml",
        job_url_marker="rf-",
    ),
    SourceConfig(
        name="Ticjob",
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
    """Build candidate job URL rows from sitemap URLs."""
    rows = []

    for position, url in enumerate(urls, start=1):
        if not is_likely_job_url(url, source):
            continue

        matched_keywords = get_matched_keywords(url)

        rows.append(
            {
                "source": source.name,
                "url": url,
                "sitemap_url": source.sitemap_url,
                "sitemap_position": position,
                "matched_keywords": ", ".join(matched_keywords),
                "keyword_score": len(matched_keywords),
            }
        )

    return rows


def select_sample(rows: list[dict[str, Any]], max_urls: int) -> list[dict[str, Any]]:
    """Select a reproducible sample prioritizing relevant keyword matches."""
    sorted_rows = sorted(
        rows,
        key=lambda row: (-row["keyword_score"], row["sitemap_position"]),
    )

    return sorted_rows[:max_urls]


def main() -> None:
    selected_rows = []

    with requests.Session() as session:
        for source in SOURCES:
            print("=" * 80)
            print(f"Source: {source.name}")
            print(f"Sitemap: {source.sitemap_url}")

            urls = fetch_sitemap_urls(session, source.sitemap_url)
            candidate_rows = build_candidate_rows(source, urls)
            sample_rows = select_sample(candidate_rows, MAX_URLS_PER_SOURCE)

            print(f"Total sitemap URLs: {len(urls)}")
            print(f"Likely job URLs: {len(candidate_rows)}")
            print(f"Selected sample URLs: {len(sample_rows)}")

            selected_rows.extend(sample_rows)

    df = pd.DataFrame(selected_rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print()
    print(f"Saved sample job URLs to: {OUTPUT_PATH}")
    print()
    print(df[["source", "url", "matched_keywords", "keyword_score"]])


if __name__ == "__main__":
    main()
