
import {of as observableOf, Observable} from 'rxjs';
/**
 * angular2-adal - Use Azure AD Library - ADAL in Angular 2
 * @version v0.1.4
 * @link https://github.com/alenny/angular2-adal#readme
 * @license MIT
 */
import {Injectable} from '@angular/core';
import {Router, NavigationStart } from '@angular/router';
import 'rxjs/Rx';
import 'rxjs/Observable'
import {AuthenticationContext, AdalConfig, AdalUser} from './adaljs';
import {OAuthData} from './oauthdata.model';


@Injectable()
export class AdalService {

    private adalContext: AuthenticationContext;
    private oauthData: OAuthData = {
        isAuthenticated: false,
        userName: '',
        loginError: '',
        profile: {}
    };

    public init(configOptions: AdalConfig) {
        if (!configOptions) {
            throw new Error('You must set config, when calling init.');
        }

        // redirect and logout_redirect are set to current location by default
        const existingHash = window.location.hash;
        let pathDefault = window.location.href;
        if (existingHash) {
            pathDefault = pathDefault.replace(existingHash, '');

            if (existingHash.startsWith('#error=access_denied')) {
                sessionStorage.setItem('errorlogin', 'true');
            }
        }

        configOptions.redirectUri = configOptions.redirectUri || pathDefault;
        configOptions.postLogoutRedirectUri = configOptions.postLogoutRedirectUri || pathDefault;

        // create instance with given config
        this.adalContext = new AuthenticationContext(configOptions);

        // router.events.filter(event => event instanceof NavigationStart)
                     // .subscribe(event => {
                           // this.handleLocationChange(event as NavigationStart)
                        // });

        // loginresource is used to set authenticated status
        this.updateDataFromCache(this.adalContext.config.loginResource);
    }

    public handleLocationChange(event: NavigationStart ) {
        this.adalContext.verbose('Location change event to ' + event.url);

        setInterval(() => {

                }, 4);
    }

    public get config(): AdalConfig {
        return this.adalContext.config;
    }

    public get userInfo(): OAuthData {
        return this.oauthData;
    }

    public login(): void {
        this.adalContext.login();
    }

    public loginInProgress(): boolean {
        return this.adalContext.loginInProgress();
    }

    public logOut(): void {
        this.adalContext.logOut();
        // let logoutWindow = window.open('https://login.microsoftonline.com/common/oauth2/logout', 'logoutWindow');
    }



    public handleWindowCallbackUrl(theUrl: string): Observable<boolean> {
        const hash = theUrl.substring(1);
        let isHash = false;
        if (this.adalContext.isCallback(hash)) {
            isHash = true;
            const requestInfo = this.adalContext.getRequestInfo(hash);
            this.adalContext.saveTokenFromHash(requestInfo);
            if (requestInfo.requestType === this.adalContext.REQUEST_TYPE.LOGIN) {
                this.updateDataFromCache(this.adalContext.config.loginResource);
            } else if (requestInfo.requestType === this.adalContext.REQUEST_TYPE.RENEW_TOKEN) {
                this.adalContext.callback = window.parent['callBackMappedToRenewStates'][requestInfo.stateResponse];
            }

            if (requestInfo.stateMatch) {
                if (typeof this.adalContext.callback === 'function') {
                    if (requestInfo.requestType === this.adalContext.REQUEST_TYPE.RENEW_TOKEN) {
                        // Idtoken or Accestoken can be renewed
                        if (requestInfo.parameters['access_token']) {
                            this.adalContext.callback(this.adalContext._getItem(this.adalContext.CONSTANTS.STORAGE.ERROR_DESCRIPTION)
                                , requestInfo.parameters['access_token']);
                        } else if (requestInfo.parameters['error']) {
                            this.adalContext.callback(this.adalContext._getItem(this.adalContext.CONSTANTS.STORAGE.ERROR_DESCRIPTION)
                              , null);
                            this.adalContext._renewFailed = true;
                        }
                    }
                }
            }
        } else {
            // No callback. App resumes after closing or moving to new page.
            // Check token and username
            this.updateDataFromCache(this.config.loginResource);
            if (!this.oauthData.isAuthenticated && this.oauthData.userName && !this.adalContext._renewActive) {
                // id_token is expired or not present
                this.acquireToken(this.config.loginResource).subscribe(token => {
                    if (token) {
                        this.oauthData.isAuthenticated = true;
                    }
                });
            }
        }

        return observableOf(isHash);
    }

    public getCachedToken(resource: string): string {
        return this.adalContext.getCachedToken(resource);
    }

    public acquireToken(resource: string): Observable<any> {
        return Observable.create(observer => {
            this.adalContext._renewActive = true;
            this.adalContext.acquireToken(resource, (error: string, tokenOut: string) => {
                this.adalContext._renewActive = false;
                if (error) {
                    this.adalContext.error('Error when acquiring token for resource ' + resource, error);
                    observer.next(null);
                } else {
                    observer.next(tokenOut);
                }
                observer.complete();
            });
        });
    }

    public getUser(): Observable<any> {
        return Observable.bindCallback(function (cb: (u: AdalUser) => void) {
            this.adalContext.getUser(function (error: string, user: AdalUser) {
                if (error) {
                    this.adalContext.error('Error when getting user', error);
                    cb(null);
                } else {
                    cb(user);
                }
            });
        })();
    }

    public clearCache(): void {
        this.adalContext.clearCache();
    }

    public clearCacheForResource(resource: string): void {
        this.adalContext.clearCacheForResource(resource);
    }

    public info(message: string): void {
        this.adalContext.info(message);
    }

    public verbose(message: string): void {
        this.adalContext.verbose(message);
    }

    public GetResourceForEndpoint(url: string): string {
        return this.adalContext.getResourceForEndpoint(url);
    }

    private updateDataFromCache(resource: string): void {
        const token = this.adalContext.getCachedToken(resource);
        this.oauthData.isAuthenticated = token !== null && token.length > 0;
        const user = this.adalContext.getCachedUser();
        if (user) {
            this.oauthData.userName = user.userName;
            this.oauthData.profile = user.profile;
            this.oauthData.loginError = this.adalContext.getLoginError();
        } else {
            this.oauthData.userName = '';
            this.oauthData.profile = {};
            this.oauthData.loginError = '';
        }
    };
}


