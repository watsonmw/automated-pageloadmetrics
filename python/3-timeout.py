import httplib
import json
import os
import time
import sys
import unittest
from selenium import webdriver

class Timeout():
    def __init__(self, timeout, name):
        self.timeout = timeout
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        runtime =  time.time() - self.start
        if (runtime > self.timeout):
            msg = '"{0}" exceeded timeout of {1} seconds'.format(self.name , self.timeout)
            raise Exception(msg)
        else:
            print '"{0}" took {1} seconds'.format(self.name , runtime)

class TimeoutTests(unittest.TestCase):
    """
    The actual test
    """
    def testSearch(self):
        driver = webdriver.Firefox()
        with Timeout(10, "Navigate to google.com"):
            driver.get("http://www.google.com")

        with Timeout(10, "Search for cheese!"):
            element = driver.find_element_by_name("q")
            element.send_keys("Cheese!")
            element.submit()

        driver.close()

if __name__ == "__main__":
    unittest.main()
