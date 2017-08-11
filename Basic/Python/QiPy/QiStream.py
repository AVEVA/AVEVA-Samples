import json
from QiStreamIndex import QiStreamIndex

class QiStream(object):
    """Qi stream definition"""
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
    def TypeId(self):
        return self.__typeId
    @TypeId.setter
    def TypeId(self, typeId):
        self.__typeId = typeId

    @property
    def BehaviorId(self):
        return self.__behaviorId
    @BehaviorId.setter
    def BehaviorId(self, behaviorId):
        self.__behaviorId = behaviorId

    @property
    def Indexes(self):
        return self.__indexes 
    @Indexes.setter
    def Indexes(self, indexes):
        self.__indexes = indexes 

    def toJsonString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id, 'TypeId' : self.TypeId }

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description
            
        if hasattr(self, 'BehaviorId'):
            dictionary['BehaviorId'] = self.BehaviorId

        if hasattr(self, 'Indexes'):
            dictionary['Indexes'] = []
            for value in self.Indexes:
                dictionary['Indexes'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return QiStream.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        stream = QiStream()

        if len(content) == 0:
            return stream

        if 'Id' in content:
            stream.Id = content['Id']

        if 'Name' in content:
            stream.Name = content['Name']

        if 'Description' in content:
            stream.Description = content['Description']

        if 'TypeId' in content:
            stream.TypeId = content['TypeId']
        
        if 'BehaviorId' in content:
            stream.BehaviorId = content['BehaviorId']
            
        if 'Indexes' in content:
            indexes = content['Indexes']
            if indexes is not None and len(indexes) > 0:
                stream.Indexes = []
                for value in indexes:
                    stream.Indexes.append(QiStreamIndex.fromDictionary(value))

        return stream

