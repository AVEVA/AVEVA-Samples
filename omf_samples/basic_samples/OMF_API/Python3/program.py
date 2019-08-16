# NOTE: this script was designed using the v1.1
# version of the OMF specification, as outlined here:
# http://omf-docs.osisoft.com/en/v1.1
#*************************************************************************************

# OMF_API_Python3
# version 0.0.4
# 8-16-19

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
import base64 


# ************************************************************************
# Specify options for sending web requests to the target PI System
# ************************************************************************

# Whether or not we are inferring where the app is pointing to from the config file
forceSending = False

# Specifys whether we are sending to PI or OCS.  The main changes are in the accepted messages and the URL.
sendingToOCS = True

# Specify whether to compress OMF message before
# sending it to ingress endpoint
USE_COMPRESSION = False

# Set this to the path of the certificate pem file if you using a self signed cert.  
# Set this to True if your cert is trusted by the Python certify.  
# Set to False if you do not want to check the certificate (NOT RECOMMENDED)
VERIFY_SSL = True

# Specify the timeout, in seconds, for sending web requests
# (if it takes longer than this to send a message, an error will be thrown)
WEB_REQUEST_TIMEOUT_SECONDS = 30

# Holder for the producer token.  It is set from the configuration
producerToken = ""

# Holder for the omfEndPoint if sending to PI.  It is set from the configuration
omfEndPoint = ""

# Holder for the checkbase if sending to PI.  It is set from the configuration
checkBase = ""

# Holder for the omfEndPoint base if sending to OCS.  Auth and OMF endpoint are built from this.  It is set from the configuration
resourceBase = ""

dataServerName = ""

username = ""

password = ""


# The version of the OMFmessages
omfVersion = "1.1"

# Holders for data message values
integer_boolean_value = 0
string_boolean_value = "True"
integer_index1 = 0
integer_index2_1 = 1
integer_index2_2 = 1

# Token information
__expiration = 0
__token = ""

# Auth information.  It is set from the configuration
clientId = ""
clientSecret = ""

def getToken():
    # Gets the oken for the omfsendpoint    
    global __expiration, __token, resourceBase, clientId, clientSecret, producerToken, sendingToOCS

    if(not sendingToOCS):
        return producerToken

    if ((__expiration - time.time()) > 5 * 60):
        return __token

    # we can't short circuit it, so we must go retreive it.

    discoveryUrl = requests.get(
        resourceBase + "/identity/.well-known/openid-configuration",
        headers= {"Accept" : "application/json"},
        verify = VERIFY_SSL)

    if discoveryUrl.status_code < 200 or discoveryUrl.status_code >= 300:
        discoveryUrl.close()
        print("Failed to get access token endpoint from discovery URL: {status}:{reason}".
                        format(status=discoveryUrl.status_code, reason=discoveryUrl.text))
        raise ValueError

    tokenEndpoint = json.loads(discoveryUrl.content)["token_endpoint"]

    tokenInformation = requests.post(
        tokenEndpoint,
        data = {"client_id" : clientId,
                "client_secret" : clientSecret,
                "grant_type" : "client_credentials"},
        verify = VERIFY_SSL)

    token = json.loads(tokenInformation.content)

    if token is None:
        raise Exception("Failed to retrieve Token")

    __expiration = float(token['expires_in']) + time.time()
    __token = token['access_token']
    return __token


# ************************************************************************
# Helper function: REQUIRED: wrapper function for sending an HTTPS message
# ************************************************************************

# Define a helper function to allow easily sending web request messages;
# this function can later be customized to allow you to port this script to other languages.
# All it does is take in a data object and a message type, and it sends an HTTPS
# request to the target OMF endpoint

