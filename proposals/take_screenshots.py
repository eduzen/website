"""Take screenshots of all three redesign proposals using Playwright."""

import pathlib

from playwright.sync_api import sync_playwright

PROPOSALS_DIR = pathlib.Path(__file__).parent
PROPOSALS = [
    ("proposal-a-philosopher-engineer.html", "Proposal A — Philosopher Engineer"),
    ("proposal-b-modern-systems-portfolio.html", "Proposal B — Modern Systems Portfolio"),
    ("proposal-c-experimental-author.html", "Proposal C — Experimental Author"),
]

# Force all reveal elements to be visible (they start hidden for scroll animation)
FORCE_VISIBLE_JS = """
document.querySelectorAll('.reveal, .reveal-left').forEach(el => {
    el.classList.add('visible');
    el.style.opacity = '1';
    el.style.transform = 'none';
});
"""


def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for filename, label in PROPOSALS:
            file_path = PROPOSALS_DIR / filename
            html_content = file_path.read_text()
            stem = file_path.stem

            # Desktop full-page screenshot
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.set_content(html_content, wait_until="commit")
            page.wait_for_timeout(3000)  # let fonts load
            page.evaluate(FORCE_VISIBLE_JS)
            page.wait_for_timeout(500)
            page.screenshot(
                path=str(PROPOSALS_DIR / f"{stem}-desktop.png"),
                full_page=True,
            )
            print(f"  [desktop] {stem}-desktop.png")

            # Hero-only screenshot (above the fold)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(200)
            page.screenshot(
                path=str(PROPOSALS_DIR / f"{stem}-hero.png"),
                full_page=False,
            )
            print(f"  [hero]    {stem}-hero.png")
            page.close()

            # Mobile screenshot
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.set_content(html_content, wait_until="commit")
            page.wait_for_timeout(3000)
            page.evaluate(FORCE_VISIBLE_JS)
            page.wait_for_timeout(500)
            page.screenshot(
                path=str(PROPOSALS_DIR / f"{stem}-mobile.png"),
                full_page=False,
            )
            print(f"  [mobile]  {stem}-mobile.png")
            page.close()

            print(f"  Done: {label}\n")

        browser.close()
    print("All screenshots saved to proposals/")


if __name__ == "__main__":
    take_screenshots()
