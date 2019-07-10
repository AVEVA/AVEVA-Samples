# Types.py
#


import json

from .SDS.SdsType import SdsType
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
            self.__typePath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                type_id=type_id),
            headers=self.__baseClient.sdsHeaders())
        self.__baseClient.checkResponse(
            response, f"Failed to get SdsType, {type_id}.")

        _type = SdsType.fromJson(json.loads(response.content))
        response.close()
        return _type

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
            self.__typeRefCountPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                type_id=type_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to get SdsType reference count, {type_id}.")

        counts = json.loads(response.content)
        response.close()
        return counts

    def getTypes(self, namespace_id, skip=0, count=100, query=""):
        """
        Retrieves a list of types associated with the specified 'namespace_id'
            under the current tenant
        :param namespace_id: id of namespace to work against
        :param skip: number of types to skip, used for paging
        :param count: number of types to retrieve
        :param query: optional query.  Default is ""
        :return: array of types as SdsType
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__typesPath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id),
            params={"skip": skip, "count": count, "query": query},
            headers=self.__baseClient.sdsHeaders())
        self.__baseClient.checkResponse(
            response, "Failed to get all SdsTypes.")

        types = json.loads(response.content)
        results = []
        for t in types:
            results.append(SdsType.fromJson(t))
        response.close()
        return results

    def getOrCreateType(self, namespace_id, type):
        """
        Tells Sds Service to create or get a type based on local 'type'
        or get if existing type matches

        :param namespace_id: id of namespace to work against
        :param type:  the SdsType to create or get
        :return:  the created or retrieved SdsType
        """
        if namespace_id is None:
            raise TypeError
        if type is None or not isinstance(type, SdsType):
            raise TypeError
        response = requests.post(
            self.__typePath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                type_id=type.Id),
            data=type.toJson(),
            headers=self.__baseClient.sdsHeaders())
        self.__baseClient.checkResponse(
            response, f"Failed to create type, {type.Id}.")

        type = SdsType.fromJson(json.loads(response.text))
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
            self.__typePath.format(
                tenant_id=self.__tenant,
                namespace_id=namespace_id,
                type_id=type_id),
            headers=self.__baseClient.sdsHeaders())

        self.__baseClient.checkResponse(
            response, f"Failed to delete SdsType, {type_id}.")

        response.close()

    # private methods

    def __setPathAndQueryTemplates(self):
        """
        used to create needed URI for the other calls
        :return:
        """
        self.__basePath = self.__url + \
            "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        self.__typesPath = self.__basePath + "/Types"
        self.__typePath = self.__typesPath + "/{type_id}"
        self.__typeRefCountPath = self.__typePath + "/ReferenceCount"
