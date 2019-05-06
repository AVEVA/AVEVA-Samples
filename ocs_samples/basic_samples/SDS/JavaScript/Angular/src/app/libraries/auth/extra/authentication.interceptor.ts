// authentication.interceptor.ts
//

import { OidcService } from "../ocs-auth";
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from "@angular/common/http";
import { Observable } from "rxjs";
import { Injectable } from "@angular/core";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(public auth: OidcService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    request = request.clone({
      setHeaders: {
        Authorization: `${this.auth.userInfo.token_type} ${this.auth.userInfo.access_token}`
      }
    });

    return next.handle(request);
  }
}