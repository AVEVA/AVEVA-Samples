// app.routing.ts
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

import {ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DatasrcComponent} from './datasrc/datasrc.component';

const routes: Routes = [{ path: 'datasrc', component: DatasrcComponent },
                        {
                            path: '',
                            redirectTo: '/datasrc',
                            pathMatch: 'full'
                        }
                       ];

export const appRoutingProviders: any[] = [];

// Export routes
export const routing: ModuleWithProviders = RouterModule.forRoot(routes);
