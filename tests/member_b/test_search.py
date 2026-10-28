from playwright.sync_api import Page, expect


# Website URL and screenshot path
URL = "https://opencart.abstracta.us/index.php?route=common/home"
MAC_SCREENSHOT = "tests/member_b/screenshots/search_mac.png"
LOWERCASE_MAC_SCREENSHOT = "tests/member_b/screenshots/search_lowercase_mac.png"
No_SEARCH_PRODUCT="tests/member_b/screenshots/search_no_result.png"

#创建搜索函数，包括打开界面，定位搜索框，输入搜索内容，点击搜索按钮
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

#情景一: 搜索关键字为“Mac”，验证搜索结果页面显示，并且至少返回一个匹配的产品
def test_search_with_keyword_Mac(page: Page):
    # Search for products using the partial keyword "Mac"
    search_product(page, "Mac")

    # Verify that the search results page is displayed
    expect(
        page.get_by_role("heading", name="Search - Mac", exact=True)
    ).to_be_visible()

    # Verify that at least one matching product is returned
    product_links = page.locator(".product-thumb h4 a")
    expect(product_links.first).to_be_visible()

    product_names = product_links.all_inner_texts()
    assert product_names, "Expected at least one product in the search results"
    assert all("mac" in name.lower() for name in product_names)

    # Save evidence of the search results
    page.screenshot(path=MAC_SCREENSHOT , full_page=True)


 #情景二：搜索不存在的商品
def test_search_nonexistent_product(page: Page):
    # Search for a non-existent product
    search_product(page, "No Product")

    # Verify that the search results page is displayed
    expect(
        page.get_by_role("heading", name="Search - No Product", exact=True)
    ).to_be_visible()

     # Verify that the no-result message is displayed
    no_result_message = page.locator("#content").get_by_text(
        "Your shopping cart is empty!",
        exact=True,
    )
    expect(no_result_message).to_be_visible()

    # Verify that no products are returned
    product_links = page.locator(".product-thumb h4 a")
    expect(product_links).to_have_count(0)

    # Save evidence
    page.screenshot( path=No_SEARCH_PRODUCT,full_page=True,)


#情景三: 搜索小写关键字“mac”，验证搜索功能不区分大小写，并且至少返回一个匹配的产品
def test_search_with_lowercase_keyword_mac(page: Page):
    # Search for products using the lowercase keyword "mac"
    search_product(page, "mac")

    # Verify that the search results page is displayed
    expect(
        page.get_by_role("heading", name="Search - mac", exact=True)
    ).to_be_visible()

    # Verify that at least one matching product is returned
    product_links = page.locator(".product-thumb h4 a")
    expect(product_links.first).to_be_visible()

    product_names = product_links.all_inner_texts()
    assert product_names, "Expected at least one product in the search results"
    assert all("mac" in name.lower() for name in product_names)

    # Save evidence of the search results
    page.screenshot(path=LOWERCASE_MAC_SCREENSHOT, full_page=True)
