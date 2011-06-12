import time
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.google.com")
element = driver.find_element_by_name("q")
element.send_keys("Cheese!")
element.submit()
time.sleep(2.0)
driver.close()
