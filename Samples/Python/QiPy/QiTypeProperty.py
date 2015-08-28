import QiType

class QiTypeProperty(object):
    """Qi type property definition"""

    def __init__(self):
            self.__Id = ""
            self.__Name = None
            self.__Description = None
            self.__QiType = None
            self.__IsKey = False
            
    def getId(self):
        return self.__Id

    def setId(self, Id):
        self.__Id = Id

    Id = property(getId, setId)

    def getIsKey(self):
        return self.__IsKey

    def setIsKey(self, iskey):
        self.__IsKey = iskey

    IsKey = property(getIsKey, setIsKey)

    def getName(self):
        return self.__Name

    def setName(self, Name):
        self.__Name = Name

    Name = property(getName, setName)

    
    def getDescription(self):
        return self.__Description

    def setDescription(self, Description):
        self.__Description = Description

    Description = property(getDescription, setDescription)

    
    def getQiType(self):
        return self.__QiType

    def setQiType(self, QiType):
        self.__QiType = QiType

    QiType = property(getQiType, setQiType)

    
    def toDictionary(self):
        dictionary = {
            "Id" : self.__Id }

        dictionary["IsKey"] = self.__IsKey

        if self.__Name is not None and len(self.__Name) > 0:
            dictionary["Name"] = self.__Name

        if self.__Description is not None and len(self.__Description) > 0:
            dictionary["Description"] = self.__Description

        if self.__QiType is not None:
            dictionary["QiType"] = self.__QiType.toDictionary()

        return dictionary

    @staticmethod
    def fromDictionary(content):
        
        typeProperty = QiTypeProperty()

        if len(content) == 0:
            return typeProperty

        if "Id" in content:
            typeProperty.Id = content["Id"]
            
        if "IsKey" in content:
            typeProperty.IsKey = content["IsKey"]

        if "Name" in content:
            typeProperty.Name = content["Name"]

        if "Description" in content:
            typeProperty.Description = content["Description"]

        if "QiType" in content:
            typeProperty.QiType = QiType.QiType.fromDictionary(content["QiType"])
            
        return typeProperty