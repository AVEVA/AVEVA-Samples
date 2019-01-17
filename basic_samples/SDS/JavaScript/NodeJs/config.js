// config.js
//
// Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
//
// THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
// OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
// THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
//
// RESTRICTED RIGHTS LEGEND
// Use, duplication, or disclosure by the Government is subject to restrictions
// as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
// Computer Software clause at DFARS 252.227.7013
//
// OSIsoft, LLC
// 1600 Alvarado St, San Leandro, CA 94577

module.exports = {

    //VERY IMPORTANT: edit the following values to reflect the authorization items you were given
    authItems: {
        'resource': "https://qihomeprod.onmicrosoft.com/ocsapi",
        'authority': "https://login.windows.net/<REPLACE_WITH_TENANT_ID>.onmicrosoft.com/oauth2/token",
        'clientId': "REPLACE_WITH_APPLICATION_IDENTIFIER",
        'clientSecret': "REPLACE_WITH_APPLICATION_SECRET"
    },
    sdsServerUrl: "https://dat-a.osisoft.com",
    tenantId: "REPLACE_WITH_TENANT_ID",
    namespaceId: "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID"
}
