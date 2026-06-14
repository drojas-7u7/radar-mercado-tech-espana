from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class SourceTarget:
    name: str
    url: str
    robots_url: str


SOURCES = [
    SourceTarget(
        name="Tecnoempleo",
        url="https://www.tecnoempleo.com/",
        robots_url="https://www.tecnoempleo.com/robots.txt",
    ),
    SourceTarget(
        name="Ticjob",
        url="https://www.ticjob.es/",
        robots_url="https://www.ticjob.es/robots.txt",
    ),
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; radar-mercado-tech-espana/0.1; educational project)"
    )
}


def check_url(session: requests.Session, url: str) -> dict[str, str | int]:
    response = session.get(url, headers=HEADERS, timeout=15)

    return {
        "status_code": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("content-type", "unknown"),
        "content_length": len(response.text),
    }


def main() -> None:
    with requests.Session() as session:
        for source in SOURCES:
            print("=" * 80)
            print(f"Source: {source.name}")

            print("\nHomepage:")
            try:
                homepage_result = check_url(session, source.url)
                for key, value in homepage_result.items():
                    print(f"- {key}: {value}")
            except requests.RequestException as error:
                print(f"- error: {error}")

            print("\nRobots.txt:")
            try:
                robots_result = check_url(session, source.robots_url)
                for key, value in robots_result.items():
                    print(f"- {key}: {value}")
            except requests.RequestException as error:
                print(f"- error: {error}")

            print()


if __name__ == "__main__":
    main()
