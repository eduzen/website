import re

from playwright.sync_api import Page, expect

from .conftest import MOBILE_VIEWPORT


def _has_no_horizontal_overflow(page: Page) -> bool:
    return page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1")


def _content_width(page: Page, selector: str) -> float:
    return page.locator(selector).evaluate(
        """
        (element) => {
          const styles = window.getComputedStyle(element);
          const paddingLeft = Number.parseFloat(styles.paddingLeft);
          const paddingRight = Number.parseFloat(styles.paddingRight);
          return element.getBoundingClientRect().width - paddingLeft - paddingRight;
        }
        """
    )


def test_contact_form_labels_visible(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    expect(page.locator("label", has_text="Name")).to_be_visible()
    expect(page.locator("label", has_text="Email")).to_be_visible()
    expect(page.locator("label", has_text="Message")).to_be_visible()
    expect(page.locator("label", has_text=re.compile(r"red rabbit", re.IGNORECASE))).to_be_visible()


def test_contact_form_labels_not_white(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    white_spans = page.locator(".warm-form label span.text-white")
    expect(white_spans).to_have_count(0)


def test_contact_form_fields_fillable(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("#id_name").fill("Test User")
    page.locator("#id_email").fill("test@example.com")
    page.locator("#id_message").fill("Hello, this is a test message.")
    page.locator("#id_captcha").fill("red")

    expect(page.locator("#id_name")).to_have_value("Test User")
    expect(page.locator("#id_email")).to_have_value("test@example.com")
    expect(page.locator("#id_message")).to_have_value("Hello, this is a test message.")
    expect(page.locator("#id_captcha")).to_have_value("red")


def test_contact_form_validation_errors_on_empty_submit(page: Page, live_server, accept_dialogs):
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("input[type='submit']").click()

    expect(page).to_have_url(re.compile(r"/en/contact/"))


def test_contact_form_invalid_email(page: Page, live_server, accept_dialogs):
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("#id_name").fill("Test User")
    page.locator("#id_email").fill("not-an-email")
    page.locator("#id_message").fill("Test message")
    page.locator("#id_captcha").fill("red")

    page.locator("input[type='submit']").click()

    expect(page).to_have_url(re.compile(r"/en/contact/"))


def test_contact_form_wrong_captcha(page: Page, live_server, accept_dialogs):
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("#id_name").fill("Test User")
    page.locator("#id_email").fill("test@example.com")
    page.locator("#id_message").fill("Test message")
    page.locator("#id_captcha").fill("blue")

    page.locator("input[type='submit']").click()

    expect(page).to_have_url(re.compile(r"/contact/"))


def test_contact_form_successful_submit(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    page.locator("#id_name").fill("Test User")
    page.locator("#id_email").fill("test@example.com")
    page.locator("#id_message").fill("Hello, this is a test message from Playwright.")
    page.locator("#id_captcha").fill("red")

    page.locator("input[type='submit']").click()

    # The custom <dialog> confirmation appears — click "Send" to confirm
    page.locator("#confirmDialog .confirm-dialog__btn--confirm").click()

    # Telegram is skipped in test env (placeholder token) — form always succeeds
    expect(page.locator("#content")).to_contain_text("Thank you")


def test_contact_form_successful_submit_spanish_captcha(page: Page, live_server):
    page.goto(f"{live_server.url}/es/contact/")

    page.locator("#id_name").fill("Usuario Test")
    page.locator("#id_email").fill("test@example.com")
    page.locator("#id_message").fill("Hola, este es un mensaje de prueba.")
    page.locator("#id_captcha").fill("rojo")

    page.locator("input[type='submit']").click()

    # The custom <dialog> confirmation appears — click confirm button
    page.locator("#confirmDialog .confirm-dialog__btn--confirm").click()

    expect(page.locator("#content")).to_contain_text("Usuario Test")


def test_contact_form_submit_button_warm_theme(page: Page, live_server):
    page.goto(f"{live_server.url}/en/contact/")

    submit_btn = page.locator("input[type='submit']")
    expect(submit_btn).to_be_visible()

    btn_classes = submit_btn.get_attribute("class") or ""
    assert "bg-purple" not in btn_classes, "Submit button still has old purple styling"


def test_contact_form_responsive(page: Page, live_server):
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{live_server.url}/en/contact/")

    expect(page.locator(".warm-form")).to_be_visible()
    expect(page.locator("label", has_text="Name")).to_be_visible()
    expect(page.locator("#id_name")).to_be_visible()

    page.locator("#id_name").fill("Mobile User")
    expect(page.locator("#id_name")).to_have_value("Mobile User")

    form_box = page.locator(".warm-form").bounding_box()
    assert form_box is not None
    assert form_box["x"] >= 0
    assert form_box["width"] <= MOBILE_VIEWPORT["width"]

    submit_box = page.locator("input[type='submit']").bounding_box()
    assert submit_box is not None
    assert submit_box["width"] >= _content_width(page, ".warm-form") - 2

    assert _has_no_horizontal_overflow(page)
