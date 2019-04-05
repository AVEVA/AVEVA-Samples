# SdsStreamViewProperty.py
#
# Copyright 2019 OSIsoft, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json 

class SdsStreamViewProperty(object):
    """Sds StreamView Property definition"""
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
    def SdsStreamView(self):
        return self.__sdsStreamView
    @SdsStreamView.setter
    def SdsStreamView(self, description):
        self.__sdsStreamView = description
        
    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'SourceId' : self.SourceId, 'TargetId' : self.TargetId }

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
		
        if 'SdsStreamView' in content:
            
            from .SdsStreamView import SdsStreamView 
            streamViewProperty.SdsStreamView = SdsStreamView.fromDictionary(content['SdsStreamView'])

        return streamViewProperty

