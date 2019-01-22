# SdsStreamViewMap.py
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

from JsonEncoder import Encoder
import json
import inspect
from SdsStreamViewProperty import SdsStreamViewProperty

class SdsStreamViewMap(object):
    """SdsStreamViewMap definitions"""

    @property
    def SourceTypeId(self):
        return self.__sourceTypeId
    @SourceTypeId.setter
    def SourceTypeId(self, baseType):
        self.__sourceTypeId = baseType
    
    @property
    def TargetTypeId(self):
        return self.__targetTypeId
    @TargetTypeId.setter
    def TargetTypeId(self, typeCode):
        self.__targetTypeId = typeCode

    @property
    def Properties(self):
        return self.__properties
    @Properties.setter
    def Properties(self, properties):
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStreamViewMap.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        streamViewMap = SdsStreamViewMap()

        if len(content) == 0:
            return streamViewMap

        if 'TargetTypeId' in content:
            streamViewMap.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            streamViewMap.SourceTypeId = content['SourceTypeId']
       
        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                streamViewMap.Properties = []
                for value in properties:
                    streamViewMap.Properties.append(SdsStreamViewProperty.fromDictionary(value))

        return streamViewMap
