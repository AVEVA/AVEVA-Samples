<# SdsNamespace.py

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
#>

import json

class SdsNamespace(object):
    """description of class"""

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
