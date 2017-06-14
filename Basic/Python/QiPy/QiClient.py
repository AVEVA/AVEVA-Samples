from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

import adal as adal

from QiError import QiError
from QiType import QiType
from QiStream import QiStream
from QiStreamBehavior import QiStreamBehavior
from QiBoundaryType import QiBoundaryType
from JsonEncoder import Encoder
import requests
import time


class QiClient(object):
    """description of class"""

    def __init__(self, tenant, url, resource, authority, appId, appKey):
        self.__version = 0.1

        self.__tenant = tenant
        # self.__uri = self.__validateUri(url)
        self.__uri = url
        self.__resource = resource
        self.__appId = appId
        self.__appKey = appKey

        self.__authority = authority

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

    ### used for local debugging only ###
    #####################################
    def createTenant(self):
        tenant_dict = {'Id' : 'testtenant'}
        payload = json.dumps(tenant_dict)
        response = requests.post("http://localhost:5000/api/Tenants", data=payload, headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating tenant")
        else:
            response.close()
            raise QiError("Failed to create tenant. {status}:{reason}".format(status=response.status_code, reason=response.reason))

        response.close()

    def createNamespace(self, namespace_id):
        namespace_dict = {'Id' : namespace_id}
        payload = json.dumps(namespace_dict)
        response = requests.post("http://localhost:5000/api/Tenants/" + self.__tenant + "/Namespaces", data=payload, headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating namespace")
        else:
            response.close()
            raise QiError("Failed to create namespace. {status}:{reason}".format(status=response.status_code, reason=response.reason))

        response.close()

    def getNamespaces(self):
        response = requests.get("http://localhost:5000/api/Tenants/" + self.__tenant + "/Namespaces", headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeed in getting namespaces")
        else:
            response.close()
            raise QiError("Failed to get namespaces. {status}:{reason}".format(status=response.status_code, reason=response.reason))

        content = json.loads(response.content)
        response.close()
        return content

    #####################################
    #####################################

    def createType(self, namespace_id, type):
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, QiType):
            raise TypeError

        response = requests.post(
            self.__uri + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=type.toString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:  # Succees
            print("Succeeded in creating type")
        else:
            response.close()
            raise QiError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.reason))

        type = QiType.fromString(response.content)
        response.close()
        return type

    def getType(self, namespace_id, type_id):
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting type")
        else:
            response.close()
            raise QiError("Failed to get QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.reason))

        typesresponse = response.content
        response.close()
        return QiType.fromString(typesresponse)

    def getTypes(self, namespace_id):
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all types")
        else:
            response.close()
            raise QiError("Failed to get all QiTypes. {status}:{reason}".
                          format(status=response.status_code, reason=response.reason))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiType.fromDictionary(item))
        response.close()
        return results

    def deleteType(self, namespace_id, type_id):
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.__uri + self.__getTypePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting type")
        else:
            response.close()
            raise QiError("Failed to delete QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.reason))

        response.close()

    def createBehavior(self, namespace_id, behavior):
        if namespace_id is None:
            raise TypeError
        if behavior is None or not isinstance(behavior, QiStreamBehavior):
            raise TypeError

        response = requests.post(
            self.__uri + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=behavior.toString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating behavior")
        else:
            response.close()
            raise QiError("Failed to create QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior.Id, status=response.status_code, reason=response.reason))

        string = response.content
        behavior = QiStreamBehavior.fromString(string)
        response.close()
        return behavior

    def getBehavior(self, namespace_id, behavior_id):
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__getBehaviorPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       behavior_id=behavior_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting behavior")
        else:
            response.close()
            raise QiError("Failed to get QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.reason))

        string = response.content
        behavior = QiStreamBehavior.fromString(string)
        response.close()
        return behavior

    def getBehaviors(self, namespace_id, skip, count):
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__getBehaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all behaviors")
        else:
            response.close()
            raise QiError("Failed to get all QiBehaviors. {status}:{reason}".
                          format(status=response.status_code, reason=response.reason))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStreamBehavior.fromDictionary(item))
        response.close()
        return results

    def deleteBehavior(self, namespace_id, behavior_id):
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.delete(
            self.__uri + self.__getBehaviorPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        behavior_id=behavior_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting behavior")
        else:
            response.close()
            raise QiError("Failed to delete QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.reason))

        response.close()

    def createStream(self, namespace_id, stream):
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        response = requests.post(
            self.__uri + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=stream.toString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating stream")

        if response.status_code != 200 and response.status_code != 201:
            response.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.reason))

        stream = QiStream.fromString(response.content)
        response.close()
        return stream

    def getStream(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting stream")
        else:
            response.close()
            raise QiError("Failed to get QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        streamResponse = response.content
        response.close()
        return QiStream.fromDictionary(json.loads(streamResponse))

    def getStreams(self, namespace_id, query, skip, count):
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError
        if skip is None:
            raise TypeError
        if count is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all streams")
        else:
            response.close()
            raise QiError("Failed to get all QiStreams. {status}:{reason}".
                          format(status=response.status_code, reason=response.reason))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStream.fromDictionary(item))
        response.close()
        return results

    def updateStream(self, namespace_id, stream):
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        response = requests.put(
            self.__uri + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream.Id), data=stream.toString(), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating stream")
        else:
            response.close()
            raise QiError("Failed to update QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.reason))

        response.close()

    def deleteStream(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.__uri + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting stream")
        else:
            response.close()
            raise QiError("Failed to delete QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def insertValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.post(
            self.__uri + self.__insertValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in inserting value")
        else:
            response.close()
            raise QiError("Failed to insert value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))
        response.close()

    def insertValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.post(
            self.__uri + self.__insertValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in inserting multiple values")
        else:
            raise QiError("Failed to insert multiple values for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

    def getValue(self, namespace_id, stream_id, index):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError

        response = requests.get(self.__uri + self.__getSingleQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=index), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting value")
        else:
            response.close()
            raise QiError("Failed to get value for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        streamResponse = response.content
        response.close()
        return json.loads(streamResponse)

    def getLastValue(self, namespace_id, stream_id):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__uri + self.__getLastValue.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                    stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting last value")
        else:
            response.close()
            raise QiError("Failed to get last value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        streamResponse = response.content
        response.close()
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

        response = requests.get(
            self.__uri + self.__getWindowValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                            stream_id=stream_id, start=start, end=end),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting window values")
        else:
            response.close()
            raise QiError("Failed to get window values for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        streamResponse = response.content
        response.close()
        return json.loads(streamResponse)

    def getRangeValues(self, namespace_id, stream_id, start, skip, count, reverse, boundary_type):
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
        if boundary_type is None or not isinstance(boundary_type, QiBoundaryType):
            raise TypeError

        response = requests.get(
            self.__uri + self.__getRangeValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                           stream_id=stream_id, start=start, skip=skip, count=count,
                                                           reverse=reverse, boundary_type=boundary_type.value), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting range of values")
        else:
            response.close()
            raise QiError("Failed to get range of values from QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        stream_response = response.content
        response.close()
        return json.loads(stream_response)

    def updateValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.put(self.__uri + self.__updateValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating value")
        else:
            response.close()
            raise QiError("Failed to update value for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def updateValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.put(self.__uri + self.__updateValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating all values")
        else:
            response.close()
            raise QiError("Failed to update all values for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def replaceValue(self, namespace_id, stream_id, value):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.put(
            self.__uri + self.__replaceValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in replacing value")
        else:
            response.close()
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def replaceValues(self, namespace_id, stream_id, values):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.put(self.__uri + self.__replaceValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                                             stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in replacing all values")
        else:
            response.close()
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def removeValue(self, namespace_id, stream_id, index):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError

        response = requests.delete(
            self.__uri + self.__removeSingleValueQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                              stream_id=stream_id, index=index), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in removing value")
        else:
            response.close()
            raise QiError("Failed to remove value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    def removeWindowValues(self, namespace_id, stream_id, start, end):
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.delete(self.__uri + self.__removeWindowValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, start=start, end=end), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in removing all values")
        else:
            response.close()
            raise QiError("Failed to remove all values for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.reason))

        response.close()

    # private methods

    def __getToken(self):
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        context = adal.AuthenticationContext(self.__authority, validate_authority=True)
        token = context.acquire_token_with_client_credentials(self.__resource, self.__appId, self.__appKey)

        if token is None:
            raise Exception("Failed to retrieve AAD Token")

        self.__expiration = float(token['expiresIn']) + time.time()
        self.__token = token['accessToken']
        return self.__token

    def __qiHeaders(self):
        return {"Authorization": "bearer %s" % self.__getToken(),
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
                }

    def __validateUri(self, url):
        splitUri = urlparse(url)
        return splitUri.netloc + splitUri.path

    def __setPathAndQueryTemplates(self):
        self.__basePath = "/api/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types"
        self.__getTypePath = self.__typesPath + "/{type_id}"  # deleting uses this same URI
        self.__getTypesPath = self.__typesPath + "?skip={skip}&count={count}"
        self.__behaviorsPath = self.__basePath + "/Behaviors"
        self.__getBehaviorPath = self.__behaviorsPath + "/{behavior_id}"  # deleting uses this same URI
        self.__getBehaviorsPath = self.__behaviorsPath + "?skip={skip}&count={count}"
        self.__streamsPath = self.__basePath + "/Streams"
        self.__getStreamPath = self.__streamsPath + "/{stream_id}"  # updating and deleting uses this same URI

        self.__dataPath = self.__basePath + "/Streams/{stream_id}/Data"
        self.__insertValuePath = self.__dataPath + "/InsertValue"
        self.__insertValuesPath = self.__dataPath + "/InsertValues"
        self.__replaceValuePath = self.__dataPath + "/ReplaceValue"
        self.__replaceValuesPath = self.__dataPath + "/ReplaceValues"
        self.__updateValuePath = self.__dataPath + "/UpdateValue"
        self.__updateValuesPath = self.__dataPath + "/UpdateValues"
        self.__getSingleQuery = self.__dataPath + "/GetValue?index={index}"
        self.__getLastValue = self.__dataPath + "/GetLastValue"
        self.__getWindowValuesQuery = self.__dataPath + "/GetWindowValues?startIndex={start}&endIndex={end}"
        self.__getRangeValuesQuery = self.__dataPath + "/GetRangeValues?startIndex={start}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundary_type}"
        self.__removeSingleValueQuery = self.__dataPath + "/RemoveValue?index={index}"
        self.__removeWindowValuesQuery = self.__dataPath + "/RemoveWindowValues?startIndex={start}&endIndex={end}"
