import httplib
import json
import os
import time
import sys
import unittest
from selenium import webdriver

"""
class Timeout
Prints execution times for blocks of code.
Raises a timeout exception if the block took longer than the
specified timeout in seconds to complete.
"""
class Timeout():
    """
    Takes a timeout in seconds and name to indentify the block
    """
    def __init__(self, timeout, name):
        self.timeout = timeout
        self.name = name

    def __enter__(self):
        self.start = time.time()

    """
    On block exit check that the block executed within the timeout.
    If it did, print the time the block took to execute.
    If it did not, raise a timeout exception.
    """
    def __exit__(self, *args):
        runtime =  time.time() - self.start
        if (runtime > self.timeout):
            msg = '"{0}" exceeded timeout of {1} seconds'.format(self.name , self.timeout)
            raise Exception(msg)
        else:
            print '"{0}" took {1} seconds'.format(self.name , runtime)

class TimeoutTests(unittest.TestCase):
    """
    Navigate to google and search for Cheese!
    The test is split into two steps.  Each step has a description
    and a timeout.
    """
    def testSearch(self):
        with Timeout(10, "Navigate to google.com"):
            self.driver.get("http://www.google.com")

        with Timeout(10, "Search for cheese!"):
            element = self.driver.find_element_by_name("q")
            element.send_keys("Cheese!")
            element.submit()

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
