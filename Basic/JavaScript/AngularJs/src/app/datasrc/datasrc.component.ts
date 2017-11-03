import { Component } from '@angular/core';

import {QiBoundaryType, QiRestService} from '../qi.rest.service'
import {QiType, QiStream, QiTypeProperty, QiTypeCode, QiStreamBehavior, QiStreamMode, QiView, QiViewProperty, QiViewMap} from '../qi.rest.service'

const streamId = 'WaveDataStream';
const typeId = 'WaveDataType';
const targetTypeId = "WaveDataTargetType"
const targetIntTypeId = "WaveDataTargetIntType"
const autoViewId = "WaveDataAutoView"
const manualViewId = "WaveDataManualView"
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

class  WaveDataTarget {
  OrderTarget: number;
  RadiansTarget: number;
  TauTarget: number;
  SinTarget: number;
  CosTarget: number;
  TanTarget: number;
  SinhTarget: number;
  CoshTarget: number;
  TanhTarget: number
}

class  WaveDataInteger {
  OrderTarget: number;
  SinInt: number;
  CosInt: number;
  TanInt: number;
}

@Component({
  selector: 'app-datasrc',
  templateUrl: './datasrc.component.html',
  styleUrls: ['./datasrc.component.css']
})
export class DatasrcComponent {
  stream: QiStream;
  events: WaveData[];
  targetEvents: WaveDataTarget[];
  integerEvents: WaveDataInteger[];
  viewMap: QiViewMap;
  hasEvents: boolean;
  hasView1Events: boolean;
  hasView2Events: boolean;
  hasMapProperties: boolean;

  button1Message: string;
  button2Message: string;
  button3Message: string;
  button4Message: string;
  button5Message: string;
  button6Message: string;
  button7Message: string;
  button8Message: string;
  button9Message: string;
  button10Message: string;
  button11Message: string;
  button12Message: string;
  button13Message: string;
  button14Message: string;
  button15Message: string;

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
    waveDataType.QiTypeCode = QiTypeCode.Object;

