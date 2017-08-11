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
    """Handles communication with Qi Service"""

    def __init__(self, tenant, url, resource, authority, clientId, clientSecret):
        self.__version = 0.1

        self.__tenant = tenant
        self.__url = url
        self.__resource = resource
        self.__clientId = clientId
        self.__clientSecret = clientSecret

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
        return self.__url

    def createType(self, namespace_id, type):
        """Tells Qi Service to create a type based on local 'type' object"""
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, QiType):
            raise TypeError

        response = requests.post(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=type.toJsonString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating type")
        else:
            response.close()
            raise QiError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))

        type = QiType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getType(self, namespace_id, type_id):
        """Retrieves the type specified by 'type_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting type")
        else:
            response.close()
            raise QiError("Failed to get QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))

        type = QiType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getTypes(self, namespace_id):
        """Retrieves a list of types associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all types")
        else:
            response.close()
            raise QiError("Failed to get all QiTypes. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        types = json.loads(response.content)
        results = []
        for t in types:
            results.append(QiType.fromJson(t))
        response.close()
        return results

    def deleteType(self, namespace_id, type_id):
        """Tells Qi Service to delete the type specified by 'type_id'"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__getTypePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting type")
        else:
            response.close()
            raise QiError("Failed to delete QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))

        response.close()

    def createBehavior(self, namespace_id, behavior):
        """Tells Qi Service to create a behavior based on a local QiBehavior object"""
        if namespace_id is None:
            raise TypeError
        if behavior is None or not isinstance(behavior, QiStreamBehavior):
            raise TypeError

        response = requests.post(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=behavior.toJsonString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating behavior")
        else:
            response.close()
            raise QiError("Failed to create QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior.Id, status=response.status_code, reason=response.text))

        string = response.content
        behavior = QiStreamBehavior.fromJson(json.loads(string))
        response.close()
        return behavior

    def getBehavior(self, namespace_id, behavior_id):
        """Retrieves the behavior specified by 'behavior_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getBehaviorPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       behavior_id=behavior_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting behavior")
        else:
            response.close()
            raise QiError("Failed to get QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.text))

        string = response.content
        behavior = QiStreamBehavior.fromJson(json.loads(string))
        response.close()
        return behavior

    def getBehaviors(self, namespace_id, skip, count):
        """Retrieves a list of behaviors associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all behaviors")
        else:
            response.close()
            raise QiError("Failed to get all QiBehaviors. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStreamBehavior.fromJson(item))
        response.close()
        return results

    def deleteBehavior(self, namespace_id, behavior_id):
        """Tells Qi Service to delete the behavior with the specified 'behavior_id'"""
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__getBehaviorPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        behavior_id=behavior_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting behavior")
        else:
            response.close()
            raise QiError("Failed to delete QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.text))

        response.close()

    def createStream(self, namespace_id, stream):
        """Tells Qi Service to create a stream based on the local 'stream' QiStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        response = requests.post(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            data=stream.toJsonString(), headers=self.__qiHeaders())

        if response.status_code == 200 or response.status_code == 201:
            print("Succeeded in creating stream")

        if response.status_code != 200 and response.status_code != 201:
            response.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        stream = QiStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def getStream(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Qi Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting stream")
        else:
            response.close()
            raise QiError("Failed to get QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        streamResponse = QiStream.fromJson(json.loads(response.content))
        response.close()
        return streamResponse

    def getStreams(self, namespace_id, query):
        """Retrieves a list of streams associated with 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting all streams")
        else:
            response.close()
            raise QiError("Failed to get all QiStreams. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStream.fromJson(item))
        response.close()
        return results

    def updateStream(self, namespace_id, stream):
        """Tells Qi Service to update the stream specified by the 'stream' local object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        response = requests.put(
            self.__url + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream.Id), data=stream.toJsonString(), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating stream")
        else:
            response.close()
            raise QiError("Failed to update QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteStream(self, namespace_id, stream_id):
        """Tells Qi Service to delete the stream speficied by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__getStreamPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                     stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in deleting stream")
        else:
            response.close()
            raise QiError("Failed to delete QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def insertValue(self, namespace_id, stream_id, value):
        """Tells Qi Service to insert a value, described by the local object 'value', into
        the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.post(
            self.__url + self.__insertValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in inserting value")
        else:
            response.close()
            raise QiError("Failed to insert value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))
        response.close()

    def insertValues(self, namespace_id, stream_id, values):
        """Tells Qi Service to insert the values, defined by the list 'values', into 
        the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.post(
            self.__url + self.__insertValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in inserting multiple values")
        else:
            raise QiError("Failed to insert multiple values for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def getValue(self, namespace_id, stream_id, qi_value_class, key):
        """Retrieves JSON object from Qi Service for value specified by 'key' from Qi Service 
        (which corresponds to the key defined by the value's type)"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if key is None:
            raise TypeError

        response = requests.get(self.__url + self.__getSingleQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=key), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting value")
        else:
            response.close()
            raise QiError("Failed to get value for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = response.content
        response.close()
        return qi_value_class.fromJson(json.loads(content))

    def getLastValue(self, namespace_id, stream_id, qi_value_class):
        """Retrieves JSON object from Qi Service the last value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if qi_value_class is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getLastValue.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                    stream_id=stream_id), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting last value")
        else:
            response.close()
            raise QiError("Failed to get last value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = response.content
        response.close()
        return qi_value_class.fromJson(json.loads(content))

    def getWindowValues(self, namespace_id, stream_id, qi_value_class, start, end):
        """Retrieves JSON object representing a window of values from the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if qi_value_class is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getWindowValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                            stream_id=stream_id, start=start, end=end),
            headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting window values")
        else:
            response.close()
            raise QiError("Failed to get window values for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        values = []
        for c in content:
            values.append(qi_value_class.fromJson(c))
        return values

    def getRangeValues(self, namespace_id, stream_id, qi_value_class, start, skip, count, reverse, boundary_type):
        """Retrieves JSON object representing a range of values from the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if qi_value_class is None:
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
            self.__url + self.__getRangeValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                           stream_id=stream_id, start=start, skip=skip, count=count,
                                                           reverse=reverse, boundary_type=boundary_type.value), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in getting range of values")
        else:
            response.close()
            raise QiError("Failed to get range of values from QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        values = []
        for c in content:
            values.append(qi_value_class.fromJson(c))
        return values

    def updateValue(self, namespace_id, stream_id, value):
        """Tells Qi Service to update the value described by 'value', a local QiValue object"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.put(self.__url + self.__updateValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating value")
        else:
            response.close()
            raise QiError("Failed to update value for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def updateValues(self, namespace_id, stream_id, values):
        """Tells Qi Service to update values defined by the QiValue list, 'values'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.put(self.__url + self.__updateValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in updating all values")
        else:
            response.close()
            raise QiError("Failed to update all values for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def replaceValue(self, namespace_id, stream_id, value):
        """Tells Qi Service to replace the value specified by 'value'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        payload = json.dumps(value, cls=Encoder)
        response = requests.put(
            self.__url + self.__replaceValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in replacing value")
        else:
            response.close()
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def replaceValues(self, namespace_id, stream_id, values):
        """Tells Qi Service to replace the values defined by the list 'values'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        payload = json.dumps(values, cls=Encoder)
        response = requests.put(self.__url + self.__replaceValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                                             stream_id=stream_id), data=payload, headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in replacing all values")
        else:
            response.close()
            raise QiError("Failed to replace value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def removeValue(self, namespace_id, stream_id, key):
        """Tells Qi Service to delete the value with a key property matching 'key'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if key is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__removeSingleValueQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                              stream_id=stream_id, index=key), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in removing value")
        else:
            response.close()
            raise QiError("Failed to remove value for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def removeWindowValues(self, namespace_id, stream_id, start, end):
        """Tells Qi Service to delete a window of values in the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.delete(self.__url + self.__removeWindowValuesQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, start=start, end=end), headers=self.__qiHeaders())

        if response.status_code == 200:
            print("Succeeded in removing all values")
        else:
            response.close()
            raise QiError("Failed to remove all values for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    # private methods

    def __getToken(self):
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        context = adal.AuthenticationContext(self.__authority, validate_authority=True)
        token = context.acquire_token_with_client_credentials(self.__resource, self.__clientId, self.__clientSecret)

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
