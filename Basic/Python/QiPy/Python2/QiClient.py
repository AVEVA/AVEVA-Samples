
import urlparse
import json

import adal as adal

from QiError import QiError
from QiType import QiType
from QiStream import QiStream
from QiView import QiView
from QiViewMap import QiViewMap
from QiStreamBehavior import QiStreamBehavior
from QiBoundaryType import QiBoundaryType

import requests
import time


class QiClient(object):
    """Handles communication with Qi Service"""

    def __init__(self, tenant, url, resource, authority, clientId, clientSecret):
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
    def Uri(self):
        return self.__url

    def getType(self, namespace_id, type_id):
        """Retrieves the type specified by 'type_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        type = QiType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getTypeReferenceCount(self, namespace_id, type_id):
        """Retrieves the number of times the type is referenced"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id) + "/ReferenceCount",
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiType reference count, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        count = json.loads(response.content)
        response.close()
        return int(count)

    def getTypes(self, namespace_id, skip=0, count=100):
        """Retrieves a list of types associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getTypesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get all QiTypes. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        types = json.loads(response.content)
        results = []
        for t in types:
            results.append(QiType.fromJson(t))
        response.close()
        return results

    def getOrCreateType(self, namespace_id, type):
        """Tells Qi Service to create a type based on local 'type' or get if existing type matches"""
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, QiType):
            raise TypeError

        response = requests.post(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type.Id),
            data=type.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))
        
        type = QiType.fromJson(json.loads(response.content))
        response.close()
        return type

    def createOrUpdateType(self, namespace_id, type):
        """Tells Qi Service to create a type based on local 'type' object"""
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, QiType):
            raise TypeError

        response = requests.put(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type.Id),
            data=type.toJson(), headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))
        
        response.close()

    def deleteType(self, namespace_id, type_id):
        """Tells Qi Service to delete the type specified by 'type_id'"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__typesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__qiHeaders())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to delete QiType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))

        response.close()

    def getBehavior(self, namespace_id, behavior_id):
        """Retrieves the behavior specified by 'behavior_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
            behavior_id=behavior_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.text))

        behavior = QiStreamBehavior.fromJson(json.loads(response.content))
        response.close()
        return behavior

    def getBehaviorReferenceCount(self, namespace_id, behavior_id):
        """Retrieves the behavior reference count"""
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, behavior_id=behavior_id) + "/ReferenceCount", 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiBehavior reference count, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.text))

        behavior = QiStreamBehavior.fromJson(json.loads(response.content))
        response.close()
        return behavior

    def getBehaviors(self, namespace_id, skip=0, count=100):
        """Retrieves a list of behaviors associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get all QiBehaviors. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStreamBehavior.fromJson(item))
        response.close()
        return results

    def getOrCreateBehavior(self, namespace_id, behavior):
        """Tells Qi Service to create a behavior based on a local QiBehavior object"""
        if namespace_id is None:
            raise TypeError
        if behavior is None or not isinstance(behavior, QiStreamBehavior):
            raise TypeError

        response = requests.post(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, behavior_id=behavior.Id),
            data=behavior.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior.Id, status=response.status_code, reason=response.text))

        behavior = QiStreamBehavior.fromJson(json.loads(response.content))
        response.close()
        return behavior

    def createOrUpdateBehavior(self, namespace_id, behavior):
        """Tells Qi Service to create a behavior based on a local QiBehavior object"""
        if namespace_id is None:
            raise TypeError
        if behavior is None or not isinstance(behavior, QiStreamBehavior):
            raise TypeError

        response = requests.put(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, behavior_id=behavior.Id),
            data=behavior.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteBehavior(self, namespace_id, behavior_id):
        """Tells Qi Service to delete the behavior with the specified 'behavior_id'"""
        if namespace_id is None:
            raise TypeError
        if behavior_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__behaviorsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, behavior_id=behavior_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to delete QiBehavior, {behavior_id}. {status}:{reason}".
                          format(behavior_id=behavior_id, status=response.status_code, reason=response.text))

        response.close()

    def getView(self, namespace_id, view_id):
        """Retrieves the view specified by 'view_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if view_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id,
            view_id=view_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiView, {view_id}. {status}:{reason}".
                          format(view_id=view_id, status=response.status_code, reason=response.text))

        view = QiView.fromJson(json.loads(response.content))
        response.close()
        return view

    def getViewMap(self, namespace_id, view_id):
        """Retrieves the view map specified by 'view_id' from Qi Service"""
        if namespace_id is None:
            raise TypeError
        if view_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, view_id=view_id) + "/Map", 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiView, {view_id}. {status}:{reason}".
                          format(view_id=view_id, status=response.status_code, reason=response.text))

        viewMap = QiViewMap.fromJson(json.loads(response.content))
        response.close()
        return viewMap

    def getViews(self, namespace_id, skip=0, count=100):
        """Retrieves a list of views associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get all QiViews. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiView.fromJson(item))
        response.close()
        return results

    def getOrCreateView(self, namespace_id, view):
        """Tells Qi Service to create a view based on a local QiView object"""
        if namespace_id is None:
            raise TypeError
        if view is None or not isinstance(view, QiView):
            raise TypeError

        response = requests.post(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, view_id=view.Id),
            data=view.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiView, {view_id}. {status}:{reason}".
                          format(view_id=view.Id, status=response.status_code, reason=response.text))

        view = QiView.fromJson(json.loads(response.content))
        response.close()
        return view

    def createOrUpdateView(self, namespace_id, view):
        """Tells Qi Service to create a view based on a local QiView object"""
        if namespace_id is None:
            raise TypeError
        if view is None or not isinstance(view, QiView):
            raise TypeError

        response = requests.put(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, view_id=view.Id),
            data=view.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiView, {view_id}. {status}:{reason}".
                          format(view_id=view.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteView(self, namespace_id, view_id):
        """Tells Qi Service to delete the view with the specified 'view_id'"""
        if namespace_id is None:
            raise TypeError
        if view_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__viewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, view_id=view_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to delete QiView, {view_id}. {status}:{reason}".
                          format(view_id=view_id, status=response.status_code, reason=response.text))

        response.close()

    def getStream(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Qi Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        stream = QiStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def getStreamType(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Qi Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id) + "/Type", 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        type = QiType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getStreams(self, namespace_id, query="", skip=0, count=100):
        """Retrieves a list of streams associated with 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getStreamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, query=query, skip=skip, count=count),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get all QiStreams. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(QiStream.fromJson(item))
        response.close()
        return results

    def getOrCreateStream(self, namespace_id, stream):
        """Tells Qi Service to create a stream based on the local 'stream' QiStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError
        response = requests.post(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__qiHeaders())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        stream = QiStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def createOrUpdateStream(self, namespace_id, stream):
        """Tells Qi Service to create a stream based on the local 'stream' QiStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, QiStream):
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteStream(self, namespace_id, stream_id):
        """Tells Qi Service to delete the stream speficied by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to delete QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))
        response.close()

    def createOrUpdateTags(self, namespace_id, streamId, tags):
        """Tells Qi Service to create tags and associate them with the given streamId """
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            data=json.dumps(tags), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

    def createOrUpdateMetadata(self, namespace_id, streamId, metadata):
        """Tells Qi Service to create metadata and associate them with the given streamId"""
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata",
            data=json.dumps(metadata), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to create metadata for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))                          

    def getTags(self, namespace_id, streamId):
        """Tells Qi Service to get tags associated with the given streamId """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))
                
        content = json.loads(response.content)
        response.close()
        return content


    def getMetadata(self, namespace_id, streamId, key):
        """Tells Qi Service to get metadata associated with the given streamId and key"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata/" + key,
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get metadata for Stream: {stream_id} and Key {key}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))        

        content = json.loads(response.content)
        response.close()
        return content

        response.close()


    # The following section provides functionality to interact with Data
    #    We assume the value(s) passed follow the Qi object patterns supporting fromJson and toJson method

    def getValue(self, namespace_id, stream_id, index, value_class, view_id=""):
        """Retrieves JSON object from Qi Service for value specified by 'index' from Qi Service """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getValueQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=index, view_id=view_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get value for QiStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.fromJson(content)

    def getFirstValue(self, namespace_id, stream_id, value_class, view_id=""):
        """Retrieves JSON object from Qi Service the first value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getFirstValue.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, view_id=view_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get first value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.fromJson(content)

    def getLastValue(self, namespace_id, stream_id, value_class, view_id=""):
        """Retrieves JSON object from Qi Service the last value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getLastValue.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, view_id=view_id), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get last value for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.fromJson(content)

    def getWindowValues(self, namespace_id, stream_id, value_class, start, end, view_id=""):
        """Retrieves JSON object representing a window of values from the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getWindowValues.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id, start=start, end=end, view_id=view_id),
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get window values for QiStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
        return values

    def getRangeValues(self, namespace_id, stream_id, value_class, start, skip, count, reverse, boundary_type, view_id=""):
        """Retrieves JSON object representing a range of values from the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
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
                                                           reverse=reverse, boundary_type=boundary_type.value,
                                                           view_id=view_id),
           headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise QiError("Failed to get range of values from QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        values = []
        for c in content:
            values.append(value_class.fromJson(c))
        return values

    def insertValue(self, namespace_id, stream_id, value):
        """Tells Qi Service to insert a value, described by the local object 'value', into
        the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        if callable(getattr(value, "toJson", None)):
            payload = value.toJson()
        else:
            payload = value

        response = requests.post(
            self.__url + self.__insertValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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

        if callable(getattr(values[0], "toJson", None)):
            events = []
            for value in values:
                events.append(value.toDictionary())

            payload = json.dumps(events)
        else:
            payload = values

        response = requests.post(
            self.__url + self.__insertValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            raise QiError("Failed to insert multiple values for QiStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def updateValue(self, namespace_id, stream_id, value):
        """Tells Qi Service to update the value described by 'value', a local QiValue object"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        if callable(getattr(value, "toJson", None)):
            payload = value.toJson()
        else:
            payload = value

        response = requests.put(self.__url + self.__updateValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
                                data=payload, 
                                headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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

        if callable(getattr(values[0], "toJson", None)):
            events = []
            for value in values:
                events.append(value.toDictionary())
            payload = json.dumps(events)
        else:
            payload = values

        response = requests.put(self.__url + self.__updateValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
                                data=payload, 
                                headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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

        if callable(getattr(value, "toJson", None)):
            payload = value.toJson()
        else:
            payload = value

        response = requests.put(
            self.__url + self.__replaceValuePath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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

        if callable(getattr(values[0], "toJson", None)):
            events = []
            for value in values:
                events.append(value.toDictionary())
            payload = json.dumps(events)
        else:
            payload = values

        response = requests.put(
            self.__url + self.__replaceValuesPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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
            self.__url + self.__removeValue.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=key), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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

        response = requests.delete(
            self.__url + self.__removeWindowValues.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, start=start, end=end), 
            headers=self.__qiHeaders())
        if response.status_code < 200 or response.status_code >= 300:
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
        self.__typesPath = self.__basePath + "/Types/{type_id}"
        self.__getTypesPath = self.__basePath + "/Types?skip={skip}&count={count}"
        self.__behaviorsPath = self.__basePath + "/Behaviors/{behavior_id}"
        self.__getBehaviorsPath = self.__basePath + "/Behaviors?skip={skip}&count={count}"
        self.__viewsPath = self.__basePath + "/Views/{view_id}"
        self.__getViewsPath = self.__basePath + "/Views?skip={skip}&count={count}"
        self.__streamsPath = self.__basePath + "/Streams/{stream_id}"
        self.__getStreamsPath = self.__basePath + "/Streams?query={query}&skip={skip}&count={count}"

        self.__dataPath = self.__basePath + "/Streams/{stream_id}/Data"
        self.__getValueQuery = self.__dataPath + "/GetValue?index={index}&viewId={view_id}"
        self.__getFirstValue = self.__dataPath + "/GetFirstValue?viewId={view_id}"
        self.__getLastValue = self.__dataPath + "/GetLastValue?viewId={view_id}"
        self.__getWindowValues = self.__dataPath + "/GetWindowValues?startIndex={start}&endIndex={end}&viewId={view_id}"
        self.__getRangeValuesQuery = self.__dataPath + "/GetRangeValues?startIndex={start}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundary_type}&viewId={view_id}"

        self.__insertValuePath = self.__dataPath + "/InsertValue"
        self.__insertValuesPath = self.__dataPath + "/InsertValues"
        self.__updateValuePath = self.__dataPath + "/UpdateValue"
        self.__updateValuesPath = self.__dataPath + "/UpdateValues"
        self.__replaceValuePath = self.__dataPath + "/ReplaceValue"
        self.__replaceValuesPath = self.__dataPath + "/ReplaceValues"
        self.__removeValue = self.__dataPath + "/RemoveValue?index={index}"
        self.__removeWindowValues = self.__dataPath + "/RemoveWindowValues?startIndex={start}&endIndex={end}"
