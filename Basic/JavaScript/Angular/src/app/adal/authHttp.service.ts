/**
 * ng2-adal - Use Azure AD Library - ADAL in Angular 2
 * @version v0.1.0
 * @link https://github.com/sureshchahal/angular2-adal#readme
 * @license MIT
 */
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';

import {HttpClient, HttpHeaders, HttpParams, HttpResponse} from "@angular/common/http";

type HttpClientOptions = {
    headers?: HttpHeaders,
    observe: 'response',
    params?: HttpParams,
    reportProgress?: boolean,
    responseType?: 'json',
    withCredentials?: boolean,
}

@Injectable()
export class AuthHttp {
    constructor
    (
        private http: HttpClient,
    ) {
    }

    private coerceObserve(options: HttpClientOptions) {
        if (!options) {
            options = {
                observe: 'response'
            } as HttpClientOptions
        }

        return options;
    }

    head (url: string, options?: HttpClientOptions): Observable<HttpResponse<Object>> {
        return this.http.head(url, this.coerceObserve(options));
    }

    get(url: string, options?: HttpClientOptions): Observable<HttpResponse<Object>> {
        return this.http.get(url, this.coerceObserve(options));
    }

    delete(url: string, options?: HttpClientOptions) : Observable<HttpResponse<Object>> {
        return this.http.delete(url, this.coerceObserve(options));
    }

    post(url: string, body: any, options?: HttpClientOptions ): Observable<HttpResponse<Object>> {
        return this.http.post(url, body, this.coerceObserve(options));
    }

    patch(url: string, body: any, options?: HttpClientOptions): Observable<HttpResponse<Object>> {
        return this.http.patch(url, body, this.coerceObserve(options));
    }

    put (url: string, body: any, options?: HttpClientOptions): Observable<HttpResponse<Object>> {
        return this.http.put(url, body, this.coerceObserve(options));
    }

}
