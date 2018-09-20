<# sds_type_data.py

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

import datetime
import json
from performance_counters import PerformanceCounters as PC


class SdsTypeData:
    def __init__(self, type_id=None, time=None):
        self.type_id = type_id
        self.time = time

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        if self.time:
            time = self.time
        else:
            time = datetime.datetime.utcnow()
        dictionary = {'Time': str(time), 'Typeid': self.type_id}
        for k, v in self.__dict__.items():
            if k != "time" and k != "typeId":
                dictionary[k] = v
        self.__properties = dictionary
        return dictionary

    def from_json(self, json_obj):
        return self.from_dictionary(json_obj)

    def from_dictionary(self, content):
        if self is None:
            return SdsTypeData()
        data_obj = SdsTypeData(self.type_id)
        prop_names = PC().get_counter_names(self.type_id)

        data_obj.__setattr__('time', content['Time'])
        for prop in prop_names:
            # Pre-Assign the default
            data_obj.__setattr__(prop, 0)

            if prop in content:
                value = content[prop]
                if value is not None:
                    data_obj.__setattr__(prop, value)
        return data_obj
