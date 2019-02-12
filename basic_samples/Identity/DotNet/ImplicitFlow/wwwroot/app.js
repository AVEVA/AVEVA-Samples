/// <reference path="oidc-client.js" />

// app.js
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

function log() {
    document.getElementById('results').innerText = '';
    console;
    Array.prototype.forEach.call(arguments, function (msg) {
        if (msg instanceof Error) {
            msg = "Error: " + msg.message;
        }
        else if (typeof msg !== 'string') {
            msg = JSON.stringify(msg, null, 2);
        }
        document.getElementById('results').innerHTML += msg + '\r\n';
    });
}

document.getElementById("login").addEventListener("click", login, false);
document.getElementById("logout").addEventListener("click", logout, false);
document.getElementById("tenant").addEventListener("click", getTenant, false);

var mgr = new Oidc.UserManager(config);

mgr.getUser().then(function (user) {
    if (user) {
        log("User logged in", user.profile);
    }
    else {
        log("User not logged in");
    }
});

function login() {
    mgr.signinRedirect();
}

function getTenant() {
    mgr.getUser().then(function(user) {
        if (user) {
            var accessToken = user.access_token;
            // get the header
            var bearer = 'Bearer ' + accessToken;

            // form url
            var host = window.config.authority.replace('identity', '');
            var tenantId = window.config.acr_values.replace('tenant:', '');
            const url = host + 'api/tenants/' + tenantId;

            // Set header
            $.ajaxSetup({
                headers: {
                    'Authorization': bearer
                }
            });

            // Make request
            $.getJSON(url,
                function(result) {
                    log(result);
                });
        } else {
            log("Tenant Information" ,"User not logged in");
        }
    });
}

function logout() {
    mgr.signoutRedirect();
}