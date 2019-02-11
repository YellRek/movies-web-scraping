from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import time

def get_chrome_driver(url):
    SESSION_CHROME_DIR = "C:\\Users\\jonatas.campos\\AppData\\Local\\Google\\Chrome\\User Data"
    WEBDRIVER_PATH = "C:\\webdriver\\chromedriver.exe"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("user-data-dir=" + SESSION_CHROME_DIR)
    driver = webdriver.Chrome(chrome_options = chrome_options, executable_path = WEBDRIVER_PATH)
    #driver.maximize_window()
    driver.get(url)

    return driver