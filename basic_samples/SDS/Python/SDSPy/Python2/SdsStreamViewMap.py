# SdsStreamViewMap.py
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

from JsonEncoder import Encoder
import json
import inspect
from SdsStreamViewProperty import SdsStreamViewProperty

class SdsStreamViewMap(object):
    """SdsStreamViewMap definitions"""

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
        dictionary = { 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

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
                    streamViewMap.Properties.append(SdsStreamViewProperty.fromDictionary(value))

        return streamViewMap
