
import {timeout} from 'rxjs/operators';
import { Injectable } from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest} from '@angular/common/http';

import { Observable } from 'rxjs';
import {AdalService} from "./adal.service";

/** Append ADAL Authentication Headers to Outbound Requests */
@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor(private adalService: AdalService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const resource = this.adalService.GetResourceForEndpoint(req.url);

        if (resource) {
            if (this.adalService.userInfo.isAuthenticated) {
                let tokenStored = this.adalService.getCachedToken(resource);

                if (!tokenStored) {

                    return this.adalService.acquireToken(resource).mergeMap((token: string) => {
                        tokenStored = token;
                        if (!req.headers.has('Authorization')) {
                            req = req.clone({
                                setHeaders: {
                                    'Authorization': `Bearer ${tokenStored}`
                                }
                            });
                        }

                        return next.handle(req);
                    });
                    
                } else {
                    if (!req.headers.has('Authorization')) {
                        req = req.clone({
                            setHeaders: {
                                'Authorization': `Bearer ${tokenStored}`
                            }
                        });
                    }

                    return next.handle(req);
                }
            } else {
                return Observable.throwError('User not authenticated');
            }
        } else {
           return Observable.throwError(`ADAL resource for endpoint ${req.url} is null or undefined`);
        }

    }
}