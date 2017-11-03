import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, IQiConfigSet } from './osiconfiguration.service'
import {Router} from '@angular/router';

const config: IQiConfigSet = {
  Subscription: 'REPLACE_WITH_AZURE_SUBSCRIPTION',
  ClientID: 'REPLACE_WITH_APPLICATION_ID',
  SystemEndpoint: 'REPLACE_WITH_SYSTEM_ENDPOINT',
  SystemResourceURI: 'REPLACE_WITH_SYSTEM_RESOURCE_URI',
  QiEndPoint: 'REPLACE_WITH_QI_ENDPOINT',
  QiResourceURI: 'REPLACE_WITH_QI_RESOURCE_URI',
  TenantId: 'REPLACE_WITH_TENANT_ID',
  NamespaceId: 'REPLACE_WITH_NAMESPACE'
} 

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
      this.adalService.handleWindowCallbackUrl(path.url.substring(1));
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
