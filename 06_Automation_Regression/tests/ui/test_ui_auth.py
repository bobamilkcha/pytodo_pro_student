import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"


def test_wts_01_02_08_auth_lifecycle(browser):
    """WTS-01, WTS-02, WTS-08: End-to-end browser registration, logout, login, and logout."""
    username = f"ui{uuid.uuid4().hex[:6]}"
    password = "Password123"

    # 1. WTS-01: Register a new user via the web form
    browser.get(f"{BASE_URL}/register")
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(browser, 5).until(EC.url_changes(f"{BASE_URL}/register"))
    assert "/login" not in browser.current_url
    assert "/register" not in browser.current_url

    # 2. WTS-08: Log out and confirm protected route redirects to /login
    browser.get(f"{BASE_URL}/logout")
    browser.get(f"{BASE_URL}/")
    assert "/login" in browser.current_url

    # 3. WTS-02: Log back in with the registered account
    browser.get(f"{BASE_URL}/login")
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(browser, 5).until(EC.url_changes(f"{BASE_URL}/login"))
    assert "/login" not in browser.current_url
    assert username in browser.page_source

    # 4. WTS-08: Final logout check
    browser.get(f"{BASE_URL}/logout")
    browser.get(f"{BASE_URL}/dashboard")
    assert "/login" in browser.current_url