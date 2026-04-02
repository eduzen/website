import pytest
from playwright.sync_api import Page, expect

from blog.tests.factories import PostFactory


def _has_no_horizontal_overflow(page: Page) -> bool:
    return page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1")


def _element_dimensions(page: Page, selector: str) -> dict[str, float]:
    js = """
(element) => ({
  width: element.getBoundingClientRect().width,
  height: element.getBoundingClientRect().height,
})
"""
    return page.locator(selector).evaluate(js)


def _element_vertical_position(page: Page, selector: str) -> dict[str, float]:
    js = """
(element) => ({
  top: element.getBoundingClientRect().top,
  bottom: element.getBoundingClientRect().bottom,
})
"""
    return page.locator(selector).evaluate(js)


def test_homepage_loads(page: Page, live_server):
    """Test that the homepage loads successfully."""
    page.goto(live_server.url)

    # Expect the redirected URL with language prefix
    expect(page).to_have_url(f"{live_server.url}/en/")
    expect(page).to_have_title("eduzen")
    expect(page.locator("nav")).to_be_visible()
    expect(page.locator("#content")).to_be_visible()


def test_navigation_links(page: Page, live_server):
    """Test that main navigation links work."""
    page.goto(live_server.url)

    # Test blog link (use first visible one)
    blog_link = page.locator("a[href*='/blog/']").first
    expect(blog_link).to_be_visible()

    # Test about link (use first visible one)
    about_link = page.locator("a[href*='/about/']").first
    expect(about_link).to_be_visible()

    # Click about link and verify navigation
    about_link.click()
    expect(page).to_have_url(f"{live_server.url}/en/about/")


def test_htmx_navigation(page: Page, live_server):
    """Test HTMX navigation functionality."""
    page.goto(live_server.url)

    # Click on a navigation link and verify HTMX behavior (use first one)
    about_link = page.locator("a[hx-get][href*='/about/']").first
    if about_link.count() > 0:
        about_link.click()

        # Wait for HTMX to update content
        page.wait_for_timeout(1000)

        # Verify URL changed (HTMX should push URL)
        expect(page).to_have_url(f"{live_server.url}/en/about/")

        # Verify content area was updated
        expect(page.locator("#content")).to_be_visible()


def test_responsive_design(page: Page, live_server):
    """Test mobile navigation, hero placement, and overflow protection."""
    # Test desktop view
    page.set_viewport_size({"width": 1200, "height": 800})
    page.goto(live_server.url)

    # Check navigation is visible on desktop
    nav = page.locator("nav")
    expect(nav).to_be_visible()

    # Test mobile view
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(live_server.url)

    # Navigation should still be present and tappable.
    expect(nav).to_be_visible()
    mobile_menu_button = page.locator("#main-navbar button.md\\:hidden")
    expect(mobile_menu_button).to_be_visible()

    dimensions = _element_dimensions(page, "#main-navbar button.md\\:hidden")
    assert dimensions["width"] >= 44
    assert dimensions["height"] >= 44

    mobile_menu_button.click()
    expect(page.locator(".mobile-menu-bg")).to_be_visible()

    nav_position = _element_vertical_position(page, "#main-navbar")
    hero_position = _element_vertical_position(page, ".hero")
    assert hero_position["top"] <= nav_position["bottom"] + 16

    assert _has_no_horizontal_overflow(page)


def test_global_wave_layers_use_duplicated_2400_paths(page: Page, live_server):
    """Ensure global wave layers use single 2400-wide looping SVG paths."""
    for route in ("/en/", "/en/about/"):
        page.goto(f"{live_server.url}{route}")

        for layer in ("1", "2", "3"):
            svg = page.locator(f"svg.page-waves__layer--{layer}")
            expect(svg).to_have_count(1)
            expect(svg).to_have_attribute("viewBox", "0 0 2400 200")
            expect(svg.locator("path")).to_have_count(1)


@pytest.mark.django_db
def test_blog_list_responsive_layout(page: Page, live_server):
    """Test blog list remains readable on tablet widths."""
    PostFactory(title="Responsive layouts need room to breathe")

    for viewport in ({"width": 768, "height": 1024}, {"width": 1024, "height": 768}):
        page.set_viewport_size(viewport)
        page.goto(f"{live_server.url}/en/blog/")

        expect(page.locator(".essay-item").first).to_be_visible()
        expect(page.locator(".essay-title").first).to_contain_text("Responsive layouts")
        assert _has_no_horizontal_overflow(page)
