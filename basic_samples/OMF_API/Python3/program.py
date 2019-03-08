# program.py
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

# NOTE: this script was designed using the v1.0
# version of the OMF specification, as outlined here:
# http://omf-docs.osisoft.com/en/v1.0
# For more info, see OMF Developer Companion Guide:
# http://omf-companion-docs.osisoft.com
#*************************************************************************************

# ************************************************************************
# Import necessary packages
# ************************************************************************

import configparser
import json
import time
import datetime
import platform
import socket
import gzip
import random 
import requests
import traceback


# ************************************************************************
# Specify options for sending web requests to the target PI System
# ************************************************************************

# Specify whether to compress OMF message before
# sending it to ingress endpoint
USE_COMPRESSION = True

# If self-signed certificates are used (true by default),
# do not verify HTTPS SSL certificates; normally, leave this as is
VERIFY_SSL = False

# Specify the timeout, in seconds, for sending web requests
# (if it takes longer than this to send a message, an error will be thrown)
WEB_REQUEST_TIMEOUT_SECONDS = 30

# Holder for the producer token.  It is set from the configuration
# For more information see PI Connector Administration Guide
producerToken = ""

# Holder for the omfEndPoint.  It is set from the configuration
# For more information see PI Connector Administration Guide
omfEndPoint = ""

integer_boolean_value = 0
string_boolean_value = "True"

integer_index1 = 0
integer_index2_1 = 1
integer_index2_2 = 1

# ************************************************************************
# Helper function: REQUIRED: wrapper function for sending an HTTPS message
# ************************************************************************

# Define a helper function to allow easily sending web request messages;
# this function can later be customized to allow you to port this script to other languages.
# All it does is take in a data object and a message type, and it sends an HTTPS
# request to the target OMF endpoint
def send_omf_message_to_endpoint(message_type, message_omf_json):
    global producerToken, omfEndPoint
    # Compress json omf payload, if specified
    compression = 'none'
    if USE_COMPRESSION:
        msg_body = gzip.compress(bytes(json.dumps(message_omf_json), 'utf-8'))
        compression = 'gzip'
    else:
        msg_body = json.dumps(message_omf_json)
    # Assemble headers
    msg_headers = {
        'producertoken': producerToken,
        'messagetype': message_type,
        'action': 'create',
        'messageformat': 'JSON',
        'omfversion': '1.0',
        'compression': compression
    }
    # Send the request, and collect the response
    response = requests.post(
        omfEndPoint,
        headers = msg_headers,
        data = msg_body,
        verify = VERIFY_SSL,
        timeout = WEB_REQUEST_TIMEOUT_SECONDS
    )
    
    # response code in 200s if the request was successful!
    if response.status_code < 200 or response.status_code >= 300:
        response.close()
        raise Exception("OMF message was unsuccessful, {message_type}. {status}:{reason}".
                        format(message_type=message_type, status=response.status_code, reason=response.text))
    else:
        print('Response from relay from the initial "{0}" message: {1} {2}'.format(message_type, response.status_code, response.text))
    

def getCurrentTime():
    return datetime.datetime.utcnow().isoformat() + 'Z'


# Creates a JSON packet containing data values for containers
# of type FirstDynamicType defined below
def create_data_values_for_first_dynamic_type(containerid):
    return [
        {
            "containerid": containerid,
            "values": [
                {
                    "timestamp": getCurrentTime(),
                    "IntegerProperty": int(100*random.random())
                }
            ]
        }
    ]

# Creates a JSON packet containing data values for containers
# of type SecondDynamicType defined below
def create_data_values_for_second_dynamic_type(containerid):
    global string_boolean_value
    if string_boolean_value == "True":
        string_boolean_value = "False"
    else:
        string_boolean_value = "True"

    return [
        {
            "containerid": containerid,
            "values": [
                {
                    "timestamp": getCurrentTime(),
                    "NumberProperty1": 100*random.random(),
                    "NumberProperty2": 100*random.random(),
                    "StringEnum": string_boolean_value
                }
            ]
        }
    ]


