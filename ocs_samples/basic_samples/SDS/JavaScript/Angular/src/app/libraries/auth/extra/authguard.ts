// authguard.ts
//

import { Injectable } from "@angular/core";
import { CanActivate, RouterStateSnapshot, ActivatedRouteSnapshot } from "@angular/router";
import { OidcService } from '../ocs-auth'

@Injectable()
export class AuthenticationGuard implements CanActivate {
    constructor(private auth: OidcService) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        return (this.auth.userInfo !== null);
    }
}