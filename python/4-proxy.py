import httplib
import json
import os
import time
import unittest
from selenium import webdriver

proxy_host = "localhost"
proxy_api_port = 9090

"""
Send REST API request to the BrowserMob Proxy
"""
def _proxy_request(http_request_type, url):
    conn = httplib.HTTPConnection(proxy_host, proxy_api_port)
    conn.request(http_request_type, url)
    response = conn.getresponse()
    return response.read()

def main():
    print "Staring new proxy port..."
    data = json.loads(_proxy_request("POST", "/proxy"))
    proxy_port = data['port']
    proxy_base_url = "/proxy/" + str(proxy_port)

    print "HTTP Proxy up and running at: " + proxy_host + ":" + str(proxy_port)

    print "Telling proxy to record HTTP traffic..."
    _proxy_request("PUT", proxy_base_url + "/har?initialPageRef=ProxyTest")

    raw_input("Press the any key to get HAR from proxy...")
    har = _proxy_request("GET", proxy_base_url + "/har")

    print json.dumps(json.loads(har), sort_keys=True, indent=4)

    print "Ending proxy connection..."
    _proxy_request("DELETE", proxy_base_url)


if __name__ == "__main__":
    main()
