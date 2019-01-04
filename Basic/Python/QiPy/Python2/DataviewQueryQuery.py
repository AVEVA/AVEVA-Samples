# DataviewQueryQuery.py
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

