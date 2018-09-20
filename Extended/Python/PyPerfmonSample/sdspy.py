''' sdspy.py

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
'''

# sdspy

import configparser
import datetime
import json
from performance_counters import PerformanceCounters as PC
from sds_client import SdsClient
from sds_stream import SdsStream
from sds_type import SdsType
from sds_type_code import SdsTypeCode
from sds_type_data import SdsTypeData
from sds_type_property import SdsTypeProperty
import time
import xml.etree.ElementTree
import xml
