# JsonEncoder.py
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

from json import JSONEncoder
import inspect
import collections

def isprop(v):
  return isinstance(v, property)

class Encoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj, collections.Iterable):
            # Contend with objects that can be iterated over
            objJson = []
            for o in obj:
                objJson.append(default(o))
            return objJson
        else:
            objJson = {}
            properties = inspect.getmembers(type(obj), isprop)
            if len(properties) > 0:
                for property in properties:
                    value = property[1].fget(obj)
                    if value is not None:
                        objJson[property[0]] = value
            else:
                # If we fail to find properties, we simply serialize the attributes
                objAttribs = obj.__dict__
                for attrib in objAttribs:
                    if objAttribs[attrib] is not None:
                        objJson[attrib] = objAttribs[attrib]
            return objJson
