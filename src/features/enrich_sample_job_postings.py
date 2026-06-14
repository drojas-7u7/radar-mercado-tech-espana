from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/interim/job_postings_sample.csv")
OUTPUT_PATH = Path("data/processed/job_postings_sample_enriched.csv")
MIN_DATE_POSTED = "2026-01-01"


TECHNOLOGY_KEYWORDS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "Java": ["java"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Microservices": ["microservicios", "microservices"],
    "Spring": ["spring"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Spark": ["spark"],
    "Pandas": ["pandas"],
    "Machine Learning": ["machine learning", "ml"],
    "ETL": ["etl"],
}


def normalize_text(value: object) -> str:
    """Normalize text for rule-based detection."""
    if value is None or pd.isna(value):
        return ""

    text = str(value).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_search_text(row: pd.Series) -> str:
    """Combine relevant text fields for feature detection."""
    fields = [
        row.get("title", ""),
        row.get("description", ""),
        row.get("employment_type", ""),
        row.get("location_locality", ""),
        row.get("location_region", ""),
    ]
    return normalize_text(" ".join(str(field) for field in fields if not pd.isna(field)))


def detect_work_mode(text: str) -> str:
    """Detect work mode using simple, transparent rules."""
    hybrid_patterns = [
        "locationhybrid",
        "hybrid",
        "hibrido",
        "modelo hibrido",
        "modalidad hibrida",
        "3 days a week in the office",
        "days a week in the office",
        "dias a la semana en oficina",
        "dias por semana en oficina",
    ]

    remote_patterns = [
        "modalidad de trabajo: remoto",
        "modalidad remoto",
        "remoto",
        "remote",
        "teletrabajo",
        "wfh",
    ]

    onsite_patterns = [
        "presencial",
        "onsite",
        "on-site",
        "trabajo en oficina",
    ]

    office_days_pattern = re.search(
        r"\b\d+\s+(days|dias).{0,40}(office|oficina)\b",
        text,
    )

    if any(pattern in text for pattern in hybrid_patterns) or office_days_pattern:
        return "hybrid"

    if any(pattern in text for pattern in remote_patterns):
        return "remote"

    if any(pattern in text for pattern in onsite_patterns):
        return "onsite"

    return "unknown"


def detect_seniority(text: str) -> str:
    """Detect seniority using stricter keyword rules to reduce false positives."""
    lead_patterns = [
        r"\btech lead\b",
        r"\btechnical lead\b",
        r"\bteam lead\b",
        r"\blead developer\b",
        r"\blead engineer\b",
        r"\blead data engineer\b",
        r"\bprincipal engineer\b",
        r"\bprincipal developer\b",
        r"\bengineering manager\b",
    ]

    if any(re.search(pattern, text) for pattern in lead_patterns):
        return "lead"

    if re.search(r"\bsenior\b|\bsr\.?\b", text):
        return "senior"

    junior_patterns = [
        r"\bjunior\b",
        r"\bjr\.?\b",
        r"\btrainee\b",
        r"\bbecario\b",
        r"\ben practicas\b",
        r"\bcontrato en practicas\b",
        r"\bpracticas remuneradas\b",
    ]

    if any(re.search(pattern, text) for pattern in junior_patterns):
        return "junior"

    if re.search(r"\bmid\b|\bmiddle\b|\bsemi senior\b|\bsemisenior\b", text):
        return "mid"

    return "unknown"


def detect_technologies(text: str) -> str:
    """Detect technologies mentioned in title or description."""
    detected = []

    for technology, keywords in TECHNOLOGY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            detected.append(technology)

    return ", ".join(detected)


def detect_role_category(text: str) -> str:
    """Classify job posting into a broad role category."""
    if any(keyword in text for keyword in ["data engineer", "data analyst", "data scientist", "business intelligence", "bi "]):
        return "Data"

    if any(keyword in text for keyword in ["backend", "java developer", "microservicios", "api", "spring"]):
        return "Backend"

    if any(keyword in text for keyword in ["frontend", "front-end", "react", "angular", "vue"]):
        return "Frontend"

    if any(keyword in text for keyword in ["devops", "sre", "kubernetes", "docker", "cloud"]):
        return "DevOps"

    if any(keyword in text for keyword in ["cybersecurity", "ciberseguridad", "security", "soc"]):
        return "Cybersecurity"

    if any(keyword in text for keyword in ["qa", "tester", "testing", "quality assurance"]):
        return "QA"

    if any(keyword in text for keyword in ["sistemas", "systems", "sysadmin", "network", "redes"]):
        return "Systems"

    return "Other"


def normalize_country(row: pd.Series) -> str:
    """Infer normalized country when the source is a Spanish job portal."""
    raw_country = row.get("location_country", "")

    if not pd.isna(raw_country) and str(raw_country).strip():
        return str(raw_country).strip().upper()

    source = normalize_text(row.get("source", ""))

    if source in {"tecnoempleo", "ticjob"}:
        return "ES"

    return ""


def filter_recent_job_postings(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only job postings published from the configured minimum date."""
    dates = pd.to_datetime(df["date_posted"], errors="coerce")
    min_date = pd.Timestamp(MIN_DATE_POSTED)
    return df[dates >= min_date].copy()


def enrich_job_postings(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived fields to job postings."""
    enriched = df.copy()

    enriched["location_country_raw"] = enriched["location_country"]
    enriched["location_country_normalized"] = enriched.apply(normalize_country, axis=1)

    search_text = enriched.apply(build_search_text, axis=1)

    enriched["work_mode"] = search_text.apply(detect_work_mode)
    enriched["seniority"] = search_text.apply(detect_seniority)
    enriched["technologies_detected"] = search_text.apply(detect_technologies)
    enriched["role_category"] = search_text.apply(detect_role_category)
    enriched["processed_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return enriched


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    filtered = filter_recent_job_postings(df)
    enriched = enrich_job_postings(filtered)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(OUTPUT_PATH, index=False)

    print(f"Loaded rows: {len(df)}")
    print(f"Rows after date filter >= {MIN_DATE_POSTED}: {len(filtered)}")
    print(f"Rows removed by date filter: {len(df) - len(filtered)}")
    print(f"Saved enriched dataset to: {OUTPUT_PATH}")
    print()
    print(
        enriched[
            [
                "source",
                "title",
                "work_mode",
                "seniority",
                "technologies_detected",
                "role_category",
                "location_country_raw",
                "location_country_normalized",
                "salary_data_type",
            ]
        ]
    )


if __name__ == "__main__":
    main()
