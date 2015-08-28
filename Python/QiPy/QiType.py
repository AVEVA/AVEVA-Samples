from enum import Enum
import json
from QiTypeCode import QiTypeCode
from QiTypeProperty import QiTypeProperty

class QiType(object):
    """Qi type definitions"""

    __qiTypeCodeMap = {
        QiTypeCode.Empty : 0,
        QiTypeCode.Object : 1,
        QiTypeCode.DBNull : 2,
        QiTypeCode.Boolean : 3,
        QiTypeCode.Char : 4,
        QiTypeCode.SByte : 5,
        QiTypeCode.Byte : 6,
        QiTypeCode.Int16 : 7,
        QiTypeCode.UInt16 : 8,
        QiTypeCode.Int32 : 9,
        QiTypeCode.UInt32 : 10,
        QiTypeCode.Int64 : 11,
        QiTypeCode.UInt64 : 12,
        QiTypeCode.Single : 13,
        QiTypeCode.Double : 14,
        QiTypeCode.Decimal : 15,
        QiTypeCode.DateTime : 16,
        QiTypeCode.String : 18,
        QiTypeCode.Guid : 19,
        QiTypeCode.DateTimeOffset : 20,
        QiTypeCode.TimeSpan : 21,
        QiTypeCode.Version : 22    
        }


    def __init__(self):
        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
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
        for key, val in self.__qiTypeCodeMap.iteritems():
            if self.__QiTypeCode == val:
                return key        

    def setQiTypeCode(self, QiTypeCode):
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode]

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
         return QiType.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):
        
        type = QiType()

        if len(content) == 0:
            return type

        if "Id" in content:
            type.Id = content["Id"]

        if "Name" in content:
            type.Name = content["Name"]

        if "Description" in content:
            type.Description = content["Description"]

        if "QiTypeCode" in content:            
            type.__QiTypeCode = content["QiTypeCode"]            
       
        if "Properties" in content:
            type.Properties = []
            properties = content["Properties"]

            if properties is not None and len(properties) > 0:
                for value in properties:
                    type.Properties.append(QiTypeProperty.fromDictionary(value))

        return type

        
    #qiTypeCodeMap = {
    #    "Empty" : 0,
    #    "Object" : 1,
    #    "DBNull" : 2,
    #    "Boolean" : 3,
    #    "Char" : 4,
    #    "SByte" : 5,
    #    "Byte" : 6,
    #    "Int16" : 7,
    #    "UInt16" : 8,
    #    "Int32" : 9,
    #    "UInt32" : 10,
    #    "Int64" : 11,
    #    "UInt64" : 12,
    #    "Single" : 13,
    #    "Double" : 14,
    #    "Decimal" : 15,
    #    "DateTime" : 16,
    #    "String" : 18,
    #    "Guid" : 19,
    #    "DateTimeOffset" : 20,
    #    "TimeSpan" : 21,
    #    "Version" : 22    
    #    }