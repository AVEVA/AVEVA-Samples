# SdsDataviewQuery.py
#
# Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
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

import json
from SdsDataviewQueryQuery import SdsDataviewQueryQuery

class SdsDataviewQuery(object):
    """Sds dataview definition"""
    @property
    def Id(self):
        return self.__id
    @Id.setter
    def Id(self, id):
        self.__id = id
    
    @property
    def Query(self):
        return self.__query
    @Query.setter
    def Query(self, query):
        self.__query = query    


    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        # required properties
        dictionary = { 'Id' : self.Id}
        dictionary['Query'] = self.Query.toDictionary()
	
        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return SdsDataviewQuery.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        dataviewQuery = SdsDataviewQuery()

        if len(content) == 0:
            return dataviewQuery

        if 'Id' in content:
            dataviewQuery.Id = content['Id']
			
        if 'Query' in content:
            dataviewQuery.Query = SdsDataviewQueryQuery.fromDictionary(content['Query'])


        return dataviewQuery

