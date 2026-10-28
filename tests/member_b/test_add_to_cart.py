from playwright.sync_api import Page, expect

# Website URL and screenshot path
URL = "https://opencart.abstracta.us/index.php?route=common/home"
ADD_IMAC1 = "tests/member_b/screenshots/test_add_imac_to_cart.png"
ADD_TWO_PRODUCTS = "tests/member_b/screenshots/test_add_two_products_to_cart.png"
ADD_SAME_PRODUCT_TWICE = "tests/member_b/screenshots/test_add_same_product_twice.png"

#创建搜索Mac的函数，包括打开界面，定位搜索框，输入搜索内容，点击搜索按钮
def search_mac(page: Page):
    # Navigate to the OpenCart website
    page.goto(URL)

    # Locate the search input field and enter the product name
    search_input = page.get_by_placeholder("Search")
    expect(search_input).to_be_visible()
    search_input.fill("Mac")

    # Click the search button
    search_button = page.locator("#search button")
    expect(search_button).to_be_visible()
    search_button.click()

#情景一：添加一项iMac到购物车，并且验证购物车中显示正确的商品名称和价格
def test_add_imac_to_cart(page: Page):
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

    # Verify that the success message is displayed
    success_message = page.locator(".alert-success")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("iMac")

    cart_button = page.locator("#cart > button")
    expect(cart_button).to_contain_text("1 item(s)")
    expect(cart_button).to_contain_text("$122.00")

    # Open the cart and verify the product name and price
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

    # Save evidence
    page.screenshot(
        path=ADD_IMAC1,
        full_page=True,
    )


#情景二：添加iMac和MacBook到购物车，并验证两件商品的名称和总价
def test_add_two_different_products(page: Page):
    search_mac(page)

    # This helper function is used only in scenario two
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

    # Add iMac to the cart
    add_product_to_cart("iMac")
    expect(cart_button).to_contain_text("1 item(s)")

    # Add MacBook to the cart
    add_product_to_cart("MacBook")

    # Verify that the cart contains two items and the correct total
    expect(cart_button).to_contain_text("2 item(s)")
    expect(cart_button).to_contain_text("$724.00")

    # Open the cart and verify both product names
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

    # Verify that the Total row displays $724.00
    total_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_text("Total", exact=True)
    )
    total_value = total_row.get_by_role("cell").last
    expect(total_value).to_have_text("$724.00")

    # Save evidence
    page.screenshot(
        path=ADD_TWO_PRODUCTS,
        full_page=True,
    )


#情景三：重复添加两次iMac，并验证商品数量和总价
def test_add_same_product_twice(page: Page):
    search_mac(page)

    # This helper function is used only in scenario three
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

    # Add iMac to the cart for the first time
    add_imac_to_cart()
    expect(cart_button).to_contain_text("1 item(s)")

    # Add iMac to the cart for the second time
    add_imac_to_cart()

    # Verify that the cart contains two items and the correct total
    expect(cart_button).to_contain_text("2 item(s)")
    expect(cart_button).to_contain_text("$244.00")

    # Open the cart and verify the product name and quantity
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

    # Verify that the Total row displays $244.00
    total_row = cart_dropdown.get_by_role("row").filter(
        has=page.get_by_text("Total", exact=True)
    )
    total_value = total_row.get_by_role("cell").last
    expect(total_value).to_have_text("$244.00")

    # Save evidence
    page.screenshot(
        path=ADD_SAME_PRODUCT_TWICE,
        full_page=True,
    )
