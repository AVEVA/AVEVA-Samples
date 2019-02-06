// app.component.ts
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

import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, ISdsConfigSet } from './osiconfiguration.service'
import { Router } from '@angular/router';

const config: ISdsConfigSet = {
    ClientID: 'PLACEHOLDER_REPLACE_WITH_CLIENTID',
    SdsEndPoint: 'PLACEHOLDER_REPLACE_WITH_SDS_SERVER_URL',
    SdsResourceURI: 'PLACEHOLDER_REPLACE_WITH_RESOURCE',
    TenantId: 'PLACEHOLDER_REPLACE_WITH_TENANT_ID',
    NamespaceId: 'REPLACE_WITH_NAMESPACE',
    ApiVersion: 'v1-preview'
};

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})
export class AppComponent {
  constructor(private adalService: AdalService,
              private configurationService: ConfigurationService,
              private router: Router) {
    this.configurationService.AmbientConfiguration = config;
    this.adalService.init(this.configurationService.adalConfig);

    this.router.events.subscribe((path: any) => {
      console.log('path = ', path);
      if (path) {
        if (path.url) {
            this.adalService.handleWindowCallbackUrl(path.url.substring(1));
        }
      }
    });
  }

  logOutUser(): void {
    this.adalService.logOut();
  }

  loginUser(): void {
    this.adalService.login();
  }

  isAuthenticated(): boolean {
    return this.adalService.userInfo.isAuthenticated;
  }

  getUserName(): string {
    if (this.adalService.userInfo.isAuthenticated) {
      return this.adalService.userInfo.profile.name;
    } else {
      return null;
    }
  }
}
