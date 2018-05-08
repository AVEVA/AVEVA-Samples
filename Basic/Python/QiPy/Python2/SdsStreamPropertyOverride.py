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
    def InterpolationModeOverride(self):
        return self.__interpolationModeOverride
    @InterpolationModeOverride.setter
    def InterpolationModeOverride(self, interpolationModeOverride):
        self.__interpolationModeOverride = interpolationModeOverride

    @property
    def UomOverride(self):
        return self.__uomOverride
    @UomOverride.setter
    def UomOverride(self, uomOverride):
        self.__uomOverride = uomOverride

    def toJson(self):
        return json.dumps(self.toDictionary())
    
    def toDictionary(self):
        # required properties
        dictionary = { 'SdsTypePropertyId' : self.SdsTypePropertyId }

        # optional properties
        if hasattr(self, 'UomOverride'):
            dictionary['UomOverride'] = self.UomOverride

        if hasattr(self, 'InterpolationModeOverride'):
            dictionary['InterpolationModeOverride'] = self.InterpolationModeOverride

        return dictionary

    @staticmethod
    def fromDictionary(content):
        propertyOverride = SdsStreamPropertyOverride()

        if len(content) == 0:
            return propertyOverride

        if 'SdsTypePropertyId' in content:
            propertyOverride.SdsTypePropertyId = content['SdsTypePropertyId']

        if 'UomOverride' in content:
            propertyOverride.UomOverride = content['UomOverride']

        if 'InterpolationModeOverride' in content:
            propertyOverride.InterpolationModeOverride = content['InterpolationModeOverride']

        return propertyOverride