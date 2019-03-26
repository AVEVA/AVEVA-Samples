# DataviewGroupRule.py
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

class DataviewGroupRule(object):
    """Sds dataview definition"""
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Type(self):
        return self.__type
    @Type.setter
    def Type(self, type_):
        self.__type = type_    

    
    @property
    def TokenRules(self):
        return self.__tokenRules
    @TokenRules.setter
    def TokenRules(self, tokenRules):
        self.__tokenRules = tokenRules    

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id}
        
        if hasattr(self, 'Type'):
            dictionary['Type'] = self.Type

        if hasattr(self, 'TokenRules'):
            dictionary['TokenRules'] = self.TokenRules
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewGroupRule.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewGroupRule = DataviewGroupRule()

        if len(content) == 0:
            return dataviewGroupRule

        if 'Id' in content:
            dataviewGroupRule.Id = content['Id']
			

        if 'Type' in content:
            dataviewGroupRule.Id = content['Type']
            

        if 'TokenRules' in content:
            dataviewGroupRule.Id = content['TokenRules']


        return dataviewGroupRule

