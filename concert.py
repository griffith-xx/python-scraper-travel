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

        # ตรวจสอบ status_code ก่อนทำ scraping
        if status_code and status_code != 200:
            return {
                "success": False,
                "url": url,
                "message": f"HTTP Error: Status code {status_code}",
                "status_code": status_code,
            }

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(timeout)

        driver.get(url)
        title = driver.title

        try:
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.concert-title-box")
                )
            )
            name = name_element.text
        except:
            name = None

        return {
            "success": True,
            "url": url,
            "title": title,
            "name": name,
            "status_code": status_code or 200,
        }

    except Exception as e:
        error_message = str(e)

        # จัดการ error message ให้อ่านง่ายขึ้น
        if "timeout" in error_message.lower():
            error_message = f"Page load timeout: The page took longer than {timeout} seconds to load"
        elif "no such element" in error_message.lower():
            error_message = "Unable to find required elements on the page"
        elif "invalid argument" in error_message.lower():
            error_message = "Invalid URL format"

        return {
            "success": False,
            "url": url,
            "message": error_message,
            "error": str(e),
            "status_code": status_code or 500,
        }

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__": 
    url = "https://www.theconcert.com/concert/4263"
    result = get_page_destination_data(url,headless=False, timeout=10)
    print(result)