def send_omf_message_to_endpoint(message_type, message_omf_json, action = 'create'):
    # Sends the request out to the preconfigured endpoint..

    global producerToken, omfEndPoint, omfVersion, sendingToOCS, username, password
    # Compress json omf payload, if specified
    compression = 'none'
    if USE_COMPRESSION:
        msg_body = gzip.compress(bytes(json.dumps(message_omf_json), 'utf-8'))
        compression = 'gzip'
    else:
        msg_body = json.dumps(message_omf_json)

    msg_headers = getHeaders(compression,message_type,action)
    response = {}
    # Assemble headers   
    if sendingToOCS:     
        response = requests.post(
            omfEndPoint,
            headers = msg_headers,
            data = msg_body,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS
        )
    else:   
        response = requests.post(
            omfEndPoint,
            headers = msg_headers,
            data = msg_body,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS,
            auth=(username,password)
        )

    # Send the request, and collect the response

    if response.status_code == 409:
        return

    
    # response code in 200s if the request was successful!
    if response.status_code < 200 or response.status_code >= 300:
        print(msg_headers)
        response.close()
        print('Response from relay was bad.  "{0}" message: {1} {2}.  Message holdings: {3}'.format(message_type, response.status_code, response.text, message_omf_json))
        print()
        raise Exception("OMF message was unsuccessful, {message_type}. {status}:{reason}".format(message_type=message_type, status=response.status_code, reason=response.text))
 


def getHeaders(compression = "", message_type = "" , action = ""):
    global sendingToOCS

    # Assemble headers   
    if sendingToOCS:     
        msg_headers = {
            "Authorization": "Bearer %s" % getToken(),
            'producertoken': getToken(),
            'messagetype': message_type,
            'action': action,
            'messageformat': 'JSON',
            'omfversion': omfVersion,
            'compression': compression
        }
    else:   
        msg_headers = {
            "x-requested-with": "xmlhttprequest",
            'messagetype': message_type,
            'action': action,
            'messageformat': 'JSON',
            'omfversion': omfVersion
        }
        if(compression == "gzip"):
            msg_headers["compression"] = "gzip"
    return msg_headers


def checkValueGone(url):
    # Sends the request out to the preconfigured endpoint..

    global producerToken, sendingToOCS, username, password

    # Assemble headers        
    msg_headers = getHeaders()

    # Send the request, and collect the response
    if sendingToOCS:     
        response = requests.get(
            url,
            headers = msg_headers,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS
        )
    else:
        response = requests.get(
            url,
            headers = msg_headers,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS,
            auth=(username,password)
        )
    
    # response code in 200s if the request was successful!
    if response.status_code >= 200 and response.status_code < 300:
        response.close()
        print('Value found.  This is unexpected.  "{0}"'.format(response.status_code))
        print()
        raise Exception("Check message was failed. {status}:{reason}".format( status=response.status_code, reason=response.text))
    return response.text
   

def checkValue(url):
    # Sends the request out to the preconfigured endpoint..

    global producerToken, sendingToOCS, username, password

    # Assemble headers        
    msg_headers = getHeaders()

    # Send the request, and collect the response
    if sendingToOCS:     
        response = requests.get(
            url,
            headers = msg_headers,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS
        )
    else:
        response = requests.get(
            url,
            headers = msg_headers,
            verify = VERIFY_SSL,
            timeout = WEB_REQUEST_TIMEOUT_SECONDS,
            auth=(username,password)
        )
    
    # response code in 200s if the request was successful!
    if response.status_code < 200 or response.status_code >= 300:
        response.close()
        print('Response from endpoint was bad.  "{0}"'.format(response.status_code))
        print()
        raise Exception("OMF message was unsuccessful. {status}:{reason}".format( status=response.status_code, reason=response.text))
    return response.text
    
def getCurrentTime():
    # Returns the current time
    return datetime.datetime.utcnow().isoformat() + 'Z'

# Creates a JSON packet containing data values for containers
# of type FirstDynamicType defined below
def create_data_values_for_first_dynamic_type(containerid):
    # Returns a JSON representation of data for the first dynamic type.
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
    # Returns a JSON representation of data for the the second type.
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
    # Returns a JSON representation of data for the third dynamic type.
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
    # Returns a JSON representation of data for the nontime stap and multi-index types.
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

