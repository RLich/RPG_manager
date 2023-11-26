from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.private_data import *
import time


class GUIHandler:
    def __init__(self):
        print("__WebDriver is starting__")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def log_into_messenger(self):
        driver = self.driver
        messenger_url = "https://www.messenger.com/"
        driver.maximize_window()
        driver.get(messenger_url)

        cookie_accept_xpath = "//button[@data-cookiebanner='accept_only_essential_button']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, cookie_accept_xpath)))
        driver.find_element(By.XPATH, cookie_accept_xpath).click()

        login_email_field_xpath = "//input[@id='email']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, login_email_field_xpath)))
        login_email_field = driver.find_element(By.XPATH, login_email_field_xpath)
        login_email_field.send_keys(bot_gmail_address)

        login_password_field = driver.find_element(By.XPATH, "//input[@id='pass']")
        login_password_field.send_keys(facebook_password)

        login_button = driver.find_element(By.XPATH, "//button[@id='loginbutton']")
        login_button.click()

    def select_user_via_sidebar(self, username):
        driver = self.driver
        print("Selecting %s on Messenger" % username)
        if self.is_username_already_selected_bool(username=username) is True:
            pass
        else:
            user_image_on_sidebar = "//img[@alt='%s']" % username
            javascript_click = driver.find_element(By.XPATH, user_image_on_sidebar)
            driver.execute_script("arguments[0].click();", javascript_click)

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
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            if driver.find_element(By.XPATH, xpath).text == username:
                print("User already selected on Messenger")
                return True
        except BaseException:
            return False

    def quit(self):
        print("__Closing WebDriver__")
        driver = self.driver
        driver.quit()
