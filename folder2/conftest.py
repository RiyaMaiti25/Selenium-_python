import os
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver(request):
    """Initializes and closes Chrome Browser for each test execution."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hooks into PyTest execution to attach screenshots to HTML report on failure."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        driver = getattr(item.cls, "driver", None) if item.cls else None
        if driver and report.failed:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = os.path.join("screenshots", f"{item.name}_failure.png")
            driver.save_screenshot(screenshot_path)
            if os.path.exists(screenshot_path):
                html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:300px;height:200px;" onclick="window.open(this.src)"/></div>'
                extra.append(pytest_html.extras.html(html))
        report.extra = extra