# sds_stream_index.py
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


class SdsStreamIndex(object):
    """Sds Stream Index definitions"""

    @property
    def sds_type_property_id(self):
        return self.__sds_type_property_id

    @sds_type_property_id.setter
    def sds_type_property_id(self, sds_type_property_id):
        self.__sds_type_property_id = sds_type_property_id

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'sds_type_property_id': self.sds_type_property_id}

        return json.loads(dictionary)

    @staticmethod
    def from_dictionary(content):
        type_property_id = SdsStreamIndex()

        if len(content) == 0:
            return type_property_id

        if 'sds_type_property_id' in content:
            type_property_id.sds_type_property_id = content['sds_type_property_id']

        return type_property_id
