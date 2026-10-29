from playwright.sync_api import Page, expect


URL = "https://opencart.abstracta.us/index.php?route=common/home"
MAC_IMAGE = "tests/member_b/screenshots/search_mac.png"
LOWERCASE_IMAGE = "tests/member_b/screenshots/search_lowercase_mac.png"
NO_RESULT_IMAGE = "tests/member_b/screenshots/search_no_result.png"


# Search for a product.
def search_product(page: Page, product_name: str):
    page.goto(URL)

    search_input = page.get_by_placeholder("Search")
    expect(search_input).to_be_visible()
    search_input.fill(product_name)

    search_button = page.locator("#search button")
    expect(search_button).to_be_visible()
    search_button.click()


# Scenario 1: Search for Mac.
def test_search_mac(page: Page):
    search_product(page, "Mac")

    expect(
        page.get_by_role("heading", name="Search - Mac", exact=True)
    ).to_be_visible()

    product_links = page.locator(".product-thumb h4 a")
    expect(product_links.first).to_be_visible()

    product_names = product_links.all_inner_texts()
    assert product_names, "Expected at least one product in the search results"
    assert all("mac" in name.lower() for name in product_names)

    page.screenshot(
        path=MAC_IMAGE,
        full_page=True,
    )


# Scenario 2: Search for a product that does not exist.
def test_search_no_product(page: Page):
    search_product(page, "No Product")

    expect(
        page.get_by_role("heading", name="Search - No Product", exact=True)
    ).to_be_visible()

    # The demo site uses this cart-related text as its no-result message.
    no_result_message = page.locator("#content").get_by_text(
        "Your shopping cart is empty!",
        exact=True,
    )
    expect(no_result_message).to_be_visible()

    product_links = page.locator(".product-thumb h4 a")
    expect(product_links).to_have_count(0)

    page.screenshot(
        path=NO_RESULT_IMAGE,
        full_page=True,
    )


# Scenario 3: Search for lowercase mac.
def test_search_lowercase_mac(page: Page):
    search_product(page, "mac")

    expect(
        page.get_by_role("heading", name="Search - mac", exact=True)
    ).to_be_visible()

    product_links = page.locator(".product-thumb h4 a")
    expect(product_links.first).to_be_visible()

    product_names = product_links.all_inner_texts()
    assert product_names, "Expected at least one product in the search results"
    assert all("mac" in name.lower() for name in product_names)

    page.screenshot(
        path=LOWERCASE_IMAGE,
        full_page=True,
    )
