import json

class QiNamespace(object):
    """description of class"""

    def __init__(self):
        self.__Id = 0
    
    def getId(self):
        return self.__Id

    def setId(self, id):
        self.__Id = id

    Id = property(getId, setId)

    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        
        dictionary = { "Id" : self.__Id }

        return dictionary

    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return QiNamespace.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):
        namespace = QiNamespace()

        if len(content) == 0:
            return typeProperty

        if "Id" in content:
            namespace.Id = content["Id"]
            
        return namespace