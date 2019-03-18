# SdsStreamView.py
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

import json
import inspect
from .SdsStreamViewProperty import SdsStreamViewProperty

class SdsStreamView(object):
    """Sds StreamView definitions"""
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
    def SourceTypeId(self):
        return self.__sourceTypeId
    @SourceTypeId.setter
    def SourceTypeId(self, baseType):
        self.__sourceTypeId = baseType
    
    @property
    def TargetTypeId(self):
        return self.__targetTypeId
    @TargetTypeId.setter
    def TargetTypeId(self, typeCode):
        self.__targetTypeId = typeCode

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
        dictionary = { 'Id' : self.Id, 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

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
                    streamView.Properties.append(SdsStreamViewProperty.fromDictionary(value))

        return streamView
