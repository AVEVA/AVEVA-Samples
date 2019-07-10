# Streams.py
#

import json

from .SDS.SdsStream import SdsStream
from .SDS.SdsType import SdsType
from .SDS.SdsStreamView import SdsStreamView
from .SDS.SdsStreamViewMap import SdsStreamViewMap
from .SDS.SdsBoundaryType import SdsBoundaryType
import requests


class Streams(object):
    """
    Client for interacting with Streams
    """

    def __init__(self, client):
        """
        :param client: base client that handles auth and base routing
        """
        self.__apiVersion = client.api_version
        self.__tenant = client.tenant
        self.__uri_API = client.uri_API
        self.__baseClient = client

        self.__setPathAndQueryTemplates()

    def getStreamView(self, namespace_id, streamView_id):
        """
        Retrieves the streamView specified by 'streamView_id' from Sds Service
        :param namespace_id: namespace to work against
        :param streamView_id: streamview id to get
        :return: Streamview as SDsStreamview
        """
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.get(
            self.__streamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                streamView_id=streamView_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get SdsStreamView, {streamView_id}.")

        streamView = SdsStreamView.fromJson(json.loads(response.content))
        response.close()
        return streamView

    def getStreamViewMap(self, namespace_id, streamView_id):
        """
        Retrieves the streamView map specified by 'streamView_id' from Sds
            Service
        :param namespace_id: namespace to work against
        :param streamView_id:  streamview map to get
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.get(
            self.__streamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                streamView_id=streamView_id) + "/Map",
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get SdsStreamViewMap, {streamView_id}.")

        streamViewMap = SdsStreamViewMap.fromJson(json.loads(response.text))
        response.close()
        return streamViewMap

    def getStreamViews(self, namespace_id, skip=0, count=100):
        """
        Retrieves a list of streamViews associated with the specified
            'namespace_id' under the current tenant
        :param namespace_id: namespace to work against
        :param skip: number of streamviews to skip for paging
        :param count: number streamviews in a page
        :return: array of SdsStreamviews
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__getStreamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders())
        self.__baseClient.checkResponse(
            response, "Failed to get all SdsStreamViews.")

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(SdsStreamView.fromJson(item))
        response.close()
        return results

    def getOrCreateStreamView(self, namespace_id, streamView):
        """
        Tells Sds Service to create a streamView based on a local
            SdsStreamView object
        :param namespace_id: namespace to work against
        :param streamView: Streamview object to create in OCS
        :return: created Streamview as SdsStreamview
        """
        if namespace_id is None:
            raise TypeError
        if streamView is None or not isinstance(streamView, SdsStreamView):
            raise TypeError

        response = requests.post(
            self.__streamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                streamView_id=streamView.Id),
            data=streamView.toJson(),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create SdsStreamView, {streamView.Id}.")

        streamView = SdsStreamView.fromJson(json.loads(response.text))
        response.close()
        return streamView

    def createOrUpdateStreamView(self, namespace_id, streamView):
        """
        Tells Sds Service to create a streamView based on a local
            SdsStreamView object
        :param namespace_id: namespace to work against
        :param streamView: Streamview object to create or update in OCS
        :return: created Streamview as SdsStream
        """
        if namespace_id is None:
            raise TypeError
        if streamView is None or not isinstance(streamView, SdsStreamView):
            raise TypeError

        response = requests.put(
            self.__streamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                streamView_id=streamView.Id),
            data=streamView.toJson(),
            headers=self.__baseClient.sdsHeaders())
        self.__baseClient.checkResponse(
            response, f"Failed to create SdsStreamView, {streamView.Id}.")

        response.close()

    def deleteStreamView(self, namespace_id, streamView_id):
        """
        Tells Sds Service to delete the streamView with the specified
            'streamView_id'
        :param namespace_id: namespace to work against
        :param streamView_id: id of streamview to delete
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if streamView_id is None:
            raise TypeError

        response = requests.delete(
            self.__streamViewsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                streamView_id=streamView_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to delete SdsStreamView, {streamView_id}.")

        response.close()

    def getStream(self, namespace_id, stream_id):
        """
        Retrieves a stream specified by 'stream_id' from the Sds Service
        :param namespace_id: namespace to work against
        :param stream_id: id of the stream
        :return:the Stream as SdsStream
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get SdsStream, {stream_id}.")

        stream = SdsStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def getStreamType(self, namespace_id, stream_id):
        """
        Retrieves a stream specified by 'stream_id' from the Sds Service
        :param namespace_id: namespace to work against
        :param stream_id: id of the stream
        :return: the stream type as an SdsType
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id) + "/Type",
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get SdsStream type,  {stream_id}.")

        type = SdsType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getStreams(self, namespace_id, query="", skip=0, count=100):
        """
        Retrieves a list of streams associated with 'namespace_id' under
            the current tenant"
        :param namespace_id: namespace to work against
        :param query: filtering query
        :param skip: number of streams to skip for paging
        :param count: number of streams to limit to
        :return: array of SdsStreams
        """
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError

        response = requests.get(
            self.__getStreamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id),
            params={"query": query, "skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, "Failed to get all SdsStreams.")

        content = json.loads(response.content)
        results: [SdsStream] = []
        for item in content:
            results.append(SdsStream.fromJson(item))
        response.close()
        return results

    def getOrCreateStream(self, namespace_id, stream):
        """
        Tells Sds Service to create a stream based on the local 'stream'
            SdsStream object
        :param namespace_id: namespace to work against
        :param stream: the stream to Create or retreive, as a SDsStream
        :return: the created Stream as an SdsStream
        """
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError
        response = requests.post(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream.Id),
            data=stream.toJson(),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create SdsStream, {stream.Id}.")

        stream = SdsStream.fromJson(json.loads(response.content))
        response.close()
        return stream

    def createOrUpdateStream(self, namespace_id, stream):
        """
        Tells Sds Service to create a stream based on the local 'stream'
            SdsStream object
        :param namespace_id: namespace to work against
        :param stream: the stream to Create or update, as a SDsStream
        :return: the created or updated Stream as an SdsStream
        """
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError

        response = requests.put(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream.Id),
            data=stream.toJson(),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create SdsStream, {stream.Id}.")

        response.close()

    def updateStreamType(self, namespace_id, streamId, streamViewId):
        """
        Tells Sds Service to update a stream based on the local 'stream'
             SdsStream object
        :param namespace_id: namespace to work against
        :param stream_id: id of the stream to change the type of
        :param streamViewId: if of the streamview to change the type to
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if streamId is None:
            raise TypeError
        if streamViewId is None:
            raise TypeError

        response = requests.put(
            self.__updateStreamTypePath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=streamId),
            params={"streamViewId": streamViewId},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to update SdsStream type, {streamId}.")

        response.close()

    def deleteStream(self, namespace_id, stream_id):
        """
        Tells Sds Service to delete the stream speficied by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to delete
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to delete SdsStream, {stream_id}.")

        response.close()

    def createOrUpdateTags(self, namespace_id, streamId, tags):
        """
        "Tells Sds Service to create tags and associate them with the given
            streamId
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to update with tags
        :param tags: tags to create or update.  expected for is an array of
            strings
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=streamId) + "/Tags",
            data=json.dumps(tags),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create tags for Stream: {streamId}.")

    def createOrUpdateMetadata(self, namespace_id, streamId, metadata):
        """
        Tells Sds Service to create metadata and associate them with the given
            streamId
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to update with metadata
        :param metadata: metadata to create or update.  expected for is an
            dict(string,string)
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=streamId) + "/Metadata",
            data=json.dumps(metadata),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to create metadata for Stream: {streamId}.")

    def getTags(self, namespace_id, streamId):
        """
        Tells Sds Service to get tags associated with the given streamId
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the tags of
        :return: stream's tags
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=streamId) + "/Tags",
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get tags for Stream: {streamId}.")

        content = json.loads(response.text)
        response.close()
        return content

    def getMetadata(self, namespace_id, streamId, key):
        """
        Tells Sds Service to get metadata associated with the given streamId
            and key
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the metadata value of
        :param key: specific metadata field to retreive
        :return: value at the key
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__streamsPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=streamId) + "/Metadata/" + key,
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get metadata for Stream: {streamId}.")

        content = json.loads(response.text)
        response.close()
        return content

    # The following section provides functionality to interact with Data
    #  We assume the value(s) passed follow the Sds object patterns
    #  supporting fromJson and toJson method

    def getValue(self, namespace_id, stream_id, index, value_class=None):
        """
        Retrieves JSON object from Sds Service for value specified by 'index'
            from Sds Service
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param index: index at which to get a value
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson()  Default is None.
            If None returns a dynamic Python object from the data.
        :return: the value.  If value_class is defined it is in this type.
            Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError

        response = requests.get(
            self.__dataPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"index": index},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get value for SdsStream: {stream_id}.")

        content = json.loads(response.content)
        response.close()

        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getFirstValue(self, namespace_id, stream_id, value_class=None):
        """
        Retrieves JSON object from Sds Service the first value to be added to
            the stream specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson()  Default is None.
            If None returns a dynamic Python object from the data.
        :return: the value.  If value_class is defined it is in this type.
            Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__getFirstValue.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get first value for SdsStream: {stream_id}.")

        content = json.loads(response.content)
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getLastValue(self, namespace_id, stream_id, value_class=None):
        """
        Retrieves JSON object from Sds Service the last value to be added to
            the stream specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson()  Default is None.
            If None returns a dynamic Python object from the data.
        :return: the value.  If value_class is defined it is in this type.
            Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.__getLastValue.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get last value for SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content
        return value_class.fromJson(content)

    def getWindowValues(self, namespace_id, stream_id, value_class, start, end,
                        filter=""):
        """
        Retrieves JSON object representing a window of values from the stream
            specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson().
            If None returns a dynamic Python object from the data.
        :param start: Starting index
        :param end: Ending index
        :param filter: An optional filter.  By Default it is "".
        :return: an array of values.
            If value_class is defined it is in this type.
            Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.get(
            self.__dataPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"startIndex": start, "endIndex": end, "filter": filter},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get window values"
                      " for SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
        return values

    def getWindowValuesForm(self, namespace_id, stream_id, value_class, start,
                            end, form=""):
        """
        Retrieves JSON object representing a window of values from the stream
            specified by 'stream_id'.  Use this to get the data in a different
            return form
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
        Type must support .fromJson().
        If None returns a dynamic Python object from the data.
        :param start: Starting index
        :param end: Ending index
        :param form: form of the data
        :return: An array of the data in type specified if value_class
            defined.  Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.get(
            self.__dataPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"startIndex": start, "endIndex": end, "form": form},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get window values for SdsStream, "
                      "form : {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
        return values

    def getRangeValues(self, namespace_id, stream_id, value_class, start, skip,
                       count, reverse, boundary_type, streamView_id=""):
        """
        Retrieves JSON object representing a range of values from the stream
            specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson(). If None returns a dynamic Python
            object from the data.
        :param start: Starting index
        :param skip: number of values to skip after start index.
            Important in paging
        :param count: number of values to return
        :param reverse: which direction to go when getting values
        :param boundary_type: the boundary condition to use.
            Can be an SdsBoundaryType or the integer value
        :param streamView_id: streamview to map the results to
        :return: An array of the data in type specified if value_class
            is defined.  Otherwise it is a dynamic Python object
        """
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
        if boundary_type is None:
            raise TypeError

        boundary = boundary_type
        if isinstance(boundary_type, SdsBoundaryType):
            boundary = boundary_type.value

        response = requests.get(
            self.__transform.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"startIndex": start, "skip": skip, "count": count,
                    "reverse": reverse, "boundary_type": boundary,
                    "streamView_id": streamView_id},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get range values for"
            " SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content
        values = []
        for c in content:
            values.append(value_class.fromJson(c))
        return values

    def getRangeValuesInterpolated(self, namespace_id, stream_id, value_class,
                                   start, end, count):
        """
        Retrieves JSON object representing a range of values from the stream
            specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson(). If None returns a dynamic Python
            object from the data.
        :param start: starting index
        :param end:  ending index
        :param count: number of datapoints to retrieve
        :return: An array of the data in type specified if value_class is
        defined.  Otherwise it is a dynamic Python object
        """

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

        response = requests.get(
            self.__getRangeInterpolatedQuery.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"startIndex": start, "endIndex": end, "count": count},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get range values for"
                      " SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content
        values = []
        for c in content:
            values.append(value_class.fromJson(c))
        return values

    def getSampledValues(self, namespace_id, stream_id, value_class, start,
                         end, sample_by, intervals, filter="",
                         stream_view_id=""):
        """
        Returns data sampled by intervals between a specified start and end
            index.
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson().
            If None returns a dynamic Python object from the data.
        :param start: starting index for intervals
        :param end:  ending index for intervals
        :param sample_by: property or properties to use when sampling
        :param intervals: number of intervals requested
        :param boundary: optional SdsBoundaryType specifies the handling of
            events at or near the startIndex and endIndex
        :param start_boundary: optional SdsBoundaryType specifies the handling
            of events at or near the startIndex
        :param end_boundary: optional SdsBoundaryType specifies the handling
            of events at or near the endIndex
        :param filter: optional filter to apply
        :param stream_view_id: optional streamview identifier
        :return: An array of the data in type specified if value_class is
            defined.  Otherwise it is a dynamic Python object
        """

        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError
        if sample_by is None:
            raise TypeError
        if intervals is None:
            raise TypeError

        # if stream_view_id is not set, do not specify /transform/ route
        # and stream_view_id parameter
        if len(stream_view_id) == 0:
            _path = self.__getSampledValues.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id)

        else:
            _path = self.__getSampledValuesT.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id)

        response = requests.get(
                _path,
                params={"startIndex": start,
                        "endIndex": end,
                        "sampleBy": sample_by,
                        "intervals": intervals,
                        "filter": filter,
                        "stream_view_id": stream_view_id},
                headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get sampled values for"
                      " SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()

        if value_class is None:
            return content
        values = []
        for c in content:
            values.append(value_class.fromJson(c))
        return values

    def getSummaries(self, namespace_id, stream_id, value_class, start, end,
                     count, stream_view_id="", filter=""):
        """
        Retrieves JSON object representing a summary for the stream specified
            by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson().
            If None returns a dynamic Python object from the data.
        Note- for this function the default return json string is not a
            JSON array of the value, so the same type definition won't work.
        :param start: starting index
        :param end:  ending index
        :param count: number of datapoints in summary
        :param stream_view_id: streamview to tranform the data into
        :param filter: filter to apply
        :return: An array of the data summary in type specified if value_class
            is defined.  Otherwise it is a dynamic Python object
        """

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

        # if stream_view_id is not set, do not specify /transform/ route
        # and stream_view_id parameter
        if len(stream_view_id) == 0:
            _path = self.__getSummaries.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id)
        else:
            _path = self.__getSummariesT.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id)

        response = requests.get(
                _path,
                params={"startIndex": start,
                        "endIndex": end,
                        "count": count,
                        "filter": filter,
                        "streamViewId": stream_view_id},
                headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get summaries for SdsStream: {stream_id}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content

        values = []
        for c in content:
            values.append(value_class.fromDictionary(c))
        return values

    def insertValues(self, namespace_id, stream_id, values):
        """
        Tells Sds Service to insert the values, defined by the list 'values',
        into the stream specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get data into
        :param values: values to sends into OCS.
            Can be string of json array of values.
            Can be an array of values of a type that has toJson defined.
        :return:
        """
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
            self.__insertValuesPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            data=payload,
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to insert multiple values for "
                      " SdsStream: {stream_id}.")

    def updateValues(self, namespace_id, stream_id, values):
        """
        Tells Sds Service to update values defined by the SdsValue list,
            'values'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get data updated
        :param values: values to update in OCS.
        Can be string of json array of values.
        Can be an array of values of a type that has toJson defined.
        :return:
        """
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

        response = requests.put(self.__updateValuesPath.format(
                                    tenant_id=self.__tenant,
                                    namespace_id=namespace_id,
                                    stream_id=stream_id),
                                data=payload,
                                headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response,  f"Failed to update all values "
                       " for SdsStream: {stream_id}.")

        response.close()

    def replaceValues(self, namespace_id, stream_id, values):
        """
        Tells Sds Service to replace the values defined by the list 'values'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get data replaced
        :param values: values to replace in OCS.
            Can be string of json array of values.
            Can be an array of values of a type that has toJson defined.
        :return:
        """
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
            self.__replaceValuesPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            data=payload,
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to replace values for SdsStream: {stream_id}.")

        response.close()

    def removeValue(self, namespace_id, stream_id, key):
        """
        Tells Sds Service to delete the value with a key property matching
            'key'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get data removed
        :param key: the index to remove
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if key is None:
            raise TypeError

        response = requests.delete(
            self.__dataPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"index": key},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to remove value for SdsStream: {stream_id}.")

        response.close()

    def removeWindowValues(self, namespace_id, stream_id, start, end):
        """
        Tells Sds Service to delete a window of values in the stream specified
            by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_id: id of the stream to get data removed
        :param start: starting index
        :param end: ending index
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError

        response = requests.delete(
            self.__dataPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                stream_id=stream_id),
            params={"startIndex": start, "endIndex": end},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to remove all values for "
                      " SdsStream: {stream_id}.")

        response.close()

    def getStreamsWindow(self, namespace_id, stream_ids, value_class, start,
                         end, joinMode=1):
        """
        Retrieves JSON object representing a window of values from the stream
             specified by 'stream_id'
        :param namespace_id: id of namespace to work against
        :param stream_ids: ids of the streams to get the data of
        :param value_class: use this to cast the value into a given type.
            Type must support .fromJson(). If None returns a dynamic Python
            object from the data.
        :param start: Starting index
        :param end: Ending index
        :param joinMode: Join mode, supports numbers or strings.
            Defaults to outer
        :return: an array of values.
            If value_class is defined it is in this type.
            Otherwise it is a dynamic Python object
        """
        if namespace_id is None:
            raise TypeError
        if stream_ids is None:
            raise TypeError
        if not stream_ids:
            raise TypeError
        if start is None:
            raise TypeError
        if end is None:
            raise TypeError
        if joinMode is None:
            raise TypeError

        response = requests.get(
            self.__bulkStreams.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id),
            params={"streams": ','.join(stream_ids),
                    "startIndex": start,
                    "endIndex": end,
                    "joinMode": joinMode},
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get bulk values for"
                      " SdsStream: {stream_ids}.")

        content = json.loads(response.text)
        response.close()
        if value_class is None:
            return content

        values = []
        for valueArray in content:
            valuesInside = []
            for value in valueArray:
                valuesInside.append(value_class.fromDictionary(value))
            values.append(valuesInside)
        return values

    # private methods

    def __setPathAndQueryTemplates(self):
        """
        creates the urls that are used
        :return:
        """
        self.__basePath = self.__uri_API + \
            "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__getStreamViewsPath = self.__basePath + "/StreamViews"
        self.__streamViewsPath = self.__getStreamViewsPath + "/{streamView_id}"
        self.__getStreamsPath = self.__basePath + "/Streams"
        self.__streamsPath = self.__getStreamsPath + "/{stream_id}"
        self.__updateStreamTypePath = self.__streamsPath + "/Type"

        self.__dataPath = self.__streamsPath + "/Data"
        self.__getFirstValue = self.__dataPath + "/First"
        self.__getLastValue = self.__dataPath + "/Last"
        self.__transform = self.__dataPath + "/Transform"
        self.__getSummaries = self.__dataPath + "/Summaries"
        self.__getSummariesT = self.__transform + "/Summaries"
        self.__getSampledValues = self.__dataPath + "/Sampled"
        self.__getSampledValuesT = self.__transform + "/Sampled"
        self.__getRangeInterpolatedQuery = self.__transform + "/Interpolated"

        self.__insertValuesPath = self.__dataPath
        self.__updateValuesPath = self.__dataPath
        self.__replaceValuesPath = self.__dataPath + "?allowCreate=false"

        self.__bulkStreams = self.__basePath + "/Bulk/Streams/Data/Joins"
