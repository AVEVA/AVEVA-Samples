# SdsStreamPropertyOverride.py
#

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
        dictionary = {'SdsTypePropertyId': self.SdsTypePropertyId}

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
