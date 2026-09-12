"""Capture screenshots of portfolio projects for the /work page.

Usage:
    uv run playwright install chromium  # first time only
    uv run python scripts/capture_work_screenshots.py

Screenshots are saved to core/static/core/img/work/
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECTS = [
    ("maiteblog", "https://maiteblog.com"),
    ("groomit", "https://groomit.io"),
    ("champi", "https://champi.dev"),
    ("althaia", "https://althaia.nl"),
]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "core" / "static" / "core" / "img" / "work"
VIEWPORT = {"width": 1280, "height": 720}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT)

        for name, url in PROJECTS:
            print(f"Capturing {name} ({url})...")
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1000)  # let animations settle
                path = OUTPUT_DIR / f"{name}.jpg"
                page.screenshot(path=path, type="jpeg", quality=85)
                print(f"  -> saved {path}")
            except Exception as e:
                print(f"  !! failed: {e}")

        browser.close()

    print(f"\nDone. Screenshots in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
