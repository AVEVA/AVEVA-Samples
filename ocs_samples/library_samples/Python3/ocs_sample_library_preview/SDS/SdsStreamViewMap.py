# SdsStreamViewMap.py
#

import json
from .SdsStreamViewProperty import SdsStreamViewProperty


class SdsStreamViewMap(object):
    """
    SdsStreamViewMap definitions
    """

    @property
    def SourceTypeId(self):
        """
        required
        :return:
        """
        return self.__sourceTypeId

    @SourceTypeId.setter
    def SourceTypeId(self, baseType):
        """
        required
        :param baseType:
        :return:
        """
        self.__sourceTypeId = baseType

    @property
    def TargetTypeId(self):
        """
        required
        :return:
        """
        return self.__targetTypeId

    @TargetTypeId.setter
    def TargetTypeId(self, typeCode):
        """
        required
        :param typeCode:
        :return:
        """
        self.__targetTypeId = typeCode

    @property
    def Properties(self):
        """
        list of SdsStreamViewMapProperty    not required
        :return:
        """
        return self.__properties

    @Properties.setter
    def Properties(self, properties):
        """
        list of SdsStreamViewMapProperty    not required
        :param properties:
        :return:
        """
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'SourceTypeId': self.SourceTypeId,
                      'TargetTypeId': self.TargetTypeId}

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStreamViewMap.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        streamViewMap = SdsStreamViewMap()

        if len(content) == 0:
            return streamViewMap

        if 'TargetTypeId' in content:
            streamViewMap.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            streamViewMap.SourceTypeId = content['SourceTypeId']

        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                streamViewMap.Properties = []
                for value in properties:
                    streamViewMap.Properties.append(
                        SdsStreamViewProperty.fromDictionary(value))

        return streamViewMap
