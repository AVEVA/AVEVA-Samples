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
import { AppComponent } from './app.component';
import { SdsRestService } from './sds/sds.rest.service';
import { DatasrcComponent } from './datasrc/datasrc.component';
import { routing, appRoutingProviders  } from './app.routing';
import {HttpClientModule, HTTP_INTERCEPTORS} from "@angular/common/http";
import { OidcService, OAuthLoginComponent, OAuthLogoutComponent, OAuthCallbackHandlerGuard } from '@osisoft/identity-ts';
import { AuthenticationGuard } from './auth/authguard';
import { AuthInterceptor } from './auth/authentication.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    DatasrcComponent,
    OAuthLoginComponent,
    OAuthLogoutComponent
  ],
  imports: [
    BrowserModule,
    NgbModule.forRoot(),
    routing,
    HttpClientModule
  ],
  providers: [
    appRoutingProviders,
    SdsRestService,
    OidcService,
    AuthenticationGuard,
    OAuthCallbackHandlerGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
