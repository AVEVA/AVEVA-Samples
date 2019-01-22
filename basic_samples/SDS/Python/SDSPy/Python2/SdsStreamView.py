# SdsStreamView.py
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

class SdsStreamView(object):
    """Sds streamView definitions"""
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
        dictionary = { 'Id' : self.Id, 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStreamView.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        streamView = SdsStreamView()

        if len(content) == 0:
            return streamView

        if 'Id' in content:
            streamView.Id = content['Id']

        if 'Name' in content:
            streamView.Name = content['Name']

        if 'Description' in content:
            streamView.Description = content['Description']

        if 'TargetTypeId' in content:
            streamView.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            streamView.SourceTypeId = content['SourceTypeId']
       
        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                streamView.Properties = []
                for value in properties:
                    streamView.Properties.append(SdsStreamViewProperty.fromDictionary(value))

        return streamView
