# DataviewGroupRule.py
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

class DataviewGroupRule(object):
    
    def __init__(self, id = None, type_= None, tokenRules = None):
        self.__id = id
        self.__type= type_
        self.__tokenRules = tokenRules


    """Sds dataview definition"""
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Type(self):
        return self.__type
    @Type.setter
    def Type(self, type_):
        self.__type = type_    

    
    @property
    def TokenRules(self):
        return self.__tokenRules
    @TokenRules.setter
    def TokenRules(self, tokenRules):
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
            dataviewGroupRule.Id = content['Type']
            

        if 'TokenRules' in content:
            dataviewGroupRule.Id = content['TokenRules']


        return dataviewGroupRule

