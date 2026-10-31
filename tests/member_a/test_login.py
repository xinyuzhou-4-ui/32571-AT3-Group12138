from playwright.sync_api import Page, expect

LOGIN_URL = "https://opencart.abstracta.us/index.php?route=account/login"
LOGIN_SUCCESS_IMAGE = "tests/member_a/screenshots/test_login_success.png"
WRONG_PASSWORD_IMAGE = "tests/member_a/screenshots/test_login_wrong_password.png"
UNREGISTERED_EMAIL_IMAGE = (
    "tests/member_a/screenshots/test_login_unregistered_email.png"
)


# Scene 1: Logging in with the correct email and password
def test_login_success(page: Page):
    page.goto(LOGIN_URL)

    # type the valid email and password you have registered
    page.fill("#input-email", "RA-326@gmail.com")
    page.fill("#input-password", "1234")
    page.click("input[type='submit']")

    # validate it returns to account page
    expect(page).to_have_url(
        "https://opencart.abstracta.us/index.php?route=account/account"
    )
    expect(page.locator("#content h2").first).to_have_text("My Account")

    page.screenshot(
        path=LOGIN_SUCCESS_IMAGE,
        full_page=True,
    )


# Scene 2: Using the correct email and incorrect password
def test_login_wrong_password(page: Page):
    page.goto(LOGIN_URL)

    page.fill("#input-email", "RA-326@gmail.com")
    page.fill("#input-password", "12345")
    page.click("input[type='submit']")

    # Validate warning prompt
    warning = page.locator(".alert-danger")
    expect(warning).to_contain_text(
        "Warning: No match for E-Mail Address and/or Password."
    )

    page.screenshot(
        path=WRONG_PASSWORD_IMAGE,
        full_page=True,
    )


# Scene 3: Logging in with an unregistered email address
def test_login_unregistered_email(page: Page):
    page.goto(LOGIN_URL)

    page.fill("#input-email", "Raymond_GZ0326@gmail.com")
    page.fill("#input-password", "1234")
    page.click("input[type='submit']")

    # Validate warning prompt
    warning = page.locator(".alert-danger")
    expect(warning).to_contain_text(
        "Warning: No match for E-Mail Address and/or Password."
    )

    page.screenshot(
        path=UNREGISTERED_EMAIL_IMAGE,
        full_page=True,
    )
