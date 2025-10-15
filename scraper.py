from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


def get_page_destination_data(url, headless=True, timeout=10):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = None
    status_code = None

    try:
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            status_code = response.status_code
        except:
            try:
                response = requests.get(url, timeout=5, allow_redirects=True)
                status_code = response.status_code
            except:
                status_code = None

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(timeout)

        driver.get(url)
        title = driver.title

        try:
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1[data-selenium='hotel-header-name']")
                )
            )
            name = name_element.text
        except:
            name = None

        try:
            address_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span[data-selenium='hotel-address-map']")
                )
            )
            address = address_element.text
        except:
            address = None

        return {
            "success": True,
            "data": {
                "title": title,
                "name": name,
                "address": address,
            },
            "url": url,
            "status_code": status_code or 200,
        }

    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "status_code": status_code or 500,
        }

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    url = "https://www.agoda.com/th-th/palette-luxe-north-pattaya/hotel/pattaya-th.html"
    result = get_page_destination_data(url, headless=False, timeout=10)
    print(result)
