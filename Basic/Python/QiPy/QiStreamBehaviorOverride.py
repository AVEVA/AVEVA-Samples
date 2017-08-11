from enum import Enum
import json
from QiStreamMode import QiStreamMode

class QiStreamBehaviorOverride(object):
    """Qi behavior override definition"""

    def __init__(self):
        self.__mode = QiStreamMode.Default
    
    @property
    def Mode(self):
        return self.__mode
    @Mode.setter
    def Mode(self, mode):
        self.__mode = mode

    @property
    def QiTypePropertyId(self):
        return self.__qiTypePropertyId
    @QiTypePropertyId.setter
    def QiTypePropertyId(self, qiTypePropertyId):
        self.__qiTypePropertyId = qiTypePropertyId

    def toJsonString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = { 'Mode' : self.Mode }
        
        if hasattr(self, 'QiTypePropertyId'):
            dictionary['QiTypePropertyId'] = self.QiTypePropertyId

        return json.loads(dictionary)

    @staticmethod
    def fromDictionary(content):
        streamBehaviorOverride = QiStreamBehaviorOverride()

        if len(content) == 0:
            return streamBehaviorOverride

        if 'Mode' in content:
            streamBehaviorOverride.Mode = content['Mode']

        if 'QiTypePropertyId' in content:
            stream.QiTypePropertyId = content['QiTypePropertyId']
            
        return stream