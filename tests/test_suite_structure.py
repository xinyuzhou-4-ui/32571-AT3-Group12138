from pathlib import Path


TESTS_ROOT = Path(__file__).parent
EXPECTED_TEST_MODULES = {
    "member_a/test_login.py",
    "member_a/test_logout.py",
    "member_a/test_registration.py",
    "member_b/test_add_to_cart.py",
    "member_b/test_search.py",
    "member_b/test_shopping_cart.py",
}


def test_expected_functional_test_modules_exist():
    actual_modules = {
        path.relative_to(TESTS_ROOT).as_posix()
        for path in TESTS_ROOT.glob("member_*/test_*.py")
    }

    assert actual_modules == EXPECTED_TEST_MODULES


def test_functional_scenario_count():
    scenario_count = sum(
        source_file.read_text(encoding="utf-8").count("def test_")
        for source_file in TESTS_ROOT.glob("member_*/test_*.py")
    )

    # Deliberately incorrect for the CI failure demonstration; fixed next.
    assert scenario_count == 19
