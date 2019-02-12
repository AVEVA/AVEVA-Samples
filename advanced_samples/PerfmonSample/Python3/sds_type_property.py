# sds_type_property.py
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
import sds_type


class SdsTypeProperty(object):
    """Sds type property definition"""
    def __init__(self):
        self.__IsKey = False

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
    def IsKey(self):
        return self.__IsKey

    @IsKey.setter
    def IsKey(self, IsKey):
        self.__IsKey = IsKey

    @property
    def SdsType(self):
        return self.__SdsType

    @SdsType.setter
    def SdsType(self, SdsType):
        self.__SdsType = SdsType

    def to_dictionary(self):
        dictionary = {'IsKey': self.IsKey}

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'SdsType'):
            dictionary['SdsType'] = self.SdsType.to_dictionary()

        if hasattr(self, 'Value'):
            if isinstance(self.Value, Enum):
                dictionary['Value'] = self.Value.name
            else:
                dictionary['Value'] = self.Value

        if hasattr(self, 'Order'):
            dictionary['Order'] = self.Order

        return dictionary

    @staticmethod
    def from_dictionary(content):
        prop_names = ['Id', 'IsKey', 'Name', 'Description', 'SdsType', 'Value', 'Order']
        type_property = SdsTypeProperty()

        if len(content) == 0:
            return type_property

        for prop_name in prop_names:
            if prop_name in content:
                if prop_name == 'SdsType':
                    val = sds_type.SdsType.from_dictionary(content['SdsType'])
                else:
                    val = content[prop_name]
                type_property.__setattr__(prop_name, val)

        return type_property
