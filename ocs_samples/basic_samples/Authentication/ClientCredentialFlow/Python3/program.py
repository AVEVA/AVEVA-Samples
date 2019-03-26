# program.py
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

from authpy import *
import configparser
import json
import requests

def main():
    try:
        config = configparser.ConfigParser()
        config.read_file('config.ini')

        client = AuthClientCredential(config.get('Access', 'Resource'), config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))
        url = client.getBasePath()

        tenant_id = config.get('Access', 'Tenant')
        api_version = config.get('Access', 'ApiVersion')

        response = requests.get(
                client.getBasePath() + '/api/{api_version}/Tenants/{tenant_id}'.format(api_version= api_version, tenant_id=tenant_id),
                headers= client.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise Error("Failed to get tenant, {tenant_id}. {status}:{reason}".format(tenant_id=tenant_id, status=response.status_code, reason=response.text))
            
        content = json.loads(response.content)
        response.close()
        assert content["Id"] == tenant_id, "Error in getting tenant back"
        print("Tenant Id matches expected result")


    except Exception as i:
        print(("Encountered Error: {error}".format(error = i)))
        print()

main()
print("done")

def test_main():
    main()
