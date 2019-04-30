# BaseClient.py
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

from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

from .SdsError import SdsError 

import requests
import time


class BaseClient(object):
    """Handles communication with Sds Service.  Internal Use"""

    def __init__(self, apiversion, tenant, url, clientId, clientSecret):
        self.__apiversion = apiversion
        self.__tenant = tenant
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__url = url # if resource.endswith("/")  else resource + "/" 

        self.__token = ""
        self.__expiration = 0
        self.__getToken()

        self.__uri_API =  url + '/api/' + apiversion

    
    @property
    def uri(self):
        """
        Gets the base url
        :return:
        """
        return self.__url

        
    @property
    def uri_API(self):
        """
        Returns the base URL plus api versioning information
        :return:
        """
        return self.__uri_API
    
    @property
    def api_version(self):
        """
        Returns just the base api versioning information
        :return:
        """
        return self.__apiversion
        
    @property
    def tenant(self):
        """
        Returns the tenant ID
        :return:
        """
        return self.__tenant

    def __getToken(self):
        """
        Gets the bearer token
        :return:
        """
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        discoveryUrl = requests.get(
            self.__url + "/identity/.well-known/openid-configuration",
            headers= {"Accept" : "application/json"})

        if discoveryUrl.status_code < 200 or discoveryUrl.status_code >= 300:
            discoveryUrl.close()
            raise SdsError("Failed to get access token endpoint from discovery URL: {status}:{reason}".
                            format(status=discoveryUrl.status_code, reason=discoveryUrl.text))

        tokenEndpoint = json.loads(discoveryUrl.content)["token_endpoint"]

        tokenInformation = requests.post(
            tokenEndpoint,
            data = {"client_id" : self.__clientId,
                    "client_secret" : self.__clientSecret,
                    "grant_type" : "client_credentials"})

        token = json.loads(tokenInformation.content)

        if token is None:
            raise Exception("Failed to retrieve Token")

        self.__expiration = float(token['expires_in']) + time.time()
        self.__token = token['access_token']
        return self.__token

    def sdsHeaders(self):
        """
        Gets the base headers needed for OCS call
        :return:
        """
        return {"Authorization": "Bearer %s" % self.__getToken(),
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
                }
