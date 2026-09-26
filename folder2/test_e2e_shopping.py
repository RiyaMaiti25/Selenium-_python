import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import configuration and parameters from pure Python file
from data.test_data import APP_URL, USER_EMAIL, USER_PASSWORD, SEARCH_TERM, UPDATED_QUANTITY


@pytest.mark.usefixtures("driver")
class TestEcommerceWorkflow:

    def capture_step_screenshot(self, step_name):
        """Helper utility to save step-by-step screenshots."""
        os.makedirs("screenshots", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
        self.driver.save_screenshot(path)

    def test_complete_checkout_flow(self):
        wait = WebDriverWait(self.driver, 12)

        # 1. Launch Browser & Open Application
        self.driver.get(APP_URL)
        assert "Your Store" in self.driver.title
        self.capture_step_screenshot("01_Launch_Browser")

        # 2. Login to Application
        my_account = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='My Account']")))
        my_account.click()
        login_option = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        login_option.click()

        wait.until(EC.presence_of_element_located((By.ID, "input-email"))).send_keys(USER_EMAIL)
        self.driver.find_element(By.ID, "input-password").send_keys(USER_PASSWORD)
        self.driver.find_element(By.XPATH, "//input[@value='Login']").click()
        self.capture_step_screenshot("02_Logged_In")

        # 3. Search Product
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_input.clear()
        search_input.send_keys(SEARCH_TERM)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-default.btn-lg").click()
        self.capture_step_screenshot("03_Search_Results")

        # 4. Add Product to Cart
        product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, SEARCH_TERM)))
        product_link.click()
        
        add_cart_btn = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        add_cart_btn.click()

        # 5. Handle Alert Banner
        alert_banner = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        assert "Success: You have added" in alert_banner.text
        self.capture_step_screenshot("04_Added_To_Cart_Banner")

        # 6. Navigate to Cart & Update Quantity
        cart_nav = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Shopping Cart']")))
        cart_nav.click()

        qty_box = wait.until(EC.presence_of_element_located((By.XPATH, "//form[@action]/div/table/tbody/tr/td[4]//input")))
        qty_box.clear()
        qty_box.send_keys(UPDATED_QUANTITY)

        update_btn = self.driver.find_element(By.XPATH, "//button[@data-original-title='Update']")
        update_btn.click()

        # 7. Validate Cart Update
        updated_alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        assert "Success: You have modified your shopping cart!" in updated_alert.text
        
        updated_qty = self.driver.find_element(By.XPATH, "//form[@action]/div/table/tbody/tr/td[4]//input").get_attribute("value")
        assert updated_qty == UPDATED_QUANTITY
        self.capture_step_screenshot("05_Cart_Quantity_Updated")