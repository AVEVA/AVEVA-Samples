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
    """
    DataviewGroupRule
    """
    
    def __init__(self, id = None, type_= None, tokenRules = None):
        self.__id = id
        self.__type= type_
        self.__tokenRules = tokenRules


    @property
    def Id(self):
        """
        unique id   required
        :return:
        """
        return self.__id
    @Id.setter
    def Id(self, id):
        """
        unique id   required
        :param id:
        :return:
        """
        self.__id = id
    
    @property
    def Type(self):
        """
        Stream property to base grouping on   not required
        :return:
        """
        return self.__type
    @Type.setter
    def Type(self, type_):
        """
        Stream property to base grouping on   not required
        :param type_:
        :return:
        """
        self.__type = type_    

    
    @property
    def TokenRules(self):
        """
        token rules that create patterns for groups   required
        :return:
        """
        return self.__tokenRules
    @TokenRules.setter
    def TokenRules(self, tokenRules):
        """
        token rules that create patterns for groups   required
        :param tokenRules:
        :return:
        """
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
            dataviewGroupRule.Type = content['Type']
            

        if 'TokenRules' in content:
            dataviewGroupRule.TokenRules = content['TokenRules']


        return dataviewGroupRule

