# DataviewMapping.py
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
from .DataviewMappingColumn import DataviewMappingColumn

class DataviewMapping(object):

    

    def __init__(self, isDefault = None, columns = None):
        
        self.__columns = columns

        if isDefault:
            self.__isDefault = isDefault
        else:
            if columns:
                self.__isDefault = False
            else:
                self.__isDefault = True



    """Sds dataview definition"""
    @property
    def IsDefault(self):
        """
        boolean  	Determines whether default parameters should be used   not required
        :return:
        """
        return self.__isDefault
    @IsDefault.setter
    def IsDefault(self, isDefault):
        """
        boolean  	Determines whether default parameters should be used   not required
        :param isDefault:
        :return:
        """
        self.__isDefault = isDefault
    
    @property
    def Columns(self):
        """
        array of DataviewMappingColumn   required  unless IsDefault is true
        :return:
        """
        return self.__columns
    @Columns.setter
    def Columns(self, columns ):
        """
        array of DataviewMappingColumn   required  unless IsDefault is true
        :param columns:
        :return:
        """
        self.__columns = columns    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'IsDefault' : self.IsDefault}
	
        if hasattr(self, 'Columns') and self.Columns is not None:
            dictionary['Columns'] = []
            for value in self.Columns:
                dictionary['Columns'].append(value.toDictionary())			

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewMapping.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewMapping = DataviewMapping()

        if len(content) == 0:
            return dataviewMapping

        if 'IsDefault' in content:
            dataviewMapping.IsDefault = content['IsDefault']
        
        if 'Columns' in content:
            columns = content['Columns']
            if columns is not None and len(columns) > 0:
                dataviewMapping.Columns = []
                for value in columns:
                    dataviewMapping.Columns.append(DataviewMappingColumn.fromDictionary(value))
                    
        return dataviewMapping

