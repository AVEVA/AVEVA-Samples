# Streams.py
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

from .SdsError import SdsError
from .SDS.SdsStream import SdsStream
from .SDS.SdsType import SdsType
from .SDS.SdsStreamView import SdsStreamView
from .SDS.SdsStreamViewMap import SdsStreamViewMap
from .SDS.SdsBoundaryType import SdsBoundaryType
import requests


class Streams(object):
    """Handles communication with Sds Service"""

    def __init__(self, client):
        self.__apiVersion = client.api_version
        self.__tenant = client.tenant
        self.__uri_API = client.uri_API
        self.__baseClient = client

        self.__setPathAndQueryTemplates()

    def getStreamView(self, namespace_id, streamView_id):
        """Retrieves the streamView specified by 'streamView_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.get(
            self.__uri_API + self.__getStreamView.format(tenant_id=self.__tenant, namespace_id=namespace_id,
            streamView_id=streamView_id), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamViewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView_id) + "/Map", 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__getStreamViewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamViewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView.Id),
            data=streamView.toJson(), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamViewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView.Id),
            data=streamView.toJson(), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamViewsPath.format(tenant_id=self.__tenant, namespace_id=namespace_id, streamView_id=streamView_id), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id) + "/Type", 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__getStreamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, query=query, skip=skip, count=count),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get all SdsStreams. {status}:{reason}".
                          format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results: [SdsStream] = []
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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__baseClient.sdsHeaders())

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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream.Id),
            data=stream.toJson(), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            data=json.dumps(tags), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=streamId, status=response.status_code, reason=response.text))

    def createOrUpdateMetadata(self, namespace_id, streamId, metadata):
        """Tells Sds Service to create metadata and associate them with the given streamId"""
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata",
            data=json.dumps(metadata), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to create metadata for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=streamId, status=response.status_code, reason=response.text))                          

    def getTags(self, namespace_id, streamId):
        """Tells Sds Service to get tags associated with the given streamId """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Tags",
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get tags for Stream: {stream_id}. {status}:{reason}".
                          format(stream_id=streamId, status=response.status_code, reason=response.text))
                
        content = json.loads(response.content.decode('utf-8'))
        response.close()
        return content


    def getMetadata(self, namespace_id, streamId, key):
        """Tells Sds Service to get metadata associated with the given streamId and key"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__uri_API + self.__streamsPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=streamId) + "/Metadata/" + key,
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get metadata for Stream: {stream_id} and Key {key}. {status}:{reason}".
                          format(stream_id=streamId, status=response.status_code, reason=response.text))        

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
            self.__uri_API + self.__getValueQuery.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=index), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get value for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getFirstValue(self, namespace_id, stream_id, value_class):
        """Retrieves JSON object from Sds Service the first value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__uri_API + self.__getFirstValue.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get first value for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getLastValue(self, namespace_id, stream_id, value_class):
        """Retrieves JSON object from Sds Service the last value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__uri_API + self.__getLastValue.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
           headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get last value for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getWindowValues(self, namespace_id, stream_id, value_class, start, end):
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
            self.__uri_API + self.__getWindowValues.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id, start=start, end=end),
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__getRangeValuesQuery.format( tenant_id=self.__tenant, namespace_id=namespace_id,
                                                           stream_id=stream_id, start=start, skip=skip, count=count,
                                                           reverse=reverse, boundary_type=boundary_type.value,
                                                           streamView_id=streamView_id),
           headers=self.__baseClient.sdsHeaders())
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

    def getSummaries(self, namespace_id, stream_id, value_class, start, end, count, stream_view_id = "", filter = ""):
        """Retrieves JSON object representing a summary for the stream specified by 'stream_id'"""

        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError
        if count is None:
            raise TypeError

        # if stream_view_id is not set, do not specify /transform/ route and stream_view_id parameter
        if len(stream_view_id) == 0:
            _path = self.__getSummaries.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                       stream_id=stream_id, start=start, end=end, count=count,filter= filter)
        else:
            _path = self.__getSummariesT.format(tenant_id=self.__tenant, namespace_id=namespace_id,
                                                        stream_id=stream_id, start=start, end=end, count=count,filter= filter,stream_view_id=stream_view_id)

        response = requests.get(
                self.__uri_API + _path,
                headers=self.__baseClient.sdsHeaders())          

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get summaries for SdsStream {stream_id}. {status}:{reason}".
                          format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content.decode('utf-8'))
        response.close()
        if value_class is None:
            return content

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
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
            self.__uri_API + self.__insertValuesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__baseClient.sdsHeaders())
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

        response = requests.put(self.__uri_API + self.__updateValuesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
                                data=payload, 
                                headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__replaceValuesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id), 
            data=payload, 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__removeValue.format( tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, index=key), 
            headers=self.__baseClient.sdsHeaders())
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
            self.__uri_API + self.__removeWindowValues.format(tenant_id=self.__tenant, namespace_id=namespace_id, stream_id=stream_id, start=start, end=end), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to remove all values for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()
		
		
    # private methods


    def __setPathAndQueryTemplates(self):
        self.__basePath = "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types/{type_id}"
        self.__getTypesPath = self.__basePath + "/Types?skip={skip}&count={count}"
        self.__streamViewsPath = self.__basePath + "/StreamViews/{streamView_id}"
        self.__getStreamViewsPath = self.__basePath + "/StreamViews?skip={skip}&count={count}"
        self.__streamsPath = self.__basePath + "/Streams/{stream_id}"
        self.__getStreamsPath = self.__basePath + "/Streams?query={query}&skip={skip}&count={count}"

        self.__dataPath = self.__basePath + "/Streams/{stream_id}/Data"
        self.__getValueQuery = self.__dataPath + "?index={index}"
        self.__getFirstValue = self.__dataPath + "/First?"
        self.__getLastValue = self.__dataPath + "/Last?"
        self.__getWindowValues = self.__dataPath + "?startIndex={start}&endIndex={end}"
        self.__getRangeValuesQuery = self.__dataPath + "/Transform?startIndex={start}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundary_type}&streamViewId={streamView_id}"
        self.__getSummaries = self.__dataPath + "/Summaries?startIndex={start}&endIndex={end}&Count={count}&filter={filter}"
        self.__getSummariesT = self.__dataPath + "/Transform/Summaries?startIndex={start}&endIndex={end}&Count={count}&streamViewId={stream_view_id}&filter={filter}"

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
