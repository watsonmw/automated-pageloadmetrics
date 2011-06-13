import httplib
import json
import os
import time
import sys
import unittest
from selenium import webdriver
from selenium.common import exceptions

proxy_host = "localhost"
proxy_api_port = 9090
logs_dir = "logs/" + str(time.time()) + "/"

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
    """
    Load the page and record the time it took
    """
    def test_PageLoad(self):
        with Timeout(30, "Navigate to webmetrics.com"):
            self.driver.get("http://www.webmetrics.com")

    """
    Now load the page without 3rd party content
    """
    def test_PageLoadNoThirdPartyContent(self):
        """Tell the proxy to only allow requests to webmetrics.com"""
        self._proxy_request("PUT", self.proxy_base_url +
            "/whitelist?regex=.*webmetrics\\.com.*")

        with Timeout(30, "Navigate to webmetrics.com (no 3rd party content)"):
            self.driver.get("http://www.webmetrics.com")

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
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        print "Saving results to " + logs_dir
        base_file = logs_dir + self._testname()

        print "  Saving screenshot..."
        self.driver.save_screenshot(base_file + ".png")

        self.driver.quit()

        print "  Saving har..."
        har = self._proxy_request("GET", self.proxy_base_url + "/har")
        har_file =  base_file + '.har'

        f = open(har_file, 'w')
        f.write(self._pretty_print(har))
        f.close
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


if __name__ == "__main__":
    unittest.main()
