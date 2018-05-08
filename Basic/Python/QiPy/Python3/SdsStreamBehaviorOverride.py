from enum import Enum
import json
from SdsStreamMode import SdsStreamMode

class SdsStreamBehaviorOverride(object):
    """Sds behavior override definition"""

    def __init__(self):
        self.__mode = SdsStreamMode.Default
    
    @property
    def Mode(self):
        return self.__mode
    @Mode.setter
    def Mode(self, mode):
        self.__mode = mode

    @property
    def SdsTypePropertyId(self):
        return self.__sdsTypePropertyId
    @SdsTypePropertyId.setter
    def SdsTypePropertyId(self, sdsTypePropertyId):
        self.__sdsTypePropertyId = sdsTypePropertyId

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = { 'Mode' : self.Mode }
        
        if hasattr(self, 'SdsTypePropertyId'):
            dictionary['SdsTypePropertyId'] = self.SdsTypePropertyId

        return json.loads(dictionary)

    @staticmethod
    def fromDictionary(content):
        streamBehaviorOverride = SdsStreamBehaviorOverride()

        if len(content) == 0:
            return streamBehaviorOverride

        if 'Mode' in content:
            streamBehaviorOverride.Mode = content['Mode']

        if 'SdsTypePropertyId' in content:
            stream.SdsTypePropertyId = content['SdsTypePropertyId']
            
        return stream