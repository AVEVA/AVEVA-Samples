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
    def PropertyMappingRule(self):
        return self.__propertyMappingRule
    @PropertyMappingRule.setter
    def PropertyMappingRule(self, propertyMappingRule):
        self.__propertyMappingRule= propertyMappingRule
    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Name' : self.Name}
        dictionary['IsKey'] = self.IsKey
        
        if hasattr(self, 'PropertyMappingRule'):
            dictionary['PropertyMappingRule'] = self.PropertyMappingRule      

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

        if 'PropertyMappingRule' in content:
            dataviewMappingColumn.PropertyMappingRule = content['PropertyMappingRule']       
            

        return dataviewMappingColumn

