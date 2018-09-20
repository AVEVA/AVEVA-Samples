from JsonEncoder import Encoder
import json
import inspect
from SdsViewProperty import SdsViewProperty

class SdsView(object):
    """Sds view definitions"""
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
    def Description(self):
        return self.__description
    @Description.setter
    def Description(self, description):
        self.__description = description

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
        dictionary = { 'Id' : self.Id, 'SourceTypeId' : self.SourceTypeId, 'TargetTypeId' : self.TargetTypeId }

        # optional properties
        if hasattr(self, 'Properties'):
            dictionary['Properties'] = []
            for value in self.Properties:
                dictionary['Properties'].append(value.toDictionary())

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsView.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        view = SdsView()

        if len(content) == 0:
            return view

        if 'Id' in content:
            view.Id = content['Id']

        if 'Name' in content:
            view.Name = content['Name']

        if 'Description' in content:
            view.Description = content['Description']

        if 'TargetTypeId' in content:
            view.TargetTypeId = content['TargetTypeId']

        if 'SourceTypeId' in content:
            view.SourceTypeId = content['SourceTypeId']
       
        if 'Properties' in content:
            properties = content['Properties']
            if properties is not None and len(properties) > 0:
                view.Properties = []
                for value in properties:
                    view.Properties.append(SdsViewProperty.fromDictionary(value))

        return view