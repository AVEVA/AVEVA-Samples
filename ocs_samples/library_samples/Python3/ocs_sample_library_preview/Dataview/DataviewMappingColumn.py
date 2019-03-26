# DataviewMappingColumn.py
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

class DataviewMappingColumn(object):
    """Sds dataview definition"""
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, name):
        self.__name = name
    
    @property
    def IsKey(self):
        return self.__isKey
    @IsKey.setter
    def IsKey(self, isKey):
        self.__isKey= isKey

    @property
    def DataType(self):
        return self.__dataType
    @DataType.setter
    def DataType(self, dataType):
        self.__dataType = dataType
		   
    @property
    def MappingRule(self):
        return self.__MappingRule
    @MappingRule.setter
    def MappingRule(self, MappingRule):
        self.__MappingRule= MappingRule
    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Name' : self.Name}
        dictionary['IsKey'] = self.IsKey
        
        if hasattr(self, 'DataType'):
            dictionary['DataType'] = self.DataType
        
        if hasattr(self, 'MappingRule'):
            dictionary['MappingRule'] = self.MappingRule      

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewMappingColumn.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewMappingColumn = DataviewMappingColumn()

        if len(content) == 0:
            return dataviewMappingColumn

        if 'Name' in content:
            dataviewMappingColumn.Name = content['Name']

        if 'IsKey' in content:
            dataviewMappingColumn.IsKey = content['IsKey']

        if 'DataType' in content:
            dataviewMappingColumn.DataType = content['DataType']

        if 'MappingRule' in content:
            dataviewMappingColumn.MappingRule = content['MappingRule']       
            

        return dataviewMappingColumn

