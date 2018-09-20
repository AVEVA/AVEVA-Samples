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