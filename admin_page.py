from playwright.sync_api import Page

class AdminPage:
    def __init__(self, page: Page):
        self.page = page

    def go_to_admin(self):
        self.page.get_by_role("link", name="Admin").click()

    def click_add_user(self):
        self.page.get_by_role("button", name="Add").click()

    def search_user(self, username):
        self.page.locator('input[name="username"]').fill(username)
        self.page.get_by_role("button", name="Search").click()

    def delete_user(self, username):
        row = self.page.locator(f"text={username}").first.locator("..").locator("button[title='Delete']")
        row.click()
        self.page.get_by_role("button", name="Yes, Delete").click()
