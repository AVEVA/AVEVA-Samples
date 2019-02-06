# helper_functions.py
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

def cleanup_single(client, namespace_id, type_id):
    print("Deleting stream, '{}'".format(type_id))
    supress_error(lambda: client.delete_stream(namespace_id, type_id))
    print("Deleting type, '{}'".format(type_id))
    supress_error(lambda: client.delete_type(namespace_id, type_id))


def cleanup(client, namespace_id, types_names):
    print("Cleaning up...")
    for i, type_id in enumerate(types_names):
        cleanup_single(client, namespace_id, type_id)


def to_string(event):
    string = ""
    for k, v in event.__dict__.items():
        if k != 'type_id':
            if k == 'time':
                string = "{}: {}".format(v, string)
            elif v is None:
                string += "{}: , ".format(k)
            else:
                string += "{}: {}, ".format(k, v)
    return string[:-2]


def supress_error(sds_call):
    try:
        sds_call()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))
