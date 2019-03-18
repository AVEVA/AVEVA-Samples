# DataviewIndexConfig.py
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

class DataviewIndexConfig(object):
    """ dataview index config definition"""
    @property
    def IsDefault(self):
        return self.__isDefault
    @IsDefault.setter
    def IsDefault(self, isDefault):
        self.__isDefault = isDefault
    
    @property
    def StartIndex(self):
        return self.__startIndex
    @StartIndex.setter
    def StartIndex(self, startIndex ):
        self.__startIndex = startIndex    
    
    @property
    def EndIndex(self):
        return self.__endIndex
    @EndIndex.setter
    def EndIndex(self, endIndex ):
        self.__endIndex = endIndex    
		
    @property
    def Mode(self):
        return self.__mode
    @Mode.setter
    def Mode(self, mode ):
        self.__mode = mode 
		
    @property
    def Interval(self):
        return self.__interval
    @Interval.setter
    def Interval(self, interval ):
        self.__interval = interval 


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'IsDefault' : self.IsDefault}
	
        if hasattr(self, 'StartIndex'):
            dictionary['StartIndex'] = self.StartIndex

        if hasattr(self, 'EndIndex'):
            dictionary['EndIndex'] = self.EndIndex

        if hasattr(self, 'Mode'):
            dictionary['Mode'] = self.Mode

        if hasattr(self, 'Interval'):
            dictionary['Interval'] = self.Interval			

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewIndexConfig.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewIndexConfig = DataviewIndexConfig()

        if len(content) == 0:
            return dataviewIndexConfig

        if 'IsDefault' in content:
            dataviewIndexConfig.IsDefault = content['IsDefault']

        if 'StartIndex' in content:
            dataviewIndexConfig.StartIndex = content['StartIndex']

        if 'EndIndex' in content:
            dataviewIndexConfig.EndIndex = content['EndIndex']

        if 'Mode' in content:
            dataviewIndexConfig.Mode = content['Mode']

        if 'Interval' in content:
            dataviewIndexConfig.Interval = content['Interval']
        
            

        return dataviewIndexConfig

