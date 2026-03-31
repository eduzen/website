import pytest
from playwright.sync_api import Page, expect

from .conftest import LANG_BTN, LANG_DROPDOWN, MOBILE_VIEWPORT


def _switch_to_spanish(page: Page):
    """Open dropdown and click the Spanish link (second link)."""
    page.locator(LANG_BTN).click()
    page.locator(LANG_DROPDOWN).locator("a").nth(1).click()


def _switch_to_english(page: Page):
    """Open dropdown and click the English link (first link)."""
    page.locator(LANG_BTN).click()
    page.locator(LANG_DROPDOWN).locator("a").nth(0).click()


def test_language_dropdown_opens_and_closes(page: Page, live_server):
    """Test that the language dropdown toggles on click and closes on click-away."""
    page.goto(f"{live_server.url}/en/")

    dropdown = page.locator(LANG_DROPDOWN)
    expect(dropdown).to_be_hidden()

    page.locator(LANG_BTN).click()
    expect(dropdown).to_be_visible()

    page.locator("#content").click()
    expect(dropdown).to_be_hidden()


def test_switch_from_english_to_spanish(page: Page, live_server):
    page.goto(f"{live_server.url}/en/")
    _switch_to_spanish(page)
    expect(page).to_have_url(f"{live_server.url}/es/")


def test_switch_from_spanish_to_english(page: Page, live_server):
    page.goto(f"{live_server.url}/es/")
    _switch_to_english(page)
    expect(page).to_have_url(f"{live_server.url}/en/")


@pytest.mark.parametrize("path", ["/contact/", "/blog/", "/about/"])
def test_language_switch_preserves_page(page: Page, live_server, path):
    """Test that switching language preserves the current page path."""
    page.goto(f"{live_server.url}/en{path}")
    _switch_to_spanish(page)
    expect(page).to_have_url(f"{live_server.url}/es{path}")


def test_language_flag_shows_correct_icon(page: Page, live_server):
    page.goto(f"{live_server.url}/en/")
    expect(page.locator(f"{LANG_BTN} .fi-gb")).to_be_visible()

    page.goto(f"{live_server.url}/es/")
    expect(page.locator(f"{LANG_BTN} .fi-es")).to_be_visible()


def test_language_switch_after_htmx_navigation(page: Page, live_server):
    """Test language switching works after HTMX navigation changes the URL."""
    page.goto(f"{live_server.url}/en/")

    page.locator("a[hx-get][href*='/about/']").first.click()
    page.wait_for_url(f"{live_server.url}/en/about/")

    _switch_to_spanish(page)
    expect(page).to_have_url(f"{live_server.url}/es/about/")


def test_mobile_language_switching(page: Page, live_server):
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("button.md\\:hidden").click()

    mobile_btn = page.locator(".language-button").nth(1)
    mobile_btn.click()

    mobile_dropdown = mobile_btn.locator("..").locator("[x-show='open']")
    mobile_dropdown.locator("a").nth(1).click()

    expect(page).to_have_url(f"{live_server.url}/es/contact/")


def test_dropdown_does_not_duplicate(page: Page, live_server):
    page.goto(f"{live_server.url}/en/")

    btn = page.locator(LANG_BTN)
    btn.click()
    btn.click()
    btn.click()

    expect(page.locator(LANG_DROPDOWN)).to_have_count(1)