    return waveDataType;
  }

  buildWaveDataTargetType() {
    const doubleType = new QiType();
    doubleType.Id = 'doubleType';
    doubleType.QiTypeCode = QiTypeCode.Double;

    const intType = new QiType();
    intType.Id = 'intType';
    intType.QiTypeCode = QiTypeCode.Int32;

    const orderTargetProperty = new QiTypeProperty();
    orderTargetProperty.Id = 'OrderTarget';
    orderTargetProperty.QiType = intType;
    orderTargetProperty.IsKey = true;

    const radiansTargetProperty = new QiTypeProperty();
    radiansTargetProperty.Id = 'RadiansTarget';
    radiansTargetProperty.QiType = doubleType;

    const tauTargetProperty = new QiTypeProperty();
    tauTargetProperty.Id = 'TauTarget';
    tauTargetProperty.QiType = doubleType;

    const sinTargetProperty = new QiTypeProperty();
    sinTargetProperty.Id = 'SinTarget';
    sinTargetProperty.QiType = doubleType;

    const cosTargetProperty = new QiTypeProperty();
    cosTargetProperty.Id = 'CosTarget';
    cosTargetProperty.QiType = doubleType;

    const tanTargetProperty = new QiTypeProperty();
    tanTargetProperty.Id = 'TanTarget';
    tanTargetProperty.QiType = doubleType;

    const sinhTargetProperty = new QiTypeProperty();
    sinhTargetProperty.Id = 'SinhTarget';
    sinhTargetProperty.QiType = doubleType;

    const coshTargetProperty = new QiTypeProperty();
    coshTargetProperty.Id = 'CoshTarget';
    coshTargetProperty.QiType = doubleType;

    const tanhTargetProperty = new QiTypeProperty();
    tanhTargetProperty.Id = 'TanhTarget';
    tanhTargetProperty.QiType = doubleType;

    const waveDataTargetType = new QiType();
    waveDataTargetType.Id = targetTypeId;
    waveDataTargetType.Name = 'WaveDataTargetType_AngularSample';
    waveDataTargetType.Description = 'This is a sample QiType for storing WaveDataTarget events';
    waveDataTargetType.Properties = [orderTargetProperty, radiansTargetProperty, tauTargetProperty, sinTargetProperty,
      cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty];
    waveDataTargetType.QiTypeCode = QiTypeCode.Object;

    return waveDataTargetType;
  }

  buildWaveDataIntegerType() {

    const intType = new QiType();
    intType.Id = 'intType';
    intType.QiTypeCode = QiTypeCode.Int32;

    const orderTargetProperty = new QiTypeProperty();
    orderTargetProperty.Id = 'OrderTarget';
    orderTargetProperty.QiType = intType;
    orderTargetProperty.IsKey = true;

    const sinIntProperty = new QiTypeProperty();
    sinIntProperty.Id = 'SinhInt';
    sinIntProperty.QiType = intType;

    const cosIntProperty = new QiTypeProperty();
    cosIntProperty.Id = 'CoshInt';
    cosIntProperty.QiType = intType;

    const tanIntProperty = new QiTypeProperty();
    tanIntProperty.Id = 'TanhInt';
    tanIntProperty.QiType = intType;


    const waveDataIntType = new QiType();
    waveDataIntType.Id = targetIntTypeId;
    waveDataIntType.Name = 'WaveDataIntegerType_AngularSample';
    waveDataIntType.Description = 'This is a sample QiType for storing WaveDataInteger events';
    waveDataIntType.Properties = [orderTargetProperty, sinIntProperty, cosIntProperty, tanIntProperty];
    waveDataIntType.QiTypeCode = QiTypeCode.Object;

    return waveDataIntType;
  }

  buildAutoView() {
        const autoView = new QiView();
        autoView.Id = autoViewId;
        autoView.Name = "WaveData_AutoView";
        autoView.Description = "This view uses Qi Types of the same shape and will map automatically."
        autoView.SourceTypeId = typeId;
        autoView.TargetTypeId = targetTypeId;
        return autoView;
      }

  buildManualView() {
        const manualView = new QiView();
        manualView.Id = manualViewId;
        manualView.Name = "WaveData_AutoView";
        manualView.Description = "This view uses Qi Types of different shapes, mappings are made explicitly with QiViewProperties."
        manualView.SourceTypeId = typeId;
        manualView.TargetTypeId = targetIntTypeId;

        const viewProperty0 = new QiViewProperty();
        viewProperty0.SourceId = 'Order';
        viewProperty0.TargetId = 'OrderTarget';

        const viewProperty1 = new QiViewProperty();
        viewProperty1.SourceId = 'Sinh';
        viewProperty1.TargetId = 'SinhInt';

        const viewProperty2 = new QiViewProperty();
        viewProperty2.SourceId = 'Cosh';
        viewProperty2.TargetId = 'CoshInt';

        const viewProperty3 = new QiViewProperty();
        viewProperty3.SourceId = 'Tanh';
        viewProperty3.TargetId = 'TanhInt';
        
        manualView.Properties = [viewProperty0, viewProperty1, viewProperty2, viewProperty3];
        return manualView;
  }   
  newWaveDataEvent(order: number, range: number, multiplier: number) {
    const radians = 2 * Math.PI/ multiplier;

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

  writeSingleWaveDataEvent() {
    this.qiService.insertValue(streamId, this.newWaveDataEvent(0, 2.5, 2)).subscribe(res => {
      this.button3Message = res.status;
    },
    err => {
      this.button3Message = err;
    });
  }

  writeWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 20; i += 2) {
      list.push(this.newWaveDataEvent(i, 12, 24));
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
    this.qiService.getRangeValues(streamId, '1', 40, QiBoundaryType.ExactOrCalculated)
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

  updateWaveDataEvents(){    
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 2.5, 5));
    }
    this.qiService.updateValues(streamId, list).subscribe(res => {
      this.button14Message = res.status;
    },
    err => {
      this.button14Message = err;
    });
  }

  replaceWaveDataEvents(){    
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 1.5, 10));
    }
    this.qiService.replaceValues(streamId, list).subscribe(res => {
      this.button15Message = res.status;
    },
    err => {
      this.button15Message = err;
    });
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

  createAutoviewTargetType() {
    const type = this.buildWaveDataTargetType();
    this.qiService.createType(type).subscribe(res => {
      this.button6Message = res.status;
    },
    err => {
      this.button6Message = err;
    });
  }

  createAutoview() {
    const view = this.buildAutoView();
    this.qiService.createView(view).subscribe(res => {
      this.button7Message = res.status;
    },
    err => {
      this.button7Message = err;
    });
  }

  retrieveWaveDataEventsAutoview() {
    this.hasView1Events = false;
    this.qiService.getRangeValues(streamId, '1', 5, QiBoundaryType.ExactOrCalculated, autoViewId)
      .map(res => res.json())
      .subscribe(res => {
        this.targetEvents = res as WaveDataTarget[];
        this.hasView1Events = true;
        this.button8Message = `Found ${this.targetEvents.length} events`
      },
      err => {
        this.button8Message = err;
      });
  }

  createQiViewPropertiesAndManualType() {
    const type = this.buildWaveDataIntegerType();
    this.qiService.createType(type).subscribe(res => {
      this.button9Message = res.status;
    },
    err => {
      this.button9Message = err;
    });
    const view = this.buildManualView();
    this.qiService.createView(view).subscribe(res => {
      this.button9Message = res.status;
    },
    err => {
      this.button9Message = err;
    });
  }

  retrieveWaveDataEventsManualview() {
    this.hasView2Events = false;
    this.qiService.getRangeValues(streamId, '3', 5, QiBoundaryType.ExactOrCalculated, manualViewId)
      .map(res => res.json())
      .subscribe(res => {
        this.integerEvents = res as WaveDataInteger[];
        this.hasView2Events = true;
        this.button10Message = `Found ${this.integerEvents.length} events`
      },
      err => {
        this.button10Message = err;
      });
  }

  getQiViewMap() {
    this.qiService.getViewMap(manualViewId)
      .map(res => res.json())
      .subscribe(res => {
        this.viewMap = res as QiViewMap;
        this.hasMapProperties = true;
      this.button11Message = `QiViewMap`
    },
      err => {
        this.button11Message = err;
      });
  }

  deleteAllValues() {
    this.qiService.deleteWindowValues(streamId, "0", "200")
      .subscribe(res => {
        this.button13Message = res.status;
    },
      err => {
        this.button13Message = err;
      });
  }

  cleanup() {
    this.qiService.deleteStream(streamId).subscribe(() => {
      // you can't delete a type/behavior if there are existing streams
      // that depend on it, so we must make sure the stream is deleted first.
      this.qiService.deleteType(typeId).subscribe()
      this.qiService.deleteType(targetTypeId).subscribe()
      this.qiService.deleteType(targetIntTypeId).subscribe()
      this.qiService.deleteView(autoViewId).subscribe()
      this.qiService.deleteView(manualViewId).subscribe()
      this.qiService.deleteBehavior(behaviorId).subscribe();
    });
    this.hasEvents = false;
    this.button12Message = "All Objects Deleted"
  }
}