def oneTimeSendMessages(action = 'create'):    
    # Wrapper around all of the data and container messages.  
    global omfVersion, sendingToOCS

    # ************************************************************************
    # Send the types messages to define the types of streams that will be sent.
    # These types are referenced in all later messages
    # ************************************************************************

    # The sample divides types, and sends static and dynamic types
    # separatly only for readability; you can send all the type definitions
    # in one message, as far as its size is below maximum allowed - 192K
    # ************************************************************************



    # Step 3
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
                    "description": "not in use"
                },
                "name": {
                    "type": "string",
                    "isname": True,
                    "description": "not in use"
                },
                "StringProperty": {
                    "type": "string",
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
                    "description": "not in use"
                },
                "name": {
                    "type": "string",
                    "isname": True,
                    "description": "not in use"
                },
                "StringProperty": {
                    "type": "string",
                    "description": "Second static asset type's configuration attribute"
                }
            }
        }
    ],
    action)

    # Step 4
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
                    "description": "not in use"
                },
                "IntegerProperty": {
                    "type": "integer",
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
                    "description": "not in use"
                },
                "NumberProperty1": {
                    "type": "number",
                    "description": "PI point data referenced number attribute 1",
                    "format": "float64"
                },
                "NumberProperty2": {
                    "type": "number",
                    "description": "PI point data referenced number attribute 2",
                    "format": "float64"
                },
                "StringEnum": {
                    "type": "string",
                    "enum": ["False", "True"],
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
                    "description": "not in use"
                },
                "IntegerEnum": {
                    "type": "integer",
                    "format": "int16",
                    "enum": [0, 1],
                    "description": "Integer enumeration to replace boolean type"
                }
            }
        }
    ],action)

    # Step 5
    # Note for PI these messages throw errors if you send them
    # Send a JSON packet to define dynamic types   
    if(sendingToOCS):
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
        ],action)


    # ************************************************************************
    # Send a JSON packet to define containerids and the type
    # (using the types listed above) for each new data events container.
    # This instantiates these particular containers.
    # We can now directly start sending data to it using its Id.
    # ************************************************************************

    # Step 6
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
    ],action)

    
    # Note for PI these messages throw errors. 
    
    if(sendingToOCS):
        send_omf_message_to_endpoint("container", [
            {
                "id": "Container5",
                "typeid": "NonTimeStampIndex"
            },
            {
                "id": "Container6",
                "typeid": "MultiIndex"
            }
        ],action)


    # ************************************************************************
    # Send the messages to create the PI AF asset structure
    #
    # The following packets can be sent in one data message; the example
    # splits the data into several messages only for readability;
    # you can send all of the following data in one message,
    # as far as its size is below maximum allowed - 192K
    # ************************************************************************

    # Note for OCS these messages are ignored. 

    # Step 7
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
    ],action)


    # Step 8
    # Send a JSON packet to define links between assets
    # to create AF Asset structure
    '''
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
    ],action)
    '''

    # Send a JSON packet to define links between assets and
    # containerids to create attributes with PI point references
    # from containerid properties
    '''
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
    ],action)
    '''
    
def checkDeletes():    
    global checkBase, dataServerName

    print("Check Deletes")
    time.sleep(2)

    if(sendingToOCS):
        checkValueGone(checkBase + '/Streams' + '/Container1')
    else:
        json1 = checkValue(checkBase + "/dataservers?name=" + dataServerName)
        pointsURL = json.loads(json1)['Links']['Points']
        json1 = checkValue(pointsURL + "?nameFilter=container1*")
        links = json.loads(json1)['Links']
        assert len(links) == 0





def checkSends(lastVal):    
    global checkBase, dataServerName

    print("Checks")

    if(sendingToOCS):

        # just getting back the type or stream means that it worked
        json1 = checkValue(checkBase + '/Types' + '/FirstDynamicType')
        #print(json1)
        json1 = checkValue(checkBase + '/Streams' + '/Container1')
        #print(json1)
        json1 = checkValue(checkBase + '/Streams' + '/Container1'+ '/Data/last')

        # just checking to make sure some data made it it, could do a more comprhensive check but this is ok...
        assert lastVal[0]['values'][0]['IntegerProperty']  == json.loads(json1)['IntegerProperty']


    else:
        #print(json1)
        json1 = checkValue(checkBase + "/dataservers?name=" + dataServerName)
        pointsURL = json.loads(json1)['Links']['Points']

        json1 = checkValue(pointsURL + "?nameFilter=container1*")
        endValueURL = json.loads(json1)['Items'][0]['Links']['Value']
        
        json1 = checkValue(endValueURL)

        # just checking to make sure some data made it it, could do a more comprhensive check but this is ok...
        assert lastVal[0]['values'][0]['IntegerProperty']  == json.loads(json1)['Value']

