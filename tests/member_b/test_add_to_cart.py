from playwright.sync_api import Page, expect


URL = "https://opencart.abstracta.us/index.php?route=common/home"
ONE_IMAC_IMAGE = "tests/member_b/screenshots/test_add_imac_to_cart.png"
TWO_PRODUCTS_IMAGE = "tests/member_b/screenshots/test_add_two_products_to_cart.png"
TWO_IMACS_IMAGE = "tests/member_b/screenshots/test_add_same_product_twice.png"


# Search for Mac products.
def search_mac(page: Page):
    page.goto(URL)

    search_input = page.get_by_placeholder("Search")
    expect(search_input).to_be_visible()
    search_input.fill("Mac")

    search_button = page.locator("#search button")
    expect(search_button).to_be_visible()
    search_button.click()


# Scenario 1: Add one iMac.
def test_add_one_imac(page: Page):
    search_mac(page)

    imac_card = page.locator(".product-thumb").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    expect(imac_card).to_be_visible()

    add_to_cart_button = imac_card.get_by_role(
        "button",
        name="Add to Cart",
    )
    expect(add_to_cart_button).to_be_visible()
    add_to_cart_button.click()

    success_message = page.locator(".alert-success")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("iMac")

    cart_button = page.locator("#cart > button")
    expect(cart_button).to_contain_text("1 item(s)")
    expect(cart_button).to_contain_text("$122.00")

    cart_button.click()
    cart_dropdown = page.locator("#cart")
    expect(
        cart_dropdown.locator("td.text-left").get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    ).to_be_visible()

    total_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_text("Total", exact=True)
    )
    total_value = total_row.get_by_role("cell").last
    expect(total_value).to_have_text("$122.00")

    page.screenshot(
        path=ONE_IMAC_IMAGE,
        full_page=True,
    )


# Scenario 2: Add two different products.
def test_add_two_products(page: Page):
    search_mac(page)

    # Use the same steps for both products.
    def add_product_to_cart(product_name: str):
        product_card = page.locator(".product-thumb").filter(
            has=page.get_by_role(
                "link",
                name=product_name,
                exact=True,
            )
        )
        expect(product_card).to_be_visible()

        add_to_cart_button = product_card.get_by_role(
            "button",
            name="Add to Cart",
        )
        expect(add_to_cart_button).to_be_visible()
        add_to_cart_button.click()

        success_message = page.locator(".alert-success").last
        expect(success_message).to_be_visible()
        expect(success_message).to_contain_text(product_name)

    cart_button = page.locator("#cart > button")

    add_product_to_cart("iMac")
    expect(cart_button).to_contain_text("1 item(s)")

    add_product_to_cart("MacBook")
    expect(cart_button).to_contain_text("2 item(s)")
    expect(cart_button).to_contain_text("$724.00")

    cart_button.click()
    cart_dropdown = page.locator("#cart")
    product_name_cells = cart_dropdown.locator("td.text-left")

    expect(
        product_name_cells.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    ).to_be_visible()
    expect(
        product_name_cells.get_by_role(
            "link",
            name="MacBook",
            exact=True,
        )
    ).to_be_visible()

    total_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_text("Total", exact=True)
    )
    total_value = total_row.get_by_role("cell").last
    expect(total_value).to_have_text("$724.00")

    page.screenshot(
        path=TWO_PRODUCTS_IMAGE,
        full_page=True,
    )


# Scenario 3: Add iMac twice.
def test_add_same_product_twice(page: Page):
    search_mac(page)

    # Use the same steps for both additions.
    def add_imac_to_cart():
        imac_card = page.locator(".product-thumb").filter(
            has=page.get_by_role(
                "link",
                name="iMac",
                exact=True,
            )
        )
        expect(imac_card).to_be_visible()

        add_to_cart_button = imac_card.get_by_role(
            "button",
            name="Add to Cart",
        )
        expect(add_to_cart_button).to_be_visible()
        add_to_cart_button.click()

        success_message = page.locator(".alert-success").last
        expect(success_message).to_be_visible()
        expect(success_message).to_contain_text("iMac")

    cart_button = page.locator("#cart > button")

    add_imac_to_cart()
    expect(cart_button).to_contain_text("1 item(s)")

    add_imac_to_cart()
    expect(cart_button).to_contain_text("2 item(s)")
    expect(cart_button).to_contain_text("$244.00")

    cart_button.click()
    cart_dropdown = page.locator("#cart")
    imac_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_role(
            "link",
            name="iMac",
            exact=True,
        )
    )
    expect(imac_row).to_be_visible()
    expect(imac_row).to_contain_text("x 2")

    total_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_text("Total", exact=True)
    )
    total_value = total_row.get_by_role("cell").last
    expect(total_value).to_have_text("$244.00")

    page.screenshot(
        path=TWO_IMACS_IMAGE,
        full_page=True,
    )
