import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://opencart.abstracta.us/index.php?route=account/login"
ACCOUNT_URL = "https://opencart.abstracta.us/index.php?route=account/account"


# Auxiliary function: Login account
def login_helper(page: Page):
    page.goto(LOGIN_URL)
    page.fill("#input-email", "RA-326@gmail.com")
    page.fill("#input-password", "1234")
    page.click("input[type='submit']")


# scene 1: logout normally
def test_logout_success(page: Page):
    login_helper(page)

    # click Logout button on the sidebar
    page.click("a.list-group-item:has-text('Logout')")

    # validate turn to logout page
    expect(page).to_have_url(
        "https://opencart.abstracta.us/index.php?route=account/logout"
    )
    expect(page.locator("#content p").first).to_have_text(
        "You have been logged off your account. It is now safe to leave the computer."
    )


# scene 2: cannot access the protected account after logout
def test_cannot_access_account_after_logout(page: Page):
    login_helper(page)

    # execute logout
    page.click("a.list-group-item:has-text('Logout')")

    # Attempt to directly access the protected account page URL
    page.goto(ACCOUNT_URL)

    # Verify it is redirected back to the login page
    expect(page).to_have_url(LOGIN_URL)


# Scene 3: Using the browser back button after exiting
def test_logout_browser_back(page: Page):
    login_helper(page)

    # execute logout
    page.click("a.list-group-item:has-text('Logout')")

    # Simulate clicking the browser back button
    page.go_back()
    page.reload()  # refresh the page

    # Verify it is still in an unlogged-in state/has been redirected to log in
    expect(page).to_have_url(LOGIN_URL)
