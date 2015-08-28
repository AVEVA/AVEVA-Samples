# qipy
# chad@osisoft.com

from urlparse import urlparse
import urllib
import httplib as http
import json
from QiType import QiType
from QiStream import QiStream
from QiTypeProperty import QiTypeProperty
from QiError import QiError

class QiClient(object):
    """description of class"""

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
        #conn = http.HTTPConnection(self.url)
        #conn.request("HEAD", "/Qi/Types", headers = self.__qi_headers())
        #response = conn.getresponse()        
        #if response.status != 200:
        #    raise QiError("Failed to connect to Qi endpoint {status}:{reason}".
        #                  format(status = response.status, reason = response.reason))


        print "Qi endpoint at {url}".format(url = self.url)

    
    # Qi Type
    
    def createType(self, qi_type):
        if qi_type is None:
            return
       
        if not isinstance(qi_type, QiType):
            return
  
        conn = http.HTTPConnection(self.url)
        conn.request("POST", "/Qi/Types/", qi_type.toString(), self.__qi_headers())
        response = conn.getresponse()
        
        if response.status == 302: # Found                         
            url = urlparse(response.getheader("Location"))            
            conn = http.HTTPConnection(self.url)
            conn.request("GET", url.path, headers = self.__qi_headers())            
            response = conn.getresponse()

        if response.status == 200 or response.status == 201:
            type = QiType.fromString(response.read().decode())
            conn.close()
            return type
        else:
            conn.close()
            raise QiError("Failed to create type. {status}:{reason}".format(status = response.status, reason = response.reason))
    
    def getTypes(self):
        conn = http.HTTPConnection(self.url)
        
        conn.request("GET", "/qi/types/", headers = self.__qi_headers())
        response = conn.getresponse()

        if response.status != 200:            
            conn.close()
            raise QiError("Failed to get QiTypes {status}:{reason}".
                          format(status = response.status, reason = response.reason))
        
        typesresponse = response.read().decode()
        conn.close()
        typeslist = json.loads(typesresponse)
        returnlist = []
        for typedict in typeslist:
            returnlist.append(QiType.fromDictionary(typedict))
        
        return returnlist

    def getType(self, type_id):
        conn = http.HTTPConnection(self.url)
        
        conn.request("GET", "/qi/types/" + type_id, headers = self.__qi_headers())
        response = conn.getresponse()
        if response.status != 200:            
            conn.close()
            raise QiError("Failed to get QiType, {type_id}. {status}:{reason}".
                          format(type_id = type_id, status = response.status, reason = response.reason))
        
        typesresponse = response.read().decode()
        conn.close()
        return QiType.fromString(typesresponse)        
                
    def deleteType(self, type_id):
        if type_id is None:
            return
        conn = http.HTTPConnection(self.url)
        conn.request('DELETE', '/Qi/Types/' + type_id, headers = self.__qi_headers())
        response = conn.getresponse()
        
        if response.status != 200:            
            conn.close()
            raise QiError("Failed to delete QiType, {type_id}. {status}:{reason}".
                          format(type_id = type_id, status = response.status, reason = response.reason))


    # Qi Stream

    def createStream(self, qi_stream):
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            return
   
        conn = http.HTTPConnection(self.url)
        conn.request("POST", "/qi/streams", qi_stream.toString(), self.__qi_headers())

        response = conn.getresponse()
     
        if response.status == 302:
            url =  urlparse(response.getheader("Location"))
            response.close()

            conn.request("GET", url.path, headers = self.__qi_headers())
            response = conn.getresponse()

        if response.status == 200 or response.status == 201:
            stream = QiStream.fromString(response.read().decode())
            conn.close()
            return stream
        else:
            conn.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))
        

    def getStream(self, stream_id):
        conn = http.HTTPConnection(self.url)
        
        conn.request("GET", "/qi/streams/" + stream_id, headers = self.__qi_headers())
        response = conn.getresponse()

        if response.status != 200:            
            conn.close()
            raise QiError("Failed to get QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        conn.close()
        return QiStream.fromDictionary(json.loads(streamResponse))        

    def getStreams(self):
        conn = http.HTTPConnection(self.url)
        
        conn.request("GET", "/qi/streams/", headers = self.__qi_headers())
        response = conn.getresponse()

        if response.status != 200:            
            conn.close()
            raise QiError("Failed to get QiStreams. {status}:{reason}".
                          format(status = response.status, reason = response.reason))
        
        streamssresponse = response.read().decode()
        conn.close()
        streamsslist = json.loads(streamssresponse)
        returnlist = []
        for streamdict in streamsslist:
            returnlist.append(QiStream.fromDictionary(streamdict))
        
        return returnlist

    def editStream(self, qi_stream): 
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            return
   
        conn = http.HTTPConnection(self.url)
        conn.request("PUT", "/qi/streams/" + qi_stream.Id, qi_stream.toString(), self.__qi_headers())

        response = conn.getresponse()
     
        if response.status != 200:
            conn.close()
            raise QiError("Failed to edit QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))

        conn.close()


    def deleteStream(self, stream_id):
        conn = http.HTTPConnection(self.url)
        
        conn.request("DELETE", "/qi/streams/" + stream_id, headers = self.__qi_headers())
        response = conn.getresponse()

        if response.status != 200:            
            conn.close()
            raise QiError("Failed to delete QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        conn.close()
    

    # Stream data

    def getLastValue(self, qi_stream):
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            raise TypeError("stream must be a valid QiStream")
         
        conn = http.HTTPConnection(self.url)
        conn.request("GET", "/qi/streams/" + qi_stream.Id + "/data/getlastvalue", 
                     headers = self.__qi_headers())
        response = conn.getresponse()

        if response.status != 200:            
            conn.close()
            raise QiError("Failed to get last value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        conn.close()
        return json.loads(streamResponse)

    def insertValue(self, qi_stream, value):
        """
        Insert the specified value into this Qi stream.
        The value parameter must be a dictionary of data matching
        the stream type. For example:
        {"Value": 102.3, "Timestamp": "2015-08-12T22:07:49.4472922Z" }
        """
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            raise TypeError("stream must be a valid QiStream")

        payload = json.dumps(value)

        conn = http.HTTPConnection(self.url)
        conn.request("POST", "/qi/streams/" + qi_stream.Id + "/data/insertvalue", 
                     payload, self.__qi_headers())

        response = conn.getresponse()

        if response.status != 200:
            conn.close()
            raise QiError("Failed to insert value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))
                
    def replaceValue(self, qi_stream, value):
        """
        Update the specified value, as matched by *key* type property
        into this Qi stream. The value parameter must be a dictionary of data matching
        the stream type. For example:
        {"Value": 102.3, "Timestamp": "2015-08-12T22:07:49.4472922Z" }
        """
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            raise TypeError("stream must be a valid QiStream")

        payload = json.dumps(value)

        conn = http.HTTPConnection(self.url)
        conn.request("PUT", "/qi/streams/" + qi_stream.Id + "/data/replaceValue", 
                     payload, self.__qi_headers())

        response = conn.getresponse()

        if response.status != 200:
            conn.close()
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))
            
    def removeValue(self, qi_stream, index):
        """
        Delete the value at the specified index. The value index is the data stored
        in the *key* type property of the Qi type. The index parameter must be a 
        string. For example:
        '2015-08-12T22:07:49.4472922Z'
        """
        if qi_stream is None:
            return

        if not isinstance(qi_stream, QiStream):
            raise TypeError("stream must be a valid QiStream")
               
        params = urllib.urlencode({"index": index})        
        conn = http.HTTPConnection(self.url)
        conn.request("DELETE", "/qi/streams/" + qi_stream.Id + "/data/removevalue?" + params, 
                     headers = self.__qi_headers())

        response = conn.getresponse()

        if response.status != 200:
            conn.close()
            raise QiError("Failed to remove value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = qi_stream.Id, status = response.status, reason = response.reason))
               
    # Batched data

    def inserValues(self, values):
        print "*** inserValues not implemented***"

        
    def updateValues(self, values):
        print "*** updateValues not implemented***"

        
    def deleteValues(self, values):
        print "*** deleteValues not implemented***"

    # private methods
    
    def __qi_headers(self):
        return {
            "QiTenant" : self.__tenant_id(),
            "Content-type": "application/json", 
            "Accept": "text/plain"
            }
            
    def __tenant_id(self):
        return "00000000-0000-0000-0000-000000000002"
