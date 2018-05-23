import { Component } from '@angular/core';

import { AdalService } from './adal/adal.service'
import { ConfigurationService, IQiConfigSet } from './osiconfiguration.service'
import { Router } from '@angular/router';

const config: IQiConfigSet = {
  ClientID: 'bfe32ce8-4237-48ef-8898-f64b65a5ab3c',
  // QiEndPoint: 'https://historianmain.osipi.com',
  QiEndPoint: 'https://historiandev2.osipi.com',
  QiResourceURI: 'https://pihomemain.onmicrosoft.com/ocsapi',
  TenantId: 'a445ee81-2b91-4806-883b-1dc673d59147',
  NamespaceId: 'jakeTest'
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
