# DataviewQuery.py
#

import json


class DataviewQuery(object):
    """
    Dataview Query
    """

    def __init__(self, id=None, query=None):
        """

        :param id:  required
        :param query: a query string
        """
        self.__id = id
        if query:
            self.__query = query
        else:
            self.__query = ""

    @property
    def Id(self):
        """
        id   required
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """
        id   required
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Query(self):
        """
        Query string  required
        :return:
        """
        return self.__query

    @Query.setter
    def Query(self, query):
        """
        Query string  required
        :param query:
        :return:
        """
        self.__query = query

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Id': self.Id, 'Query': self.Query}

        return [dictionary]
    
    @staticmethod
    def fromJson(jsonObj):
        return DataviewQuery.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        if isinstance(content, list):
            content = content[0]
            
        dataviewQuery = DataviewQuery()

        if len(content) == 0:
            return dataviewQuery

        if 'Id' in content:
            dataviewQuery.Id = content['Id']

        if 'Query' in content:
            dataviewQuery.Query = content['Query']

        return dataviewQuery
