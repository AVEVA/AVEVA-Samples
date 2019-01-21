// app.component.ts
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

import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, ISdsConfigSet } from './osiconfiguration.service'
import { Router } from '@angular/router';

const config: ISdsConfigSet = {
    ClientID: 'PLACEHOLDER_REPLACE_WITH_CLIENTID',
    SdsEndPoint: 'PLACEHOLDER_REPLACE_WITH_SDS_SERVER_URL',
    SdsResourceURI: 'PLACEHOLDER_REPLACE_WITH_RESOURCE',
    TenantId: 'PLACEHOLDER_REPLACE_WITH_TENANT_ID',
    NamespaceId: 'REPLACE_WITH_NAMESPACE'
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
