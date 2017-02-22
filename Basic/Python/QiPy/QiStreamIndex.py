class QiStreamIndex(object):
    """Qi Stream Index definitions"""

    @property
    def QiTypePropertyId(self):
        return self.__qiTypePropertyId
    @QiTypePropertyId.setter
    def QiTypePropertyId(self, qiTypePropertyId):
        self.__qiTypePropertyId = qiTypePropertyId

    def toString(self):
        return json.dumps(self.toDictionary())
    
    def toDictionary(self):
        # required properties
        dictionary = { 'QiTypePropertyId' : self.QiTypePropertyId }

        return dictionary
 
    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiType.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):
        typePropertyId = QiStreamIndex()

        if len(content) == 0:
            return typePropertyId

        if 'QiTypePropertyId' in content:
            typePropertyId.QiTypePropertyId = content['QiTypePropertyId']

        return typePropertyId
