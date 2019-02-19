# SdsStream.py
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
from .SdsStreamIndex import SdsStreamIndex
from .SdsStreamPropertyOverride import SdsStreamPropertyOverride

class SdsStream(object):
    """Sds stream definition"""

    def __init__(self, id = None, name = None, description = None, typeId = None, propertyOverrides = None, indexes = None, interpolationMode = None, extrapolationMode = None):
        self.Id = id
        self.Name = name
        self.Description = description
        self.TypeId = typeId
        self.PropertyOverrides = propertyOverrides
        self.Indexes = indexes
        self.InterpolationMode = interpolationMode
        self.ExtrapolationMode = extrapolationMode

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
    def TypeId(self):
        return self.__typeId
    @TypeId.setter
    def TypeId(self, typeId):
        self.__typeId = typeId
		
    @property
    def PropertyOverrides(self):
        return self.__propertyOverrides
    @PropertyOverrides.setter
    def PropertyOverrides(self, propertyOverrides):
        self.__propertyOverrides = propertyOverrides

    @property
    def Indexes(self):
        return self.__indexes 
    @Indexes.setter
    def Indexes(self, indexes):
        self.__indexes = indexes

    @property
    def InterpolationMode(self):
        return self.__interpolationMode
    @InterpolationMode.setter
    def InterpolationMode(self, interpolationMode):
        self.__interpolationMode = interpolationMode

    @property
    def ExtrapolationMode(self):
        return self.__extrapolationMode
    @ExtrapolationMode.setter
    def ExtrapolationMode(self, extrapolationMode):
        self.__extrapolationMode = extrapolationMode

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id, 'TypeId' : self.TypeId }

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'InterpolationMode'):
            dictionary['InterpolationMode'] = self.InterpolationMode

        if hasattr(self, 'ExtrapolationMode'):
            dictionary['ExtrapolationMode'] = self.ExtrapolationMode
            
        if hasattr(self, 'PropertyOverrides'):
            if self.PropertyOverrides is not None:                
                dictionary['PropertyOverrides'] = []
                for value in self.PropertyOverrides:
                    dictionary['PropertyOverrides'].append(value.toDictionary())

        if hasattr(self, 'Indexes'):
            if self.Indexes is not None:     
                dictionary['Indexes'] = []
                for value in self.Indexes:
                    dictionary['Indexes'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStream.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        stream = SdsStream()

        if len(content) == 0:
            return stream

        if 'Id' in content:
            stream.Id = content['Id']

        if 'Name' in content:
            stream.Name = content['Name']

        if 'Description' in content:
            stream.Description = content['Description']

        if 'InterpolationMode' in content:
            stream.InterpolationMode = content['InterpolationMode']

        if 'ExtrapolationMode' in content:
            stream.ExtrapolationMode = content['ExtrapolationMode']

        if 'TypeId' in content:
            stream.TypeId = content['TypeId']
        
        if 'PropertyOverrides' in content:
            propertyOverrides = content['PropertyOverrides']
            if propertyOverrides is not None and len(propertyOverrides) > 0:
                stream.PropertyOverrides = []
                for value in propertyOverrides:
                    stream.PropertyOverrides.append(SdsStreamPropertyOverride.fromDictionary(value))
            
        if 'Indexes' in content:
            indexes = content['Indexes']
            if indexes is not None and len(indexes) > 0:
                stream.Indexes = []
                for value in indexes:
                    stream.Indexes.append(SdsStreamIndex.fromDictionary(value))

        return stream

