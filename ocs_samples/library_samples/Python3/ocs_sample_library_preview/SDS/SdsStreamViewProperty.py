# SdsStreamViewProperty.py
#

import json.decoder


class SdsStreamViewProperty(object):
    """Sds StreamView Property definition"""
    @property
    def SourceId(self):
        """
        required
        :return:
        """
        return self.__sourceId

    @SourceId.setter
    def SourceId(self, id):
        """
        required
        :param id:
        :return:
        """
        self.__sourceId = id

    @property
    def TargetId(self):
        """
        required
        :return:
        """
        return self.__targetId

    @TargetId.setter
    def TargetId(self, name):
        """
        required
        :param name:
        :return:
        """
        self.__targetId = name

    @property
    def SdsStreamView(self):
        """
        SdsStreamView   not required
        :return:
        """
        return self.__sdsStreamView

    @SdsStreamView.setter
    def SdsStreamView(self, description):
        """
        SdsStreamView   not required
        :param description:
        :return:
        """
        self.__sdsStreamView = description

    @property
    def Mode(self):
        return self.__mode

    @Mode.setter
    def Mode(self, mode):
        self.__mode = mode

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = {'SourceId': self.SourceId}

        if hasattr(self, 'TargetId'):
            dictionary['TargetId'] = self.TargetId

        if hasattr(self, 'Mode'):
            dictionary['Mode'] = self.Mode

        if hasattr(self, 'SdsStreamView'):
            from .SdsStreamView import SdsStreamView
            dictionary['SdsStreamView'] = self.SdsStreamView.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsStreamViewProperty.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        streamViewProperty = SdsStreamViewProperty()

        if len(content) == 0:
            return streamViewProperty

        if 'SourceId' in content:
            streamViewProperty.SourceId = content['SourceId']

        if 'TargetId' in content:
            streamViewProperty.TargetId = content['TargetId']

        if 'Mode' in content:
            streamViewProperty.Mode = content['Mode']

        if 'SdsStreamView' in content:
            from .SdsStreamView import SdsStreamView
            streamViewProperty.SdsStreamView = SdsStreamView.fromDictionary(
                content['SdsStreamView'])

        return streamViewProperty
