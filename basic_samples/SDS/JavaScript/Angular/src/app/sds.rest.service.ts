// sds.rest.service.ts
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
import { Observable } from 'rxjs';
import 'rxjs/Rx';

import { AuthHttp } from './adal/authHttp.service';
import { ConfigurationService } from './osiconfiguration.service';
import {HttpHeaders} from "@angular/common/http";


export class SdsStream {
  Id: string;
  Name: string;
  Description: string;
  TypeId: string;
  PropertyOverrides: SdsStreamPropertyOverride[];
}

export class SdsType {
  Id: string;
  Name: string;
  Description: string;
  SdsTypeCode: SdsTypeCode;
  Properties: SdsTypeProperty[];
}

export enum SdsTypeCode {
  Empty = 0,
  Object = 1,
  DBNull = 2,
  Boolean = 3,
  Char = 4,
  SByte = 5,
  Byte = 6,
  Int16 = 7,
  UInt16 = 8,
  Int32 = 9,
  UInt32 = 10,
  Int64 = 11,
  UInt64 = 12,
  Single = 13,
  Double = 14,
  Decimal = 15,
  DateTime = 16,
  String = 18,
  Guid = 19,
  DateTimeOffset = 20,
  TimeSpan = 21,
  Version = 22
}

export enum SdsStreamMode {
  Continuous = 0,
  StepWiseContinuousLeading = 1,
  StepwiseContinuousTrailing = 2,
  Discrete = 3
}

export class SdsStreamPropertyOverride {
  SdsTypePropertyId: string;
  Uom: string;
  InterpolationMode: SdsStreamMode;
}


export class SdsTypeProperty {
  Id: string;
  Name: string;
  Description: string;
  SdsType: SdsType;
  IsKey: boolean;
}

export enum SdsBoundaryType {
  Exact = 0,
  Inside = 1,
  Outside = 2,
  ExactOrCalculated = 3
}

export class SdsStreamView {
  Id: string;
  Name: string;
  Description: string;
  SourceTypeId: string;
  TargetTypeId: string;
  Properties: SdsStreamViewProperty[];
}

export class SdsStreamViewProperty {
  SourceId: string;
  TargetId: string;
  SdsStreamView: SdsStreamView;
}

export class SdsStreamViewMap {
  SourceTypeId: string;
  TargetTypeId: string;
  Properties: SdsStreamViewProperty[];
}

@Injectable()
export class SdsRestService {
  sdsUrl: string;
  sdsResource: string;
  tenantId: string;
  namespaceId: string;

  constructor(private authHttp: AuthHttp,
              private configService: ConfigurationService
              ) {
    this.sdsUrl = configService.AmbientConfiguration.SdsEndPoint;
    this.sdsResource = configService.AmbientConfiguration.SdsResourceURI;
    this.tenantId = configService.AmbientConfiguration.TenantId;
    this.namespaceId = configService.AmbientConfiguration.NamespaceId;
  }

  createStream(sdsStream: SdsStream): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${sdsStream.Id}`;
    return this.authHttp.post(url, JSON.stringify(sdsStream).toString());
  }

  updateStream(sdsStream: SdsStream): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${sdsStream.Id}`;
    return this.authHttp.put(url, JSON.stringify(sdsStream).toString());
  }

  getStreams(query: string): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams?query=${query}`;
    return this.authHttp.get(url);
  }


  deleteStream(streamId: string): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}`;
    return this.authHttp.delete(url);
  }

  createTags(streamId: string, tags: string[]): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Tags`;
    return this.authHttp.put(url, JSON.stringify(tags).toString());
  }

  createMetadata(streamId: string, metadata: object): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Metadata`;
    return this.authHttp.put(url, JSON.stringify(metadata).toString());
  }

  getTags(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Tags`;
    return this.authHttp.get(url);
  }

  getMetadata(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Metadata`;
    return this.authHttp.get(url);
  }

  getLastValue(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/GetlastValue`;
    return this.authHttp.get(url);
  }

  getRangeValues(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/GetRangeValues?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}`;
    return this.authHttp.get(url, {observe: 'response', headers: new HttpHeaders().set('Cache-Control','no-cache')});
  }

  createType(sdsType: SdsType): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${sdsType.Id}`;
    return this.authHttp.post(url, JSON.stringify(sdsType).toString());
  }

  deleteType(typeId: string): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${typeId}`;
    return this.authHttp.delete(url);
  }

  insertValue(streamId: string, event: any) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValue`;
    return this.authHttp.post(url, JSON.stringify(event).toString());
  }

  insertValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValues`;
    return this.authHttp.post(url, JSON.stringify(events).toString());
  }

  updateValue(streamId: string, event: any) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValue`;
    return this.authHttp.put(url, JSON.stringify(event).toString());
  }

  updateValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValues`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
  }

  replaceValue(streamId: string, event: any) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValue`;
    return this.authHttp.put(url, JSON.stringify(event).toString());
  }

  replaceValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValues`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
  }

  createStreamView(sdsStreamView: SdsStreamView): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${sdsStreamView.Id}`;
    return this.authHttp.post(url, JSON.stringify(sdsStreamView).toString());
  }

  deleteStreamView(streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}`;
    return this.authHttp.delete(url);
  }

  getStreamViewMap(streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}/Map`;
    return this.authHttp.get(url);
  }

  deleteValue(streamId: string, index): Observable<any> {
    const url = this.sdsUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
    return this.authHttp.delete(url);
  }

  deleteWindowValues(streamId: string, start, end):Observable<any> {
    const url = this.sdsUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
    return this.authHttp.delete(url);
  }
}
