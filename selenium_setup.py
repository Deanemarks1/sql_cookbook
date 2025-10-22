import os 
import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import time
from datetime import datetime
pd.options.display.float_format = '{:.2f}'.format
import time
from datetime import datetime, time as dtime
import pytz
from selenium.common.exceptions import WebDriverException




#read in the text message functions
sys.path.append('/Users/deanemarks/Desktop/python_cook_book')
from deane_text_functions import *







#helper functions
#################################################################################
def parse_numeric(value):
    try:
        value = value.replace('$', '').replace(',', '').strip()
        if value.endswith('T'):
            return float(value[:-1]) * 1_000_000_000_000
        elif value.endswith('B'):
            return float(value[:-1]) * 1_000_000_000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        elif value.endswith('K'):
            return float(value[:-1]) * 1_000
        else:
            return float(value)
    except:
        return 0.0  # or use None if you want to keep blanks



def clean_price(value):
    try:
        return float(value.replace('$', '').replace(',', ''))
    except:
        return 0.0  # or use None if preferred

#################################################################################








def create_browser(headless):
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")

    if headless == True:
        options.add_argument("--headless=new")  # 👈 headless mode added here

    driver = uc.Chrome(options=options)
    print("🤖 Bot Initiated\n")
    return driver







def open_new_tab(driver, url='about:blank'):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])






def list_all_tab_urls(driver):
    """
    Returns a list of URLs for all open tabs.
    """
    urls = []
    current = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        urls.append(driver.current_url)
    driver.switch_to.window(current)
    return urls





def switch_to_tab(driver, index):
    tabs = driver.window_handles
    if 0 <= index < len(tabs):
        driver.switch_to.window(tabs[index])
    else:
        raise IndexError(f"Tab index {index} out of range. Total tabs: {len(tabs)}")





def close_current_tab(driver, switch_to_index=0):
    current = driver.current_window_handle
    driver.close()
    tabs = driver.window_handles
    if tabs:
        driver.switch_to.window(tabs[switch_to_index])





def close_tab_by_index(driver, index):
    tabs = driver.window_handles
    if 0 <= index < len(tabs):
        current = driver.current_window_handle
        tab_to_close = tabs[index]
        driver.switch_to.window(tab_to_close)
        driver.close()
        remaining_tabs = driver.window_handles
        if remaining_tabs:
            if index < len(remaining_tabs):
                driver.switch_to.window(remaining_tabs[index])
            else:
                driver.switch_to.window(remaining_tabs[-1])
    else:
        raise IndexError(f"Tab index {index} out of range. Total tabs: {len(tabs)}")


