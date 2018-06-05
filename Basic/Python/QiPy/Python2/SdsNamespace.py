import json

class SdsNamespace(object):
    """description of class"""

    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id

    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id }

        return dictionary

    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return SdsNamespace.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):
        namespace = SdsNamespace()

        if len(content) == 0:
            return namespace

        if "Id" in content:
            namespace.Id = content["Id"]
            
        return namespace