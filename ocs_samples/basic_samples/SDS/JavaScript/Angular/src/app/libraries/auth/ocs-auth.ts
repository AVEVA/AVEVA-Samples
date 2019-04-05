// ocs-auth.ts
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

import { NgModule, ModuleWithProviders, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OidcService } from './lib/core/oidc.service';
import { OAuthLoginComponent } from './lib/components/oauth-login.component';
import { OAuthLogoutComponent } from './lib/components/oauth-logout.component';
import { OAuthCallbackHandlerGuard } from './lib/core/oauth-callback-handler.guard';

@NgModule({
    imports: [ CommonModule ],
    declarations: [ OAuthLoginComponent, OAuthLogoutComponent ],
    providers: [
        OidcService,
        OAuthCallbackHandlerGuard
    ]
})
export class OidcModule {
    constructor(@Optional() @SkipSelf() parentModule: OidcModule) {
        if (parentModule) {
            throw new Error('OidcModule is already loaded. Import it in the AppModule only');
        }
    }

    static forRoot(): ModuleWithProviders {
        return {
            ngModule: OidcModule,
            providers: [
                OidcService,
                OAuthCallbackHandlerGuard
            ]
        };
    }
}

export { OidcService } from './lib/core/oidc.service';
export { OAuthLoginComponent } from './lib/components/oauth-login.component';
export { OAuthLogoutComponent } from './lib/components/oauth-logout.component';
export { OAuthCallbackHandlerGuard } from './lib/core/oauth-callback-handler.guard';

