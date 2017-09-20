from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

def save_cookie(driver, file_path):
    cookie_str = 'document.cookie="{name}={value}; path={path}; domain={domain}";\n'
    with open(file_path, 'w') as w_fh:
        for cookie in driver.get_cookies():
            w_fh.write(cookie_str.format(**cookie))

def load_cookie(driver, file_path):
    with open(file_path) as r_fh:
        driver.execute_script(r_fh.read())

driver = webdriver.PhantomJS()
driver.get("http://221.7.195.46:8008/#/signin")
driver.delete_all_cookies()
load_cookie(driver, 'cookie.txt')
driver.get('http://221.7.195.46:8008/#/main/index/dashboard')
driver.maximize_window()

# locator = (By.NAME, 'username')
# try:
#     element = WebDriverWait(driver, 10, 0.5).until(
#         EC.presence_of_element_located(locator)
#     )
#     element.clear()
#     element.send_keys('15676192675')
# except Exception.__bases__ as err:
#     print(err)
# locator = (By.NAME, 'password')
# try:
#     element = WebDriverWait(driver, 10, 0.5).until(
#         EC.presence_of_element_located(locator)
#     )
#     element.clear()
#     element.send_keys('123')
# except Exception.__bases__ as err:
#     print(err)
# locator = (By.CSS_SELECTOR, 'button[ng-click="controller.login()"]')
# try:
#     element = WebDriverWait(driver, 10, 0.5).until(
#         EC.element_to_be_clickable(locator)
#     )
#     element.click()
# except Exception.__bases__ as err:
#     print(err)
locator = (By.CSS_SELECTOR, 'span[class="title ng-binding"]')
try:
    elements = WebDriverWait(driver, 10, 0.5).until(
        EC.presence_of_all_elements_located(locator)
    )
    for element in elements:
        print(element.text)
except Exception.__bases__ as err:
    print(err)

# cookie_save(driver, 'cookie.txt')

with open('err.html', 'w') as w_fh:
    w_fh.write(driver.page_source)