// optionInterceptor.ts
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

import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';

import {Observable} from 'rxjs';

/** Set Accept and Content-Type header defaults if none provided */
@Injectable()
export class OptionInterceptor implements HttpInterceptor {

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        if (!req.headers.has('Accept')) {
            req = req.clone({
                setHeaders: {
                    'Accept': 'application/json'
                }
            });
        }

        switch (req.method.toLowerCase()) {
            case 'post':
            case 'patch':
            case 'put':
                if (!req.headers.has('Content-Type')) {
                    req = req.clone({
                       setHeaders: {
                           'Content-Type': 'application/json'
                       }
                    });
                }
                break;
            default:
                break;
        }
        return next.handle(req);
    }
}
