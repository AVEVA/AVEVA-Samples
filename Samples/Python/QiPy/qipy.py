# qipy.py
# chad@osisoft.com

import urllib
import httplib as http


class QiClient:
    def __init__(self, url, apikey):
        self.url = url
        version = 0.1

        print "----------------------------------"
        print "  ___  _ ____"        
        print " / _ \(_)  _ \ _   _ "
        print "| | | | | |_) | | | |"
        print "| |_| | |  __/| |_| |"
        print " \__\_\_|_|    \__, |"
        print "               |___/ "	
        print "Version "+ str(version)
        print "----------------------------------"
        print "Qi channel at {url}".format(url = self.url)

    def getTypes(self):
        conn = http.HTTPConnection(self.url)
        params = urllib.urlencode({})
        
        conn.request("GET", "/qi/types/", params, self._qi_headers())
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data

    def _qi_headers(self):
        return {
            "QiTenant" : self._tenant_id(),
            "Content-type": "application/json", 
            "Accept": "text/plain"
            }
            
    def _tenant_id(self):
        return "00000000-0000-0000-0000-000000000002";
