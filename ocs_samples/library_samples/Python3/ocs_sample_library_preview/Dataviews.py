# Dataviews.py
#

import json

from .Dataview.Dataview import Dataview
from .Dataview.Datagroup import Datagroup

import requests


class Dataviews(object):
    """
    Client for interacting with Dataviews
    """

    def __init__(self, client):
        """
        Initiliizes the dataviews client
        :param client: This is the base client that is used to make the callss
        """
        self.__baseClient = client
        self.__setPathAndQueryTemplates()

    def postDataview(self, namespace_id, dataview):
        """Tells Sds Service to create a dataview based on local 'dataview'
            or get if existing dataview matches
        :param namespace_id: namespace to work against
        :param dataview: dataview definition.  Dataview object expected
        :return: Retrieved dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError

        response = requests.post(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview.Id,
            ),
            data=dataview.toJson(),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to create dataview, {dataview.Id}."
        )

        dataview = Dataview.fromJson(response.json())
        return dataview

    def putDataview(self, namespace_id, dataview):
        """Tells Sds Service to update a dataview based on local 'dataview'
        :param namespace_id: namespace to work against
        :param dataview: dataview defintion.  Dataview object expected
        :return: Retreived dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError
        response = requests.put(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview.Id,
            ),
            data=dataview.toJson(),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to update dataview, {dataview.Id}."
        )

        # dataview = Dataview.fromJson(response.json()) # empty content on 204 per spec (Brandon)
        return  # dataview

    def deleteDataview(self, namespace_id, dataview_id):
        """
        Tells Sds Service to delete a dataview based on 'dataview_id'
        :param namespace_id: namespace to work against
        :param dataview_id:  id of dataview to delete
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.delete(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to delete dataview, {dataview_id}."
        )

        return

    def getDataview(self, namespace_id, dataview_id):
        """
        Retrieves the dataview specified by 'dataview_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id:  id of dataview to get
        :return: Retreived dataview as Dataview object
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.get(
            self.__dataviewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get dataview, {dataview_id}."
        )

        dataview = Dataview.fromJson(response.json())
        return dataview

    def getDataviews(self, namespace_id, skip=0, count=100):
        """
        Retrieves all of the dataviews from Sds Service
        :param namespace_id: namespace to work against
        :param skip: Number of dataviews to skip
        :param count: Number of dataviews to return
        :return: array of dataviews
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataviewsPath.format(
                tenant_id=self.__baseClient.tenant, namespace_id=namespace_id
            ),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(response, "Failed to get dataviews.")

        dataviews = json.loads(response.content)
        # Need to update this to handle the array better and handle 207s from endpoint
        if hasattr(dataviews, "DataViews"):
            dataviews = dataviews["DataViews"]

        results = []
        for t in dataviews:
            results.append(Dataview.fromJson(t))
        return results

    def getDatagroups(
        self, namespace_id, dataview_id, skip=0, count=100, returnAsDynamicObject=False
    ):
        """
        Retrieves all of the datagroups from the specified dataview from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param skip: Number of datagroups to skip
        :param count: Number of datagroups to return
        :param returnAsDynamicObject: returns the collection as dynamic object
                rather than a list of dataviews.  Added because the automated
                tests were failing.  Boolean
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__datagroupPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
            ),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get datagroups for dataview, {dataview_id}."
        )

        datagroups = json.loads(response.content)

        if returnAsDynamicObject:
            return datagroups

        results = []
        for datagroup in datagroups["DataGroups"]:
            results.append(Datagroup.fromJson(datagroup))

        return results

    def getDatagroup(self, namespace_id, dataview_id, datagroup_id):
        """
        Retrieves a datagroupby 'datagroup_id' from the specified
            dataview from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param datagroup_id: datagroup to retrieve
        :return: the asked for Datagroup
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__getDatagroup.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
                datagroup_id=datagroup_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response,
            f"Failed to get datagroup, {datagroup_id}," " for dataview, {dataview_id}.",
        )

        datagroup = Datagroup.fromJson(response.json())
        return datagroup

        # needs other parameters with smart

    def getDataInterpolated(
        self,
        namespace_id,
        dataview_id,
        count=None,
        form=None,
        continuationToken=None,
        startIndex=None,
        endIndex=None,
        interval=None,
        value_class=None,
    ):
        """
        Retrieves the interpolated data of the 'dataview_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataview_id: dataview to work against
        :param skip: number of values to skip
        :param count: number of values to return
        :param form: form definition
        :param startIndex: start index
        :param endIndex: end index
        :param interval: space between values
        :param value_class: Use this to auto format the data into the defined
            type.  The tpye is expected to have a fromJson method that takes a
            dynamicObject and converts it into the defined type.
          Otherwise you get a dynamic object
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        params = {
            "count": count,
            "form": form,
            "continuationToken": continuationToken,
            "startIndex": startIndex,
            "endIndex": endIndex,
            "interval": interval,
        }
        response = requests.get(
            self.__getDataInterpolated.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataview_id=dataview_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
            params=params,
        )

        self.__baseClient.checkResponse(
            response,
            f"Failed to get dataview data interpolated for dataview, {dataview_id}.",
        )

        continuation_token = None
        next_page = response.headers.get("NextPage", None)
        if next_page: 
            token_param = "&continuationToken="
            token_position = next_page.find(token_param)
            assert token_position > 0, "Could not find continuationToken in NextPage"
            end_position = next_page.find("&", token_position+1)
            end_position = None if end_position == -1 else end_position
            continuation_token = next_page[token_position + len(token_param):end_position]

        if form is not None:
            return response.text, continuation_token

        content = response.json()

        if value_class is None:
            return content, continuation_token
        return value_class.fromJson(content), continuation_token

    def __setPathAndQueryTemplates(self):
        """
        Internal  Sets the needed URLs
        :return:
        """
        self.__basePath = (
            self.__baseClient.uri_API + "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        )

        self.__dataviewsPath = self.__basePath + "/dataviews"
        self.__dataviewPath = self.__dataviewsPath + "/{dataview_id}"
        self.__datagroupPath = self.__dataviewPath + "/datagroups"
        self.__getDatagroup = self.__datagroupPath + "/{datagroup_id}"
        self.__getDataInterpolated = self.__dataviewPath + "/data/interpolated"
