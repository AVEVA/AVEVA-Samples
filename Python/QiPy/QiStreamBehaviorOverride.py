import json

class QiStreamBehaviorOverride(object):
    """description of class"""
    def __init__(self):
        self.__QiTypePropertyId = 0
        self.__Mode = Continuous
    
    def getTypePropertyId(self):
        return self.__QiTypePropertyId

    def setTypePropertyId(self, Id):
        self.__QiTypePropertyId = Id

    QiTypePropertyId = property(getTypePropertyId, setTypePropertyId)

    def getMode(self):
        return self.__Mode

    def setMode(self, Mode):
        self.__Mode = Mode

    Mode = property(getMode, setMode)

    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        
        dictionary = {
            "QiTypePropertyId" : self.__QiTypePropertyId }

        if self.__Mode is not None:
            dictionary["Mode"] = self.__Mode

        return dictionary

    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiStreamBehaviorOverride.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):

        streambehavioroverride = QiStreamBehaviorOverride()

        if len(content) == 0:
            return None

        if "Mode" in content:
            streambehavioroverride.Mode = content["Mode"]

        if "QiTypePropertyId" in content:
            stream.QiTypePropertyId = content["QiTypePropertyId"]
            
        return stream