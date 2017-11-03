/**
 * ng2-adal - Use Azure AD Library - ADAL in Angular 2
 * @version v0.1.0
 * @link https://github.com/sureshchahal/angular2-adal#readme
 * @license MIT
 */
import {Injectable} from '@angular/core';
import {Http, Response, Headers, RequestOptionsArgs, RequestOptions, RequestMethod, URLSearchParams} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';

import {AdalService} from './adal.service';

@Injectable()
export class AuthHttp {
    constructor
    (
        private http: Http,
        private adalService: AdalService
    ) {
    }

    get(url: string, options?: RequestOptionsArgs): Observable<any> {
        const acceptheader = new Headers({ 'Accept': 'application/json;q=0.9' });
        let options1 = new RequestOptions({ method: RequestMethod.Get, headers: acceptheader });
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }

    post(url: string, body: any, options?: RequestOptionsArgs): Observable<any> {

        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        let options1 = new RequestOptions({ method: RequestMethod.Post, headers: headers });

        if (body != null) {
            options1.body = body;
        }
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }

    delete(url: string, options?: RequestOptionsArgs): Observable<any> {
        const acceptheader = new Headers({'Accept': 'application/json'});
        let options1 = new RequestOptions({ method: RequestMethod.Delete, headers: acceptheader });
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }


    patch(url: string, body: any, options?: RequestOptionsArgs): Observable<any> {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        let options1 = new RequestOptions({ method: RequestMethod.Patch, headers: headers });

        if (body != null) {
            options1.body = body;
        }
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }

    put(url: string, body: any, options?: RequestOptionsArgs): Observable<any> {

        const headers = new Headers();
        headers.append('Content-Type', 'application/json');

        let options1 = new RequestOptions({ method: RequestMethod.Put, headers: headers });

        if (body != null) {
          options1.body = body;
        }
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }

    head(url: string, options?: RequestOptionsArgs): Observable<any> {
        let options1 = new RequestOptions({ method: RequestMethod.Put });
        options1 = options1.merge(options);
        return this.sendRequest(url, options1);
    }

    private sendRequest(url: string, options: RequestOptionsArgs): Observable<any> {
        const options1 = new RequestOptions();
        options1.method = options.method;

        if (options.search != null) {
            options1.search = new URLSearchParams(options.search.toString()).clone();
        }
        if (options.body != null) {
            options1.body = options.body ;
        }


        if (options.headers != null) {
            options1.headers = new Headers(options.headers.toJSON());
        }

        const resource = this.adalService.GetResourceForEndpoint(url);
        let authenticatedCall: Observable<any>;

         if (resource) {
             if (this.adalService.userInfo.isAuthenticated) {

                const tokenstored = this.adalService.getCachedToken(resource);
                if (tokenstored) {
                    if (options1.headers == null) {
                            options1.headers = new Headers();
                    }

                    options1.headers.append('Authorization', 'Bearer ' + tokenstored);
                        return this.http.request(url, options1)
                            .catch(this.handleError);
                } else {
                    authenticatedCall = this.adalService.acquireToken(resource)
                                                        .flatMap( (token: string) => {
                                                                    console.log(token);

                                                                    if (options1.headers == null) {
                                                                        options1.headers = new Headers();
                                                                    }

                                                                    options1.headers.append('Authorization', 'Bearer ' + token);
                                                                    return this.http.request(url, options1).catch(this.handleError);
                                                            });
                }
             } else {
                authenticatedCall =  Observable.throw(new Error('User Not Authenticated.'));
             }
        } else {
            authenticatedCall = this.http.request(url, options).map(this.extractData).catch(this.handleError);
        }

        return authenticatedCall;
    }

    private extractData(res: Response) {
        if (res.status < 200 || res.status >= 300) {
            throw new Error('Bad response status: ' + res.status);
        }

        let body = {};
        // if there is some content, parse it
        if (res.status !== 204 ) {
            body = res.json();
        }

        return body || {};
    }

    private handleError(error: any) {
        // debugger;
        // In a real world app, we might send the error to remote logging infrastructure
        const errMsg = error.message || 'Server error';
        console.error(JSON.stringify(error)); // log to console instead

        return Observable.throw(error);
    }
}
