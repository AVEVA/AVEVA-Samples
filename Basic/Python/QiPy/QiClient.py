from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json
from QiError import QiError
from QiType import QiType
from QiStream import QiStream
from QiStreamBehavior import QiStreamBehavior
from QiNamespace import QiNamespace
from QiBoundaryType import QiBoundaryType
from JsonEncoder import Encoder
import requests
import time

class QiClient(object):
    """description of class"""

    def __init__(self, tenant, url, resource, appId, appKey):
        self.__version = 0.1

        self.__tenant = tenant
        self.__uri = self.__validateUri(url)
        self.__resource = resource
        self.__appId = appId
        self.__appKey = appKey

        self.__authority = "https://login.windows.net/{tenant}/oauth2/token".format(tenant = self.__tenant)

        self.__token = ""
        self.__expiration = 0
        self.__getToken()

        self.__setPathAndQueryTemplates()

    @property
    def Version(self):
        return self.__version

    @property
    def Uri(self):
        return self.__uri

    def createNamespace(self, namespace):
        if namespace is None or not isinstance(namespace, QiNamespace):
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("Post", self.__namespacesPath.format(tenant_id = self.__tenant), namespace.toString(), headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status == 302: # Found
            url = urlparse(response.getheader("Location"))
            connection = http.HTTPSConnection(self.__uri)
            connection.request("GET", url.path, headers = self.__qiHeaders())            
            response = connection.getresponse()

        if response.status != 200 and response.status != 201:
            connection.close()
            raise QiError("Failed to create Namespace. {status}:{reason}".format(status = response.status, reason = response.reason))

        namespace = QiNamespace.fromString(response.read().decode())
        connection.close()
        return namespace

    def deleteNamespace(self, namespace_id):
        if namespace_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request('DELETE', self.__namespacesPath.format(tenant_id = self.__tenant) + "/" + namespace_id, headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()
        
        if response.status != 200:
            raise QiError("Failed to delete Namespace, {namespace_id}. {status}:{reason}".
                          format(namespace_id = namespace_id, status = response.status, reason = response.reason))
    
    def createType(self, namespace_id, type):
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, QiType):
            raise TypeError
        
        connection = http.HTTPSConnection(self.__uri)
        connection.request("POST", self.__typesPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), type.toString(), self.__qiHeaders())
        response = connection.getresponse()
        
        if response.status == 302: # Found
            url = urlparse(response.getheader("Location"))
            connection = http.HTTPSConnection(self.__uri)
            connection.request("GET", url.path, headers = self.__qiHeaders())            
            response = connection.getresponse()
        
        if response.status != 200 and response.status != 201:
            connection.close()
            raise QiError("Failed to create type. {status}:{reason}".format(status = response.status, reason = response.reason))

        type = QiType.fromString(response.read().decode())
        connection.close()
        return type

    def getType(self, namespace_id, type_id):
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError
        
        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", self.__typesPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + type_id, headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get QiType, {type_id}. {status}:{reason}".
                          format(type_id = type_id, status = response.status, reason = response.reason))
        
        typesresponse = response.read().decode()
        connection.close()
        return QiType.fromString(typesresponse)        
    
    def getTypes(self, namespace_id):
        if namespace_id is None:
            raise TypeError
        
        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", self.__typesPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), headers = self.__qiHeaders())
        response = connection.getresponse()
        
        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get QiTypes {status}:{reason}".format(status = response.status, reason = response.reason))

        content = json.loads(response.read().decode())
        results = []
        for item in content:
            results.append(QiType.fromDictionary(item))
        connection.close()
        return results
                
    def deleteType(self, namespace_id, type_id):
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError
        
        connection = http.HTTPSConnection(self.__uri)
        connection.request('DELETE', self.__typesPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + type_id, headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()
        
        if response.status != 200:
            raise QiError("Failed to delete QiType, {type_id}. {status}:{reason}".
                          format(type_id = type_id, status = response.status, reason = response.reason))

    def createBehavior(self, namespace_id, behavior):
        if namespace_id is None:
            raise TypeError
        if behavior is None or not isinstance(behavior, QiStreamBehavior):
            raise TypeError
        
        connection = http.HTTPSConnection(self.__uri)
        connection.request("POST", self.__behaviorsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), behavior.toString(), self.__qiHeaders())
        response = connection.getresponse()

        if response.status == 302: # Found
            url = urlparse(response.getheader("Location"))
            connection = http.HTTPSConnection(self.__uri)
            connection.request("GET", url.path, headers = self.__qiHeaders())            
            response = connection.getresponse()

        if response.status != 200 and response.status != 201:
            connection.close()
            raise QiError("Failed to create behavior. {status}:{reason}".format(status = response.status, reason = response.reason))

        string = response.read().decode()
        behavior = QiStreamBehavior.fromString(string)
        connection.close()
        return behavior

    def getBehavior(self, namespace_id, behavior_id):
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request('GET', self.__behaviorsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + behavior_id, headers = self.__qiHeaders())
        response = connection.getresponse()
        
        if response.status != 200:
            connection.close()
            raise QiError("Failed to delete QiType, {behaviorId}. {status}:{reason}".
                            format(behaviorId = behavior_id, status = response.status, reason = response.reason))

        string = response.read().decode()
        behavior = QiStreamBehavior.fromString(string)
        connection.close()
        return behavior

    def getBehaviors(self, namespace_id):
        if namespace_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request('GET', self.__behaviorsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), headers = self.__qiHeaders())
        response = connection.getresponse()
        
        if response.status != 200:
            connection.close()
            raise QiError("Failed to delete QiType, {behaviorId}. {status}:{reason}".
                            format(behaviorId = behavior_id, status = response.status, reason = response.reason))

        content = json.loads(response.read().decode())
        results = []
        for item in content:
            results.append(QiStreamBehavior.fromDictionary(item))
        connection.close()
        return results
            
    def deleteBehavior(self, namespace_id, behavior_id):
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request('DELETE', self.__behaviorsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + behavior_id, headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()
        
        if response.status != 200:
            raise QiError("Failed to delete QiBehavior, {behaviorId}. {status}:{reason}".
                            format(behaviorId = behavior_id, status = response.status, reason = response.reason))
                          
    def createStream(self, namespace_id, stream):
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("POST", self.__streamsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), stream.toString(), self.__qiHeaders())
        response = connection.getresponse()
        
        if response.status == 302:
            url = urlparse(response.getheader("Location"))
            connection = http.HTTPSConnection(self.__uri)
            connection.request("GET", url.path, headers = self.__qiHeaders())
            response = connection.getresponse()

        if response.status != 200 and response.status != 201:
            connection.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream.Id, status = response.status, reason = response.reason))

        stream = QiStream.fromString(response.read().decode())
        connection.close()
        return stream

    def getStream(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", self.__streamsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + stream_id, headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        connection.close()
        return QiStream.fromDictionary(json.loads(streamResponse))

    def getStreams(self, namespace_id):
        if namespace_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", self.__streamsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id), headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get QiStreams. {status}:{reason}".format(status = response.status, reason = response.reason))
        
        content = json.loads(response.read().decode())
        results = []
        for item in content:
            results.append(QiStream.fromDictionary(item))
        connection.close()
        return results

    def updateStream(self, namespace_id, stream): 
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("PUT", self.__streamsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + stream.Id, stream.toString(), self.__qiHeaders())
        response = connection.getresponse()
        connection.close()
     
        if response.status != 200:
            raise QiError("Failed to edit QiStream, {stream_id}. {status}:{reason}".format(stream_id = stream.Id, status = response.status, reason = response.reason))
        
    def deleteStream(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("DELETE", self.__streamsPath.format(tenant_id = self.__tenant, namespace_id = namespace_id) + '/' + stream_id, headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:            
            raise QiError("Failed to delete QiStream {stream_id}. {status}:{reason}".format(stream_id = stream_id, status = response.status, reason = response.reason))
        
    def insertValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError
            
        payload = json.dumps(value, cls = Encoder)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("POST", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "InsertValue"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()
        
        if response.status != 200:
            raise QiError("Failed to insert value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))

    def insertValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError
            
        payload = json.dumps(values, cls = Encoder)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("POST", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "InsertValues"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to insert values for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
    
    def updateValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError
            
        payload = json.dumps(value, cls = Encoder)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("PUT", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "UpdateValue"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))

    def updateValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError
            
        payload = json.dumps(values, cls = Encoder)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("PUT", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "UpdateValues"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
                          
    def replaceValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError
            
        payload = json.dumps(value)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("PUT", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "replaceValue"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
         
    def replaceValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError
            
        payload = json.dumps(values)
        connection = http.HTTPSConnection(self.__uri)
        connection.request("PUT", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "replaceValues"), 
            payload, self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
            
    def removeValue(self, namespace_id, stream_id, index):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError
            
        connection = http.HTTPSConnection(self.__uri)
        connection.request("DELETE", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = self.__removeSingleValueQuery.format(param = urllib.parse.urlencode({"index": index}))), 
            headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to remove value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
    
    def removeWindowValues(self, namespace_id, stream_id, start, end):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError
            
        connection = http.HTTPSConnection(self.__uri)
        connection.request("DELETE", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = self.__removeWindowValuesQuery.format(
                        start = urllib.parse.urlencode({"startIndex": start}),
                        end = urllib.parse.urlencode({"endIndex": end}))), 
            headers = self.__qiHeaders())
        response = connection.getresponse()
        connection.close()

        if response.status != 200:
            raise QiError("Failed to remove value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
    def getLastValue(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = "getlastvalue"), 
            headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get last value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        connection.close()
        return json.loads(streamResponse)
                   
    def getWindowValues(self, namespace_id, stream_id, start, end):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError
            
        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = self.__getWindowValuesQuery.format(start = urllib.parse.urlencode({"startIndex": start}),
                                                      end = urllib.parse.urlencode({"endIndex": end}))),
            headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get window values for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        connection.close()
        return json.loads(streamResponse)

    def getRangeValues(self, namespace_id, stream_id, start, skip, count, reverse, boundaryType):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if skip is None:
            raise TypeError
        if count is None:
            raise TypeError
        if reverse is None or not isinstance(reverse, bool):
            raise TypeError
        if boundaryType is None or not isinstance(boundaryType, QiBoundaryType):
            raise TypeError
            
        connection = http.HTTPSConnection(self.__uri)
        connection.request("GET", "{path}/{query}".format(
                path = self.__dataPath.format(tenant_id = self.__tenant, namespace_id = namespace_id, stream_id = stream_id), 
                query = self.__getRangeValuesQuery.format(start = start, 
                                                     skip = str(skip),
                                                     count = str(count),
                                                     reverse = str(reverse),
                                                     boundaryType = str(boundaryType.name))),
            headers = self.__qiHeaders())
        response = connection.getresponse()

        if response.status != 200:            
            connection.close()
            raise QiError("Failed to get range values for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id = stream_id, status = response.status, reason = response.reason))
        
        streamResponse = response.read().decode()
        connection.close()
        return json.loads(streamResponse)
        
    # private methods

    def __getToken(self): 
        # tokens take a while to expire, so don't bother refreshing until some
        # time has passed
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        response = requests.post(self.__authority, 
                                 data = { 'grant_type' : 'client_credentials',
                                          'client_id' : self.__appId,
                                          'client_secret' : self.__appKey,
                                          'resource' : self.__resource
                                        })
        if response.status_code != 200:
            raise Exception("Failed to retrieve AAD Token")

        self.__expiration = float(response.json()['expires_on'])
        self.__token = response.json()['access_token']
        return self.__token
            
    def __qiHeaders(self):
        return { "Authorization" : "bearer %s" % self.__getToken(),
                 "Content-type": "application/json", 
                 "Accept": "text/plain"
               }

    def __validateUri(self, url):
        splitUri = urlparse(url)
        return splitUri.netloc + splitUri.path

    def __setPathAndQueryTemplates(self):
        self.__namespacesPath = "/Qi/{tenant_id}/Namespaces"
        self.__typesPath = "/Qi/{tenant_id}/{namespace_id}/Types"
        self.__behaviorsPath = "/Qi/{tenant_id}/{namespace_id}/Behaviors"
        self.__streamsPath = "/Qi/{tenant_id}/{namespace_id}/Streams"
        self.__dataPath = "/Qi/{tenant_id}/{namespace_id}/Streams/{stream_id}/Data"

        self.__removeSingleValueQuery = "RemoveValue?{param}"
        self.__removeWindowValuesQuery = "RemoveWindowValues?{start}&{end}"
        self.__getWindowValuesQuery = "GetWindowValues?{start}&{end}"
        self.__getRangeValuesQuery = "GetRangeValues?startIndex={start}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}"
