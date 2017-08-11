import { Component } from '@angular/core';

import {QiBoundaryType, QiRestService} from '../qi.rest.service'
import {QiType, QiStream, QiTypeProperty, QiTypeCode, QiStreamBehavior, QiStreamMode} from '../qi.rest.service'

const streamId = 'WaveDataStream';
const typeId = 'WaveDataType';
const behaviorId = 'SampleBehavior';

class  WaveData {
  Order: number;
  Radians: number;
  Tau: number;
  Sin: number;
  Cos: number;
  Tan: number;
  Sinh: number;
  Cosh: number;
  Tanh: number
}

@Component({
  selector: 'app-datasrc',
  templateUrl: './datasrc.component.html',
  styleUrls: ['./datasrc.component.css']
})
export class DatasrcComponent {
  stream: QiStream;
  events: WaveData[];
  hasEvents: boolean;

  button1Message: string;
  button2Message: string;
  button3Message: string;
  button4Message: string;
  button5Message: string;
  button6Message: string;

  constructor(private qiService: QiRestService) {
    this.hasEvents = false;
  }

  buildWaveDataType() {
    const doubleType = new QiType();
    doubleType.Id = 'doubleType';
    doubleType.QiTypeCode = QiTypeCode.Double;

    const intType = new QiType();
    intType.Id = 'intType';
    intType.QiTypeCode = QiTypeCode.Int32;

    const orderProperty = new QiTypeProperty();
    orderProperty.Id = 'Order';
    orderProperty.QiType = intType;
    orderProperty.IsKey = true;

    const radiansProperty = new QiTypeProperty();
    radiansProperty.Id = 'Radians';
    radiansProperty.QiType = doubleType;

    const tauProperty = new QiTypeProperty();
    tauProperty.Id = 'Tau';
    tauProperty.QiType = doubleType;

    const sinProperty = new QiTypeProperty();
    sinProperty.Id = 'Sin';
    sinProperty.QiType = doubleType;

    const cosProperty = new QiTypeProperty();
    cosProperty.Id = 'Cos';
    cosProperty.QiType = doubleType;

    const tanProperty = new QiTypeProperty();
    tanProperty.Id = 'Tan';
    tanProperty.QiType = doubleType;

    const sinhProperty = new QiTypeProperty();
    sinhProperty.Id = 'Sinh';
    sinhProperty.QiType = doubleType;

    const coshProperty = new QiTypeProperty();
    coshProperty.Id = 'Cosh';
    coshProperty.QiType = doubleType;

    const tanhProperty = new QiTypeProperty();
    tanhProperty.Id = 'Tanh';
    tanhProperty.QiType = doubleType;

    const waveDataType = new QiType();
    waveDataType.Id = typeId;
    waveDataType.Name = 'WaveDataType_AngularSample';
    waveDataType.Description = 'This is a sample QiType for storing WaveData events';
    waveDataType.Properties = [orderProperty, radiansProperty, tauProperty, sinProperty,
      cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty];
    waveDataType.QiTypeCode = QiTypeCode.Empty;

    return waveDataType;
  }

  newWaveDataEvent(order: number, range: number, multiplier: number) {
    const radians = order / range * 2 * Math.PI;

    const waveData = new WaveData();
    waveData.Order = order;
    waveData.Radians = radians;
    waveData.Tau = radians / (2 * Math.PI);
    waveData.Sin = multiplier * Math.sin(radians);
    waveData.Cos = multiplier * Math.cos(radians);
    waveData.Tan = multiplier * Math.tan(radians);
    waveData.Sinh = multiplier * Math.sinh(radians);
    waveData.Cosh = multiplier * Math.cosh(radians);
    waveData.Tanh = multiplier * Math.tanh(radians);

    return waveData;
  }

  createType() {
    const type = this.buildWaveDataType();
    this.qiService.createType(type).subscribe(res => {
      this.button1Message = res.status;
    },
    err => {
      this.button1Message = err;
    });
  }

  createStream() {
    this.stream = new QiStream();
    this.stream.Id = streamId;
    this.stream.TypeId = typeId;
    this.qiService.createStream(this.stream)
      .subscribe(res => {
      this.button2Message = res.status;
    },
      err => {
        this.button2Message = err;
      });;
  }

  createBehaviorAndUpdateStream() {
    const behavior = new QiStreamBehavior();
    behavior.Id = behaviorId;
    behavior.Name = 'SampleBehavior';
    behavior.Mode = QiStreamMode.Discrete;
    this.qiService.createBehavior(behavior).subscribe(() => {
      this.stream.BehaviorId = behaviorId;
      this.qiService.updateStream(this.stream).subscribe(res => {
        this.button5Message = res.status;
      },
      err => {
        this.button5Message = err;
      });
    })
  }

  writeWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 2; i < 200; i += 2) {
      list.push(this.newWaveDataEvent(i, 2, 3));
    }

    this.qiService.insertValues(streamId, list).subscribe(res => {
      this.button3Message = res.status;
    },
    err => {
      this.button3Message = err;
    });
  }

  retrieveWaveDataEvents() {
    this.hasEvents = false;
    this.qiService.getRangeValues(streamId, '3', 50, QiBoundaryType.ExactOrCalculated)
      .map(res => res.json())
      .subscribe(res => {
        this.events = res as WaveData[];
        this.hasEvents = true;
        this.button4Message = `Found ${this.events.length} events`
      },
      err => {
        this.button4Message = err;
      });
  }

  cleanup() {
    this.qiService.deleteStream(streamId).subscribe(() => {
      // you can't delete a type/behavior if there are existing streams
      // that depend on it, so we must make sure the stream is deleted first.
      this.qiService.deleteType(typeId).subscribe()
      this.qiService.deleteBehavior(behaviorId).subscribe();
    });
    this.hasEvents = false;
  }
}
