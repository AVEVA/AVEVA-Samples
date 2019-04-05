# SdsTypeProperty.py
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

class SdsTypeProperty(object):
    """Sds type property definition"""

    def __init__(self, id = None, name =None, description = None, isKey = False, sdsType = None, value = None, order = None):
            self.Id = id
            self.Description = description
            self.IsKey = isKey
            self.SdsType = sdsType
            self.Value = value
            self.Order = order
            
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
    def Description(self, Description):
        self.__description = Description

    @property
    def IsKey(self):
        return self.__isKey
    @IsKey.setter
    def IsKey(self, iskey):
        self.__isKey = iskey

    @property
    def SdsType(self):
        return self.__sdsType
    @SdsType.setter
    def SdsType(self, sdsType):
        self.__sdsType = sdsType

    @property
    def Value(self):
        return self.__value
    @Value.setter
    def Value(self, value):
        self.__value = value

    @property
    def Order(self):
        return self.__order
    @Order.setter
    def Order(self, order):
        self.__order = order
    
    def toDictionary(self):
        dictionary = { 'IsKey' : self.IsKey }

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'SdsType'):            
            from .SdsType import SdsType
            dictionary['SdsType'] = self.SdsType.toDictionary()

        if hasattr(self, 'Value'):
            if (isinstance(self.Value, Enum)):
                dictionary['Value'] = self.Value.name
            else:
                dictionary['Value'] = self.Value

        if hasattr(self, 'Order'):
            dictionary['Order'] = self.Order

        return dictionary

    @staticmethod
    def fromDictionary(content):
        typeProperty = SdsTypeProperty()

        if len(content) == 0:
            return typeProperty

        if 'Id' in content:
            typeProperty.Id = content['Id']
            
        if 'IsKey' in content:
            typeProperty.IsKey = content['IsKey']

        if 'Name' in content:
            typeProperty.Name = content['Name']

        if 'Description' in content:
            typeProperty.Description = content['Description']

        if 'SdsType' in content:
            from .SdsType import SdsType
            typeProperty.SdsType = SdsType.fromDictionary(content['SdsType'])

        if 'Value' in content:
            typeProperty.Value = content['Value']

        if 'Order' in content:
            typeProperty.Order = content['Order']
            
        return typeProperty
