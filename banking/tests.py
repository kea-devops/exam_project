from django.test import SimpleTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class BankingTest(SimpleTestCase):
    def setUp(self):
        service = webdriver.ChromeService(executable_path='/usr/lib/chromium/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=service, options=options)


    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get('http://139.162.186.27:8000/accounts/login/')

        email_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')

        email_field.send_keys('janedoe@gmail.com')
        password_field.send_keys('123')

        submit_button = self.driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()

        time.sleep(5)

        welcome_paragraph = self.driver.find_element(By.XPATH, "//p[contains(text(),'Welcome to the bank')]")

        print('Welcome Paragraph Text:', welcome_paragraph.text)

        self.assertEqual(welcome_paragraph.text, 'Welcome to the bank')
