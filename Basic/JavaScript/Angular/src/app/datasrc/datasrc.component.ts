import { Component } from '@angular/core';

import { QiBoundaryType, QiRestService } from '../qi.rest.service'
import { QiType, QiStream, QiTypeProperty, QiTypeCode, QiStreamBehavior,
  QiStreamMode, QiView, QiViewProperty, QiViewMap} from '../qi.rest.service'
import {HttpErrorResponse, HttpResponse} from "@angular/common/http";

const streamId = 'WaveDataStream';
const typeId = 'WaveDataType';
const targetTypeId = 'WaveDataTargetType';
const targetIntTypeId = 'WaveDataTargetIntType';
const autoViewId = 'WaveDataAutoView';
const manualViewId = 'WaveDataManualView';
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
  metadataMap: Map<string, string>;
  hasEvents: boolean;
  hasView1Events: boolean;
  hasView2Events: boolean;
  hasMapProperties: boolean;
  hasMetadata: boolean;

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
  button16Message: string;
  button17Message: string;
  button18Message: string;
  button19Message: string;

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
        autoView.Name = 'WaveData_AutoView';
        autoView.Description = 'This view uses Qi Types of the same shape and will map automatically.';
        autoView.SourceTypeId = typeId;
        autoView.TargetTypeId = targetTypeId;
        return autoView;
      }

  buildManualView() {
        const manualView = new QiView();
        manualView.Id = manualViewId;
        manualView.Name = 'WaveData_AutoView';
        manualView.Description = 'This view uses Qi Types of different shapes, mappings are made explicitly with QiViewProperties.';
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
    const radians = 2 * Math.PI / multiplier;

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
      this.button1Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button1Message = this.unhealthyResponseMessage(err);
    });
  }

  createStream() {
    this.stream = new QiStream();
    this.stream.Id = streamId;
    this.stream.TypeId = typeId;
    this.qiService.createStream(this.stream)
    .subscribe(res => {
        this.button2Message = this.healthyResponseMessage(res);
      },
      err => {
        this.button2Message = this.unhealthyResponseMessage(err);
      });
  }

  writeSingleWaveDataEvent() {
    this.qiService.insertValue(streamId, this.newWaveDataEvent(0, 2.5, 2)).subscribe(res => {
      this.button3Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button3Message = this.unhealthyResponseMessage(err);
    });
  }

  writeWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 20; i += 2) {
      list.push(this.newWaveDataEvent(i, 12, 24));
    }

    this.qiService.insertValues(streamId, list).subscribe(res => {
      this.button3Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button3Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEvents() {
    this.hasEvents = false;
    this.qiService.getRangeValues(streamId, '1', 40, QiBoundaryType.ExactOrCalculated)
      .subscribe(res => {
        this.events = res.body as WaveData[];
        this.hasEvents = true;
        this.button4Message = `Found ${this.events.length} events`
      },
      err => {
        this.button4Message = this.unhealthyResponseMessage(err);
      });
  }

  updateWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 2.5, 5));
    }
    this.qiService.updateValues(streamId, list).subscribe(res => {
      this.button14Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button14Message = this.unhealthyResponseMessage(err);
    });
  }

  replaceWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 1.5, 10));
    }
    this.qiService.replaceValues(streamId, list).subscribe(res => {
      this.button15Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button15Message = this.unhealthyResponseMessage(err);
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
        this.button5Message = this.healthyResponseMessage(res);
      },
      err => {
        this.button5Message = this.unhealthyResponseMessage(err);
      });
    })
  }

  createAutoviewTargetType() {
    const type = this.buildWaveDataTargetType();
    this.qiService.createType(type).subscribe(res => {
      this.button6Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button6Message = this.unhealthyResponseMessage(err);
    });
  }

  createAutoview() {
    const view = this.buildAutoView();
    this.qiService.createView(view).subscribe(res => {
      this.button7Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button7Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEventsAutoview() {
    this.hasView1Events = false;
    this.qiService.getRangeValues(streamId, '1', 5, QiBoundaryType.ExactOrCalculated, autoViewId)
      .subscribe(res => {
        this.targetEvents = res.body as WaveDataTarget[];
        this.hasView1Events = true;
        this.button8Message = `Found ${this.targetEvents.length} events`
      },
      err => {
        this.button8Message = this.unhealthyResponseMessage(err);
      });
  }

  createQiViewPropertiesAndManualType() {
    const type = this.buildWaveDataIntegerType();
    this.qiService.createType(type).subscribe(res => {
      this.button9Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button9Message = this.unhealthyResponseMessage(err);
    });
    const view = this.buildManualView();
    this.qiService.createView(view).subscribe(res => {
      this.button9Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button9Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEventsManualview() {
    this.hasView2Events = false;
    this.qiService.getRangeValues(streamId, '3', 5, QiBoundaryType.ExactOrCalculated, manualViewId)
      .subscribe(res => {
        this.integerEvents = res.body as WaveDataInteger[];
        this.hasView2Events = true;
        this.button10Message = `Found ${this.integerEvents.length} events`
      },
      err => {
        this.button10Message = this.unhealthyResponseMessage(err);
      });
  }

  getQiViewMap() {
    this.qiService.getViewMap(manualViewId)
      .subscribe(res => {
        this.viewMap = res.body as QiViewMap;
        this.hasMapProperties = true;
      this.button11Message = `QiViewMap`
    },
      err => {
        this.button11Message = this.unhealthyResponseMessage(err);
      });
  }

  createTagsAndMetadata() {
    const tags = [ 'waves', 'periodic', '2018', 'validated' ];
    const metadata = {Region: 'North America', Country: 'Canada', Province: 'Quebec'};
    this.qiService.createTags(streamId, tags)
    .subscribe(res => {
      this.button16Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button16Message = this.unhealthyResponseMessage(err);
    });
    this.qiService.createMetadata(streamId, metadata)
    .subscribe(res => {
      this.button16Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button16Message = this.unhealthyResponseMessage(err);
    });
  }

  getAndPrintTags() {
    this.qiService.getTags(streamId)
      .subscribe(res => {
        const tags = res.body as Array<string>;
        let result = 'Tags associated with ' + streamId + ': ';
        for (let i = 0; i < tags.length; i++) {
          result += (tags[i] + ', ');
        }

        this.button17Message = result;
    },
      err => {
        this.button17Message = this.unhealthyResponseMessage(err);
      });
  }

  getAndPrintMetadata() {
    this.qiService.getMetadata(streamId)
      .subscribe(res => {
        this.metadataMap = res.body as Map<string, string>;
        this.hasMetadata = true;
    },
      err => {
        this.button18Message = this.unhealthyResponseMessage(err);
      });
  }

  searchForQiStream() {
    this.qiService.getStreams('periodic')
      .subscribe(res => {
        let result = 'Streams associated with "periodic": ';
        const streams = res.body as Array<QiStream>;
        if (streams.length > 0) {
          for (let i = 0; i < streams.length; i++) {
            result += (streams[i].Id.toString() + ' ')
          }
          this.button19Message = result;
        } else {
          this.button19Message = 'No results found, search indexing can take up to 15 seconds, please try your request again.';
        }
    },
      err => {
        this.button19Message = this.unhealthyResponseMessage(err);
      });
  }

  deleteAllValues() {
    this.qiService.deleteWindowValues(streamId, '0', '200')
      .subscribe(res => {
        this.button13Message = this.healthyResponseMessage(res);
    },
      err => {
        this.button13Message = this.unhealthyResponseMessage(err);
      });
  }

  cleanup() {
    this.qiService.deleteStream(streamId).subscribe(() => {
      // you can't delete a type/behavior if there are existing streams
      // that depend on it, so we must make sure the stream is deleted first.
      this.qiService.deleteType(typeId).subscribe();
      this.qiService.deleteType(targetTypeId).subscribe();
      this.qiService.deleteType(targetIntTypeId).subscribe();
      this.qiService.deleteView(autoViewId).subscribe();
      this.qiService.deleteView(manualViewId).subscribe();
      this.qiService.deleteBehavior(behaviorId).subscribe();
    });
    this.hasEvents = false;
    this.button12Message = 'All Objects Deleted'
  }

  healthyResponseMessage(res: HttpResponse<any>) {
    return `${res.status} (${res.statusText})`;
  }

  unhealthyResponseMessage(err: HttpErrorResponse) {
      return `${err.status} (${err.statusText}) [${err.error.Message}]`;
  }
}
