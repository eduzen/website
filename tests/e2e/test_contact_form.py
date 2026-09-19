from playwright.sync_api import Page, expect

from .conftest import MOBILE_VIEWPORT


def test_contact_details(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    expect(page.get_by_role("heading", name="Let's connect")).to_be_visible()
    expect(page.locator(".contact-channel")).to_have_count(4)
    expect(page.locator(".contact-page form")).to_have_count(0)
    expect(page.locator(".contact-sidebar__note")).to_contain_text("Based in Amsterdam")


def test_contact_details_responsive(page: Page, live_server):
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{live_server.url}/en/contact/")

    for channel in page.locator(".contact-channel").all():
        expect(channel).to_be_visible()
    assert page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1")
