# SdsStreamView.py
#

import json
from .SdsStreamViewProperty import SdsStreamViewProperty


class SdsStreamView(object):
    """
    Sds StreamView definitions
    """

    @property
    def Id(self):
        """
        required
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """
        required
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Name(self):
        """
        not required
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        not required
        :param name:
        :return:
        """
        self.__name = name

    @property
    def Description(self):
        """
        not required
        :return:
        """
        return self.__description

    @Description.setter
    def Description(self, description):
        """
        not required
        :param description:
        :return:
        """
        self.__description = description

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
        array of SdsStreamViewProperty   not required
        :return:
        """
        return self.__properties

    @Properties.setter
    def Properties(self, properties):
        """
        array of SdsStreamViewProperty   not required
        :param properties:
        :return:
        """
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Id': self.Id, 'SourceTypeId': self.SourceTypeId,
                      'TargetTypeId': self.TargetTypeId}

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStreamView.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        streamView = SdsStreamView()

        if len(content) == 0:
            return streamView

        if 'Id' in content:
            streamView.Id = content['Id']

        if 'Name' in content:
            streamView.Name = content['Name']

        if 'Description' in content:
            streamView.Description = content['Description']

        if 'TargetTypeId' in content:
            streamView.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            streamView.SourceTypeId = content['SourceTypeId']

        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                streamView.Properties = []
                for value in properties:
                    streamView.Properties.append(
                        SdsStreamViewProperty.fromDictionary(value))

        return streamView
