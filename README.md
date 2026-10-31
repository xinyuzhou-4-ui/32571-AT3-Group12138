# OpenCart System Testing

This is our group project for automated system testing. We used Python, Pytest and Playwright to test the public [OpenCart Demo Store](https://opencart.abstracta.us/).

The project contains 6 test cases and 18 automated test scenarios. The tests cover user accounts, product search and shopping cart functions.

## Team Work

| Member | Functions |
| --- | --- |
| Member A (Wenhan Li) | F1 User Registration, F2 User Login, F3 User Logout |
| Member B (Xinyu Zhou) | F4 Product Search, F5 Add to Cart, F6 Shopping Cart Management |

## Test Files

| Function | Test file |
| --- | --- |
| User Registration | `tests/member_a/test_registration.py` |
| User Login | `tests/member_a/test_login.py` |
| User Logout | `tests/member_a/test_logout.py` |
| Product Search | `tests/member_b/test_search.py` |
| Add to Cart | `tests/member_b/test_add_to_cart.py` |
| Shopping Cart Management | `tests/member_b/test_shopping_cart.py` |

Each test file contains 3 scenarios.

## Project Structure

```text
32571-AT3-Group12138/
├── README.md
├── requirements.txt
├── pytest.ini
└── tests/
    ├── member_a/
    │   ├── screenshots/
    │   ├── test_registration.py
    │   ├── test_login.py
    │   └── test_logout.py
    └── member_b/
        ├── screenshots/
        ├── test_search.py
        ├── test_add_to_cart.py
        └── test_shopping_cart.py
```

## Setup

Clone the repository and enter the project folder:

```bash
git clone https://github.com/xinyuzhou-4-ui/32571-AT3-Group12138.git
cd 32571-AT3-Group12138
```

Create a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the packages and Chromium:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run the Tests

Run all tests:

```bash
python -m pytest -v
```

Run Member A tests:

```bash
python -m pytest -v tests/member_a
```

Run Member B tests:

```bash
python -m pytest -v tests/member_b
```

Use `--headed` if you want to see the browser:

```bash
python -m pytest -v --headed
```

## Test Method

We first checked the website manually to understand how it currently works. We then wrote automated tests based on the behaviour we observed. A passed test means the website still behaved in the same way as our original check.

Some tests passed but still showed website problems. For example, the website displayed an unrelated shopping-cart message when a product search returned no results. These issues are explained in our test report.

## Test Result

The full test suite contains 18 automated scenarios. In our recorded test run, all 18 tests ran successfully without execution errors. Screenshots from the test runs are stored in the `screenshots` folders.

The OpenCart website is a public demo website, so its data or behaviour may change at a later time.
