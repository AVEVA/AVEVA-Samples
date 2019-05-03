# SdsStreamPropertyOverride.py
#
# Copyright 2019 OSIsoft, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

class SdsStreamPropertyOverride(object):
    """
    Sds Stream PropertyOverride definitions
    """

    @property
    def SdsTypePropertyId(self):
        """
        id   required
        :return:
        """
        return self.__sdsTypePropertyId
    @SdsTypePropertyId.setter
    def SdsTypePropertyId(self, sdsTypePropertyId):
        """
        id   required
        :param sdsTypePropertyId:
        :return:
        """
        self.__sdsTypePropertyId = sdsTypePropertyId

    @property
    def InterpolationMode(self):
        """
        SdsInterpolationMode   not required
        :return:
        """
        return self.__interpolationMode
    @InterpolationMode.setter
    def InterpolationMode(self, interpolationMode):
        """
        SdsInterpolationMode   not required
        :param interpolationMode:
        :return:
        """
        self.__interpolationMode = interpolationMode

    @property
    def Uom(self):
        """
        Unit of Measure    not required
        :return:
        """
        return self.__uom
    @Uom.setter
    def Uom(self, uom):
        """
        Unit of Measure    not required
        :param uom:
        :return:
        """
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
