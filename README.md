# OpenCart Automated System Testing

This repository contains the automated system tests developed for Assignment 3 of **32571 Enterprise Software Testing** at the University of Technology Sydney. The system under test is the public [OpenCart Demo Store hosted by Abstracta](https://opencart.abstracta.us/).

The test suite uses Python, Pytest and Playwright with Chromium to cover customer-account, product-search and shopping-cart functions.

## Team Members and Responsibilities

| Student | Student ID | Role | Assigned functions |
| --- | --- | --- | --- |
| Xinyu Zhou | 25942689 | Team Leader | F4 Product Search, F5 Add to Cart, F6 Shopping Cart Management |
| Wenhan Li | 25583891 | Team Member | F1 User Registration, F2 User Login, F3 User Logout |

## Functions Under Test

| Function ID | Function | Test file |
| --- | --- | --- |
| F1 | User Registration | `tests/member_a/test_registration.py` |
| F2 | User Login | `tests/member_a/test_login.py` |
| F3 | User Logout | `tests/member_a/test_logout.py` |
| F4 | Product Search | `tests/member_b/test_search.py` |
| F5 | Add to Cart | `tests/member_b/test_add_to_cart.py` |
| F6 | Shopping Cart Management | `tests/member_b/test_shopping_cart.py` |

Each function is represented by one test case containing three automated scenarios. The complete suite therefore contains **6 test cases and 18 automated test scenarios**.

## Test Approach

The group first performed exploratory testing to observe and record the current behaviour of the OpenCart demonstration website. Automated tests were then developed as baseline regression tests to verify whether the website consistently produced the same outputs for the selected inputs.

An automated test marked as `PASS` means that the current website behaviour matched the behaviour recorded during exploratory testing. It does not necessarily mean that the behaviour satisfied every usability, security or business-quality expectation. Behaviours that matched the recorded baseline but appeared incorrect, misleading or insecure were separately documented as product defects.

## Test Scenarios

### F1 User Registration

1. Register with valid customer information and a dynamically generated email address.
2. Attempt to register using an email address that is already registered.
3. Complete all required fields but submit without accepting the Privacy Policy.

### F2 User Login

1. Log in using valid credentials.
2. Attempt to log in using a valid email address and an incorrect password.
3. Attempt to log in using an unregistered email address.

### F3 User Logout

1. Log out through the account navigation.
2. Attempt to access a protected account page after logout.
3. Use browser back navigation and refresh after logout.

### F4 Product Search

1. Search for an existing product using `Mac`.
2. Search for a product that does not exist.
3. Repeat the product search using lowercase `mac`.

### F5 Add to Cart

1. Add one iMac to the shopping cart.
2. Add two different products to the shopping cart.
3. Add the same product to the shopping cart twice.

### F6 Shopping Cart Management

1. Update the iMac quantity from 1 to 2.
2. Remove the iMac by setting its quantity to 0.
3. Enter a quantity greater than the available stock.

## Project Structure

```text
32571-AT3-Group12138/
├── pytest.ini
├── README.md
├── requirements.txt
└── tests/
    ├── member_a/
    │   ├── screenshots/
    │   │   └── 9 automated scenario screenshots
    │   ├── test_registration.py
    │   ├── test_login.py
    │   └── test_logout.py
    └── member_b/
        ├── screenshots/
        ├── test_search.py
        ├── test_add_to_cart.py
        └── test_shopping_cart.py
```

## Test Environment

The suite was developed and executed in the following environments:

- macOS on Apple Silicon with Python 3.13.2
- Windows 10 Pro on x86-64 with Python 3.14.3
- Pytest 9.1.1
- Playwright 1.64.1
- pytest-playwright 0.10.0
- Playwright Chromium

The exact Python package versions are recorded in `requirements.txt`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/xinyuzhou-4-ui/32571-AT3-Group12138.git
cd 32571-AT3-Group12138
```

### 2. Create a virtual environment

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install Playwright Chromium

```bash
python -m playwright install chromium
```

## Running the Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run one member's test suite:

```bash
python -m pytest -v tests/member_a
python -m pytest -v tests/member_b
```

Run one functional test file:

```bash
python -m pytest -v tests/member_a/test_registration.py
python -m pytest -v tests/member_b/test_search.py
```

Run the Privacy Policy registration scenario only:

```bash
python -m pytest -v tests/member_a/test_registration.py::test_register_missing_privacy_policy
```

To display the browser while the tests execute, add `--headed`:

```bash
python -m pytest -v --headed
```

## Test Results

The documented integrated test run produced the following results:

| Metric | Result |
| --- | ---: |
| Test cases | 6 |
| Automated test scenarios | 18 |
| Automated checks passed against the recorded baseline | 18 |
| Automated check failures | 0 |
| Execution errors | 0 |

The test report contains the execution output, website screenshots and detailed results for every scenario. Because the website is an externally hosted demonstration system, its data and behaviour may change after the documented test run.

## Identified Product Defects

| Defect ID | Related test | Summary |
| --- | --- | --- |
| D01 | T001 User Registration | Successful registration redirects from an HTTPS page to an HTTP account-success page. |
| D02 | T004 Product Search | A search with no matching products displays `Your shopping cart is empty!` instead of a search-related no-results message. |
| D03 | T006 Shopping Cart Management | The shopping-cart page displays an incorrect heading such as `Use Gift Certificate (10.00kg)`. |
| D04 | T006 Shopping Cart Management | An excessive quantity triggers a warning but remains in the cart, produces an unrealistic total and leaves Checkout available. |

These behaviours matched the website baseline used by the automated regression tests, but they were separately classified as security, usability or validation defects.

## Test Data and Credentials

The tests operate only against the public OpenCart demonstration website. Registration tests generate unique email addresses at runtime to reduce collisions between repeated executions. Login and logout tests use a test account created for the demonstration environment. Credentials in this repository must not be reused for personal, university or production accounts.

## Evidence

The source files contain inline comments explaining the scenarios, test data, reusable setup steps and assertions. Selected screenshots generated by the automated tests are stored under the corresponding `screenshots` directories. Complete execution evidence and the detailed analysis are provided in the submitted system test report.
