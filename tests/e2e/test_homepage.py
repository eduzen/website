from playwright.sync_api import Page, expect


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
    """Test basic responsive design elements."""
    # Test desktop view
    page.set_viewport_size({"width": 1200, "height": 800})
    page.goto(live_server.url)

    # Check navigation is visible on desktop
    nav = page.locator("nav")
    expect(nav).to_be_visible()

    # Test mobile view
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(live_server.url)

    # Navigation should still be present (might be hamburger menu)
    expect(nav).to_be_visible()
