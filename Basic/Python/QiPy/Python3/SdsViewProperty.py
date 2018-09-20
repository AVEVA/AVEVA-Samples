''' SdsViewProperty.py

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
'''

import json
import SdsView

class SdsViewProperty(object):
    """Sds View Property definition"""
    @property
    def SourceId(self):
        return self.__sourceId
    @SourceId.setter
    def SourceId(self, id):
        self.__sourceId = id
    
    @property
    def TargetId(self):
        return self.__targetId
    @TargetId.setter
    def TargetId(self, name):
        self.__targetId = name
    
    @property
    def SdsView(self):
        return self.__sdsView
    @SdsView.setter
    def SdsView(self, description):
        self.__sdsView = description
        
    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceId' : self.SourceId, 'TargetId' : self.TargetId }

        if hasattr(self, 'SdsView'):
            dictionary['SdsView'] = self.SdsView.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsViewProperty.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        viewProperty = SdsViewProperty()

        if len(content) == 0:
            return viewProperty

        if 'SourceId' in content:
            viewProperty.SourceId = content['SourceId']

        if 'TargetId' in content:
            viewProperty.TargetId = content['TargetId']
		
        if 'SdsView' in content:
            viewProperty.SdsView = SdsView.fromDictionary(content['SdsView'])

        return viewProperty

