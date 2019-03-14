import { Injectable } from "@angular/core";
import { CanActivate, RouterStateSnapshot, ActivatedRouteSnapshot } from "@angular/router";
import { Observable } from "rxjs";
import { OidcService } from "@osisoft/identity-ts";

@Injectable()
export class AuthenticationGuard implements CanActivate {
    constructor(private auth: OidcService) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        return (this.auth.userInfo !== null);
    }
}