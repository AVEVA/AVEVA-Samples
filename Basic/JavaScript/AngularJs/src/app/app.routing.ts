import {ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';



import { DatasrcComponent} from './datasrc/datasrc.component';
// import { DisplayComponent} from './savedisplay/display.component';

const routes: Routes = [{ path: 'datasrc', component: DatasrcComponent },
                        // { path: 'display', component: DisplayComponent },
                        {
                            path: '',
                            redirectTo: '/datasrc',
                            pathMatch: 'full'
                        }
                       ];



export const appRoutingProviders: any[] = [];

// Export routes
export const routing : ModuleWithProviders = RouterModule.forRoot(routes);
