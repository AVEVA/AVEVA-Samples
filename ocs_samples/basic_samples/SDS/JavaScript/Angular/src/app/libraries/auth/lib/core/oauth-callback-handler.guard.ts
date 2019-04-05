// oauth-callback-handler.guard.ts
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
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { OidcService } from '../core/oidc.service';

/**
 * This guard will run only when the user has successfully logged in and when adal tokens have been renewed. On login this logic will
 * occur in the window that the app is being run in. On token renewal this logic will occur in a hidden iframe.
 */
@Injectable()
export class OAuthCallbackHandlerGuard implements CanActivate {
  constructor(
    private router: Router,
    private oidcService: OidcService
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> {
    this.oidcService.windowCallbackInProgress = true;
    const signinCallback = window.frameElement ? this.oidcService.handleSilentCallback() : this.oidcService.handleRedirectCallback();

    return signinCallback.then(() => {
      this.oidcService.emitLoginSuccessEvent(true);
      this.oidcService.windowCallbackInProgress = false;
      this.router.navigate([]);
      return true;
    }).catch(() => {
      this.oidcService.emitLoginSuccessEvent(false);
      this.oidcService.windowCallbackInProgress = false;
      this.router.navigate(['login']);
      return false;
    });
  }
}
