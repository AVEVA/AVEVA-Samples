# program.py
#
# Copyright (C) 2019 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from ocs_sample_library_preview import *
import configparser
import datetime
import time
import math
import inspect
import collections
import traceback

namespaceId = ''
config = configparser.ConfigParser()
config.read('config.ini')

def main():
    global namespaceId

    try:
        print("--------------------------------------------------------------------")
        print(" ######                                             ######  #     # ")        
        print(" #     #   ##   #####   ##   #    # # ###### #    # #     #  #   #  ")
        print(" #     #  #  #    #    #  #  #    # # #      #    # #     #   # #   ")
        print(" #     # #    #   #   #    # #    # # #####  #    # ######     #    ")
        print(" #     # ######   #   ###### #    # # #      # ## # #          #    ")
        print(" #     # #    #   #   #    #  #  #  # #      ##  ## #          #    ")	
        print(" ######  #    #   #   #    #   ##   # ###### #    # #          #    ")	
        print("--------------------------------------------------------------------")

        ocsClient = OCSClient(config.get('Access', 'ApiVersion'), config.get('Access', 'Tenant'), config.get('Access', 'Resource'), 
                        config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

        omfType = Type.newBasicTimeNumber('basicTimeValue')
        omfContainer = Container('pumpTemp1', 'basicTimeValue')
        t= "2017-01-11T22:24:23.430Z"
        data = {"value" :51, "time" :t }
        
        omfData = Data( 'pumpTemp1', values = [data])

        ocsClient.OMF.postType(omfType)
        ocsClient.OMF.postContainer(omfContainer)
        ocsClient.OMF.postData(omfData)

        namespaceId = config.get('Configurations', 'Namespace')
        
    


    except Exception as ex:
        print(("Encountered Error: {error}".format(error = ex)))
        print
        traceback.print_exc()
        print

    finally:

        print
        print
        
       


main()
print("done")

## Straightforward test to make sure program is working using asserts in program.  Can run it yourself with pytest program.py
def test_main():
    main()