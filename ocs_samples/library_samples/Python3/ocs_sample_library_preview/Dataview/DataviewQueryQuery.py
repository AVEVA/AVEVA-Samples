# DataviewQueryQuery.py
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

class DataviewQueryQuery(object):


    def __init__(self, resource = None, field = None, value= None, function = None):
        self.__resource = resource
        self.__field= field
        self.__value = value
        self.__function = function

    """Sds dataview definition"""
    @property
    def Resource(self):
        """
        query resource can be something like "Streams", "TypeProperties"   required
        :return:
        """
        return self.__resource
    @Resource.setter
    def Resource(self, resource):
        """
        query resource   required
        :param resource:
        :return:
        """
        self.__resource = resource

    @property
    def Field(self):
        """
        query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"   required

        :return:
        """
        return self.__field
    @Field.setter
    def Field(self, field):
        """
        query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"   required
        :param field:
        :return:
        """
        self.__field = field
    
    @property
    def Value(self):
        """
        value for field to use in query   required
        :return:
        """
        return self.__value
    @Value.setter
    def Value(self, value):
        """
        value for field to use in query   required
        :param value:
        :return:
        """
        self.__value = value
    
    @property
    def Function(self):
        """
        QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"    required
        :return:
        """
        return self.__function
    @Function.setter
    def Function(self, function):
        """
        QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"    required
        :param function:
        :return:
        """
        self.__function= function
    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Resource' : self.Resource,'Field' : self.Field, 'Value' : self.Value, 'Function' : self.Function}
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewQueryQuery.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewQueryQuery = DataviewQueryQuery()

        if len(content) == 0:
            return dataviewQueryQuery

        if 'Resource' in content:
            dataviewQueryQuery.Resource = content['Resource']

        if 'Field' in content:
            dataviewQueryQuery.Field = content['Field']

        if 'Value' in content:
            dataviewQueryQuery.Value = content['Value']

        if 'Function' in content:
            dataviewQueryQuery.Function = content['Function']
        

        return dataviewQueryQuery

