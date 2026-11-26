import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"


def test_wts_03_06_07_task_lifecycle_and_confirm_dialog(browser):
    """WTS-03, WTS-06, WTS-07, TC-BB-076, GUI-11: Create, complete, cancel delete, and delete task."""
    username = f"uitask{uuid.uuid4().hex[:6]}"
    password = "Password123"
    task_title = f"Selenium Task {uuid.uuid4().hex[:4]}"

    # Register and log in
    browser.get(f"{BASE_URL}/register")
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(browser, 5).until(EC.url_changes(f"{BASE_URL}/register"))

    # 1. WTS-03: Create a new task
    browser.get(f"{BASE_URL}/tasks/new")
    browser.find_element(By.NAME, "title").send_keys(task_title)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(browser, 5).until(EC.url_changes(f"{BASE_URL}/tasks/new"))

    assert task_title in browser.page_source

    # 2. WTS-06: Toggle task from Open to Done
    toggle_btn = browser.find_element(By.CSS_SELECTOR, "form[action*='/toggle'] button")
    toggle_btn.click()
    assert task_title in browser.page_source

    # 3. TC-BB-076 / GUI-11: Click Delete and click Cancel on browser confirm popup
    delete_btn = browser.find_element(By.CSS_SELECTOR, "form[action*='/delete'] button")
    delete_btn.click()
    alert = WebDriverWait(browser, 5).until(EC.alert_is_present())
    alert.dismiss()

    # Task must still exist after canceling confirmation
    assert task_title in browser.page_source

    # 4. WTS-07: Click Delete and click OK on browser confirm popup
    delete_btn = browser.find_element(By.CSS_SELECTOR, "form[action*='/delete'] button")
    delete_btn.click()
    alert = WebDriverWait(browser, 5).until(EC.alert_is_present())
    alert.accept()

    # Task must be removed after confirming deletion
    WebDriverWait(browser, 5).until(lambda d: task_title not in d.page_source)
    assert task_title not in browser.page_source