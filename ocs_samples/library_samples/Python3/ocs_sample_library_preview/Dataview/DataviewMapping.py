# DataviewMapping.py
#

import json
from .DataviewMappingColumn import DataviewMappingColumn


class DataviewMapping(object):

    def __init__(self, columns=None):

        self.__columns = columns

    @property
    def Columns(self):
        """
        array of DataviewMappingColumn   required
        :return:
        """
        return self.__columns

    @Columns.setter
    def Columns(self, columns):
        """
        array of DataviewMappingColumn   required
        :param columns:
        :return:
        """
        self.__columns = columns

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}

        if hasattr(self, 'Columns') and self.Columns is not None:
            dictionary['Columns'] = []
            for value in self.Columns:
                dictionary['Columns'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewMapping.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewMapping = DataviewMapping()

        if len(content) == 0:
            return dataviewMapping

        if 'Columns' in content:
            columns = content['Columns']
            if columns is not None and len(columns) > 0:
                dataviewMapping.Columns = []
                for value in columns:
                    dataviewMapping.Columns.append(
                        DataviewMappingColumn.fromDictionary(value))

        return dataviewMapping
