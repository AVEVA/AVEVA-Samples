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
    """ dataview query definition """
    @property
    def Type(self):
        return self.__type
    @Type.setter
    def Type(self, type):
        self.__type = type
    
    @property
    def Value(self):
        return self.__value
    @Value.setter
    def Value(self, value):
        self.__value = value
    
    @property
    def Operator(self):
        return self.__operator
    @Operator.setter
    def Operator(self, operator):
        self.__operator= operator
    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Type' : self.Type, 'Value' : self.Value, 'Operator' : self.Operator}
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewQueryQuery.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewQueryQuery = DataviewQueryQuery()

        if len(content) == 0:
            return dataviewQueryQuery

        if 'Type' in content:
            dataviewQueryQuery.Type = content['Type']

        if 'Value' in content:
            dataviewQueryQuery.Value = content['Value']

        if 'Operator' in content:
            dataviewQueryQuery.Operator = content['Operator']
        

        return dataviewQueryQuery

