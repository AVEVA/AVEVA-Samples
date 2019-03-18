// config.js
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

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
    namespaceId: "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
    apiVersion: "v1-preview"
}
