# coding=utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import DesiredCapabilities


def init_phantomjs_driver():
    driver = webdriver.PhantomJS(executable_path='phantomjs.exe')





