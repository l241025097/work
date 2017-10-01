from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as HE
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import xlrd

def save_cookie(driver, file_path):
    cookie_str = 'document.cookie="{name}={value}; path={path}; domain={domain}";\n'
    with open(file_path, 'w') as w_fh:
        for cookie in driver.get_cookies():
            print(cookie)
            w_fh.write(cookie_str.format(**cookie))

def load_cookie(driver, file_path):
    with open(file_path) as r_fh:
        driver.execute_script(r_fh.read())

def get_current_path():
    current_path = os.path.dirname(__file__)
    if not current_path:
        current_path = os.getcwd()
    return current_path

def modify_user_password(user_info_file):

    password_format = 'Qwg#%s'
    
    current_path = get_current_path()

    options = webdriver.ChromeOptions()

    # options.binary_location = 'usr/bin/google-chrome-stable'

    prefs = {
        "download.default_directory": current_path,
        "download.directory_upgrade": True,
        "download.extensions_to_open": "",
        "download.prompt_for_download": False,
        "profile.default_content_settings.popups": 0
    }

    options.add_experimental_option('prefs', prefs)

    options.add_argument('window-size=1600x900')
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get("http://221.7.195.46:8008/#/signin")
    print("link url: http://221.7.195.46:8008/#/signin")

    # driver.delete_all_cookies()
    # load_cookie(driver, 'cookie.txt')
    # driver.get('http://221.7.195.46:8008/#/main/index/dashboard')
    # driver.maximize_window()

    locator = (By.NAME, 'username')
    try:
        element = WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located(locator),
            'fail when getting name: %s' % locator[1]
        )
        element.clear()
        element.send_keys('15607810500')
        print('fill username')
    except Exception.__bases__ as err:
        print(err)

    locator = (By.NAME, 'password')
    try:
        element = WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located(locator),
            u'fail when getting name: %s' % locator[1]
        )
        element.clear()
        element.send_keys('cn198641S')
        print('fill password')
    except Exception.__bases__ as err:
        print(err)

    locator = (By.CSS_SELECTOR, 'button[ng-click="controller.login()"]')
    try:
        element = WebDriverWait(driver, 10, 0.5).until(
            EC.element_to_be_clickable(locator),
            'fail when getting css: %s' % locator[1]
        )
        element.click()
        print('login')
    except Exception.__bases__ as err:
        print(err)

    locator = (By.CSS_SELECTOR, 'a[ui-sref="main.basis.user"]')
    try:
        element = WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located(locator),
            'fail when getting css: %s' % locator[1]
        )
        user_url = element.get_attribute('href')
        driver.get(user_url)
        print('link user_url: %s' % user_url)
    except Exception.__bases__ as err:
        print(err)

    with xlrd.open_workbook(user_info_file) as book:
        sheet = book.sheet_by_index(0)
        username_list = sheet.col_values(1)
    # with open(user_info_file) as r_fh:
    #     username_gen = (line.strip().split()[1] for line in r_fh.readlines())

    for username in username_list:

        locator = (By.CSS_SELECTOR, 'input[ng-model="controller.table.query.user_id"]')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting css: %s' % locator[1]
            )
            element.clear()
            element.send_keys(username)
            print('fill query username: ' % username)
        except Exception.__bases__ as err:
            print(err)

        locator = (By.CSS_SELECTOR, 'button[ng-click="controller.table.search()"]')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting css: %s' % locator[1]
            )
            element.click()
            print('submit query')
        except Exception.__bases__ as err:
            print(err)

        locator = (By.CSS_SELECTOR, 'td[class="ng-binding"]')
        try:
            while 1:
                try:
                    elements = WebDriverWait(driver, 10, 0.5).until(
                        EC.presence_of_all_elements_located(locator),
                        'fail when getting css: %s' % locator[1]
                    )
                    row_num = elements[0].text
                    if elements[1].text == username:
                        break
                    continue
                except HE.StaleElementReferenceException:
                    continue
            print('validate query')
        except Exception.__bases__ as err:
            print(err)
        
        locator = (By.CSS_SELECTOR, 'button[ng-click="controller.openUpdateUserDialog(row)"]')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting css: %s' % locator[1]
            )
            driver.execute_script('arguments[0].click()', element)
            print('begin edit')
        except Exception.__bases__ as err:
            print(err)
        
        locator = (By.NAME, 'userPwd')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting name: %s' % locator[1]
            )
            element.clear()
            element.send_keys(password_format % username)
            print('modify password')
        except Exception.__bases__ as err:
            print(err)
        
        locator = (By.NAME, 'userPwdTwo')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting name: %s' % locator[1]
            )
            element.clear()
            element.send_keys(password_format % username)
            print('confirm password')
        except Exception.__bases__ as err:
            print(err)
        
        locator = (By.CSS_SELECTOR, 'button[ng-click="controller.saveUser()"]')
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.presence_of_element_located(locator),
                'fail when getting css: %s' % locator[1]
            )
            driver.execute_script('arguments[0].click()', element)
            print('save edit')
        except Exception.__bases__ as err:
            print(err)

        locator = (By.CSS_SELECTOR, 'div[ng-binding-html="message"]')        
        try:
            element = WebDriverWait(driver, 10, 0.5).until(
                EC.invisibility_of_element_located(locator),
                'fail when getting id: %s' % locator[1]
            )
            print('wait editing window close')
        except Exception.__bases__ as err:
            print(err)
        sleep(2)

    # save_cookie(driver, 'cookie.txt')

    driver.close()
    driver.quit()

if __name__ == '__main__':
    modify_user_password(u'华为区.txt')
    modify_user_password(u'诺西区.txt')
    modify_user_password(u'贝尔区.txt')
