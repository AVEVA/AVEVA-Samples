# BaseClient.py
#
# Copyright (C) 2018-2019 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
#
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

from .SdsError import SdsError 

import requests
import time


class BaseClient(object):
    """Handles communication with Sds Service"""

    def __init__(self, apiversion, tenant, url, clientId, clientSecret):
        self.__apiversion = apiversion
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__url = url # if resource.endswith("/")  else resource + "/" 

        self.__token = ""
        self.__expiration = 0
        self.__getToken()

    def __getToken(self):
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
        return {"Authorization": "Bearer %s" % self.__getToken(),
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
                }
