import uuid

from playwright.sync_api import Page, expect


def test_login_invalid_credentials(page: Page, login):
    login(password="wrong-password")

    expect(page.get_by_text("Invalid credentials")).to_be_visible()


def test_login_and_add_task(logged_in_page: Page):
    page = logged_in_page
    expect(page.get_by_role("heading", name="Projects")).to_be_visible()

    # Unique title so parallel runs and leftovers from old runs don't match.
    title = f"e2e task {uuid.uuid4().hex[:8]}"
    project = page.locator("section").first
    project.get_by_placeholder("New task").fill(title)
    project.get_by_role("button", name="Add").click()

    expect(project.get_by_text(title)).to_be_visible()
