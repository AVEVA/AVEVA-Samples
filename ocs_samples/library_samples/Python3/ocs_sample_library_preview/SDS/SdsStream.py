# SdsStream.py
#

import json
from .SdsStreamIndex import SdsStreamIndex
from .SdsStreamPropertyOverride import SdsStreamPropertyOverride


class SdsStream(object):
    """Sds stream definition"""

    def __init__(self, id=None, name=None, description=None, typeId=None,
                 propertyOverrides=None, indexes=None, interpolationMode=None,
                 extrapolationMode=None):
        """

        :param id: required
        :param name: not required
        :param description: not required
        :param typeId: required
        :param propertyOverrides:  array of  SdsStreamPropertyOverride
                                   not required
        :param indexes: array of SdsStreamIndex   not required
        :param interpolationMode: SdsInterpolationMode   default is null
                                   not required
        :param extrapolationMode: SdsExtrapolationMode default is null
                                  not required
        """
        self.Id = id
        self.Name = name
        self.Description = description
        self.TypeId = typeId
        self.PropertyOverrides = propertyOverrides
        self.Indexes = indexes
        self.InterpolationMode = interpolationMode
        self.ExtrapolationMode = extrapolationMode

    @property
    def Id(self):
        """
        required
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """"
        required
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Name(self):
        """
        not required
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        not required
        :param name:
        :return:
        """
        self.__name = name

    @property
    def Description(self):
        """
        not required
        :return:
        """
        return self.__description

    @Description.setter
    def Description(self, description):
        """
        not required
        :param description:
        :return:
        """
        self.__description = description

    @property
    def TypeId(self):
        """
        required
        :return:
        """
        return self.__typeId

    @TypeId.setter
    def TypeId(self, typeId):
        """
        required
        :param typeId:
        :return:
        """
        self.__typeId = typeId

    @property
    def PropertyOverrides(self):
        """
        array of  SdsStreamPropertyOverride    not required
        :return:
        """
        return self.__propertyOverrides

    @PropertyOverrides.setter
    def PropertyOverrides(self, propertyOverrides):
        """
        array of  SdsStreamPropertyOverride    not required
        :param propertyOverrides:
        :return:
        """
        self.__propertyOverrides = propertyOverrides

    @property
    def Indexes(self):
        """
        array of SdsStreamIndex   not required
        :return:
        """
        return self.__indexes

    @Indexes.setter
    def Indexes(self, indexes):
        """
        array of SdsStreamIndex   not required
        :param indexes:
        :return:
        """
        self.__indexes = indexes

    @property
    def InterpolationMode(self):
        """
        SdsInterpolationMode   default is null   not required
        :return:
        """
        return self.__interpolationMode

    @InterpolationMode.setter
    def InterpolationMode(self, interpolationMode):
        """
        SdsInterpolationMode    default is null   not required
        :param interpolationMode:
        :return:
        """
        self.__interpolationMode = interpolationMode

    @property
    def ExtrapolationMode(self):
        """
        SdsExtrapolationMode default is null   not required
        :return:
        """
        return self.__extrapolationMode

    @ExtrapolationMode.setter
    def ExtrapolationMode(self, extrapolationMode):
        """
        SdsExtrapolationMode default is null   not required
        :param extrapolationMode:
        :return:
        """
        self.__extrapolationMode = extrapolationMode

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'Id': self.Id, 'TypeId': self.TypeId}

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'InterpolationMode'):
            dictionary['InterpolationMode'] = self.InterpolationMode

        if hasattr(self, 'ExtrapolationMode'):
            dictionary['ExtrapolationMode'] = self.ExtrapolationMode

        if hasattr(self, 'PropertyOverrides'):
            if self.PropertyOverrides is not None:
                dictionary['PropertyOverrides'] = []
                for value in self.PropertyOverrides:
                    dictionary['PropertyOverrides'].append(
                        value.toDictionary())

        if hasattr(self, 'Indexes'):
            if self.Indexes is not None:
                dictionary['Indexes'] = []
                for value in self.Indexes:
                    dictionary['Indexes'].append(value.toDictionary())

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStream.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        stream = SdsStream()

        if len(content) == 0:
            return stream

        if 'Id' in content:
            stream.Id = content['Id']

        if 'Name' in content:
            stream.Name = content['Name']

        if 'Description' in content:
            stream.Description = content['Description']

        if 'InterpolationMode' in content:
            stream.InterpolationMode = content['InterpolationMode']

        if 'ExtrapolationMode' in content:
            stream.ExtrapolationMode = content['ExtrapolationMode']

        if 'TypeId' in content:
            stream.TypeId = content['TypeId']

        if 'PropertyOverrides' in content:
            propertyOverrides = content['PropertyOverrides']
            if propertyOverrides is not None and len(propertyOverrides) > 0:
                stream.PropertyOverrides = []
                for value in propertyOverrides:
                    stream.PropertyOverrides.append(
                        SdsStreamPropertyOverride.fromDictionary(value))

        if 'Indexes' in content:
            indexes = content['Indexes']
            if indexes is not None and len(indexes) > 0:
                stream.Indexes = []
                for value in indexes:
                    stream.Indexes.append(SdsStreamIndex.fromDictionary(value))

        return stream
