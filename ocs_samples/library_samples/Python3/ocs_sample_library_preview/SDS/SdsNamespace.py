# SdsNamespace.py
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

class SdsNamespace(object):
    """
    definition of SdsNamespace
    """

    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id

    def toString(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id }

        return dictionary

    @staticmethod
    def fromString(content):
         dictionary = json.loads(content)
         return SdsNamespace.fromDictionary(dictionary)

    @staticmethod
    def fromDictionary(content):
        namespace = SdsNamespace()

        if len(content) == 0:
            return namespace

        if "Id" in content:
            namespace.Id = content["Id"]
            
        return namespace