# of type ThirdDynamicType defined below
def create_data_values_for_third_dynamic_type(containerid):
    global integer_boolean_value
    if integer_boolean_value == 0:
        integer_boolean_value = 1
    else:
        integer_boolean_value = 0
    return [
        {
            "containerid": containerid,
            "values": [
                {
                    "timestamp": getCurrentTime(),
                    "IntegerEnum": integer_boolean_value
                }
            ]
        }
    ]

# Creates a JSON packet containing data values for containers
# of type NonTimeStampIndex defined below
def create_data_values_for_NonTimeStampIndexAndMultiIndex_type(NonTimeStampIndexID, MultiIndexId):
    global integer_index1
    global integer_index2_1, integer_index2_2

    integer_index1 = integer_index1 + 2
    

    if integer_index2_2 % 3 == 0:
        integer_index2_2 = 1
        integer_index2_1 = integer_index2_1 +1
    else:
        integer_index2_2 = integer_index2_2 + 1

    return [
        {
            "containerid": NonTimeStampIndexID,
            "values": [
                {
                    "Value": random.random()*88,
                    "Int_Key": integer_index1
                },
                {
                    "Value": random.random()*88,
                    "Int_Key": integer_index1 + 1
                }
            ]
        },
        {
            "containerid": MultiIndexId,
            "values": [
                {
                    "Value1": random.random()*-125,
                    "Value2": random.random()*42,
                    "IntKey": integer_index2_1,
                    "IntKey2": integer_index2_2
                }
            ]
        }
    ]
    
# Creates a JSON packet containing data values for containers
# of type MultiIndex defined below
def create_data_values_for_MultiIndex_type(containerid):

    return [
        
    ]


