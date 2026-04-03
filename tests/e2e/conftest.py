import pytest
from playwright.sync_api import Page

MOBILE_VIEWPORT = {"width": 375, "height": 667}

# Language dropdown selectors (desktop nav)
LANG_BTN = "div.hidden.md\\:flex .language-button"
LANG_DROPDOWN = "div.hidden.md\\:flex [data-testid='language-dropdown']"


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
    page.wait_for_url(f"{base_url}/dashboard/")
    return page


@pytest.fixture
def accept_dialogs(page: Page):
    """Auto-accept browser confirmation dialogs."""
    page.on("dialog", lambda dialog: dialog.accept())
    return page
