import { Injectable } from '@angular/core';
import { AdalConfig } from './adal/adaljs'


export interface ISdsConfigSet {
  ClientID: string;
  SdsEndPoint: string;
  SdsResourceURI: string;
  TenantId: string;
  NamespaceId: string;
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
