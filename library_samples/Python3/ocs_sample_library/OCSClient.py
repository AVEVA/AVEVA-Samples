# OCSClient.py
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

from .BaseClient import BaseClient
from .DataviewClient import DataviewClient
from .SdsError import SdsError


class OCSClient:
    """Handles communication with Sds Service"""

    def __init__(self, apiversion, tenant, url, clientId, clientSecret):
        self.__baseClient = BaseClient(apiversion, tenant, url, clientId, clientSecret)
        self.__DataviewClient  = DataviewClient(tenant, url, self.__baseClient)

    @property 
    def DataviewClient(self):
        return self.__DataviewClient

    def z(self):
        return True
