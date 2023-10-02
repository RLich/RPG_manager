from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from private_data import *
import time


class GUIHandler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def log_into_messenger(self):
        driver = self.driver
        messenger_url = "https://www.messenger.com/"
        driver.maximize_window()
        driver.get(messenger_url)

        cookie_accept_xpath = "//button[@data-cookiebanner='accept_only_essential_button']"
        driver.find_element(By.XPATH, cookie_accept_xpath).click()

        login_email_field = driver.find_element(By.XPATH, "//input[@id='email']")
        login_email_field.send_keys(bot_gmail_address)

        login_password_field = driver.find_element(By.XPATH, "//input[@id='pass']")
        login_password_field.send_keys(facebook_password)

        login_button = driver.find_element(By.XPATH, "//button[@id='loginbutton']")
        login_button.click()

    def select_user_via_sidebar(self, username):
        driver = self.driver
        if self.is_username_already_selected_bool(username=username) is True:
            pass
        else:
            username_on_sidebar_xpath = "//img[@alt='%s']" % username
            driver.find_element(By.XPATH, username_on_sidebar_xpath).click()

    def send_messages(self, messages_list):
        driver = self.driver
        for message in messages_list:
            textfield_xpath = "//div[@role='textbox']"
            driver.find_element(By.XPATH, textfield_xpath).clear()
            driver.find_element(By.XPATH, textfield_xpath).send_keys(message)
            driver.find_element(By.XPATH, "//div[@aria-label='Press Enter to send']").click()
            time.sleep(1)

    def is_username_already_selected_bool(self, username):
        driver = self.driver
        wait = self.wait
        xpath = "//a[@aria-label='%s']" % username
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if driver.find_element(By.XPATH, xpath).text == username:
            return True

    def quit(self):
        driver = self.driver
        driver.quit()
