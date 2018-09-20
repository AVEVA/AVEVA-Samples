# sds_stream_index.py
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


class SdsStreamIndex(object):
    """Sds Stream Index definitions"""

    @property
    def sds_type_property_id(self):
        return self.__sds_type_property_id

    @sds_type_property_id.setter
    def sds_type_property_id(self, sds_type_property_id):
        self.__sds_type_property_id = sds_type_property_id

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'sds_type_property_id': self.sds_type_property_id}

        return json.loads(dictionary)

    @staticmethod
    def from_dictionary(content):
        type_property_id = SdsStreamIndex()

        if len(content) == 0:
            return type_property_id

        if 'sds_type_property_id' in content:
            type_property_id.sds_type_property_id = content['sds_type_property_id']

        return type_property_id
