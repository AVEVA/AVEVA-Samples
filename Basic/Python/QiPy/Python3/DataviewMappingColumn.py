# DataviewMappingColumn.py
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

