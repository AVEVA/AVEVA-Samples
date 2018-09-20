<# performance_counters.py

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

import psutil


class PerformanceCounters:
    def __init__(self):
        self.type_dict = {
            "processor": psutil.cpu_times(),
            "memory": psutil.virtual_memory()
        }

    def get_counters(self, type_id):
        return self.type_dict[type_id.lower()]

    def get_counter_names(self, type_id):
        return self.type_dict.get(type_id.lower())._fields
