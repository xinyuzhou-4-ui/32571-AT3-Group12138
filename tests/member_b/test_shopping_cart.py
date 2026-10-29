import re

from playwright.sync_api import Page, expect


URL = "https://opencart.abstracta.us/index.php?route=common/home"
UPDATE_IMAGE = "tests/member_b/screenshots/test_update_imac_quantity.png"
EMPTY_CART_IMAGE = "tests/member_b/screenshots/test_empty_shopping_cart.png"
STOCK_IMAGE = "tests/member_b/screenshots/test_quantity_beyond_stock.png"


# Search for Mac products.
def search_mac(page: Page):
    page.goto(URL)

    search_input = page.get_by_placeholder("Search")
    search_input.fill("Mac")

    search_button = page.locator("#search button")
    search_button.click()


# Add one iMac and open the cart page.
def open_cart_with_imac(page: Page):
    search_mac(page)

    imac_card = page.locator(".product-thumb").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    add_to_cart_button = imac_card.get_by_role(
        "button",
        name="Add to Cart",
    )
    add_to_cart_button.click()

    # This assertion also waits for the asynchronous cart update to finish.
    success_message = page.locator(".alert-success")
    expect(success_message).to_be_visible()

    # Keep the navigation visible when the test runs in headed mode.
    page.wait_for_timeout(1000)

    shopping_cart_link = page.locator("#top-links").get_by_role(
        "link",
        name="Shopping Cart",
    )
    shopping_cart_link.click()

    # The demo site has an incorrect page heading, so verify the route instead.
    expect(page).to_have_url(re.compile(r"route=checkout/cart"))


# Scenario 1: Change the quantity from 1 to 2.
def test_update_quantity(page: Page):
    open_cart_with_imac(page)

    imac_row = page.get_by_role("row").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    quantity_input = imac_row.get_by_role("textbox")
    quantity_input.fill("2")

    update_button = imac_row.locator('button[type="submit"]')
    update_button.click()

    update_message = page.locator(".alert-success")
    expect(update_message).to_be_visible()
    expect(quantity_input).to_have_value("2")

    # Verify both the product-line total and the final cart total.
    product_total = imac_row.get_by_role("cell").last
    expect(product_total).to_have_text("$244.00")

    cart_total_row = page.get_by_role("row").filter(
        has=page.get_by_text("Total:", exact=True)
    )
    cart_total = cart_total_row.get_by_role("cell").last
    expect(cart_total).to_have_text("$244.00")

    page.screenshot(
        path=UPDATE_IMAGE,
        full_page=True,
    )


# Scenario 2: Change the quantity to 0.
def test_quantity_zero(page: Page):
    open_cart_with_imac(page)

    imac_row = page.get_by_role("row").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    quantity_input = imac_row.get_by_role("textbox")
    quantity_input.fill("0")

    update_button = imac_row.locator('button[type="submit"]')
    update_button.click()

    # Quantity 0 should remove the product and leave an empty cart.
    expect(imac_row).to_have_count(0)

    empty_cart_message = page.locator("#content").get_by_text(
        "Your shopping cart is empty!",
        exact=True,
    )
    expect(empty_cart_message).to_be_visible()

    cart_button = page.locator("#cart > button")
    expect(cart_button).to_contain_text("0 item(s)")
    expect(cart_button).to_contain_text("$0.00")

    page.screenshot(
        path=EMPTY_CART_IMAGE,
        full_page=True,
    )


# Scenario 3: Enter a quantity greater than the stock.
def test_quantity_over_stock(page: Page):
    open_cart_with_imac(page)

    imac_row = page.get_by_role("row").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    quantity_input = imac_row.get_by_role("textbox")
    quantity_input.fill("99999")

    update_button = imac_row.locator('button[type="submit"]')
    update_button.click()

    # Excessive quantity should trigger stock validation without removing iMac.
    stock_warning = page.locator(".alert-danger")
    expect(stock_warning).to_be_visible()
    expect(stock_warning).to_contain_text(
        "not available in the desired quantity or not in stock"
    )
    expect(imac_row).to_be_visible()
    expect(quantity_input).to_have_value("99999")

    empty_cart_message = page.locator("#content").get_by_text(
        "Your shopping cart is empty!",
        exact=True,
    )
    expect(empty_cart_message).to_have_count(0)

    page.screenshot(
        path=STOCK_IMAGE,
        full_page=True,
    )
