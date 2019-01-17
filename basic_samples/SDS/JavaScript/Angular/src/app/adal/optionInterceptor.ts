// optionInterceptor.ts
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
