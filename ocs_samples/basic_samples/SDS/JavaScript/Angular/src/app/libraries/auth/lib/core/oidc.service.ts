// oidc.service.ts
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

import { Injectable } from '@angular/core';

import { UserManager, UserManagerSettings, User } from 'oidc-client';
import { Subject } from 'rxjs';

@Injectable()
export class OidcService {
  private manager: UserManager;
  private config: UserManagerSettings;
  private user: User;
  private serviceInitialized: boolean;

  public windowCallbackInProgress: boolean;
  public loginSuccess: Subject<boolean>;

  constructor() {}

  /**
   * Must be called to initialize the service with the proper configuration.
   * @param config The adal configuration object.
   */
  public init(config: UserManagerSettings) {
    this.config = config;
    this.manager = new UserManager(config);
    this.loginSuccess = new Subject<boolean>();

    this.serviceInitialized = true;
  }

  /**
   * The handleWindowCallback function is responsible for extracting tokens
   * from the ADAL return url and putting them into session/local storage. This function
   * also has a additional logic to acquire an access_token after successfully retreiving
   * or renewing a token.
   *
   * @returns The a string observable containing the access_token for the gateway if both the
   * id_token and access_token are retrieved, otherwise returns null.
   */
  public handleRedirectCallback() {
    this.checkInit();
    return this.manager.signinRedirectCallback().then(user => {
      this.user = user;
    });
  }

  public handleSilentCallback() {
    this.checkInit();
    return this.manager.signinSilentCallback();
  }

  /**
   * The acquireAccessToken function makes a call to acquireToken on the gateway endpoint resource, which is the resource
   * to obtain the access_token. If the access_token is valid it will simply be returned from the cache otherwise ADAL will
   * make a call to renew the token
   *
   * @returns A string observable containing the access_token if it is cached or successfully renewed, otherwise it returns null.
   */
  /*public acquireAccessToken(): Observable<string> {
    this.checkInit();
    return Observable.create(observer => {
      this.context.acquireToken(this.adalResource, (message: string, token: string) => {
        if (message) {
          observer.next(null);
        } else {
          observer.next(token);
        }
        observer.complete();
      });
    });
  }*/

  public login() {
    this.checkInit();
    this.manager.signinRedirect();
  }

  public logout() {
    this.checkInit();
    this.manager.signoutRedirect();
  }

  // TODO: What is this?
  public piiLogging(enable: boolean): void {
    this.checkInit();
    (<any>window).Logging.piiLoggingEnabled = enable;
  }

  public emitLoginSuccessEvent(success: boolean): void {
    this.checkInit();
    this.loginSuccess.next(success);
    this.loginSuccess.complete();
  }

  // Wrap config service functions into this service
  public getConfig(): UserManagerSettings {
    this.checkInit();
    return this.config;
  }

  private checkInit() {
    if (!this.serviceInitialized) {
      throw 'AdalService has not been initialized.';
    }
  }

  public get userInfo() {
    this.checkInit();
    // TODO: We should use manager.getUser() to fetch the user from storage.
    // However, that's an async call and will require a number of changes to the portal.
    return this.user || this.getCachedUser();
  }

  public get isAuthenticated(): boolean {
    this.checkInit();
    const userinfo: any = this.userInfo;
    return userinfo && !userinfo.expired;
  }

  // TODO: Delete this. See note in userInfo property.
  private getCachedUser() {
    const storageKey = `oidc.user:${this.config.authority}:${this.config.client_id}`;
    const userString = sessionStorage.getItem(storageKey) || localStorage.getItem(storageKey);
    return JSON.parse(userString);
  }
}
