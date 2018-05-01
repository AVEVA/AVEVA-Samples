import { Injectable } from '@angular/core';
import { AdalConfig } from './adal/adaljs'


export interface IQiConfigSet {
  ClientID: string;
  QiEndPoint: string;
  QiResourceURI: string;
  TenantId: string;
  NamespaceId: string;
}


@Injectable()
export class ConfigurationService {

  private ambientConfiguration: IQiConfigSet = null;


  public get AmbientConfiguration(): IQiConfigSet {
        return this.ambientConfiguration;
    }

  public set  AmbientConfiguration(subscription: IQiConfigSet){
    this.ambientConfiguration = subscription;
  }

  public get adalConfig(): AdalConfig {

    const config: IQiConfigSet = this.ambientConfiguration;

    return {
         tenant: 'common',
         clientId: config.ClientID,
         endpoints: [ { endpointURL: config.QiEndPoint, endpointResourceURI : config.QiResourceURI },
                    ],

         redirectUri: window.location.origin + '/',
         postLogoutRedirectUri: window.location.origin + '/'
      }
    }

  }
