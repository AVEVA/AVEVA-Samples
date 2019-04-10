// app.component.ts
//
// Copyright 2019 OSIsoft, LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// <http://www.apache.org/licenses/LICENSE-2.0>
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {OidcService} from './libraries/auth/ocs-auth'
import {UserManagerSettings, WebStorageStateStore} from 'oidc-client'
import oidcConfigJson from './config/oidc.config.json';
import sdsConfig from './config/sdsconfig.json';
import { SdsConfig } from './config/sdsconfig.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})
export class AppComponent implements OnInit {
  private sdsConfig: SdsConfig;
  private authConfig: UserManagerSettings;

  constructor(private router: Router, private auth: OidcService) {
    this.sdsConfig = sdsConfig as SdsConfig;
  }

  ngOnInit(): void {
    const configFromJson = oidcConfigJson as UserManagerSettings;
    this.authConfig = {
      ...configFromJson,
      userStore: new WebStorageStateStore({store: window.localStorage}),
      acr_values: `tenant:${this.sdsConfig.tenantId}`,
      response_type: "id_token token",
      scope: "openid ocsapi",
      filterProtocolClaims: true,
      loadUserInfo: true,
      revokeAccessTokenOnSignout: true,
      automaticSilentRenew: true,
      accessTokenExpiringNotificationTime: 60,
      silentRequestTimeout: 10000
    }

    this.auth.init(this.authConfig);
  }

  get loggedIn() {
    return (this.auth.userInfo !== null);
  }

  login() {
    this.auth.login();
  }

  logout() {
    this.auth.logout();
  }
}
