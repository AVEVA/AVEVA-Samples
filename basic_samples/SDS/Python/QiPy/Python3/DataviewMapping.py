# DataviewMapping.py
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
from DataviewMappingColumn import DataviewMappingColumn

class DataviewMapping(object):
    """Sds dataview definition"""
    @property
    def IsDefault(self):
        return self.__isDefault
    @IsDefault.setter
    def IsDefault(self, isDefault):
        self.__isDefault = isDefault
    
    @property
    def Columns(self):
        return self.__columns
    @Columns.setter
    def Columns(self, columns ):
        self.__columns = columns    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'IsDefault' : self.IsDefault}
	
        if hasattr(self, 'Columns'):
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

