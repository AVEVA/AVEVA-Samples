// app.module.ts
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

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ConfigurationService } from './osiconfiguration.service';
import { AdalService } from './adal/adal.service';
import { AppComponent } from './app.component';
import { SdsRestService } from './sds.rest.service';
import { AuthHttp } from './adal/authHttp.service';
import { DatasrcComponent } from './datasrc/datasrc.component';
import { routing, appRoutingProviders  } from './app.routing';
import {HttpClientModule, HTTP_INTERCEPTORS} from "@angular/common/http";
import {AuthInterceptor} from "./adal/authInterceptor";
import {OptionInterceptor} from "./adal/optionInterceptor";

@NgModule({
  declarations: [
    AppComponent,
    DatasrcComponent
  ],
  imports: [
    BrowserModule,
    NgbModule.forRoot(),
    routing,
    HttpClientModule
  ],
  providers: [
    ConfigurationService,
    appRoutingProviders,
    AdalService,
    SdsRestService,
    AuthHttp,
    {
        provide: HTTP_INTERCEPTORS,
        useClass: OptionInterceptor,
        multi: true
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