def oneTimeSendMessages():
    # ************************************************************************
    # Send the types messages to define the types of streams that will be sent.
    # These types are referenced in all later messages
    # ************************************************************************

    # The sample divides types, and sends static and dynamic types
    # separatly only for readability; you can send all the type definitions
    # in one message, as far as its size is below maximum allowed - 192K
    # ************************************************************************

    # Send a JSON packet to define static types
    
    # Note for OCS this message is currently ignored. 
    send_omf_message_to_endpoint("type", [
        {
            "id": "FirstStaticType",
            "name": "First static type",
            "classification": "static",
            "type": "object",
            "description": "First static asset type",
            "properties": {
                "index": {
                    "type": "string",
                    "isindex": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "name": {
                    "type": "string",
                    "isname": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "StringProperty": {
                    "type": "string",
                    "name": "First configuration attribute",
                    "description": "First static asset type's configuration attribute"
                }
            }
        },
        {
            "id": "SecondStaticType",
            "name": "Second static type",
            "classification": "static",
            "type": "object",
            "description": "Second static asset type",
            "properties": {
                "index": {
                    "type": "string",
                    "isindex": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "name": {
                    "type": "string",
                    "isname": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "StringProperty": {
                    "type": "string",
                    "name": "Second configuration attribute",
                    "description": "Second static asset type's configuration attribute"
                }
            }
        }
    ])

    # Send a JSON packet to define dynamic types
    send_omf_message_to_endpoint("type", [
        {
            "id": "FirstDynamicType",
            "name": "First dynamic type",
            "classification": "dynamic",
            "type": "object",
            "description": "not in use",
            "properties": {
                "timestamp": {
                    "format": "date-time",
                    "type": "string",
                    "isindex": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "IntegerProperty": {
                    "type": "integer",
                    "name": "Integer attribute",
                    "description": "PI point data referenced integer attribute"
                }
            }
        },
        {
            "id": "SecondDynamicType",
            "name": "Second dynamic type",
            "classification": "dynamic",
            "type": "object",
            "description": "not in use",
            "properties": {
                "timestamp": {
                    "format": "date-time",
                    "type": "string",
                    "isindex": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "NumberProperty1": {
                    "type": "number",
                    "name": "Number attribute 1",
                    "description": "PI point data referenced number attribute 1",
                    "format": "float64"
                },
                "NumberProperty2": {
                    "type": "number",
                    "name": "Number attribute 2",
                    "description": "PI point data referenced number attribute 2",
                    "format": "float64"
                },
                "StringEnum": {
                    "type": "string",
                    "enum": ["False", "True"],
                    "name": "String enumeration",
                    "description": "String enumeration to replace boolean type"
                }
            }
        },
        {
            "id": "ThirdDynamicType",
            "name": "Third dynamic type",
            "classification": "dynamic",
            "type": "object",
            "description": "not in use",
            "properties": {
                "timestamp": {
                    "format": "date-time",
                    "type": "string",
                    "isindex": True,
                    "name": "not in use",
                    "description": "not in use"
                },
                "IntegerEnum": {
                    "type": "integer",
                    "format": "int16",
                    "enum": [0, 1],
                    "name": "Integer enumeration",
                    "description": "Integer enumeration to replace boolean type"
                }
            }
        }
    ])

    # Note for PI these messages are ignored. 
    # Send a JSON packet to define dynamic types
    send_omf_message_to_endpoint("type", [
        {
            "id": "NonTimeStampIndex",
            "name": "NonTimeStampIndex",
            "classification": "dynamic",
            "type": "object",
            "description": "Integer Fun",
            "properties": {
                "Value": {
                    "type": "number",
                    "name": "Value",
                    "description": "This could be any value"
                },
                "Int_Key": {
                    "type": "integer",
                    "name": "Integer Key",
                    "isindex": True,
                    "description": "A non-time stamp key"
                }
            }
        },        
        {
            "id": "MultiIndex",
            "name": "Multi_index",
            "classification": "dynamic",
            "type": "object",
            "description": "This one has multiple indicies",
            "properties": {
                "Value": {
                    "type": "number",
                    "name": "Value1",
                    "description": "This could be any value"
                },                
                "Value2": {
                    "type": "number",
                    "name": "Value2",
                    "description": "This could be any value too"
                },
                "IntKey": {
                    "type": "integer key part 1",
                    "name": "integer key part 1",
                    "isindex": True,
                    "description": "This could represent any integer value"
                },
                "IntKey2": {
                    "type": "integer key part 2",
                    "name": "integer key part 2",
                    "isindex": True,
                    "description": "This could represent any integer value as well"
                }
            }
        }
    ])


    # ************************************************************************
    # Send a JSON packet to define containerids and the type
    # (using the types listed above) for each new data events container.
    # This instantiates these particular containers.
    # We can now directly start sending data to it using its Id.
    # ************************************************************************
    send_omf_message_to_endpoint("container", [
        {
            "id": "Container1",
            "typeid": "FirstDynamicType"
        },
        {
            "id": "Container2",
            "typeid": "FirstDynamicType"
        },
        {
            "id": "Container3",
            "typeid": "SecondDynamicType"
        },
        {
            "id": "Container4",
            "typeid": "ThirdDynamicType"
        }
    ])

    
    # Note for PI these messages are ignored. 
    send_omf_message_to_endpoint("container", [
        {
            "id": "Container5",
            "typeid": "NonTimeStampIndex"
        },
        {
            "id": "Container6",
            "typeid": "MultiIndex"
        }
    ])


    # ************************************************************************
    # Send the messages to create the PI AF asset structure
    #
    # The following packets can be sent in one data message; the example
    # splits the data into several messages only for readability;
    # you can send all of the following data in one message,
    # as far as its size is below maximum allowed - 192K
    # ************************************************************************

    # Note for OCS these messages are ignored. 

    # Send a JSON packet to define assets
    send_omf_message_to_endpoint("data", [
        {
            "typeid": "FirstStaticType",
            "values": [
                {
                    "index": "Asset1",
                    "name": "Parent element",
                    "StringProperty": "Parent element attribute value"
                }
            ]
        },
        {
            "typeid": "SecondStaticType",
            "values": [
                {
                    "index": "Asset2",
                    "name": "Child element",
                    "StringProperty": "Child element attribute value"
                }
            ]
        }
    ])

    # Send a JSON packet to define links between assets
    # to create AF Asset structure
    send_omf_message_to_endpoint("data", [
        {
            "typeid": "__Link",
            "values": [
                {
                    "source": {
                            "typeid": "FirstStaticType",
                            "index": "_ROOT"
                    },
                    "target": {
                            "typeid": "FirstStaticType",
                            "index": "Asset1"
                    }
                },
                {
                    "source": {
                            "typeid": "FirstStaticType",
                            "index": "Asset1"
                    },
                    "target": {
                            "typeid": "SecondStaticType",
                            "index": "Asset2"
                    }
                }
            ]
        }
    ])

    # Send a JSON packet to define links between assets and
    # containerids to create attributes with PI point references
    # from containerid properties
    send_omf_message_to_endpoint("data", [
        {
            "typeid": "__Link",
            "values": [
                {
                    "source": {
                            "typeid": "FirstStaticType",
                            "index": "Asset1"
                    },
                    "target": {
                            "containerid": "Container1"
                    }
                },
                {
                    "source": {
                            "typeid": "SecondStaticType",
                            "index": "Asset2"
                    },
                    "target": {
                            "containerid": "Container2"
                    }
                },
                {
                    "source": {
                            "typeid": "SecondStaticType",
                            "index": "Asset2"
                    },
                    "target": {
                            "containerid": "Container3"
                    }
                },
                {
                    "source": {
                            "typeid": "SecondStaticType",
                            "index": "Asset2"
                    },
                    "target": {
                            "containerid": "Container4"
                    }
                }
            ]
        }
    ])



# ************************************************************************
# Helper functions: REQUIRED: create a JSON message that contains data values
# for all defined containerids
#
# Note: if you do not send one of the values for the container, Relay
# will emit the default value for missing property - it is the default
# behavior of JSON serialization; this might lead to undesireable
# results: for example, putting a value of zero into referenced PI
# point
# ************************************************************************


# ************************************************************************
# Finally, loop indefinitely, sending random events
# conforming to the container types that we defined earlier

# Note: PI points will be created on the first data value message
# arrived for a given container
#
# Note: values for each containerid are sent as a batch; you can update
# different containerids at different times
# ************************************************************************
def main(test = False):
    success = True
    try:
        global producerToken, omfEndPoint
        print('------------------------------------------------------------------')
        print(' .d88888b.  888b     d888 8888888888        8888888b. Y88b   d88P ')        
        print('d88P" "Y88b 8888b   d8888 888               888   Y88b Y88b d88P  ')
        print('888     888 88888b.d88888 888               888    888  Y88o88P   ')
        print('888     888 888Y88888P888 8888888           888   d88P   Y888P    ')
        print('888     888 888 Y888P 888 888               8888888P"     888     ')
        print('888     888 888  Y8P  888 888               888           888     ')	
        print('Y88b. .d88P 888   "   888 888               888           888     ')	
        print(' "Y88888P"  888       888 888      88888888 888           888     ')	
        print('------------------------------------------------------------------')

        config = configparser.ConfigParser()
        config.read('config.ini')

        namespaceId = config.get('Configurations', 'Namespace')
        resourceBase = config.get('Access', 'Resource')
        tenant = config.get('Access', 'Tenant')
        apiversion = config.get('Access', 'ApiVersion')
        producerToken = config.get('Credentials', 'ProducerToken')
        completedURL = config.get('Access', 'OMFEndpoint')

        if completedURL is not None:
            omfEndPoint = completedURL
        else:
            omfEndPoint = resourceBase + '/api/' + apiversion + '/tenants/' + tenant + '/namespaces/' + namespaceId +'/omf'
        

    # ************************************************************************
    # Turn off HTTPS warnings, if desired
    # ************************************************************************

    #    if not VERIFY_SSL:
    #        requests.packages.urllib3.disable_warnings()

        oneTimeSendMessages()

        count = 0
        while (not test) and count < 10:
            send_omf_message_to_endpoint("data", create_data_values_for_first_dynamic_type("container1"))
            send_omf_message_to_endpoint("data", create_data_values_for_first_dynamic_type("container2"))
            send_omf_message_to_endpoint("data", create_data_values_for_second_dynamic_type("container3"))
            send_omf_message_to_endpoint("data", create_data_values_for_third_dynamic_type("container4"))
            send_omf_message_to_endpoint("data", create_data_values_for_NonTimeStampIndexAndMultiIndex_type("container5", "container6"))
            time.sleep(1)
            count = count +1
    except Exception as ex:
        print(("Encountered Error: {error}".format(error = ex)))
        print
        traceback.print_exc()
        print
        success = False
        if test:
            raise ex

    finally:
        print 
        return success       

main()
print("done")

## Straightforward test to make sure program is working without an error in program.  Can run it yourself with pytest program.py
def test_main():
    main(True)