import time
from playwright.sync_api import Page, expect

REGISTER_URL = "https://opencart.abstracta.us/index.php?route=account/register"
REGISTRATION_SUCCESS_IMAGE = (
    "tests/member_a/screenshots/test_registration_success.png"
)
DUPLICATE_EMAIL_IMAGE = (
    "tests/member_a/screenshots/test_registration_duplicate_email.png"
)
PRIVACY_POLICY_IMAGE = (
    "tests/member_a/screenshots/test_missing_privacy_policy.png"
)


# Scene 1: Successful registration using valid information
def test_register_success(page: Page):
    page.goto(REGISTER_URL)

    # Dynamically generate a unique email address to prevent errors due to duplicate email addresses during multiple runs
    unique_email = f"test_{int(time.time())}@example.com"

    page.fill("#input-firstname", "Dee")
    page.fill("#input-lastname", "Jay")
    page.fill("#input-email", unique_email)
    page.fill("#input-telephone", "1234567890")
    page.fill("#input-password", "1234")
    page.fill("#input-confirm", "1234")

    # Check the privacy policy consent box
    page.check("input[name='agree']")
    page.click("input[type='submit']")

    # Verify URL redirection and successful prompt text
    expect(page).to_have_url(
        "http://opencart.abstracta.us/index.php?route=account/success"
    )
    expect(page.locator("#content p").first).to_contain_text(
        "Congratulations! Your new account has been successfully created!"
    )

    page.screenshot(
        path=REGISTRATION_SUCCESS_IMAGE,
        full_page=True,
    )


# Scene 2: Using an already registered email address
def test_register_duplicate_email(page: Page):
    page.goto(REGISTER_URL)

    # Use a fixed email address that has already been occupied
    page.fill("#input-firstname", "Dee")
    page.fill("#input-lastname", "Jay")
    page.fill("#input-email", "demo@example.com")
    page.fill("#input-telephone", "1234567890")
    page.fill("#input-password", "1234")
    page.fill("#input-confirm", "1234")

    page.check("input[name='agree']")
    page.click("input[type='submit']")

    # Verify the warning prompt indicating that the email has already been registered
    warning = page.locator(".alert-danger")
    expect(warning).to_contain_text("Warning: E-Mail Address is already registered!")

    page.screenshot(
        path=DUPLICATE_EMAIL_IMAGE,
        full_page=True,
    )


# Scenario 3: Submit valid registration details without accepting the Privacy Policy
def test_register_missing_privacy_policy(page: Page):
    page.goto(REGISTER_URL)

    # Use a unique email so that the Privacy Policy is the only missing requirement.
    unique_email = f"privacy_test_{int(time.time())}@example.com"

    page.fill("#input-firstname", "Dee")
    page.fill("#input-lastname", "Jay")
    page.fill("#input-email", unique_email)
    page.fill("#input-telephone", "1234567890")
    page.fill("#input-password", "1234")
    page.fill("#input-confirm", "1234")

    # Intentionally leave the Privacy Policy checkbox unselected.
    page.click("input[type='submit']")

    # Verify that registration is rejected because the policy was not accepted.
    warning = page.locator(".alert-danger")
    expect(warning).to_contain_text("Warning: You must agree to the Privacy Policy!")

    page.screenshot(
        path=PRIVACY_POLICY_IMAGE,
        full_page=True,
    )
