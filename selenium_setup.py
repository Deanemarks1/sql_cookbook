# ============================================================
# SELENIUM ENGINE v1 (CLEAN FACTORY ONLY)
# ============================================================

print("Imported Selenium engine -- v2")

# ============================================================
# CORE IMPORTS
# ============================================================

import ssl
import selenium
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException
)

print("Selenium Version :", selenium.__version__)
print("SSL Backend      :", ssl.OPENSSL_VERSION)
print("==============================\n")


# ============================================================
# BROWSER FACTORY
# (NO DRIVER CREATED HERE)
# ============================================================

def create_browser(
        headless=True,
        load_strategy="eager",
        disable_images=False,
        disable_gpu=True
    ):

    options = uc.ChromeOptions()

    # Page Load Strategy
    options.page_load_strategy = load_strategy   # normal | eager | none

    # Core Stability Flags
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if disable_gpu:
        options.add_argument("--disable-gpu")

    if headless:
        options.add_argument("--headless=new")

    # Optional: Disable images for speed
    if disable_images:
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)

    print("🤖 Bot Initiated\n")
    return driver


# ============================================================
# TAB UTILITIES
# ============================================================

def open_new_tab(driver, url="about:blank"):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


def list_all_tab_urls(driver):
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
        raise IndexError(
            f"Tab index {index} out of range. Total tabs: {len(tabs)}"
        )


def close_current_tab(driver, switch_to_index=0):
    driver.close()

    tabs = driver.window_handles

    if tabs:
        driver.switch_to.window(tabs[switch_to_index])


def close_tab_by_index(driver, index):
    tabs = driver.window_handles

    if 0 <= index < len(tabs):

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
        raise IndexError(
            f"Tab index {index} out of range. Total tabs: {len(tabs)}"
        )
