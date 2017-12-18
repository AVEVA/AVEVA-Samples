import json
import QiView

class QiViewProperty(object):
    """Qi View Property definition"""
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
    def QiView(self):
        return self.__qiView
    @QiView.setter
    def QiView(self, description):
        self.__qiView = description
        
    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceId' : self.SourceId, 'TargetId' : self.TargetId }

        if hasattr(self, 'QiView'):
            dictionary['QiView'] = self.QiView.toDictionary()

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return QiViewProperty.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        viewProperty = QiViewProperty()

        if len(content) == 0:
            return viewProperty

        if 'SourceId' in content:
            viewProperty.SourceId = content['SourceId']

        if 'TargetId' in content:
            viewProperty.TargetId = content['TargetId']
		
        if 'QiView' in content:
            viewProperty.QiView = QiView.fromDictionary(content['QiView'])

        return viewProperty

