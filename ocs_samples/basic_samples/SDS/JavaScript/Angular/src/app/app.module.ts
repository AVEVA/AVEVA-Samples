// app.module.ts
//

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppComponent } from './app.component';
import { SdsRestService } from './sds/sds.rest.service';
import { DatasrcComponent } from './datasrc/datasrc.component';
import { routing, appRoutingProviders  } from './app.routing';
import {HttpClientModule, HTTP_INTERCEPTORS} from "@angular/common/http";
import { OidcService, OAuthLoginComponent, OAuthLogoutComponent, OAuthCallbackHandlerGuard } from '../app/libraries/auth/ocs-auth';
import { AuthenticationGuard } from '../app/libraries/auth/extra/authguard';
import { AuthInterceptor } from '../app/libraries/auth/extra/authentication.interceptor';

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
