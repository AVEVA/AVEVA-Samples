# DataviewIndexConfig.py
#

import json
from dateutil import parser


class DataviewIndexConfig(object):
    """
    DataviewIndexConfig
    """

    def __init__(self, startIndex=None, endIndex=None, mode=None, interval=None):
        self.__startIndex = startIndex
        self.__endIndex = endIndex
        self.__mode = mode
        self.__interval = interval

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

    def toJson(self, withSeconds=False): 
        return json.dumps(self.toDictionary(withSeconds))

    def toDictionary(self, withSeconds=False):
        # required properties
        dictionary = {}
        if hasattr(self, 'IsDefault'):
            dictionary = {'IsDefault': self.IsDefault}

        if hasattr(self, 'StartIndex'):
            dictionary['StartIndex'] = self.__toTimeSecondsFormat(self.StartIndex, withSeconds)

        if hasattr(self, 'EndIndex'):
            dictionary['EndIndex'] = self.__toTimeSecondsFormat(self.EndIndex, withSeconds)

        if hasattr(self, 'Mode'):
            dictionary['Mode'] = self.Mode

        if hasattr(self, 'Interval'):
            dictionary['Interval'] = self.Interval

        return dictionary

    def __toTimeSecondsFormat(self, t, withSeconds=False):
        if not withSeconds:
            return t
        else:
            return (parser.parse(t)).isoformat(timespec='seconds') + "Z"
    
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
