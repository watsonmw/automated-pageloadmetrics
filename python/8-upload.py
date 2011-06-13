import httplib, urllib
import json
import os
import time
import sys
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.common import exceptions

proxy_host = "localhost"
proxy_api_port = 9090

harpoon_host = "labs.webmetrics.com:8080"
harpoon_url = "/test-results"

class Timeout():
    def __init__(self, timeout, name):
        self.timeout = timeout
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        runtime =  time.time() - self.start
        if (runtime > self.timeout):
            msg = '"{0}" took {1} seconds exceeding timeout of {2} seconds'
            raise Exception(msg.format(self.name , runtime, self.timeout))
        else:
            print '"{0}" took {1} seconds'.format(self.name , runtime)

class WebDriverTest(unittest.TestCase):
    def log_errors(func):
        def wrapper(*arg):
            that = arg[0]
            that.e = None
            try:
              return func(*arg)
            except:
              that.e = sys.exc_info()
              raise
        return wrapper

    """
    Go to google and search for cheese!
    """
    @log_errors
    def testSearch(self):
        with Timeout(10, "Navigate to google.com"):
            self.driver.get("http://www.google.com")

        cheese = None

        with Timeout(10, "Search for cheese!"):
            element = self.driver.find_element_by_name("q")
            element.send_keys("Cheese!")
            element.submit()
            find_cheese = lambda: self.driver.find_element_by_link_text("Cheese - Wikipedia, the free encyclopedia")
            cheese = self.wait_for(find_cheese, 10)

        with Timeout(10, "Click the wikipedia link!"):
            cheese.click()

    """
    Test setup.
     - Connect to the BrowserMob proxy and create a new proxy port.
     - Bring up FireFox on that port
    """
    def setUp(self):
        data = json.loads(self._proxy_request("POST", "/proxy"))
        proxy_port = data['port']
        self.proxy_base_url = "/proxy/" + str(proxy_port)

        self._proxy_request("PUT", self.proxy_base_url + "/har?initialPageRef=" + self._testname());

        """Setup the firefox profile to attach to the proxy"""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.http", "\"" + proxy_host + "\"")
        profile.set_preference("network.proxy.http_port", proxy_port)
        profile.set_preference("network.proxy.type", 1)
        profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile = profile)

    """
    Save off screenshot and HAR for the test
    """
    def tearDown(self):
        """ Make the logs dir"""
        dir = "logs/" + str(time.time()) + "/"
        if not os.path.exists(dir):
            os.makedirs(dir)

        print "Saving results to " + dir
        base_file = dir + self._testname()

        if (self.e):
            print "  Saving error message..."
            f = open(base_file + ".txt", 'w')
            f.write(str(self.e))
            f.close

        print "  Saving screenshot..." 
        self.driver.save_screenshot(base_file + ".png")

        self.driver.quit()

        print "  Saving har..."
        har = self._proxy_request("GET", self.proxy_base_url + "/har")
        har_file =  base_file + '.har'
        f = open(har_file, 'w')
        f.write(self._pretty_print(har))
        f.close

        print "  Uploading har..."
        self._harpoon_upload(har)

        self._proxy_request("DELETE", self.proxy_base_url)

    """
    Wait for an element to exist.  Takes a lamdba function that finds the element
    and a timeout value.
    """
    def wait_for(self, func, timeout):
        start_time = time.time()
        cur_time  = start_time
        while (cur_time - start_time < timeout):
            try:
                return func()
            except(exceptions.NoSuchElementException):
                pass

            cur_time = time.time()
            time.sleep(0.2)

        raise Exception("Timed out looking for element after " + timeout + " seconds")

    """
    Return the current test name
    """
    def _testname(self):
        return self.id().split(".").pop()

    """
    Send an REST API request to the BrowserMob Proxy
    """
    def _proxy_request(self, http_request_type, url):
        conn = httplib.HTTPConnection(proxy_host, proxy_api_port)
        conn.request(http_request_type, url)
        response = conn.getresponse()
        return response.read()

    """
    Take in a json string and return a pretty printed one
    """
    def _pretty_print(self, s):
        return json.dumps(json.loads(s), sort_keys=True, indent=4)

    """
    Upload to HAR and test results to Harpoon
    """
    def _harpoon_upload(self, har_string):
        har = json.loads(har_string)

        # Use the first URL from the logs as the description
        description = ""
        try:
            entries = har['log']['entries']
            description = entries[0]['request']['url']
        except:
            pass

        conn = httplib.HTTPConnection(harpoon_host)

        headers = {
            }

        result = {
            'apiKey': None,
            'name': self._testname(),
            'description': description,
            'har': har,
            'created': int(time.time() * 1000)
            }

        if self.e:
            result['error'] = {
                'code': None,
                'message': str(self.e[1]),
                'file': None,
                'line': None,
                }
            result['success'] = False
        else:
            result['success'] = True

        body = json.dumps(result)

        conn.request("POST", harpoon_url, body, headers)
        response = conn.getresponse()
        print response.read()
        conn.close()

if __name__ == "__main__":
    unittest.main()
