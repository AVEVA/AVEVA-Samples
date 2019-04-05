// oauth-login.component.ts
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
import { OidcService } from '../core/oidc.service';

@Component({
    selector: 'adal-login',
    template: ''
})
export class OAuthLoginComponent {
    constructor(private oidcService: OidcService) {
        this.oidcService.login();
    }
}
