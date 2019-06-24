# SdsStreamIndex.py
#

import json


class SdsStreamIndex(object):
    """
    Sds Stream Index definitions
    """

    @property
    def SdsTypePropertyId(self):
        """
        id of property   required
        :return:
        """
        return self.__sdsTypePropertyId

    @SdsTypePropertyId.setter
    def SdsTypePropertyId(self, sdsTypePropertyId):
        """
        id of property   required
        :param sdsTypePropertyId:
        :return:
        """
        self.__sdsTypePropertyId = sdsTypePropertyId

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'SdsTypePropertyId': self.SdsTypePropertyId}

        return dictionary

    @staticmethod
    def fromDictionary(content):
        typePropertyId = SdsStreamIndex()

        if len(content) == 0:
            return typePropertyId

        if 'SdsTypePropertyId' in content:
            typePropertyId.SdsTypePropertyId = content['SdsTypePropertyId']

        return typePropertyId
