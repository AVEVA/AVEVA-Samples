# Types.py
#


from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

from .SdsError import SdsError
from .SDS.SdsType import SdsType
from .SDS.SdsBoundaryType import SdsBoundaryType
import requests


class Types(object):
    """
    Handles communication with Sds Service
    """

    def __init__(self, client):
        self.__apiVersion = client.api_version
        self.__tenant = client.tenant
        self.__url = client.uri_API
        self.__baseClient = client

        self.__setPathAndQueryTemplates()

    def getType(self, namespace_id, type_id):
        """
        Retrieves the type specified by 'type_id' from Sds Service
        :param namespace_id: id of namespace to work against
        :param type_id: id of the type to get
        :return:the type as an SdsType
        """
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        type = SdsType.fromJson(json.loads(response.content))
        response.close()
        return type

    def getTypeReferenceCount(self, namespace_id, type_id):
        """
        Retrieves the number of times the type is referenced
        :param namespace_id: id of namespace to work against
        :param type_id: id of the type to get references of
        :return: reference count python dynamic object
        """
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__typesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id) + "/ReferenceCount",
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get SdsType reference count, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))
        
        counts = json.loads(response.content)
        response.close()
        return counts

    def getTypes(self, namespace_id, skip=0, count=100, query = ""):
        """
        Retrieves a list of types associated with the specified 'namespace_id' under the current tenant
        :param namespace_id: id of namespace to work against
        :param skip: number of types to skip, used for paging
        :param count: number of types to retrieve
        :param query: optional query.  Default is ""
        :return: array of types as SdsType
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__url + self.__getTypesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, skip=skip, count=count, query = query),
            headers=self.__baseClient.sdsHeaders())
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
        """
        Tells Sds Service to create or get a type based on local 'type' or get if existing type matches

        :param namespace_id: id of namespace to work against
        :param type:  the SdsType to create or get
        :return:  the created or retrieved SdsType
        """
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, SdsType):
            raise TypeError
        response = requests.post(
            self.__url + self.__typesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type.Id),
            data=type.toJson(), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to create type, {type_id}. {status}:{reason}".format(type_id=type.Id, status=response.status_code, reason=response.text))
        
        type = SdsType.fromJson(json.loads(response.content.decode('utf-8')))
        response.close()
        return type

    def deleteType(self, namespace_id, type_id):
        """
        Tells Sds Service to delete the type specified by 'type_id'

        :param namespace_id: id of namespace to work against
        :param type_id:  id of the type to delete
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if type_id is None:
            raise TypeError

        response = requests.delete(
            self.__url + self.__typesPath.format( tenant_id=self.__tenant, namespace_id=namespace_id, type_id=type_id),
            headers=self.__baseClient.sdsHeaders())

        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to delete SdsType, {type_id}. {status}:{reason}".
                          format(type_id=type_id, status=response.status_code, reason=response.text))

        response.close()
		
		
    # private methods


    def __setPathAndQueryTemplates(self):
        """
        used to create needed URI for the other calls
        :return:
        """
        self.__basePath = "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types/{type_id}"
        self.__getTypesPath = self.__basePath + "/Types?skip={skip}&count={count}&query={query}"
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
