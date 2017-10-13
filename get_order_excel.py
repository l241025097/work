#!usr/bin/python
#coding:utf8
'''
通过“省份工单统计（地市维度）”功能下载沃运维省份工单统计中的工单到mongo oss数据库中
'''

import datetime
import json
import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as je
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import lxml.html
import MySQLdb

import DBM
import pymongo
import xlrd
from print_r import print_r

from pandas import read_excel
import urllib

reload(sys)
sys.setdefaultencoding('utf8')

def connect_mongo_source(host='127.0.0.1', port='61111', user='luoyl25', pwd='S198641cn', db='front_source'):
    '''连接数据库'''
    pwd = urllib.quote_plus(pwd)
    connect_str = 'mongodb://' + user + ':' + pwd + '@' + host + ':' + port + '/' + db
    client = pymongo.MongoClient(connect_str)
    dbh = client[db]
    return dbh

def deal_excel(file_path, collection):
    '''读取excel并写入数据库'''
    dbh = connect_mongo_source(db='oss')
    dbh.get_collection(collection).drop()
    dict_list = read_excel(file_path).to_dict(orient='record')
    dbh.get_collection(collection).insert_many(dict_list)
    os.remove(file_path)
    print 'finish'

def change_url(driver_obj, original_url, limit_time=30):
    '''新页面打开后等待url切换'''
    loop_limit = limit_time
    while loop_limit:
        loop_limit -= 1
        if driver_obj.current_url != original_url:
            break
        time.sleep(1)
    return driver_obj.current_url

def write_html(driver_obj, file_name):
    '''将html写入文件中'''
    with open(file_name, 'w') as file_handle:
        file_handle.write(driver_obj.page_source)

def utf8_gbk(msg):
    '''将utf8编码转换为gbk编码'''
    return msg.decode('utf8').encode('gbk')

