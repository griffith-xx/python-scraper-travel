from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/th-th/baron-beach-hotel/hotel/pattaya-th.html?ds=lQ6UVmoPoGPBue45")
print(driver.title)
driver.quit()