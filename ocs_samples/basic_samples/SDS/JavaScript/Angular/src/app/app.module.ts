// app.module.ts
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

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