def process(start_time=None, end_time=None, item=u'省份工单统计（地市维度）', condition=u'总计@@0@@ALL', collection='all'):
    current_path = os.path.dirname(__file__)
    if not current_path:
        current_path = os.getcwd()
    locator = None
    element_obj = None
    err_msg = None
    index_url = r'http://10.245.0.225/uf/login/login.jsp'
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': current_path}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(index_url)
    driver.find_element_by_id('username').send_keys('luoyl25')
    driver.find_element_by_id('password').send_keys('S198641cn')
    driver.find_element_by_id('loginbtn').click()

    err_msg = '1:切换主页帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('i1'),
            utf8_gbk(err_msg))
    except Exception.__bases__ as err:
        print err

    err_msg = '2:获取查询页url失败'
    try:
        locator = (By.ID, 'EOM_FM_WEB')
        WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg))
        element_obj = driver.find_element(*locator)
    except Exception.__bases__ as err:
        print err

    old_url = driver.current_url

    if element_obj != None:
        java_script = element_obj.get_attribute('href')
        driver.execute_script(java_script)
        element_obj = None

    order_url = change_url(driver, old_url)
    driver.close()
    driver.quit()

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(index_url)
    driver.find_element_by_id('username').send_keys('luoyl25')
    driver.find_element_by_id('password').send_keys('S198641cn')
    driver.find_element_by_id('loginbtn').click()

    err_msg = '3:第2次切换主页帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('i1'),
            utf8_gbk(err_msg))
        driver.execute_script('window.open("' + order_url + '")')
    except Exception.__bases__ as err:
        print err

    err_msg = '4:使用新窗口打开查询页失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.number_of_windows_to_be(2),
            utf8_gbk(err_msg))
        driver.switch_to_window(driver.window_handles[1])
    except Exception.__bases__ as err:
        print err

    err_msg = '5:切换查询选项帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('menu_show_for_regist_review_iframe'),
            utf8_gbk(err_msg))
    except Exception.__bases__ as err:
        print err

    err_msg = '6:获取所有查询选项失败'
    try:
        locator = (By.CSS_SELECTOR, 'ul#menu-ul li a')
        WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg))
        element_obj = driver.find_elements(*locator)
    except Exception.__bases__ as err:
        print err

    if element_obj != None:
        for eobj in element_obj:
            if eobj.text == item:
                eobj.click()
                time.sleep(1)
        element_obj = None

    err_msg = '7:切换工单列表帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('__menu_body'),
            utf8_gbk(err_msg))
    except Exception.__bases__ as err:
        bar_sign = False
        print err

    err_msg = '8:填写时间表单失败'
    now_time = datetime.datetime.now()
    weekday = now_time.weekday()
    if weekday > 2:
        before_time = now_time - datetime.timedelta(days=(weekday - 2))
    else:
        before_time = now_time - datetime.timedelta(days=(7 - (2 - weekday)))
    end_time = end_time if end_time else now_time.strftime('%Y-%m-%d 00:00:00')
    start_time = start_time if start_time else before_time.strftime('%Y-%m-%d 00:00:00')
    try:
        locator = (By.ID, 'dtGridContainer_2_1_2')
        WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        start_obj = driver.find_element_by_id('startTime')
        end_obj = driver.find_element_by_id('endTime')
        start_obj.clear()
        end_obj.clear()
        start_obj.send_keys(start_time)
        end_obj.send_keys(end_time)
        driver.find_element_by_css_selector('button[onclick="queryDate()"]').click()
        WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
    except Exception.__bases__ as err:
        print err

    err_msg = '9:等待进度条失败'
    try:
        locator = (By.CSS_SELECTOR, 'div[id*="dt_grid_process_bar_top"]')
        WebDriverWait(driver, 5, 0.5).until(
            je.visibility_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        WebDriverWait(driver, 30, 0.5).until(
            je.invisibility_of_element_located(locator),
            utf8_gbk(err_msg)
        )
    except Exception.__bases__ as err:
        print err

    if condition is not None:
        driver.find_element_by_css_selector(u'a[onclick="orderroom(\''+condition+'\')"]').click()
        driver.switch_to_window(driver.window_handles[-1])

    err_msg = '10:获取excel按钮失败'
    try:
        locator = (By.CSS_SELECTOR, 'a[id*="exportExcelGrid"]')
        element_obj = WebDriverWait(driver, 10, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        element_obj.click()
    except Exception.__bases__ as err:
        print err

    err_msg = '11:获取excel字段选择帧失败'
    try:
        locator = (By.CSS_SELECTOR, 'div[id*="dtGridExport_excel"]')
        WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        locator_str = 'input[name*="dt_grid_export_export_all_data_excel"]'
        locator = (By.CSS_SELECTOR, locator_str)
        WebDriverWait(driver, 30, 0.5).until(
            je.visibility_of_element_located(locator)
        )
        element_obj = driver.find_elements_by_css_selector(locator_str)
        for eobj in element_obj:
            if int(eobj.get_attribute('value')) == 1:
                eobj.click()
                break
        driver.find_element_by_css_selector('button[id*="dt_grid_export_execute_excel"]').click()
    except Exception.__bases__ as err:
        print err

    time.sleep(30)
    driver.close()
    driver.quit()

    file_name = u'省份故障分析.xls' if condition is None else u'工单详情.xls'
    file_path = os.path.join(current_path, file_name)
    deal_excel(file_path, collection)

def user():
    current_path = os.path.dirname(__file__)
    if not current_path:
        current_path = os.getcwd()
    locator = None
    eobj = None
    err_msg = None
    index_url = r'http://10.245.0.225/uf/login/login.jsp'
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': current_path}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(index_url)
    driver.find_element_by_id('username').send_keys('luoyl25')
    driver.find_element_by_id('password').send_keys('S198641cn')
    driver.find_element_by_id('loginbtn').click()
    
    err_msg = '1:显示应用中心失败'
    try:
        locator = (By.ID, 'YYZX')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        eobj.click()
    except Exception.__bases__ as err:
        print err

    err_msg = '2:点击电子运维失败'
    try:
        locator = (By.ID, 'sec_menu_1101')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        driver.execute_script("document.body.scrollTop=0")
        eobj.click()
    except Exception.__bases__ as err:
        print err

    time.sleep(3)

    err_msg = '3:点击组织树管理失败'
    try:
        locator = (By.ID, 'appid_13')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        eobj.click()
    except Exception.__bases__ as err:
        print err

    err_msg = '4:切换分公司组织数帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('menu_show_for_regist_review_iframe'),
            utf8_gbk(err_msg))
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('mainFrame'),
            utf8_gbk(err_msg))
    except Exception.__bases__ as err:
        print err

    err_msg = '5:点击分公司组织树失败'
    try:
        locator = (By.ID, 'tree_9_span')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg)
        )
        eobj.click()
    except Exception.__bases__ as err:
        print err
    
    err_msg = '6:切换用户界面帧失败'
    try:
        WebDriverWait(driver, 30, 0.5).until(
            je.frame_to_be_available_and_switch_to_it('userFrame'),
            utf8_gbk(err_msg))
    except Exception.__bases__ as err:
        print err
    
    err_msg = '7:点击下载用户信息按钮失败'
    try:
        locator = (By.ID, 'exportId')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg))
        eobj.click()
    except Exception.__bases__ as err:
        print err

    err_msg = '8:获取ok按钮失败'
    try:
        locator = (By.ID, 'mb_btn_ok')
        eobj = WebDriverWait(driver, 30, 0.5).until(
            je.presence_of_element_located(locator),
            utf8_gbk(err_msg))
        eobj.click()
    except Exception.__bases__ as err:
        print err

    time.sleep(10)
    driver.close()
    driver.quit()
    for each in os.listdir(current_path):
        if os.path.isfile(each):
            if re.search(u'用户信息', each.decode('gbk')):
                file_name = each
                break
    os.listdir(current_path)
    file_path = os.path.join(current_path, file_name)
    deal_excel(file_path, 'user')

# if __name__ == '__main__':
    # user()
    # process(start_time=None, end_time=None, condition=u'总计@@0@@ALL', collection='all')
    # process(start_time=None, end_time=None, condition=u'总计@@0@@NOACCEPT', collection='receive')
    # process(start_time=None, end_time=None, item=u'省份故障分析', condition=None, collection='analysis')
    # current_path = os.path.dirname(__file__)
    # if not current_path:
    #     current_path = os.getcwd()
    
    

