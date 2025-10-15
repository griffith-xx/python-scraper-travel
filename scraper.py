
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_page_destination_data(url, headless=True, timeout=10):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = None

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(timeout)

        driver.get(url)
        title = driver.title

        return {
            "success": True,
            "title": title,
            "url": url,
        }

    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    url = "https://www.agoda.com/th-th"
    result = get_page_destination_data(url, headless=True, timeout=10)
    print(result)
