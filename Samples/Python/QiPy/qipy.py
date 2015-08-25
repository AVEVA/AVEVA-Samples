# qipy.py
# chad@osisoft.com
version = 0.1
def info():
	
	print "----------------------------------"
	print "  ___  _ ____"        
	print " / _ \(_)  _ \ _   _ "
	print "| | | | | |_) | | | |"
	print "| |_| | |  __/| |_| |"
	print " \__\_\_|_|    \__, |"
	print "               |___/ "
	
	
	print "Version "+ str(version)
	print "----------------------------------"
	
 

import urllib, httplib as http

class source:
	def __init__(self, url, port):
		self.url = url
		self.port = port
		print "Qi source at {url}:{port}".format(url = self.url, port = self.port)

	def connect(self):
		conn = http.HTTPConnection(self.url, self.port)
		params = urllib.urlencode({})
		headers = {
			"QiTenant" : "00000000-0000-0000-0000-000000000002",
			"Content-type": "application/json", 
			"Accept": "text/plain"
			}
		conn.request("GET", "/qi/types/", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
			
		
