// osiconfiguration.service.ts
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

import { Injectable } from '@angular/core';
import { AdalConfig } from './adal/adaljs'


export interface ISdsConfigSet {
  ClientID: string;
  SdsEndPoint: string;
  SdsResourceURI: string;
  TenantId: string;
  NamespaceId: string;
  ApiVersion: string;
}


@Injectable()
export class ConfigurationService {

  private ambientConfiguration: ISdsConfigSet = null;


  public get AmbientConfiguration(): ISdsConfigSet {
        return this.ambientConfiguration;
    }

  public set  AmbientConfiguration(subscription: ISdsConfigSet){
    this.ambientConfiguration = subscription;
  }

  public get adalConfig(): AdalConfig {

    const config: ISdsConfigSet = this.ambientConfiguration;

    return {
         tenant: 'common',
         clientId: config.ClientID,
         endpoints: [ { endpointURL: config.SdsEndPoint, endpointResourceURI : config.SdsResourceURI },
                    ],

         redirectUri: window.location.origin + '/',
         postLogoutRedirectUri: window.location.origin + '/'
      }
    }

  }
