import time

# Import the WebDriver interface from the Selenium module
from selenium import webdriver

# Launch Firefox using WebDriver
driver = webdriver.Firefox()

# Navigate to google.com
driver.get("http://www.google.com")

# Find the search box
element = driver.find_element_by_name("q")

# Type 'Cheese!' and submit the form
element.send_keys("Cheese!")
element.submit()

# Wait for the page to load
time.sleep(2.0)

# Close the browser
driver.close()
