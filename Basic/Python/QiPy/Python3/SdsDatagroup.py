# SdsDatagroup.py
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

class SdsDatagroup(object):
    """Sds Datagroup definition"""
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
        return SdsDatagroup.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataGroup = SdsDatagroup()

        if len(content) == 0:
            return dataGroup

        if 'DataItems' in content:
            dataGroup.DataItems = content['DataItems']
			
        if 'Tokens' in content:
            dataGroup.Tokens = content['Tokens']

        return dataGroup

