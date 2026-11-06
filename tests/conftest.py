import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Allow tests to reach the demo site while its TLS certificate is expired."""
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }
