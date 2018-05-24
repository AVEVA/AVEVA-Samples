import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/Rx';

import { AuthHttp } from './adal/authHttp.service';
import { ConfigurationService } from './osiconfiguration.service';
import {HttpHeaders} from "@angular/common/http";


export class QiStream {
  Id: string;
  Name: string;
  Description: string;
  TypeId: string;
  BehaviorId: string;
}

export class QiType {
  Id: string;
  Name: string;
  Description: string;
  QiTypeCode: QiTypeCode;
  Properties: QiTypeProperty[];
}

export enum QiTypeCode {
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

export enum QiStreamMode {
  Continuous = 0,
  StepWiseContinuousLeading = 1,
  StepwiseContinuousTrailing = 2,
  Discrete = 3
}

export class QiStreamBehavior {
  Id: string;
  Name: string;
  Mode: QiStreamMode;
}


export class QiTypeProperty {
  Id: string;
  Name: string;
  Description: string;
  QiType: QiType;
  IsKey: boolean;
}

export enum QiBoundaryType {
  Exact = 0,
  Inside = 1,
  Outside = 2,
  ExactOrCalculated = 3
}

export class QiView {
  Id: string;
  Name: string;
  Description: string;
  SourceTypeId: string;
  TargetTypeId: string;
  Properties: QiViewProperty[];
}

export class QiViewProperty {
  SourceId: string;
  TargetId: string;
  QiView: QiView;
}

export class QiViewMap {
  SourceTypeId: string;
  TargetTypeId: string;
  Properties: QiViewProperty[];
}

@Injectable()
export class QiRestService {
  qiUrl: string;
  qiResource: string;
  tenantId: string;
  namespaceId: string;

  constructor(private authHttp: AuthHttp,
              private configService: ConfigurationService
              ) {
    this.qiUrl = configService.AmbientConfiguration.QiEndPoint;
    this.qiResource = configService.AmbientConfiguration.QiResourceURI;
    this.tenantId = configService.AmbientConfiguration.TenantId;
    this.namespaceId = configService.AmbientConfiguration.NamespaceId;
  }

  createStream(qiStream: QiStream): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${qiStream.Id}`;
    return this.authHttp.post(url, JSON.stringify(qiStream).toString());
  }

  updateStream(qiStream: QiStream): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${qiStream.Id}`;
    return this.authHttp.put(url, JSON.stringify(qiStream).toString());
  }

  getStreams(query: string): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams?query=${query}`;
    return this.authHttp.get(url);
  }


  deleteStream(streamId: string): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}`;
    return this.authHttp.delete(url);
  }

  createTags(streamId: string, tags: string[]): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Tags`;
    return this.authHttp.put(url, JSON.stringify(tags).toString());
  }

  createMetadata(streamId: string, metadata: object): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Metadata`;
    return this.authHttp.put(url, JSON.stringify(metadata).toString());
  }

  getTags(streamId: string): Observable<any> {
    const url = this.qiUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Tags`;
    return this.authHttp.get(url);
  }

  getMetadata(streamId: string): Observable<any> {
    const url = this.qiUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` + `/Metadata`;
    return this.authHttp.get(url);
  }

  getLastValue(streamId: string): Observable<any> {
    const url = this.qiUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/GetlastValue`;
    return this.authHttp.get(url);
  }

  getRangeValues(streamId: string, start, count, boundary: QiBoundaryType, viewId: string = ''): Observable<any> {
    const url = this.qiUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/GetRangeValues?startIndex=${start}&count=${count}&boundaryType=${boundary}&viewId=${viewId}`;
    return this.authHttp.get(url, {observe: 'response', headers: new HttpHeaders().set('Cache-Control','no-cache')});
  }

  createType(qiType: QiType): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${qiType.Id}`;
    return this.authHttp.post(url, JSON.stringify(qiType).toString());
  }

  deleteType(typeId: string): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${typeId}`;
    return this.authHttp.delete(url);
  }

  insertValue(streamId: string, event: any) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValue`;
    return this.authHttp.post(url, JSON.stringify(event).toString());
  }

  insertValues(streamId: string, events: Array<any>) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValues`;
    return this.authHttp.post(url, JSON.stringify(events).toString());
  }

  updateValue(streamId: string, event: any) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValue`;
    return this.authHttp.put(url, JSON.stringify(event).toString());
  }

  updateValues(streamId: string, events: Array<any>) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValues`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
  }

  replaceValue(streamId: string, event: any) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValue`;
    return this.authHttp.put(url, JSON.stringify(event).toString());
  }

  replaceValues(streamId: string, events: Array<any>) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValues`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
  }

  createBehavior(behavior: QiStreamBehavior) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Behaviors/${behavior.Id}`;
    return this.authHttp.post(url, JSON.stringify(behavior).toString());
  }

  deleteBehavior(behaviorId: string) {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Behaviors/${behaviorId}`;
    return this.authHttp.delete(url);
  }

  createView(qiView: QiView): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Views/${qiView.Id}`;
    return this.authHttp.post(url, JSON.stringify(qiView).toString());
  }

  deleteView(viewId: string): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Views/${viewId}`;
    return this.authHttp.delete(url);
  }

  getViewMap(viewId: string): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Views/${viewId}/Map`;
    return this.authHttp.get(url);
  }

  deleteValue(streamId: string, index): Observable<any> {
    const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
    return this.authHttp.delete(url);
  }

  deleteWindowValues(streamId: string, start, end):Observable<any> {
    const url = this.qiUrl +
      `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
    return this.authHttp.delete(url);
  }
}
