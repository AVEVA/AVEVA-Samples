# performance_counters.py
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

import psutil


class PerformanceCounters:
    def __init__(self):
        self.type_dict = {
            "processor": psutil.cpu_times(),
            "memory": psutil.virtual_memory()
        }

    def get_counters(self, type_id):
        return self.type_dict[type_id.lower()]

    def get_counter_names(self, type_id):
        return self.type_dict.get(type_id.lower())._fields
