from JsonEncoder import Encoder
import json
import inspect
from SdsViewProperty import SdsViewProperty

class SdsViewMap(object):
    """SdsViewMap definitions"""

    @property
    def SourceTypeId(self):
        return self.__sourceTypeId
    @SourceTypeId.setter
    def SourceTypeId(self, baseType):
        self.__sourceTypeId = baseType
    
    @property
    def TargetTypeId(self):
        return self.__targetTypeId
    @TargetTypeId.setter
    def TargetTypeId(self, typeCode):
        self.__targetTypeId = typeCode

    @property
    def Properties(self):
        return self.__properties
    @Properties.setter
    def Properties(self, properties):
        self.__properties = properties

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsViewMap.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        viewMap = SdsViewMap()

        if len(content) == 0:
            return viewMap

        if 'TargetTypeId' in content:
            viewMap.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            viewMap.SourceTypeId = content['SourceTypeId']
       
        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                viewMap.Properties = []
                for value in properties:
                    viewMap.Properties.append(SdsViewProperty.fromDictionary(value))

        return viewMap