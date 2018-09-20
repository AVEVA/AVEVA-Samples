import json
import SdsView

class SdsViewProperty(object):
    """Sds View Property definition"""
    @property
    def SourceId(self):
        return self.__sourceId
    @SourceId.setter
    def SourceId(self, id):
        self.__sourceId = id
    
    @property
    def TargetId(self):
        return self.__targetId
    @TargetId.setter
    def TargetId(self, name):
        self.__targetId = name
    
    @property
    def SdsView(self):
        return self.__sdsView
    @SdsView.setter
    def SdsView(self, description):
        self.__sdsView = description
        
    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceId' : self.SourceId, 'TargetId' : self.TargetId }

        if hasattr(self, 'SdsView'):
            dictionary['SdsView'] = self.SdsView.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsViewProperty.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        viewProperty = SdsViewProperty()

        if len(content) == 0:
            return viewProperty

        if 'SourceId' in content:
            viewProperty.SourceId = content['SourceId']

        if 'TargetId' in content:
            viewProperty.TargetId = content['TargetId']
		
        if 'SdsView' in content:
            viewProperty.SdsView = SdsView.fromDictionary(content['SdsView'])

        return viewProperty

