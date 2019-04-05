# DataviewQuery.py
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
from .DataviewQueryQuery import DataviewQueryQuery

class DataviewQuery(object):    

    def __init__(self, id = None,  resource = None, field = None, value= None, operator = None,  query = None):
        self.__id = id
        if query:
            self.__query = query
        else:
            self.__query = DataviewQueryQuery(resource, field, value, operator)      

    """Sds dataview definition"""
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Query(self):
        return self.__query
    @Query.setter
    def Query(self, query):
        self.__query = query    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id}
        dictionary['Query'] = self.Query.toDictionary()
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewQuery.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewQuery = DataviewQuery()

        if len(content) == 0:
            return dataviewQuery

        if 'Id' in content:
            dataviewQuery.Id = content['Id']
			
        if 'Query' in content:
            dataviewQuery.Query = DataviewQueryQuery.fromDictionary(content['Query'])


        return dataviewQuery

