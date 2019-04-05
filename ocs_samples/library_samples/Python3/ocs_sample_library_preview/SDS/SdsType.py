# SdsType.py
#
# Copyright 2019 OSIsoft, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
import json
import inspect
from .SdsTypeCode import SdsTypeCode
from .SdsTypeProperty import SdsTypeProperty

class SdsType(object):
    """Sds type definitions"""
    def __init__(self, id = None, name = None, description = None, baseType = None, sdsTypeCode = SdsTypeCode.Empty, properties = None):
        self.SdsTypeCode = sdsTypeCode
        self.Id = id
        self.Name = name
        self.Description = description
        self.BaseType = baseType
        self.Properties = properties


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
    def SdsTypeCode(self):
        return self.__typeCode
    @SdsTypeCode.setter
    def SdsTypeCode(self, typeCode):
        self.__typeCode = typeCode

    @property
    def Properties(self):
        return self.__properties
    @Properties.setter
    def Properties(self, properties):
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SdsTypeCode' : self.SdsTypeCode.value }

        # optional properties
        if hasattr(self, 'Properties') :
            if(self.Properties is not None):
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
                    type.Properties.append(SdsTypeProperty.fromDictionary(value))

        return type
