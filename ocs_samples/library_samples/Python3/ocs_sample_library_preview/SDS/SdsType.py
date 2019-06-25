# SdsType.py
#

import json
from .SdsTypeCode import SdsTypeCode
from .SdsTypeProperty import SdsTypeProperty


class SdsType(object):
    """Sds type definitions"""
    def __init__(self, id=None, name=None, description=None, baseType=None,
                 sdsTypeCode=SdsTypeCode.Empty, properties=[]):
        """

        :param id: required
        :param name: not required
        :param description: not required
        :param baseType: not required
        :param sdsTypeCode: SdsTypeCode    required
        :param properties: array of SdsTypeProperty   required
        """
        self.SdsTypeCode = sdsTypeCode
        self.Id = id
        self.Name = name
        self.Description = description
        self.BaseType = baseType
        self.Properties = properties

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
    def BaseType(self):
        """
        not required
        :return:
        """
        return self.__baseType

    @BaseType.setter
    def BaseType(self, baseType):
        """
        not required
        :param baseType:
        :return:
        """
        self.__baseType = baseType

    @property
    def SdsTypeCode(self):
        """
        required
        :return:
        """
        return self.__typeCode

    @SdsTypeCode.setter
    def SdsTypeCode(self, typeCode):
        """
        SdsTypeCode    required
        :param typeCode:
        :return:
        """
        self.__typeCode = typeCode

    @property
    def Properties(self):
        """
        SdsTypeCode  required
        :return:
        """
        return self.__properties

    @Properties.setter
    def Properties(self, properties):
        """
        required
        :param properties:
        :return:
        """
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'SdsTypeCode': self.SdsTypeCode.value}

        # optional properties
        if hasattr(self, 'Properties'):
            if(self.Properties):
                dictionary['Properties'] = []
                for value in self.Properties:
                    dictionary['Properties'].append(value.toDictionary())

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        # if self.BaseType is not None and len(self.BaseType) > 0:
        if hasattr(self, 'BaseType'):
            if(self.BaseType is not None):
                dictionary['BaseType'] = self.BaseType.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsType.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        type = SdsType()

        if len(content) == 0:
            return type

        if 'Id' in content:
            type.Id = content['Id']

        if 'Name' in content:
            type.Name = content['Name']

        if 'Description' in content:
            type.Description = content['Description']

        if 'SdsTypeCode' in content:
            type.SdsTypeCode = SdsTypeCode(content['SdsTypeCode'])

        if 'BaseType' in content:
            type.BaseType = SdsType.fromDictionary(content['BaseType'])

        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                type.Properties = []
                for value in properties:
                    type.Properties.append(
                        SdsTypeProperty.fromDictionary(value))

        return type
