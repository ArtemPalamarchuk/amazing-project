from collections.abc import Callable

import pytest
from playwright.sync_api import Page

# Must match api/management/commands/seed_e2e.py
E2E_USERNAME = "e2e"
E2E_PASSWORD = "e2e-pass"


@pytest.fixture
def login(page: Page) -> Callable[[str], None]:
    def _login(password: str = E2E_PASSWORD) -> None:
        page.goto("/")
        page.get_by_placeholder("Username").fill(E2E_USERNAME)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Log in").click()

    return _login


@pytest.fixture
def logged_in_page(page: Page, login) -> Page:
    login()
    return page