def supressError(sdsCall):
    #easily call a function and not have to wrap it individually for failure
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error = e)))

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

def getConfig(section, field):
    #Reads the config file for the field specified
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.has_option(section,field) and config.get(section,field) or ""

# ************************************************************************
# Note: PI points will be created on the first data value message
# arrived for a given container
# ************************************************************************
def main(test = False):
    # Main program.  Seperated out so that we can add a test function and call this easily
    global omfVersion, resourceBase, producerToken, omfEndPoint, clientId, clientSecret, checkBase
    global dataServerName, forceSending, sendingToOCS, VERIFY_SSL, username, password
    success = True
    try:
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

        # Step 1
        #OCS configuration
        namespaceId = getConfig('Configurations', 'Namespace') 
        resourceBase = getConfig('Access', 'Resource')
        tenant = getConfig('Access', 'Tenant')
        apiversion = getConfig('Access', 'ApiVersion')
        producerToken = getConfig('Credentials', 'ProducerToken')
        producerToken = getConfig('Credentials', 'ProducerToken')
        clientId = getConfig('Credentials', 'ClientId')
        clientSecret = getConfig('Credentials', 'ClientSecret')
        
        #PI Web API configuration
        dataServerName = getConfig('Configurations', 'DataServerName') 
        verify = getConfig('Configurations', 'VERIFY_SSL') 
        username = getConfig('Credentials', 'username') 
        password = getConfig('Credentials', 'password') 

        #shared configuration
        resourceBase = getConfig('Access', 'Resource')

        if verify is not None:
            if verify == "False":
                VERIFY_SSL =  False

        if not forceSending:
            if tenant is "":
                sendingToOCS = False
            else:
                sendingToOCS = True

        if sendingToOCS:
            checkBase = resourceBase + '/api/' + apiversion + '/tenants/' + tenant + '/namespaces/' + namespaceId
            omfEndPoint = checkBase +'/omf'
        else:
            checkBase = resourceBase 
            omfEndPoint = checkBase + '/omf'
        
        if not VERIFY_SSL:
            print("You are not verifying the certificate of the end point.  This is not advised for any system as there are security issues with doing this.")

        # Step 2
        getToken()




        # Steps 3-8 contained in here
        oneTimeSendMessages()

        # Step 9
        count = 0
        lastVal = ''
        time.sleep(1)
        while count == 0 or ((not test) and count < 2):
            val = create_data_values_for_first_dynamic_type("Container1")
            lastVal = val
            send_omf_message_to_endpoint("data", val)
            send_omf_message_to_endpoint("data", create_data_values_for_first_dynamic_type("Container2"))
            send_omf_message_to_endpoint("data", create_data_values_for_second_dynamic_type("Container3"))
            send_omf_message_to_endpoint("data", create_data_values_for_third_dynamic_type("Container4"))            
            if(sendingToOCS):
                send_omf_message_to_endpoint("data", create_data_values_for_NonTimeStampIndexAndMultiIndex_type("Container5", "Container6"))
            time.sleep(1)
            count = count +1
        checkSends(lastVal)
    except Exception as ex:
        print(("Encountered Error: {error}".format(error = ex)))
        print
        traceback.print_exc()
        print
        success = False
        if test:
            raise ex

    finally:
        print ('Deletings')

        # Step 10
        oneTimeSendMessages('delete')
        checkDeletes()
        print 
        return success       

main()
print("done")

## Straightforward test to make sure program is working without an error in program.  Can run it yourself with pytest program.py
def test_main():
    #Tests to make sure the sample runs as expected
    main(True)
