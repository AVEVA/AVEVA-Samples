# sds_client.py
#
# Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
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

import adal
from helper_functions import *
import json
import requests
from sds_error import SdsError
from sds_type import SdsType
from sds_stream import SdsStream
from urllib.parse import urlparse
import time


class SdsClient(object):
    """Handles communication with Sds Service"""
    def __init__(self, api_version, tenant, resource, clientId, clientSecret):
        self.apiVersion = api_version
        self.tenantId = tenant
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.url = resource

        self.__token = ""
        self.__expiration = 0
        self.__get_token()

        self.__set_path_and_query_templates()
        self.type_names = None

    @property
    def Uri(self):
        return self.url

    def get_type(self, namespace_id, type_id):
        """Retrieves the type specified by 'type_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__typesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id, type_id=type_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get SdsType, {type_id}. {status}:{reason}".
                           format(type_id=type_id, status=response.status_code, reason=response.text))

        sds_type = SdsType.from_json(json.loads(response.content))
        response.close()
        return sds_type

    def get_type_reference_count(self, namespace_id, type_id):
        """Retrieves the number of times the type is referenced"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__typesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                               type_id=type_id) + "/ReferenceCount",
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get SdsType reference count, {type_id}. {status}:{reason}".
                           format(type_id=type_id, status=response.status_code, reason=response.text))

        count = json.loads(response.content)
        response.close()
        return int(count)

    def get_types(self, namespace_id, skip=0, count=100):
        """Retrieves a list of types associated with the specified 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__getTypesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id, skip=skip,
                                                  count=count),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get all SdsTypes. {status}:{reason}".
                           format(status=response.status_code, reason=response.text))

        types = json.loads(response.content)
        results = []
        for t in types:
            results.append(SdsType.from_json(t))
        response.close()
        return results

    def get_or_create_type(self, namespace_id, event_type):
        """Tells Sds Service to create a type based on local 'type' or get if existing type matches"""
        if namespace_id is None:
            raise TypeError
        if event_type is None or not isinstance(event_type, SdsType):
            raise TypeError

        req_url = self.url + self.__typesPath.format(
            tenant_id=self.tenantId,
            namespace_id=namespace_id,
            type_id=event_type.Id)
        response = requests.post(
            url=req_url,
            data=event_type.to_json(),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=event_type.Id,
                                                                             status=response.status_code,
                                                                             reason=response.text))

        event_type = SdsType.from_json(json.loads(response.content))
        response.close()
        return event_type

    def create_or_update_type(self, namespace_id, event_type):
        """Tells Sds Service to create a type based on local 'type' object"""
        if namespace_id is None:
            raise TypeError
        if event_type is None or not isinstance(event_type, SdsType):
            raise TypeError

        response = requests.put(
            self.url + self.__typesPath.format(self.tenantId, namespace_id, event_type.Id),
            data=event_type.to_json(), headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=event_type.Id,
                                                                             status=response.status_code,
                                                                             reason=response.text))

        response.close()

    def delete_type(self, namespace_id, type_id):
        """Tells Sds Service to delete the type specified by 'type_id'"""
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.url + self.__typesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id, type_id=type_id),
            headers=self.__sds_headers())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsType, {type_id}. {status}:{reason}".
                           format(type_id=type_id, status=response.status_code, reason=response.text))
        response.close()

    def get_stream(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Sds Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        stream = SdsStream.from_json(json.loads(response.content))
        response.close()
        return stream

    def get_stream_type(self, namespace_id, stream_id):
        """Retrieves a stream specified by 'stream_id' from the Sds Service"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id) + "/Type",
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        event_type = SdsType.from_json(json.loads(response.content))
        response.close()
        return event_type

    def get_streams(self, namespace_id, query="", skip=0, count=100):
        """Retrieves a list of streams associated with 'namespace_id' under the current tenant"""
        if namespace_id is None:
            raise TypeError
        if query is None:
            raise TypeError

        response = requests.get(
            self.url + self.__getStreamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id, query=query,
                                                    skip=skip, count=count),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get all SdsStreams. {status}:{reason}".
                           format(status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        results = []
        for item in content:
            results.append(SdsStream.from_json(item))
        response.close()
        return results

    def get_or_create_stream(self, namespace_id, stream):
        """Tells Sds Service to create a stream based on the local 'stream' SdsStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError
        response = requests.post(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream.Id),
            data=stream.to_json(),
            headers=self.__sds_headers())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to create SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        stream = SdsStream.from_json(json.loads(response.content))
        response.close()
        return stream

    def create_or_update_stream(self, namespace_id, stream):
        """Tells Sds Service to create a stream based on the local 'stream' SdsStream object"""
        if namespace_id is None:
            raise TypeError
        if stream is None or not isinstance(stream, SdsStream):
            raise TypeError
        req_url = self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                       stream_id=stream.Id)
        payload = stream.to_json()
        hdrs = self.__sds_headers()

        response = requests.put(
            url=req_url,
            data=payload,
            headers=hdrs)
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to create SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream.Id, status=response.status_code, reason=response.text))

        response.close()

    def delete_stream(self, namespace_id, stream_id):
        """Tells Sds Service to delete the stream speficied by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError

        response = requests.delete(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def create_or_update_tags(self, namespace_id, stream_id, tags):
        """Tells Sds Service to create tags and associate them with the given streamid """
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id) + "/Tags",
            data=json.dumps(tags),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to create tags for Stream: {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def create_or_update_metadata(self, namespace_id, stream_id, metadata):
        """Tells Sds Service to create metadata and associate them with the given streamid"""
        if namespace_id is None:
            raise TypeError

        response = requests.put(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id) + "/Metadata",
            data=json.dumps(metadata),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to create metadata for Stream: {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def get_tags(self, namespace_id, stream_id):
        """Tells Sds Service to get tags associated with the given streamid """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id) + "/Tags",
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to get tags for Stream: {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return content

    def get_metadata(self, namespace_id, stream_id, key):
        """Tells Sds Service to get metadata associated with the given streamid and key"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.url + self.__streamsPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id) + "/Metadata/" + key,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get metadata for Stream: {stream_id} and Key {key}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, key=key, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return content

    # The following section provides functionality to interact with Data
    #    We assume the value(s) passed follow the Sds object patterns supporting from_json and to_json method

    def get_value(self, namespace_id, stream_id, index, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service for value specified by 'index' from Sds Service """
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if index is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.url + self.__getValueQuery.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                   stream_id=stream_id, index=index, streamView_id=streamView_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to get value for SdsStream, {stream_id}. {status}:{reason}".format(stream_id=stream_id,
                                                                                           status=response.status_code,
                                                                                           reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.from_json(content)

    def get_first_value(self, namespace_id, stream_id, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service the first value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.url + self.__getFirstValue.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                   stream_id=stream_id, streamView_id=streamView_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get first value for SdsStream {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.from_json(content)

    def get_last_value(self, namespace_id, stream_id, value_class, streamView_id=""):
        """Retrieves JSON object from Sds Service the last value to be added to the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value_class is None:
            raise TypeError

        response = requests.get(
            self.url + self.__getLastValue.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                  stream_id=stream_id, streamView_id=streamView_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get last value for SdsStream {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
        return value_class.from_json(content)

    def get_window_values(self, namespace_id, stream_id, value_class, start, end, streamView_id=""):
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
            self.url + self.__getWindowValues.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                     stream_id=stream_id, start=start, end=end, streamView_id=streamView_id),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get window values for SdsStream {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()

        values = []
        for c in content:
            values.append(value_class.from_dictionary(c))
        return values

    def insert_value(self, namespace_id, stream_id, value):
        """Tells Sds Service to insert a value, described by the local object 'value', into
        the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        if callable(getattr(value, "to_json", None)):
            payload = value.to_json()
        else:
            payload = value

        response = requests.post(
            self.url + self.__insertValuePath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                     stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to insert value for SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))
        response.close()

    def insert_values(self, namespace_id, stream_id, values):
        """Tells Sds Service to insert the values, defined by the list 'values', into
        the stream specified by 'stream_id'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        if callable(getattr(values[0], "to_json", None)):
            events = []
            for value in values:
                time.sleep(0.5)
                events.append(value.to_dictionary())
            payload = json.dumps(events)
        else:
            payload = values

        response = requests.post(
            self.url + self.__insertValuesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                      stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            cleanup(self, namespace_id, self.type_names)
            raise SdsError("Failed to insert multiple values for SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

    def update_value(self, namespace_id, stream_id, value):
        """Tells Sds Service to update the value described by 'value', a local SdsValue object"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        if callable(getattr(value, "to_json", None)):
            payload = value.to_json()
        else:
            payload = value

        response = requests.put(
            self.url + self.__updateValuePath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                     stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to update value for SdsStream, {}. {}:{}".format(stream_id,
                                                                         response.status_code,
                                                                         response.text))

        response.close()

    def update_values(self, namespace_id, stream_id, values):
        """Tells Sds Service to update values defined by the SdsValue list, 'values'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        if callable(getattr(values[0], "to_json", None)):
            events = []
            for value in values:
                events.append(value.to_dictionary())
            payload = json.dumps(events)
        else:
            payload = values

        response = requests.put(
            self.url + self.__updateValuesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                      stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to update all values for SdsStream, {}. {}:{}".format(stream_id,
                                                                              response.status_code,
                                                                              response.text))

        response.close()

    def replace_value(self, namespace_id, stream_id, value):
        """Tells Sds Service to replace the value specified by 'value'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if value is None:
            raise TypeError

        if callable(getattr(value, "to_json", None)):
            payload = value.to_json()
        else:
            payload = value

        response = requests.put(
            self.url + self.__replaceValuePath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                      stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to replace value for SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def replace_values(self, namespace_id, stream_id, values):
        """Tells Sds Service to replace the values defined by the list 'values'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if values is None:
            raise TypeError

        if callable(getattr(values[0], "to_json", None)):
            events = []
            for value in values:
                events.append(value.to_dictionary())
            payload = json.dumps(events)
        else:
            payload = values

        response = requests.put(
            self.url + self.__replaceValuesPath.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                       stream_id=stream_id),
            data=payload,
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to replace value for SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def remove_value(self, namespace_id, stream_id, key):
        """Tells Sds Service to delete the value with a key property matching 'key'"""
        if namespace_id is None:
            raise TypeError
        if stream_id is None:
            raise TypeError
        if key is None:
            raise TypeError

        response = requests.delete(
            self.url + self.__removeValue.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                 stream_id=stream_id, index=key),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to remove value for SdsStream, {stream_id}. {status}:{reason}".
                           format(stream_id=stream_id, status=response.status_code, reason=response.text))

        response.close()

    def remove_window_value(self, namespace_id, stream_id, start, end):
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
            self.url + self.__removeWindowValues.format(tenant_id=self.tenantId, namespace_id=namespace_id,
                                                        stream_id=stream_id, start=start, end=end),
            headers=self.__sds_headers())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to remove all values for SdsStream, {}. {}:{}".format(stream_id,
                                                                              response.status_code,
                                                                              response.text))

        response.close()

    # private methods

    def __get_token(self):
        if (self.__expiration - time.time()) > 5 * 60:
            return self.__token

        discoveryUrl = requests.get(
            self.url + "/identity/.well-known/openid-configuration",
            headers= {"Accept" : "application/json"})

        if discoveryUrl.status_code < 200 or discoveryUrl.status_code >= 300:
            discoveryUrl.close()
            raise SdsError("Failed to get access token endpoint from discovery URL: {status}:{reason}".
                            format(status=discoveryUrl.status_code, reason=discoveryUrl.text))

        tokenEndpoint = json.loads(discoveryUrl.content)["token_endpoint"]

        tokenInformation = requests.post(
            tokenEndpoint,
            data = {"client_id" : self.clientId,
                    "client_secret" : self.clientSecret,
                    "grant_type" : "client_credentials"})

        token = json.loads(tokenInformation.content)

        if token is None:
            raise Exception("Failed to retrieve Token")
            
        if token is None:
            raise Exception("Failed to retrieve AAD Token")

        self.__expiration = float(token['expires_in']) + time.time()
        self.__token = token['access_token']
        return self.__token

    def __sds_headers(self):
        return {"Authorization": "bearer %s" % self.__get_token(),
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
                }

    @staticmethod
    def __validate_uri(url):
        split_uri = urlparse(url)
        return split_uri.netloc + split_uri.path

    def __set_path_and_query_templates(self):
        self.__basePath = "/api/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types/{type_id}"
        self.__getTypesPath = self.__basePath + "/Types?skip={skip}&count={count}"
        self.__streamViewsPath = self.__basePath + "/StreamViews/{streamView_id}"
        self.__getStreamViewsPath = self.__basePath + "/StreamViews?skip={skip}&count={count}"
        self.__streamsPath = self.__basePath + "/Streams/{stream_id}"
        self.__getStreamsPath = self.__basePath + "/Streams?query={query}&skip={skip}&count={count}"

        self.__dataPath = self.__basePath + "/Streams/{stream_id}/Data"
        self.__getValueQuery = self.__dataPath + "/GetValue?index={index}&streamViewId={streamView_id}"
        self.__getFirstValue = self.__dataPath + "/GetFirstValue?streamViewId={streamView_id}"
        self.__getLastValue = self.__dataPath + "/GetLastValue?streamViewId={streamView_id}"
        self.__getWindowValues = self.__dataPath + "/GetWindowValues?startIndex={start}&endIndex={end}&streamViewId={streamView_id}"
        self.__getRangeValuesQuery = self.__dataPath + "/GetRangeValues?startIndex={start}" \
                                                       "&skip={skip}" \
                                                       "&count={count}" \
                                                       "&reversed={reverse}" \
                                                       "&boundaryType={boundary_type}" \
                                                       "&streamViewId={streamView_id}"

        self.__insertValuePath = self.__dataPath + "/InsertValue"
        self.__insertValuesPath = self.__dataPath + "/InsertValues"
        self.__updateValuePath = self.__dataPath + "/UpdateValue"
        self.__updateValuesPath = self.__dataPath + "/UpdateValues"
        self.__replaceValuePath = self.__dataPath + "/ReplaceValue"
        self.__replaceValuesPath = self.__dataPath + "/ReplaceValues"
        self.__removeValue = self.__dataPath + "/RemoveValue?index={index}"
        self.__removeWindowValues = self.__dataPath + "/RemoveWindowValues?startIndex={start}&endIndex={end}"
