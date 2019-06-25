# DataviewIndexConfig.py
#

import json


class DataviewIndexConfig(object):
    """
    DataviewIndexConfig
    """

    @property
    def StartIndex(self):
        """
        start index in ISO 8601 format   required
        :return:
        """
        return self.__startIndex

    @StartIndex.setter
    def StartIndex(self, startIndex):
        """
        start index in ISO 8601 format   required
        :param startIndex:
        :return:
        """
        self.__startIndex = startIndex

    @property
    def EndIndex(self):
        """
        end index in  ISO 8601 format   required
        :return:
        """
        return self.__endIndex

    @EndIndex.setter
    def EndIndex(self, endIndex):
        """
        end index in  ISO 8601 format   required
        :param endIndex:
        :return:
        """
        self.__endIndex = endIndex

    @property
    def Mode(self):
        """
        data retrieval mode, for example: Interpolated  required
        :return:
        """
        return self.__mode

    @Mode.setter
    def Mode(self, mode):
        """
        data retrieval mode, for example: Interpolated  required
        :param mode:
        :return:
        """
        self.__mode = mode

    @property
    def Interval(self):
        """
        data retrieval interval   required
        :return:
        """
        return self.__interval

    @Interval.setter
    def Interval(self, interval):
        """
        data retrieval interval   required
        :param interval:
        :return:
        """
        self.__interval = interval

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {}
        if hasattr(self, 'IsDefault'):
            dictionary = {'IsDefault': self.IsDefault}

        if hasattr(self, 'StartIndex'):
            dictionary['StartIndex'] = self.StartIndex

        if hasattr(self, 'EndIndex'):
            dictionary['EndIndex'] = self.EndIndex

        if hasattr(self, 'Mode'):
            dictionary['Mode'] = self.Mode

        if hasattr(self, 'Interval'):
            dictionary['Interval'] = self.Interval

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return DataviewIndexConfig.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewIndexConfig = DataviewIndexConfig()

        if len(content) == 0:
            return dataviewIndexConfig

        if 'IsDefault' in content:
            dataviewIndexConfig.IsDefault = content['IsDefault']

        if 'StartIndex' in content:
            dataviewIndexConfig.StartIndex = content['StartIndex']

        if 'EndIndex' in content:
            dataviewIndexConfig.EndIndex = content['EndIndex']

        if 'Mode' in content:
            dataviewIndexConfig.Mode = content['Mode']

        if 'Interval' in content:
            dataviewIndexConfig.Interval = content['Interval']

        return dataviewIndexConfig
