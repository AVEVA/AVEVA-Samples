from QiStreamMode import QiStreamMode
import json

class QiStreamBehavior(object):
    
    def __init__(self):
        self.__Id = None
        self.__Name = None
        self.__Mode = QiStreamMode.Continuous
        self.__ExtrapolationMode = None
        self.__Overrides = []
        
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
    
    def getMode(self):
        return self.__Mode
    
    def setMode(self, Mode):
        self.__Mode = Mode
    
    Mode = property(getMode, setMode)
    
    def getExtrapolationMode(self):
        return self.__ExtrapolationMode
    
    def setExtrapolationMode(self, ExtrapolationMode):
        self.__ExtrapolationMode = ExtrapolationMode
    
    ExtrapolationMode = property(getExtrapolationMode, setExtrapolationMode)
    
    def getOverrides(self):
        return self.__Overrides
    
    def setOverrides(self, Overrides):
        self.__Overrides = Overrides
    
    Overrides = property(getOverrides, setOverrides)
    
    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        
        dictionary = {
            "Id" : self.__Id }

        if self.__Name is not None and len(self.__Name) > 0:
            dictionary["Name"] = self.__Name

        if self.__Mode is not None:
            dictionary["Mode"] = self.__Mode

        if self.__ExtrapolationMode is not None:
            dictionary["ExtrapolationMode"] = self.__ExtrapolationMode
        
        if self.__Overrides is not None:
            dictionary["Overrides"] = self.__Overrides

        return dictionary
        
    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiStreamBehavior.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):

        behavior = QiStreamBehavior()

        if len(content) == 0:
            return None

        if "Id" in content:
            behavior.Id = content["Id"]

        if "Name" in content:
            behavior.Name = content["Name"]

        if "Mode" in content:
            #behavior.Mode = QiStreamMode(content["Mode"])
            behavior.Mode = content["Mode"]

        if "TypeId" in content:
            behavior.ExtrapolationMode = content["ExtrapolationMode"]
        
        if "BehaviorId" in content:
            behavior.Overrides = content["Overrides"]
            
        return behavior