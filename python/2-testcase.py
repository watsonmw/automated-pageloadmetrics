import unittest
from selenium import webdriver

class BrowserTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def testSearch(self):
        google = self.driver.get("http://www.google.com")
        element = self.driver.find_element_by_name("q")
        element.send_keys("Cheese!")
        element.submit()


if __name__ == "__main__":
    unittest.main()
