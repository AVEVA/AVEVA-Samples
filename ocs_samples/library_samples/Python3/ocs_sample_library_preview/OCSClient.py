# OCSClient.py
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

from .BaseClient import BaseClient
from .Dataviews import Dataviews
from .Types import Types
from .Streams import Streams
from .SdsError import SdsError


class OCSClient:
    """Handles communication with Sds Service"""

    def __init__(self, apiversion, tenant, url, clientId, clientSecret, acceptVerbosity=False):
        self.__baseClient = BaseClient(apiversion, tenant, url, clientId, clientSecret, acceptVerbosity)

        self.__Dataviews  = Dataviews(self.__baseClient)
        self.__Types  = Types(self.__baseClient)
        self.__Streams  = Streams(self.__baseClient)


    @property 
    def uri(self):
        return self.__baseClient.uri

    @property 
    def tenant(self):
        return self.__baseClient.tenant

    @property
    def acceptverbosity(self):
        return self.__baseClient.AcceptVerbosity
    @acceptverbosity.setter
    def acceptverbosity(self, AcceptVerbosity):
        self.__baseClient.AcceptVerbosity = AcceptVerbosity

    @property 
    def Dataviews(self):
        return self.__Dataviews

    @property 
    def Types(self):
        return self.__Types

    @property 
    def Streams(self):
        return self.__Streams
