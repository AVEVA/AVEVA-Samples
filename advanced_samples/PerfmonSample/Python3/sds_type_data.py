# sds_type_data.py
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

import datetime
import json
from performance_counters import PerformanceCounters as PC


class SdsTypeData:
    def __init__(self, type_id=None, time=None):
        self.type_id = type_id
        self.time = time

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        if self.time:
            time = self.time
        else:
            time = datetime.datetime.utcnow()
        dictionary = {'Time': str(time), 'Typeid': self.type_id}
        for k, v in self.__dict__.items():
            if k != "time" and k != "typeId":
                dictionary[k] = v
        self.__properties = dictionary
        return dictionary

    def from_json(self, json_obj):
        return self.from_dictionary(json_obj)

    def from_dictionary(self, content):
        if self is None:
            return SdsTypeData()
        data_obj = SdsTypeData(self.type_id)
        prop_names = PC().get_counter_names(self.type_id)

        data_obj.__setattr__('time', content['Time'])
        for prop in prop_names:
            # Pre-Assign the default
            data_obj.__setattr__(prop, 0)

            if prop in content:
                value = content[prop]
                if value is not None:
                    data_obj.__setattr__(prop, value)
        return data_obj
