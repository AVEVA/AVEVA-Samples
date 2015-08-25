from enum import Enum
import json

class QiType(object):
    """Qi type definitions"""

    def __init__(self):
        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = QiTypeCode.Object
        self.__Properties = []

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

    
    def getQiTypeCode(self):
        return self.__QiTypeCode

    def setQiTypeCode(self, QiTypeCode):
        self.__QiTypeCode = QiTypeCode

    QiTypeCode = property(getQiTypeCode, setQiTypeCode)


    def getProperties(self):
        return self.__Properties

    def setProperties(self, Properties):
        self.__Properties = Properties

    Properties = property(getProperties, setProperties)

    def toString(self):
        return json.dumps(self.toDictionary())
    
    def toDictionary(self):
        dictionary = {
            "Id" : self.__Id,
            "QiTypeCode" : self.__QiTypeCode }

        if self.__Name is not None and len(self.__Name) > 0:
            dictionary["Name"] = self.__Name

        if self.__Description is not None and len(self.__Description) > 0:
            dictionary["Description"] = self.__Description

        if self.__Properties is not None and len(self.__Properties) > 0:
            dictionary["Properties"] = []
        
        for value in self.__Properties:
            dictionary['Properties'].append(value.toDictionary())

        return dictionary
 
    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiType.fromDictionary(dictionary);

    @staticmethod
    def fromDictionary(content):
        
        type = QiType()

        if len(content) == 0:
            return type;

        if "Id" in content:
            type.Id = content["Id"]

        if "Name" in content:
            type.Name = content["Name"]

        if "Description" in content:
            type.Description = content["Description"]

        if "QiTypeCode" in content:
            type.QiTypeCode = QiTypeCode(str(content["QiTypeCode"]))
       
        if "Properties" in content:
            type.Properties = []
            properties = content["Properties"];

            if properties is not None and len(properties) > 0:
                for value in properties:
                    type.Properties.append(QiTypeProperty.fromDictionary(value))

        return type;

