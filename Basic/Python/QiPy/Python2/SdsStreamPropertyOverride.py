<# SdsStreamPropertyOverride.py

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
#>

import json

class SdsStreamPropertyOverride(object):
    """Sds Stream PropertyOverride definitions"""

    @property
    def SdsTypePropertyId(self):
        return self.__sdsTypePropertyId
    @SdsTypePropertyId.setter
    def SdsTypePropertyId(self, sdsTypePropertyId):
        self.__sdsTypePropertyId = sdsTypePropertyId

    @property
    def InterpolationMode(self):
        return self.__interpolationMode
    @InterpolationMode.setter
    def InterpolationMode(self, interpolationMode):
        self.__interpolationMode = interpolationMode

    @property
    def Uom(self):
        return self.__uom
    @Uom.setter
    def Uom(self, uom):
        self.__uom = uom

    def toJson(self):
        return json.dumps(self.toDictionary())
    
    def toDictionary(self):
        # required properties
        dictionary = { 'SdsTypePropertyId' : self.SdsTypePropertyId }

        # optional properties
        if hasattr(self, 'Uom'):
            dictionary['Uom'] = self.Uom

        if hasattr(self, 'InterpolationMode'):
            dictionary['InterpolationMode'] = self.InterpolationMode

        return dictionary

    @staticmethod
    def fromDictionary(content):
        propertyOverride = SdsStreamPropertyOverride()

        if len(content) == 0:
            return propertyOverride

        if 'SdsTypePropertyId' in content:
            propertyOverride.SdsTypePropertyId = content['SdsTypePropertyId']

        if 'Uom' in content:
            propertyOverride.Uom = content['Uom']

        if 'InterpolationMode' in content:
            propertyOverride.InterpolationMode = content['InterpolationMode']

        return propertyOverride
