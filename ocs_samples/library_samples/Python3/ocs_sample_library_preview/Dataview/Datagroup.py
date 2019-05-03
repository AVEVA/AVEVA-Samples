# Datagroup.py
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

class Datagroup(object):
    """
    Datagroup definition
    """

    @property
    def Tokens(self):
        return self.__tokens
    @Tokens.setter
    def Tokens(self, tokens):
        self.__tokens = tokens
    
    @property
    def DataItems(self):
        return self.__dataItems
    @DataItems.setter
    def DataItems(self, dataItems):
        self.__dataItems = dataItems    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'DataItems' : self.DataItems, 'Tokens' : self.Tokens}
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return Datagroup.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataGroup = Datagroup()

        if len(content) == 0:
            return dataGroup

        if 'DataItems' in content:
            dataGroup.DataItems = content['DataItems']
			
        if 'Tokens' in content:
            dataGroup.Tokens = content['Tokens']

        return dataGroup

