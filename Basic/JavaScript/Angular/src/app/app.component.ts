import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, IQiConfigSet } from './osiconfiguration.service'
import { Router } from '@angular/router';

const config: IQiConfigSet = {
    ClientID: 'PLACEHOLDER_REPLACE_WITH_CLIENTID',
    QiEndPoint: 'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL',
    QiResourceURI: 'PLACEHOLDER_REPLACE_WITH_RESOURCE',
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
      if (!path) {
          this.adalService.handleWindowCallbackUrl(path.url.substring(1));
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
