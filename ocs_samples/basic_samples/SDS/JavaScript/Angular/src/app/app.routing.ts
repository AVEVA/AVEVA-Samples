// app.routing.ts
//

import {ModuleWithProviders, Provider } from '@angular/core';
import { Routes, RouterModule, PreloadAllModules } from '@angular/router';

import { DatasrcComponent} from './datasrc/datasrc.component';
import { OAuthLoginComponent, OAuthLogoutComponent, OAuthCallbackHandlerGuard } from '../app/libraries/auth/ocs-auth';
import {AuthenticationGuard} from 'app/libraries/auth/extra/authguard'

const routes: Routes = [
    {
        path: 'login',
        component: DatasrcComponent,
    },
    {
        path: 'logout',
        component: OAuthLogoutComponent
    },
    {
        path: 'auth-callback',
        component: OAuthLoginComponent,
        canActivate: [OAuthCallbackHandlerGuard]
    },
    {
        path: '',
        component: DatasrcComponent,
        canActivate: [AuthenticationGuard]
    },
    {
        path: '**',
        redirectTo: ''
    }
];

export const appRoutingProviders: Provider[] = [];

// Export routes
export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {preloadingStrategy: PreloadAllModules});
