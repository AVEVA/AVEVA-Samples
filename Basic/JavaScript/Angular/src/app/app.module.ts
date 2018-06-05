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
