import json

class QiStream(object):
    """Qi stream definition"""

    def __init__(self):
        self.__Id = 0
        self.__Name = None
        self.__Description = None
        self.__TypeId = None
    
    def getId(self):
        return self.__Id

    def setId(self, Id):
        self.__Id = Id

    Id = property(getId, setId)


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


    def getTypeId(self):
        return self.__TypeId

    def setTypeId(self, TypeId):
        self.__TypeId = TypeId

    TypeId = property(getTypeId, setTypeId)

    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        
        dictionary = {
            "Id" : self.__Id }

        if self.__Name is not None and len(self.__Name) > 0:
            dictionary["Name"] = self.__Name

        if self.__Description is not None and len(self.__Description) > 0:
            dictionary["Description"] = self.__Description

        if self.__TypeId is not None:
            dictionary["TypeId"] = self.TypeId

        return dictionary

    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiStream.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):

        stream = QiStream()

        if len(content) == 0:
            return typeProperty

        if "Id" in content:
            stream.Id = content["Id"]

        if "Name" in content:
            stream.Name = content["Name"]

        if "Description" in content:
            stream.Description = content["Description"]

        if "TypeId" in content:
            stream.TypeId = content["TypeId"]
            
        return stream

