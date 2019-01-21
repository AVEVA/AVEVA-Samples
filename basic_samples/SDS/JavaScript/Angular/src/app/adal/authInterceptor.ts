// authInterceptor.ts
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
