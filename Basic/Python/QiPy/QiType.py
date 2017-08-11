from enum import Enum
from JsonEncoder import Encoder
import json
import inspect
from QiTypeCode import QiTypeCode
from QiTypeProperty import QiTypeProperty

class QiType(object):
    """Qi type definitions"""
    def __init__(self):
        self.QiTypeCode = QiTypeCode.Empty

    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, name):
        self.__name = name
    
    @property
    def Description(self):
        return self.__description
    @Description.setter
    def Description(self, description):
        self.__description = description

    @property
    def BaseType(self):
        return self.__baseType
    @BaseType.setter
    def BaseType(self, baseType):
        self.__baseType = baseType
    
    @property
    def QiTypeCode(self):
        return self.__typeCode
    @QiTypeCode.setter
    def QiTypeCode(self, typeCode):
        self.__typeCode = typeCode

    @property
    def Properties(self):
        return self.__properties
    @Properties.setter
    def Properties(self, properties):
        self.__properties = properties

    def toJsonString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'QiTypeCode' : self.QiTypeCode.value }

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        #if self.BaseType is not None and len(self.BaseType) > 0:
        if hasattr(self, 'BaseType'):
            dictionary['BaseType'] = self.BaseType.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return QiType.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        type = QiType()

        if len(content) == 0:
            return type

        if 'Id' in content:
            type.Id = content['Id']

        if 'Name' in content:
            type.Name = content['Name']

        if 'Description' in content:
            type.Description = content['Description']

        if 'QiTypeCode' in content:
            type.QiTypeCode = QiTypeCode(content['QiTypeCode'])

        if 'BaseType' in content:
            type.BaseType = QiType.fromDictionary(content['BaseType'])
       
        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                type.Properties = []
                for value in properties:
                    type.Properties.append(QiTypeProperty.fromDictionary(value))

        return type