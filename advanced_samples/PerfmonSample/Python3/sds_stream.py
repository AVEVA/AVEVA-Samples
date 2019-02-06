# sds_stream.py
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
from sds_stream_index import SdsStreamIndex


class SdsStream(object):
    """Sds stream definition"""
    def __init__(self, stream_id, name, type_id, description):
        self.Id = stream_id
        self.name = name
        self.__type_id = type_id
        self.__description = description

    @property
    def Id(self):
        return self.__id

    @Id.setter
    def Id(self, id):
        self.__id = id

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, name):
        self.__name = name

    @property
    def Description(self):
        return self.__description

    @Description.setter
    def Description(self, description):
        self.__description = description

    @property
    def TypeId(self):
        return self.__type_id

    @TypeId.setter
    def TypeId(self, typeId):
        self.__type_id = typeId

    @property
    def Indexes(self):
        return self.__indexes

    @Indexes.setter
    def Indexes(self, indexes):
        self.__indexes = indexes

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'Id': self.Id, 'TypeId': self.TypeId}

        # optional properties
        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description
			
        if hasattr(self, 'Indexes'):
            dictionary['Indexes'] = []
            for value in self.Indexes:
                dictionary['Indexes'].append(value.to_dictionary())

        return dictionary

    @staticmethod
    def from_json(json_obj):
        return SdsStream.from_dictionary(json_obj)

    @staticmethod
    def from_dictionary(content):
        stream = SdsStream()

        if len(content) == 0:
            return stream

        if 'Id' in content:
            stream.Id = content['Id']

        if 'Name' in content:
            stream.Name = content['Name']

        if 'Description' in content:
            stream.Description = content['Description']

        if 'TypeId' in content:
            stream.TypeId = content['TypeId']
			
        if 'Indexes' in content:
            indexes = content['Indexes']
            if indexes is not None and len(indexes) > 0:
                stream.Indexes = []
                for value in indexes:
                    stream.Indexes.append(SdsStreamIndex.from_dictionary(value))

        return stream
