import pytest
from playwright.sync_api import Page


@pytest.fixture
def homepage(page: Page, base_url: str):
    """Fixture that navigates to homepage and returns page."""
    page.goto(f"{base_url}/")
    return page


@pytest.fixture
def login_page(page: Page, base_url: str):
    """Fixture that navigates to login page."""
    page.goto(f"{base_url}/login/")
    return page


@pytest.fixture
def authenticated_user(page: Page, base_url: str):
    """Fixture that logs in a test user."""
    page.goto(f"{base_url}/login/")
    page.fill("#username", "testuser")
    page.fill("#password", "testpass")
    page.click("button[type='submit']")
    # Wait for navigation to complete
    page.wait_for_url(f"{base_url}/dashboard/")
    return page
