from enum import Enum
import json
from QiStreamMode import QiStreamMode
from QiStreamExtrapolation import QiStreamExtrapolation
from QiStreamBehaviorOverride import QiStreamBehaviorOverride

class QiStreamBehavior(object):
    """Qi behavior definition"""

    def __init__(self):
        self.__mode = QiStreamMode.Default
        self.__extrapolationMode = QiStreamExtrapolation.All
    
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, name):
        self.__name = name

    @property
    def Mode(self):
        return self.__mode
    @Mode.setter
    def Mode(self, mode):
        self.__mode = mode

    @property
    def ExtrapolationMode(self):
        return self.__extrapolationMode
    @ExtrapolationMode.setter
    def ExtrapolationMode(self, extrapolationMode):
        self.__extrapolationMode = extrapolationMode
    
    @property
    def Overrides(self):
        return self.__overrides
    @Overrides.setter
    def Overrides(self, overrides):
        self.__overrides = overrides

    def toJsonString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id, 'Mode' : self.Mode.value, 'ExtrapolationMode' : self.ExtrapolationMode.value }

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Overrides'):
            dictionary['Overrides'] = []
            for value in self.Overrides:
                dictionary['Overrides'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return QiStreamBehavior.fromDictionary(jsonObj)
    
    @staticmethod
    def fromDictionary(content):

        behavior = QiStreamBehavior()

        if len(content) == 0:
            return None

        if 'Id' in content:
            behavior.Id = content['Id']

        if 'Name' in content:
            behavior.Name = content['Name']

        if 'Mode' in content:
            behavior.Mode = QiStreamMode(content['Mode'])

        if 'ExtrapolationMode' in content:
            behavior.ExtrapolationMode = QiStreamExtrapolation(content['ExtrapolationMode'])
        
        if 'BehaviorId' in content:
            overrides = content['Overrides']
            if overrides is not None and len(overrides) > 0:
                behavior.Overrides = []
                for value in overrides:
                    behavior.Overrides.append(QiStreamBehaviorOverride.fromDictionary(value))
            
        return behavior