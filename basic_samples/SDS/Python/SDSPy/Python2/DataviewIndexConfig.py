# DataviewIndexConfig.py
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

class DataviewIndexConfig(object):
    """ dataview index config definition"""
    @property
    def IsDefault(self):
        return self.__isDefault
    @IsDefault.setter
    def IsDefault(self, isDefault):
        self.__isDefault = isDefault
    
    @property
    def StartIndex(self):
        return self.__startIndex
    @StartIndex.setter
    def StartIndex(self, startIndex ):
        self.__startIndex = startIndex    
    
    @property
    def EndIndex(self):
        return self.__endIndex
    @EndIndex.setter
    def EndIndex(self, endIndex ):
        self.__endIndex = endIndex    
		
    @property
    def Mode(self):
        return self.__mode
    @Mode.setter
    def Mode(self, mode ):
        self.__mode = mode 
		
    @property
    def Interval(self):
        return self.__interval
    @Interval.setter
    def Interval(self, interval ):
        self.__interval = interval 


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'IsDefault' : self.IsDefault}
	
        if hasattr(self, 'StartIndex'):
            dictionary['StartIndex'] = self.StartIndex

        if hasattr(self, 'EndIndex'):
            dictionary['EndIndex'] = self.EndIndex

        if hasattr(self, 'Mode'):
            dictionary['Mode'] = self.Mode

        if hasattr(self, 'Interval'):
            dictionary['Interval'] = self.Interval			

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewIndexConfig.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewIndexConfig = DataviewIndexConfig()

        if len(content) == 0:
            return dataviewIndexConfig

        if 'IsDefault' in content:
            dataviewIndexConfig.IsDefault = content['IsDefault']

        if 'StartIndex' in content:
            dataviewIndexConfig.StartIndex = content['StartIndex']

        if 'EndIndex' in content:
            dataviewIndexConfig.EndIndex = content['EndIndex']

        if 'Mode' in content:
            dataviewIndexConfig.Mode = content['Mode']

        if 'Interval' in content:
            dataviewIndexConfig.Interval = content['Interval']
        
            

        return dataviewIndexConfig

