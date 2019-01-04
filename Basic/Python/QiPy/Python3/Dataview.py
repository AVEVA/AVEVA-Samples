# Dataview.py
#
# Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
#
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

import json
from DataviewQuery import DataviewQuery
from DataviewMapping import DataviewMapping
from DataviewIndexConfig import DataviewIndexConfig
from DataviewGroupRule import DataviewGroupRule

class Dataview(object):
    """Sds dataview definition"""
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, name):
        self.__name = name
    
    @property
    def Description(self):
        return self.__description
    @Description.setter
    def Description(self, description):
        self.__description = description
        		
    @property
    def Queries(self):
        return self.__queries
    @Queries.setter
    def Queries(self, queries):
        self.__queries = queries

    @property
    def Mappings(self):
        return self.__mappings 
    @Mappings.setter
    def Mappings(self, mappings):
        self.__mappings = mappings

    @property
    def IndexConfig(self):
        return self.__indexConfig
    @IndexConfig.setter
    def IndexConfig(self, indexConfig):
        self.__indexConfig = indexConfig

    @property
    def IndexDataType(self):
        return self.__indexDataType
    @IndexDataType.setter
    def IndexDataType(self, indexDataType):
        self.__indexDataType = indexDataType

    @property
    def GroupRules(self):
        return self.__groupRules
    @GroupRules.setter
    def GroupRules(self, groupRules):
        self.__groupRules = groupRules


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id}
	
        dictionary['Queries'] = []
        for value in self.Queries:
            dictionary['Queries'].append(value.toDictionary())			

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'Mappings'):
            dictionary['Mappings'] = self.Mappings.toDictionary()

        if hasattr(self, 'IndexConfig'):
            dictionary['IndexConfig'] = self.IndexConfig.toDictionary()

        if hasattr(self, 'IndexDataType'):
            dictionary['IndexDataType'] = self.IndexDataType


        if hasattr(self, 'GroupRules'):
            dictionary['GroupRules'] = []
            for value in self.GroupRules:
                dictionary['GroupRules'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return Dataview.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataview = Dataview()

        if len(content) == 0:
            return dataview

        if 'Id' in content:
            dataview.Id = content['Id']

        if 'Name' in content:
            dataview.Name = content['Name']

        if 'Description' in content:
            dataview.Description = content['Description']

        
        if 'Queries' in content:
            queries = content['Queries']
            if queries is not None and len(queries) > 0:
                dataview.Queries = []
                for value in queries:
                    dataview.Queries.append(DataviewQuery.fromDictionary(value))

        if 'Mappings' in content:
            dataview.Mappings = DataviewMapping.fromDictionary(content['Mappings'])

        if 'IndexConfig' in content:
            dataview.IndexConfig = DataviewIndexConfig.fromDictionary(content['IndexConfig'])

        if 'IndexDataType' in content:
            dataview.IndexDataType = content['IndexDataType']
            
        
        if 'GroupRules' in content:
            groupRules = content['GroupRules']
            if groupRules is not None and len(groupRules) > 0:
                dataview.GroupRules = []
                for value in groupRules:
                    dataview.GroupRules.append(DataviewGroupRule.fromDictionary(value))


        return dataview

