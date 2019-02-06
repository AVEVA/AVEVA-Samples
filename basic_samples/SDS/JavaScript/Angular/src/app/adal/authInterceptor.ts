// authInterceptor.ts
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
