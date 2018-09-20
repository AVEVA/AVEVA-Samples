class SdsStreamIndex(object):
    """Sds Stream Index definitions"""

    @property
    def SdsTypePropertyId(self):
        return self.__sdsTypePropertyId
    @SdsTypePropertyId.setter
    def SdsTypePropertyId(self, sdsTypePropertyId):
        self.__sdsTypePropertyId = sdsTypePropertyId

    def toJson(self):
        return json.dumps(self.toDictionary())
    
    def toDictionary(self):
        # required properties
        dictionary = { 'SdsTypePropertyId' : self.SdsTypePropertyId }

        return json.loads(dictionary)

    @staticmethod
    def fromDictionary(content):
        typePropertyId = SdsStreamIndex()

        if len(content) == 0:
            return typePropertyId

        if 'SdsTypePropertyId' in content:
            typePropertyId.SdsTypePropertyId = content['SdsTypePropertyId']

        return typePropertyId
