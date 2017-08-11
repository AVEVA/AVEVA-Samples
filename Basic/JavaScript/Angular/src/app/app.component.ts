import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, IQiConfigSet } from './osiconfiguration.service'
import {Router} from '@angular/router';

const config: IQiConfigSet = {
  Subscription: 'Subscription Name',
  ClientID: 'ENTER CLIENT ID',
  SystemEndpoint: 'ENTER SYSTEM ENDPOINT',
  SystemResourceURI: 'ENTER SYSTEM RESOURCE URI',
  QiEndPoint: 'ENTER QI ENDPOINT',
  QiResourceURI: 'ENTER QI RESOURCE URI',
  TenantId: 'ENTER TENANT ID',
  NamespaceId: 'ENTER NAMESPACE ID'
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
