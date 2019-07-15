// sds.rest.service.ts
//

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import 'rxjs/Rx';
import {HttpHeaders, HttpClient} from "@angular/common/http";
import sdsConfig from '../config/sdsconfig.json';
import { SdsConfig } from '../config/sdsconfig.js';


export class SdsStream {
  Id: string;
  Name: string;
  Description: string;
  TypeId: string;
  PropertyOverrides: SdsStreamPropertyOverride[];
  Indexes: SdsStreamIndex[];
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

export class SdsStreamIndex {
  SdsTypePropertyId: string;
}


export class SdsTypeProperty {
  Id: string;
  Name: string;
  Description: string;
  SdsType: SdsType;
  IsKey: boolean;
  Order: number;
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
  tenantId: string;
  namespaceId: string;
  apiVersion: string;
  options: any

  constructor(private authHttp: HttpClient) {
    const config = sdsConfig as SdsConfig;
    this.sdsUrl = config.serviceBaseUri;
    this.tenantId = config.tenantId;
    this.namespaceId = config.namespaceId;
    this.apiVersion = config.apiVersion;
    this.options = {
      observe: 'response',
      headers: new HttpHeaders({
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Accept': 'applications/json'
      })
    };
  }

  createStream(sdsStream: SdsStream): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${sdsStream.Id}`;
    return this.authHttp.post(url, JSON.stringify(sdsStream).toString(), this.options);
  }

  updateStream(sdsStream: SdsStream): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${sdsStream.Id}`;
    return this.authHttp.put(url, JSON.stringify(sdsStream).toString(), this.options);
  }

  getStream(streamId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}`;
    return this.authHttp.get(url, this.options);
  }


  getStreams(query: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams?query=${query}`;
    return this.authHttp.get(url, this.options);
  }


  deleteStream(streamId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}`;
    return this.authHttp.delete(url, this.options);
  }

  createTags(streamId: string, tags: string[]): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Tags`;
    return this.authHttp.put(url, JSON.stringify(tags).toString(), this.options);
  }

  createMetadata(streamId: string, metadata: object): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Metadata`;
    return this.authHttp.put(url, JSON.stringify(metadata).toString(), this.options);
  }

  getTags(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Tags`;
    return this.authHttp.get(url, this.options);
  }

  getMetadata(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Metadata`;
    return this.authHttp.get(url, this.options);
  }

  getLastValue(streamId: string): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Last`;
    return this.authHttp.get(url, this.options);
  }

  getWindowValues (streamId: string, start, end, filter: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data?startIndex=${start}&endIndex=${end}&filter=${filter}`;
    return this.authHttp.get(url, this.options);
  }

  getSampledValues (streamId: string, start, end, intervals, sampleBy, filter: string = '', streamViewId=''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Sampled?startIndex=${start}&endIndex=${end}&intervals=${intervals}&sampleBy=${sampleBy}&filter=${filter}&streamViewId=${streamViewId}`;
    return this.authHttp.get(url, this.options);
  }

  getWindowValuesInterpolated (streamId: string, start, end, count: number): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Transform/Interpolated?startIndex=${start}&endIndex=${end}&count=${count}`;
    return this.authHttp.get(url, this.options);
  }

  getRangeValues(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Transform?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}`;
    return this.authHttp.get(url, this.options);
  }

  getRangeValuesHeaders(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Transform?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}&form=tableh`;
    return this.authHttp.get(url, this.options);
  }

  getTypes(skip: number, count: number, query: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types?skip=${skip}&count=${count}&query=${query}`;
    return this.authHttp.get(url, this.options);
  }

  createType(sdsType: SdsType): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${sdsType.Id}`;
    return this.authHttp.post(url, sdsType, this.options);
  }
  
  updateStreamType(streamId: string, streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Type?streamViewId=${streamViewId}`;
    return this.authHttp.put(url, '', this.options);
  }

  deleteType(typeId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${typeId}`;
    return this.authHttp.delete(url, this.options);
  }

  insertValues(streamId: string, events: Array<any>): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data`;
    return this.authHttp.post(url, JSON.stringify(events).toString(),this.options);
  }

  updateValues(streamId: string, events: Array<any>): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data`;
    return this.authHttp.put(url, JSON.stringify(events).toString(), this.options);
  }

  replaceValues(streamId: string, events: Array<any>): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data?allowCreate=false`;
    return this.authHttp.put(url, JSON.stringify(events).toString(), this.options);
  }

  createStreamView(sdsStreamView: SdsStreamView): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${sdsStreamView.Id}`;
    return this.authHttp.post(url, JSON.stringify(sdsStreamView).toString(), this.options);
  }

  deleteStreamView(streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}`;
    return this.authHttp.delete(url, this.options);
  }

  getStreamViewMap(streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}/Map`;
    return this.authHttp.get(url, this.options);
  }

  deleteValue(streamId: string, index): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data?index=${index}`;
    return this.authHttp.delete(url, this.options);
  }

  deleteWindowValues(streamId: string, start, end): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data?startIndex=${start}&endIndex=${end}`;
    return this.authHttp.delete(url, this.options);
  }
}
