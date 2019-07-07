# coding=utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import argparse
import os


# url = "https://10.20.10.20:28001/ibm/console/logon.jsp"
def get_args():
    parser = argparse.ArgumentParser(description='WAS login')
    parser.add_argument('-u', '--url', required=True, action='store', help='Url')
    parser.add_argument('-i', '--id', required=True, action='store', help='ID')
    parser.add_argument('-p', '--password', required=False, action='store', help='Password')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        executable_path='geckodriver',
        firefox_options=options)
    driver.get(args.url)
    driver.find_element_by_id("j_username").send_keys(args.id)
    driver.find_element_by_id("j_password").send_keys(args.password)
    driver.find_element_by_id("other").click()
    driver.save_screenshot('screen.png')
    login_button = driver.find_elements_by_class_name('loginButton')
    if len(login_button) > 0:
        login_button[0].click()
    driver.save_screenshot('screen2.png')
    driver.switch_to.frame("header")
    _header = driver.find_element_by_xpath('//div[@id="ibm-banner-content"]').text
    driver.close()
    if "Welcome" in _header:
        print("登陆成功 %s" % _header)
    else:
        print(driver.page_source)
        os.system(1)


if __name__ == '__main__':
    main()
