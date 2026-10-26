from playwright.sync_api import Page, expect


# Website URL and screenshot path
URL = "https://opencart.abstracta.us/index.php?route=common/home"
MAC_SCREENSHOT = "tests/member_b/screenshots/search_mac.png"


def search_product(page: Page, product_name: str):
    # Navigate to the OpenCart website
    page.goto(URL)

    # Locate the search input field and enter the product name
    search_input = page.get_by_placeholder("Search")
    expect(search_input).to_be_visible()
    search_input.fill(product_name)

    # Click the search button
    search_button = page.locator("#search button")
    expect(search_button).to_be_visible()
    search_button.click()


def test_search_with_partial_keyword_mac(page: Page):
    # Search for products using the partial keyword "Mac"
    search_product(page, "Mac")

    # Verify that the search results page is displayed
    expect(page.get_by_role("heading", name="Search - Mac")).to_be_visible()

    # Verify that at least one matching product is returned
    product_links = page.locator(".product-thumb h4 a")
    expect(product_links.first).to_be_visible()

    product_names = product_links.all_inner_texts()
    assert product_names, "Expected at least one product in the search results"
    assert all("mac" in name.lower() for name in product_names)

    # Save evidence of the search results
    page.screenshot(path=MAC_SCREENSHOT , full_page=True)
