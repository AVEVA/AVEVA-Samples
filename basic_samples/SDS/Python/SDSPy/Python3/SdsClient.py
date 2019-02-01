# SdsClient.py
#
# Copyright (C) 2018-2019 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
#
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

from SdsError import SdsError
from SdsType import SdsType
from SdsStream import SdsStream
from SdsStreamView import SdsStreamView
from SdsStreamViewMap import SdsStreamViewMap
from SdsBoundaryType import SdsBoundaryType
from Dataview import Dataview
from Datagroup import Datagroup
from JsonEncoder import Encoder
import requests
import time


class SdsClient(object):
    """Handles communication with Sds Service"""

    def __init__(self, api_version, tenant, resource, clientId, clientSecret):
        self.__apiVersion = api_version
        self.__tenant = tenant
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__url = resource # if resource.endswith("/")  else resource + "/" 

        self.__token = ""
        self.__expiration = 0
        self.__getToken()

        self.__setPathAndQueryTemplates()

    @property
    def Uri(self):
        return self.__url

    def getType(self, namespace_id, type_id):
        """Retrieves the type specified by 'type_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        type = SdsType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getTypeReferenceCount(self, namespace_id, type_id):
        """Retrieves the number of times the type is referenced"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id) + "/ReferenceCount",
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsType reference count, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        count = json.loads(response.content)
        response.close()
        return int(count)

    def getTypes(self, namespace_id, skip=0, count=100):
        """Retrieves a list of types associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getTypesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get all SdsTypes. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        types = json.loads(response.content)
        results = []
        for t in types:
            results.append(SdsType.fromJson(t))
        response.close()
        return results

    def getOrCreateType(self, namespace_id, type):
        """Tells Sds Service to create a type based on local 'type' or get if existing type matches"""
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, SdsType):
            raise TypeError

        response = requests.post(
            self.__url + self.__typesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type.Id),
            data=type.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))
        
        type = SdsType.fromJson(json.loads(response.content.decode('utf-8')))
        response.close()
        return type

    def createOrUpdateType(self, namespace_id, type):
        """Tells Sds Service to create a type based on local 'type' object"""
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, SdsType):
            raise TypeError

        response = requests.put(
            self.__url + self.__typesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type.Id),
            data=type.toJson(), headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))
        
        response.close()

    def deleteType(self, namespace_id, type_id):
        """Tells Sds Service to delete the type specified by 'type_id'"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__typesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__sdsHeaders())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))

        response.close()

    def getStreamView(self, namespace_id, streamView_id):
        """Retrieves the streamView specified by 'streamView_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id,
            streamView_id=streamView_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsStreamView, {streamView_id}. {status}:{reason}".
                          format(streamView_id=streamView_id, status=response.status_code, reason=response.text))

        streamView = SdsStreamView.fromJson(json.loads(response.content))
        response.close()
        return streamView

    def getStreamViewMap(self, namespace_id, streamView_id):
        """Retrieves the streamView map specified by 'streamView_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView_id) + "/Map", 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsStreamView, {streamView_id}. {status}:{reason}".
                          format(streamView_id=streamView_id, status=response.status_code, reason=response.text))

        streamViewMap = SdsStreamViewMap.fromJson(json.loads(response.content.decode('utf-8')))
        response.close()
        return streamViewMap

    def getStreamViews(self, namespace_id, skip=0, count=100):
        """Retrieves a list of streamViews associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get all SdsStreamViews. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(SdsStreamView.fromJson(item))
        response.close()
        return results

    def getOrCreateStreamView(self, namespace_id, streamView):
        """Tells Sds Service to create a streamView based on a local SdsStreamView object"""
        if namespace_id is None:
            raise TypeError
        if streamView is None or not isinstance(streamView, SdsStreamView):
            raise TypeError

        response = requests.post(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView.Id),
            data=streamView.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create SdsStreamView, {streamView_id}. {status}:{reason}".
                          format(streamView_id=streamView.Id, status=response.status_code, reason=response.text))

        streamView = SdsStreamView.fromJson(json.loads(response.content.decode('utf-8')))
        response.close()
        return streamView

    def createOrUpdateStreamView(self, namespace_id, streamView):
        """Tells Sds Service to create a streamView based on a local SdsStreamView object"""
        if namespace_id is None:
            raise TypeError
        if streamView is None or not isinstance(streamView, SdsStreamView):
            raise TypeError

        response = requests.put(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView.Id),
            data=streamView.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create SdsStreamView, {streamView_id}. {status}:{reason}".
                          format(streamView_id=streamView.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteStreamView(self, namespace_id, streamView_id):
        """Tells Sds Service to delete the streamView with the specified 'streamView_id'"""
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__streamViewsPath.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsStreamView, {streamView_id}. {status}:{reason}".
                          format(streamView_id=streamView_id, status=response.status_code, reason=response.text))

        response.close()

    def getStream(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Sds Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        stream = SdsStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def getStreamType(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Sds Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id) + "/Type", 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        type = SdsType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getStreams(self, namespace_id, query="", skip=0, count=100):
        """Retrieves a list of streams associated with 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getStreamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, query=query, skip=skip, count=count),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get all SdsStreams. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(SdsStream.fromJson(item))
        response.close()
        return results

    def getOrCreateStream(self, namespace_id, stream):
        """Tells Sds Service to create a stream based on the local 'stream' SdsStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError
        response = requests.post(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__sdsHeaders())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        stream = SdsStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def createOrUpdateStream(self, namespace_id, stream):
        """Tells Sds Service to create a stream based on the local 'stream' SdsStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        response.close()

    def deleteStream(self, namespace_id, stream_id):
        """Tells Sds Service to delete the stream speficied by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def createOrUpdateTags(self, namespace_id, streamId, tags):
        """Tells Sds Service to create tags and associate them with the given streamId """
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            data=json.dumps(tags), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))

    def createOrUpdateMetadata(self, namespace_id, streamId, metadata):
        """Tells Sds Service to create metadata and associate them with the given streamId"""
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata",
            data=json.dumps(metadata), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create metadata for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))                          

    def getTags(self, namespace_id, streamId):
        """Tells Sds Service to get tags associated with the given streamId """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))
                
        content = json.loads(response.content.decode('utf-8'))
        response.close()
        return content


    def getMetadata(self, namespace_id, streamId, key):
        """Tells Sds Service to get metadata associated with the given streamId and key"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__streamsPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata/" + key,
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get metadata for Stream: {stream_id} and Key {key}. {status}:{reason}".
                          format(stream_id=stream.Id, status=response.status_code, reason=response.text))        

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        return content

    # The following section provides functionality to interact with Data
    #    We assume the value(s) passed follow the Sds object patterns supporting fromJson and toJson method

    def getValue(self, namespace_id, stream_id, index, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service for value specified by 'index' from Sds Service """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getValueQuery.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=index, streamView_id=streamView_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get value for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getFirstValue(self, namespace_id, stream_id, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service the first value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getFirstValue.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, streamView_id=streamView_id), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get first value for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getLastValue(self, namespace_id, stream_id, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service the last value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getLastValue.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, streamView_id=streamView_id), 
           headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get last value for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getWindowValues(self, namespace_id, stream_id, value_class, start, end, streamView_id=""):
        """Retrieves JSON object representing a window of values from the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getWindowValues.format(api_version=self.__apiVersion,tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id, start=start, end=end, streamView_id=streamView_id),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get window values for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        if value_class is None:
            return content

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
        return values

    def getRangeValues(self, namespace_id, stream_id, value_class, start, skip, count, reverse, boundary_type, streamView_id=""):
        """Retrieves JSON object representing a range of values from the stream specified by 'stream_id'"""
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
        if boundary_type is None or not isinstance(boundary_type, SdsBoundaryType):
            raise TypeError

        response = requests.get(
            self.__url + self.__getRangeValuesQuery.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id,
                                                           stream_id=stream_id, start=start, skip=skip, count=count,
                                                           reverse=reverse, boundary_type=boundary_type.value,
                                                           streamView_id=streamView_id),
           headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get range of values from SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        if value_class is None:
            return content
        values = []
        for c in content:
            values.append(value_class.fromJson(c))
        return values

    def insertValues(self, namespace_id, stream_id, values):
        """Tells Sds Service to insert the values, defined by the list 'values', into 
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
            self.__url + self.__insertValuesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            raise SdsError("Failed to insert multiple values for SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def updateValues(self, namespace_id, stream_id, values):
        """Tells Sds Service to update values defined by the SdsValue list, 'values'"""
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

        response = requests.put(self.__url + self.__updateValuesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
                                data=payload, 
                                headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to update all values for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def replaceValues(self, namespace_id, stream_id, values):
        """Tells Sds Service to replace the values defined by the list 'values'"""
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
            self.__url + self.__replaceValuesPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to replace value for SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def removeValue(self, namespace_id, stream_id, key):
        """Tells Sds Service to delete the value with a key property matching 'key'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if key is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__removeValue.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=key), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to remove value for SdsStream, {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def removeWindowValues(self, namespace_id, stream_id, start, end):
        """Tells Sds Service to delete a window of values in the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__removeWindowValues.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, start=start, end=end), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to remove all values for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()
		
		

    def postDataview(self, namespace_id, dataview):
        """Tells Sds Service to create a dataview based on local 'dataview' or get if existing dataview matches"""
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError		
		
        response = requests.post(
            self.__url + self.__dataviewPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview.Id),
            data=dataview.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to create dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview.Id, status=response.status_code, reason=response.text))
		
        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
    def patchDataview(self, namespace_id, dataview):
        """Tells Sds Service to update a dataview based on local 'dataview'"""
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError

        response = requests.patch(
            self.__url + self.__dataviewPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview.Id),
            data=dataview.toJson(), 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to update dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview.Id, status=response.status_code, reason=response.text))
        
        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
		
		
    def deleteDataview(self, namespace_id, dataview_id):
        """Tells Sds Service to delete a dataview based on 'dataview_id'"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError
	
        response = requests.delete(
            self.__url + self.__dataviewPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview_id),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to delete dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview.Id, status=response.status_code, reason=response.text))
        
        response.close()
        return
		
		
    def getDataview(self, namespace_id, dataview_id):
        """Retrieves the dataview specified by 'dataview_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__dataviewPath.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview_id),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataview, {dataview_id}. {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        
        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
    def getDataviews(self, namespace_id, skip = 0, count =100):
        """Retrieves all of the dataviews from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getDataviews.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataviews. {status}:{reason}".
                          format( status=response.status_code, reason=response.text))
        
        dataviews = json.loads(response.content)
        results = []
        for t in dataviews:
            results.append(Dataview.fromJson(t))
        response.close()
        return results
		
		
    def getDatagroups(self, namespace_id,dataview_id, skip = 0, count = 100):
        """Retrieves all of the datagroups from the specified dataview from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getDatagroups.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview_id, skip=skip, count=count),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get datagroups for dataview, . {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        

        datagroups = json.loads(response.content)
        results = {}
        for key, value in datagroups.items():
            innerobj = {}
            for key2, value2 in value.items():
                innerobj[key2] = Datagroup.fromJson(value2)
            results[key] = innerobj
        response.close()

        return results
		
		
    def getDatagroup(self, namespace_id,dataview_id, datagroup_id):
        """Retrieves a datagroupby 'datagroup_id' from the specified dataview from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getDatagroup.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview_id, datagroup_id=datagroup_id),
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get datagroup for dataview, . {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        

        datagroup = Datagroup.fromJson(json.loads(response.content))
        return datagroup
	
#needs other parameters with smart 
    def getDataviewPreview(self, namespace_id, dataview_id, startIndex = None, endIndex = None, interval = None, form = None, count = -1, value_class = None):
        """Retrieves the dataviewpreview of the 'dataview_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        urlAdd = []
        urlAddStr = ""
        
        if startIndex is not None:
            urlAdd.append("startIndex=" +startIndex)
        if endIndex is not None:
            urlAdd.append("endIndex=" +endIndex)
        if interval is not None:
            urlAdd.append("interval=" +interval)
        if form is not None:
            urlAdd.append("form=" +form)
        if count != -1:
            urlAdd.append("count=" + str(count))
        if len(urlAdd) != 0:
            urlAddStr = "?" + '&'.join(str(x) for x in urlAdd)
        
        
        response = requests.get(
            self.__url + self.__getDataviewPreview.format(api_version=self.__apiVersion, tenant_id=self.__tenant, namespace_id=namespace_id, dataview_id=dataview_id) + urlAddStr, 
            headers=self.__sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataview preview for dataview {dataview_id}. {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
		
        if value_class is None:
            return (content)
        return value_class.fromJson(content)
		

    # private methods

    def __getToken(self):
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        discoveryUrl = requests.get(
            self.__url + "/identity/.well-known/openid-configuration",
            headers= {"Accept" : "application/json"})

        if discoveryUrl.status_code < 200 or discoveryUrl.status_code >= 300:
            discoveryUrl.close()
            raise SdsError("Failed to get access token endpoint from discovery URL: {status}:{reason}".
                            format(status=discoveryUrl.status_code, reason=discoveryUrl.text))

        tokenEndpoint = json.loads(discoveryUrl.content)["token_endpoint"]

        tokenInformation = requests.post(
            tokenEndpoint,
            data = {"client_id" : self.__clientId,
                    "client_secret" : self.__clientSecret,
                    "grant_type" : "client_credentials"})

        token = json.loads(tokenInformation.content)

        if token is None:
            raise Exception("Failed to retrieve Token")

        self.__expiration = float(token['expires_in']) + time.time()
        self.__token = token['access_token']
        return self.__token

    def __sdsHeaders(self):
        return {"Authorization": "Bearer %s" % self.__getToken(),
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
                }

    def __validateUri(self, url):
        splitUri = urlparse(url)
        return splitUri.netloc + splitUri.path

    def __setPathAndQueryTemplates(self):
        self.__basePath = "/api/{api_version}/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types/{type_id}"
        self.__getTypesPath = self.__basePath + "/Types?skip={skip}&count={count}"
        self.__behaviorsPath = self.__basePath + "/Behaviors/{behavior_id}"
        self.__getBehaviorsPath = self.__basePath + "/Behaviors?skip={skip}&count={count}"
        self.__streamViewsPath = self.__basePath + "/StreamViews/{streamView_id}"
        self.__getStreamViewsPath = self.__basePath + "/StreamViews?skip={skip}&count={count}"
        self.__streamsPath = self.__basePath + "/Streams/{stream_id}"
        self.__getStreamsPath = self.__basePath + "/Streams?query={query}&skip={skip}&count={count}"

        self.__dataPath = self.__basePath + "/Streams/{stream_id}/Data"
        self.__getValueQuery = self.__dataPath + "?index={index}&streamViewId={streamView_id}"
        self.__getFirstValue = self.__dataPath + "/First?streamViewId={streamView_id}"
        self.__getLastValue = self.__dataPath + "/Last?streamViewId={streamView_id}"
        self.__getWindowValues = self.__dataPath + "?startIndex={start}&endIndex={end}&streamViewId={streamView_id}"
        self.__getRangeValuesQuery = self.__dataPath + "?startIndex={start}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundary_type}&streamViewId={streamView_id}"

        self.__insertValuesPath = self.__dataPath
        self.__updateValuesPath = self.__dataPath
        self.__replaceValuesPath = self.__dataPath + "?allowCreate=false"
        self.__removeValue = self.__dataPath + "?index={index}"
        self.__removeWindowValues = self.__dataPath + "?startIndex={start}&endIndex={end}"	
		
        self.__dataviewsPath = self.__basePath + "/Dataviews"
        self.__getDataviews= self.__dataviewsPath + "?skip={skip}&count={count}"
        self.__dataviewPath = self.__dataviewsPath + "/{dataview_id}"
        self.__datagroupPath= self.__dataviewPath + "/Datagroups"
        self.__getDatagroup = self.__datagroupPath + "/{datagroup_id}"
        self.__getDatagroups = self.__datagroupPath + "?skip={skip}&count={count}"
        self.__getDataviewPreview = self.__dataviewPath + "/preview/interpolated"
