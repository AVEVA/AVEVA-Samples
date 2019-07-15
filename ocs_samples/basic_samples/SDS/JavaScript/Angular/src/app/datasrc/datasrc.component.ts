// datasrc.component.ts
//

import { Component } from '@angular/core';

import { SdsBoundaryType, SdsRestService, SdsStreamPropertyOverride, SdsStreamIndex } from '../sds/sds.rest.service'
import { SdsType, SdsStream, SdsTypeProperty, SdsTypeCode,
  SdsStreamMode, SdsStreamView, SdsStreamViewProperty, SdsStreamViewMap} from '../sds/sds.rest.service'
import {HttpErrorResponse, HttpResponse} from "@angular/common/http";

const streamId = 'WaveDataStream';
const streamIdSecondary = 'SampleStream_Secondary';
const streamIdCompound = 'SampleStream_Compound';

const typeId = 'WaveDataType';
const compoundTypeId = 'SampleType_Compound';
const targetTypeId = 'WaveDataTargetType';
const targetIntTypeId = 'WaveDataTargetIntType';
const autoStreamViewId = 'WaveDataAutoStreamView';
const manualStreamViewId = 'WaveDataManualStreamView';

class  WaveDataCompound {
  Order: number;
  Multiplier: number;
  Radians: number;
  Tau: number;
  Sin: number;
  Cos: number;
  Tan: number;
  Sinh: number;
  Cosh: number;
  Tanh: number
}

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
  stream: SdsStream;
  streamSecondaryIndex: SdsStream;
  events: WaveData[];
  eventsHeaders: string;
  eventsInterpolated: string;
  eventsFiltered: string;
  eventsSampled: string;

  targetEvents: WaveDataTarget[];
  integerEvents: WaveDataInteger[];
  streamViewMap: SdsStreamViewMap;
  metadataMap: Map<string, string>;
  hasEvents: boolean;
  hasEventsHeaders: boolean;
  hasEventsInterpolated: boolean;
  hasEventsFiltered:boolean;

  hasStreamView1Events: boolean;
  hasStreamView2Events: boolean;
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
  getDataWithHeadersMessage: string;
  getDataInterpolatedMessage: string;
  getFilteredValuesMessage: string;
  getSampledValuesMessage: String;
  updateStreamTypeMessage: string;
  queryTypesMessage: string;
  secondaryCreateMessage: string;
  secondaryUpdateMessage: string;
  secondaryDeleteMessage: string;
  createCompoundTypeandStreamMessage: string;
  createAndRetreiveCompoundDataMessage: string;
  createAndRetreiveCompoundDataMessageData: string;

  constructor(private sdsService: SdsRestService) {
    this.hasEvents = false;
  }

  buildWaveDataCompoundType() {
    const doubleType = new SdsType();
    doubleType.Id = 'doubleType';
    doubleType.SdsTypeCode = SdsTypeCode.Double;

    const intType = new SdsType();
    intType.Id = 'intType';
    intType.SdsTypeCode = SdsTypeCode.Int32;

    const orderProperty = new SdsTypeProperty();
    orderProperty.Id = 'Order';
    orderProperty.SdsType = intType;
    orderProperty.IsKey = true;
    orderProperty.Order = 1;

    const multiplier = new SdsTypeProperty();
    multiplier.Id = 'Multiplier';
    multiplier.SdsType = intType;
    multiplier.IsKey = true;
    multiplier.Order = 2;

    const radiansProperty = new SdsTypeProperty();
    radiansProperty.Id = 'Radians';
    radiansProperty.SdsType = doubleType;

    const tauProperty = new SdsTypeProperty();
    tauProperty.Id = 'Tau';
    tauProperty.SdsType = doubleType;

    const sinProperty = new SdsTypeProperty();
    sinProperty.Id = 'Sin';
    sinProperty.SdsType = doubleType;

    const cosProperty = new SdsTypeProperty();
    cosProperty.Id = 'Cos';
    cosProperty.SdsType = doubleType;

    const tanProperty = new SdsTypeProperty();
    tanProperty.Id = 'Tan';
    tanProperty.SdsType = doubleType;

    const sinhProperty = new SdsTypeProperty();
    sinhProperty.Id = 'Sinh';
    sinhProperty.SdsType = doubleType;

    const coshProperty = new SdsTypeProperty();
    coshProperty.Id = 'Cosh';
    coshProperty.SdsType = doubleType;

    const tanhProperty = new SdsTypeProperty();
    tanhProperty.Id = 'Tanh';
    tanhProperty.SdsType = doubleType;

    const waveDataType = new SdsType();
    waveDataType.Id = compoundTypeId;
    waveDataType.Name = 'WaveDataType_AngularSample';
    waveDataType.Description = 'This is a sample SdsType for storing WaveData events';
    waveDataType.Properties = [orderProperty, multiplier, radiansProperty, tauProperty, sinProperty,
      cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty];
    waveDataType.SdsTypeCode = SdsTypeCode.Object;

    return waveDataType;
  }

  buildWaveDataType() {
    const doubleType = new SdsType();
    doubleType.Id = 'doubleType';
    doubleType.SdsTypeCode = SdsTypeCode.Double;

    const intType = new SdsType();
    intType.Id = 'intType';
    intType.SdsTypeCode = SdsTypeCode.Int32;

    const orderProperty = new SdsTypeProperty();
    orderProperty.Id = 'Order';
    orderProperty.SdsType = intType;
    orderProperty.IsKey = true;

    const radiansProperty = new SdsTypeProperty();
    radiansProperty.Id = 'Radians';
    radiansProperty.SdsType = doubleType;

    const tauProperty = new SdsTypeProperty();
    tauProperty.Id = 'Tau';
    tauProperty.SdsType = doubleType;

    const sinProperty = new SdsTypeProperty();
    sinProperty.Id = 'Sin';
    sinProperty.SdsType = doubleType;

    const cosProperty = new SdsTypeProperty();
    cosProperty.Id = 'Cos';
    cosProperty.SdsType = doubleType;

    const tanProperty = new SdsTypeProperty();
    tanProperty.Id = 'Tan';
    tanProperty.SdsType = doubleType;

    const sinhProperty = new SdsTypeProperty();
    sinhProperty.Id = 'Sinh';
    sinhProperty.SdsType = doubleType;

    const coshProperty = new SdsTypeProperty();
    coshProperty.Id = 'Cosh';
    coshProperty.SdsType = doubleType;

    const tanhProperty = new SdsTypeProperty();
    tanhProperty.Id = 'Tanh';
    tanhProperty.SdsType = doubleType;

    const waveDataType = new SdsType();
    waveDataType.Id = typeId;
    waveDataType.Name = 'WaveDataType_AngularSample';
    waveDataType.Description = 'This is a sample SdsType for storing WaveData events';
    waveDataType.Properties = [orderProperty, radiansProperty, tauProperty, sinProperty,
      cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty];
    waveDataType.SdsTypeCode = SdsTypeCode.Object;

    return waveDataType;
  }

  buildWaveDataTargetType() {
    const doubleType = new SdsType();
    doubleType.Id = 'doubleType';
    doubleType.SdsTypeCode = SdsTypeCode.Double;

    const intType = new SdsType();
    intType.Id = 'intType';
    intType.SdsTypeCode = SdsTypeCode.Int32;

    const orderTargetProperty = new SdsTypeProperty();
    orderTargetProperty.Id = 'OrderTarget';
    orderTargetProperty.SdsType = intType;
    orderTargetProperty.IsKey = true;

    const radiansTargetProperty = new SdsTypeProperty();
    radiansTargetProperty.Id = 'RadiansTarget';
    radiansTargetProperty.SdsType = doubleType;

    const tauTargetProperty = new SdsTypeProperty();
    tauTargetProperty.Id = 'TauTarget';
    tauTargetProperty.SdsType = doubleType;

    const sinTargetProperty = new SdsTypeProperty();
    sinTargetProperty.Id = 'SinTarget';
    sinTargetProperty.SdsType = doubleType;

    const cosTargetProperty = new SdsTypeProperty();
    cosTargetProperty.Id = 'CosTarget';
    cosTargetProperty.SdsType = doubleType;

    const tanTargetProperty = new SdsTypeProperty();
    tanTargetProperty.Id = 'TanTarget';
    tanTargetProperty.SdsType = doubleType;

    const sinhTargetProperty = new SdsTypeProperty();
    sinhTargetProperty.Id = 'SinhTarget';
    sinhTargetProperty.SdsType = doubleType;

    const coshTargetProperty = new SdsTypeProperty();
    coshTargetProperty.Id = 'CoshTarget';
    coshTargetProperty.SdsType = doubleType;

    const tanhTargetProperty = new SdsTypeProperty();
    tanhTargetProperty.Id = 'TanhTarget';
    tanhTargetProperty.SdsType = doubleType;

    const waveDataTargetType = new SdsType();
    waveDataTargetType.Id = targetTypeId;
    waveDataTargetType.Name = 'WaveDataTargetType_AngularSample';
    waveDataTargetType.Description = 'This is a sample SdsType for storing WaveDataTarget events';
    waveDataTargetType.Properties = [orderTargetProperty, radiansTargetProperty, tauTargetProperty, sinTargetProperty,
      cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty];
    waveDataTargetType.SdsTypeCode = SdsTypeCode.Object;

    return waveDataTargetType;
  }

  buildWaveDataIntegerType() {

    const intType = new SdsType();
    intType.Id = 'intType';
    intType.SdsTypeCode = SdsTypeCode.Int32;

    const orderTargetProperty = new SdsTypeProperty();
    orderTargetProperty.Id = 'OrderTarget';
    orderTargetProperty.SdsType = intType;
    orderTargetProperty.IsKey = true;

    const sinIntProperty = new SdsTypeProperty();
    sinIntProperty.Id = 'SinhInt';
    sinIntProperty.SdsType = intType;

    const cosIntProperty = new SdsTypeProperty();
    cosIntProperty.Id = 'CoshInt';
    cosIntProperty.SdsType = intType;

    const tanIntProperty = new SdsTypeProperty();
    tanIntProperty.Id = 'TanhInt';
    tanIntProperty.SdsType = intType;


    const waveDataIntType = new SdsType();
    waveDataIntType.Id = targetIntTypeId;
    waveDataIntType.Name = 'WaveDataIntegerType_AngularSample';
    waveDataIntType.Description = 'This is a sample SdsType for storing WaveDataInteger events';
    waveDataIntType.Properties = [orderTargetProperty, sinIntProperty, cosIntProperty, tanIntProperty];
    waveDataIntType.SdsTypeCode = SdsTypeCode.Object;

    return waveDataIntType;
  }

  buildAutoStreamView() {
        const autoStreamView = new SdsStreamView();
        autoStreamView.Id = autoStreamViewId;
        autoStreamView.Name = 'WaveData_AutoStreamView';
        autoStreamView.Description = 'This StreamView uses Sds Types of the same shape and will map automatically.';
        autoStreamView.SourceTypeId = typeId;
        autoStreamView.TargetTypeId = targetTypeId;
        return autoStreamView;
      }

  buildManualStreamView() {
        const manualStreamView = new SdsStreamView();
        manualStreamView.Id = manualStreamViewId;
        manualStreamView.Name = 'WaveData_AutoStreamView';
        manualStreamView.Description = 'This StreamView uses Sds Types of different shapes, mappings are made explicitly with SdsStreamViewProperties.';
        manualStreamView.SourceTypeId = typeId;
        manualStreamView.TargetTypeId = targetIntTypeId;

        const streamViewProperty0 = new SdsStreamViewProperty();
        streamViewProperty0.SourceId = 'Order';
        streamViewProperty0.TargetId = 'OrderTarget';

        const streamViewProperty1 = new SdsStreamViewProperty();
        streamViewProperty1.SourceId = 'Sinh';
        streamViewProperty1.TargetId = 'SinhInt';

        const streamViewProperty2 = new SdsStreamViewProperty();
        streamViewProperty2.SourceId = 'Cosh';
        streamViewProperty2.TargetId = 'CoshInt';

        const streamViewProperty3 = new SdsStreamViewProperty();
        streamViewProperty3.SourceId = 'Tanh';
        streamViewProperty3.TargetId = 'TanhInt';

        manualStreamView.Properties = [streamViewProperty0, streamViewProperty1, streamViewProperty2, streamViewProperty3];
        return manualStreamView;
  }

  newWaveDataEvent(order: number, range: number, multiplier: number) {
    const radians = order * Math.PI / 32;

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

  newWaveDataCompoundEvent(order: number, multiplier: number) {
    const radians = order * Math.PI / 32;

    const waveData = new WaveDataCompound();
    waveData.Order = order;
    waveData.Multiplier = multiplier;
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
    console.log(type);
    this.sdsService.createType(type).subscribe(res => {
      this.button1Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button1Message = this.unhealthyResponseMessage(err);
    });
  }

  createStream() {
    this.stream = new SdsStream();
    this.stream.Id = streamId;
    this.stream.TypeId = typeId;
    this.sdsService.createStream(this.stream)
    .subscribe(res => {
        this.button2Message = this.healthyResponseMessage(res);
      },
      err => {
        this.button2Message = this.unhealthyResponseMessage(err);
      });
  }

  updateStreamSecondaryIndex() {
    const index = new SdsStreamIndex();
    index.SdsTypePropertyId = 'SinhInt';
    this.sdsService.getStream(streamId)
    .subscribe(res => {
      this.stream = res.body as SdsStream;
      this.stream.Indexes = [index];
      this.sdsService.updateStream(this.stream)
      .subscribe(res2 => {
          this.secondaryUpdateMessage = this.healthyResponseMessage(res2);
        },
        err => {
          this.secondaryUpdateMessage = this.unhealthyResponseMessage(err);
        });
    },
    err => {
      this.secondaryUpdateMessage = this.unhealthyResponseMessage(err);
    });
  }

  secondaryDeleteIndex() {
    this.streamSecondaryIndex.Indexes = [];

    this.sdsService.updateStream(this.streamSecondaryIndex)
    .subscribe(res => {
        this.secondaryDeleteMessage = this.healthyResponseMessage(res) + JSON.stringify(res.body);
      },
      err => {
        this.secondaryDeleteMessage = this.unhealthyResponseMessage(err);
      });
  }

  createStreamSecondaryIndex() {
    this.streamSecondaryIndex = new SdsStream();
    const index = new SdsStreamIndex();
    index.SdsTypePropertyId = 'Radians';
    this.streamSecondaryIndex.Id = streamIdSecondary;
    this.streamSecondaryIndex.TypeId = typeId;
    this.streamSecondaryIndex.Indexes = [index];

    this.sdsService.createStream(this.streamSecondaryIndex)
    .subscribe(res => {
        this.secondaryCreateMessage = this.healthyResponseMessage(res) + JSON.stringify(res.body);
      },
      err => {
        this.secondaryCreateMessage = this.unhealthyResponseMessage(err);
      });
  }
  
  createCompoundTypeandStream() {
    const compoundType = this.buildWaveDataCompoundType()
    const compoundStream = new SdsStream();
    compoundStream.Id = streamIdCompound;
    compoundStream.TypeId = compoundTypeId;

    this.sdsService.createType(compoundType)
    .subscribe(res => {
      this.sdsService.createStream(compoundStream)
      .subscribe(res2 => {
          this.createCompoundTypeandStreamMessage = this.healthyResponseMessage(res2);
        },
        err => {
          this.createCompoundTypeandStreamMessage = this.unhealthyResponseMessage(err);
        });
    },
    err => {
      this.createCompoundTypeandStreamMessage = this.unhealthyResponseMessage(err);
    });
  }

  writeSingleWaveDataEvent() {
    const list: Array<WaveData> = [];
    list.push(this.newWaveDataEvent(0, 2.5, 2));
    this.sdsService.insertValues(streamId, list).subscribe(res => {
      this.button3Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button3Message = this.unhealthyResponseMessage(err);
    });
  }

  writeWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 20; i += 2) {
      list.push(this.newWaveDataEvent(i, 12, 2));
    }

    this.sdsService.insertValues(streamId, list).subscribe(res => {
      this.button3Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button3Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEvents() {
    this.hasEvents = false;
    this.sdsService.getRangeValues(streamId, '1', 40, SdsBoundaryType.ExactOrCalculated)
      .subscribe(res => {
        this.events = res.body as WaveData[];
        this.hasEvents = true;
        this.button4Message = `Found ${this.events.length} events`
      },
      err => {
        this.button4Message = this.unhealthyResponseMessage(err);
      });
  }

  retrieveWaveDataEventsHeaders() {
    this.hasEventsHeaders = false;
    this.sdsService.getRangeValuesHeaders(streamId, '1', 40, SdsBoundaryType.ExactOrCalculated)
      .subscribe(res => {
        this.eventsHeaders = res.body as string;
        this.hasEventsHeaders = true;
        this.getDataWithHeadersMessage = this.healthyResponseMessage(res) + JSON.stringify(this.eventsHeaders);
      },
      err => {
        this.getDataWithHeadersMessage = this.unhealthyResponseMessage(err);
      });
  }
  
  retrieveFilteredValues() {
    this.hasEventsFiltered = false;
    this.sdsService.getWindowValues(streamId, 0, 50, 'Radians%20lt%203')
      .subscribe(res => {
        this.eventsFiltered = res.body as string;
        this.hasEventsFiltered = true;
        this.getFilteredValuesMessage = this.healthyResponseMessage(res) + JSON.stringify(this.eventsFiltered);
      },
      err => {
        this.getFilteredValuesMessage = this.unhealthyResponseMessage(err);
      });
  }

  retrieveSampledValues() {
    this.sdsService.getSampledValues(streamId, 0, 40, 4, "sin")
      .subscribe(res => {
        this.eventsSampled = res.body as string;
        this.getSampledValuesMessage = this.healthyResponseMessage(res) + JSON.stringify(this.eventsSampled);
      },
      err => {
        this.getSampledValuesMessage = this.unhealthyResponseMessage(err);
      });
  }

  updateStreamType() {
    this.sdsService.updateStreamType(streamId, manualStreamViewId)
      .subscribe(res => {
        const resp = res.body as string;
        this.updateStreamTypeMessage = this.healthyResponseMessage(res);
      },
      err => {
        this.updateStreamTypeMessage = this.unhealthyResponseMessage(err);
      });
  }

  queryTypes() {
    this.sdsService.getTypes(0, 100, 'Id:*Target*')
      .subscribe(res => {
        const resp = res.body as string;
        this.queryTypesMessage = this.healthyResponseMessage(res) + JSON.stringify(resp);
      },
      err => {
        this.queryTypesMessage = this.unhealthyResponseMessage(err);
      });
  }

  retrieveInterpolatedValues() {
    this.hasEventsInterpolated = false;
    this.sdsService.getWindowValuesInterpolated(streamId, 5, 32, 4)
      .subscribe(res => {
        this.eventsInterpolated = res.body as string;
        this.hasEventsInterpolated = true;
        this.getDataInterpolatedMessage = this.healthyResponseMessage(res) + JSON.stringify(this.eventsInterpolated);
      },
      err => {
        this.getDataInterpolatedMessage = this.unhealthyResponseMessage(err);
      });
  }

  createAndRetreiveCompoundData() {
    const list: Array<WaveDataCompound> = [];
    list.push(this.newWaveDataCompoundEvent(1, 10));
    list.push(this.newWaveDataCompoundEvent(2, 2));
    list.push(this.newWaveDataCompoundEvent(3, 1));
    list.push(this.newWaveDataCompoundEvent(10, 3));
    list.push(this.newWaveDataCompoundEvent(10, 8));
    list.push(this.newWaveDataCompoundEvent(10, 10));
    this.sdsService.insertValues(streamIdCompound, list).subscribe(res => {
      this.createAndRetreiveCompoundDataMessage = this.healthyResponseMessage(res);
      this.sdsService.getWindowValues(streamIdCompound, '2|1', '10|8').subscribe(res2 => {
        this.createAndRetreiveCompoundDataMessage = this.healthyResponseMessage(res2);
        this.createAndRetreiveCompoundDataMessageData = JSON.stringify(res2.body);
      },
      err => {
        this.createAndRetreiveCompoundDataMessage = this.unhealthyResponseMessage(err);
      });
    },
    err => {
      this.createAndRetreiveCompoundDataMessage = this.unhealthyResponseMessage(err);
    });
  }

  updateWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 2.5, 4));
    }
    this.sdsService.updateValues(streamId, list).subscribe(res => {
      this.button14Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button14Message = this.unhealthyResponseMessage(err);
    });
  }

  replaceWaveDataEvents() {
    const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 1.5, 5));
    }
    this.sdsService.replaceValues(streamId, list).subscribe(res => {
      this.button15Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button15Message = this.unhealthyResponseMessage(err);
    });
  }

  createPropertyOverrideAndUpdateStream() {
    const propertyOverride = new SdsStreamPropertyOverride();
    propertyOverride.SdsTypePropertyId = "Radians";
    propertyOverride.InterpolationMode = SdsStreamMode.Discrete;
    this.stream.PropertyOverrides = [propertyOverride];
    this.sdsService.updateStream(this.stream).subscribe(res => {
      this.button5Message = this.healthyResponseMessage(res);
      },
      err => {
        this.button5Message = this.unhealthyResponseMessage(err);
      });
  }

  createAutoStreamViewTargetType() {
    const type = this.buildWaveDataTargetType();
    this.sdsService.createType(type).subscribe(res => {
      this.button6Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button6Message = this.unhealthyResponseMessage(err);
    });
  }

  createAutoStreamView() {
    const streamView = this.buildAutoStreamView();
    this.sdsService.createStreamView(streamView).subscribe(res => {
      this.button7Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button7Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEventsAutoStreamView() {
    this.hasStreamView1Events = false;
    this.sdsService.getRangeValues(streamId, '1', 5, SdsBoundaryType.ExactOrCalculated, autoStreamViewId)
      .subscribe(res => {
        this.targetEvents = res.body as WaveDataTarget[];
        this.hasStreamView1Events = true;
        this.button8Message = `Found ${this.targetEvents.length} events`
      },
      err => {
        this.button8Message = this.unhealthyResponseMessage(err);
      });
  }

  createSdsStreamViewPropertiesAndManualType() {
    const type = this.buildWaveDataIntegerType();
    this.sdsService.createType(type).subscribe(res => {
      this.button9Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button9Message = this.unhealthyResponseMessage(err);
    });
    const streamView = this.buildManualStreamView();
    this.sdsService.createStreamView(streamView).subscribe(res => {
      this.button9Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button9Message = this.unhealthyResponseMessage(err);
    });
  }

  retrieveWaveDataEventsManualStreamView() {
    this.hasStreamView2Events = false;
    this.sdsService.getRangeValues(streamId, '3', 5, SdsBoundaryType.ExactOrCalculated, manualStreamViewId)
      .subscribe(res => {
        this.integerEvents = res.body as WaveDataInteger[];
        this.hasStreamView2Events = true;
        this.button10Message = `Found ${this.integerEvents.length} events`
      },
      err => {
        this.button10Message = this.unhealthyResponseMessage(err);
      });
  }

  getSdsStreamViewMap() {
    this.sdsService.getStreamViewMap(manualStreamViewId)
      .subscribe(res => {
        this.streamViewMap = res.body as SdsStreamViewMap;
        this.hasMapProperties = true;
      this.button11Message = `SdsStreamViewMap`
    },
      err => {
        this.button11Message = this.unhealthyResponseMessage(err);
      });
  }

  createTagsAndMetadata() {
    const tags = [ 'waves', 'periodic', '2018', 'validated' ];
    const metadata = {Region: 'North America', Country: 'Canada', Province: 'Quebec'};
    this.sdsService.createTags(streamId, tags)
    .subscribe(res => {
      this.button16Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button16Message = this.unhealthyResponseMessage(err);
    });
    this.sdsService.createMetadata(streamId, metadata)
    .subscribe(res => {
      this.button16Message = this.healthyResponseMessage(res);
    },
    err => {
      this.button16Message = this.unhealthyResponseMessage(err);
    });
  }

  getAndPrintTags() {
    this.sdsService.getTags(streamId)
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
    this.sdsService.getMetadata(streamId)
      .subscribe(res => {
        this.metadataMap = res.body as Map<string, string>;
        this.hasMetadata = true;
    },
      err => {
        this.button18Message = this.unhealthyResponseMessage(err);
      });
  }      

  deleteAllValues() {
    this.sdsService.deleteWindowValues(streamId, '0', '200')
      .subscribe(res => {
        this.button13Message = this.healthyResponseMessage(res);
    },
      err => {
        this.button13Message = this.unhealthyResponseMessage(err);
      });
  }

  cleanup() {
    this.sdsService.deleteStream(streamIdSecondary).subscribe(() => {
      this.sdsService.deleteStream(streamId).subscribe(() => {
        // you can't delete a type if there are existing streams or streamViews
        // that depend on it, so we must make sure the stream is deleted first.
        this.sdsService.deleteStreamView(autoStreamViewId).subscribe(res => {
          this.button12Message = this.healthyResponseMessage(res);
      },
        err => {
          this.button12Message = this.unhealthyResponseMessage(err);
        });
        this.sdsService.deleteStreamView(manualStreamViewId).subscribe(res => {
          this.button12Message = this.healthyResponseMessage(res);
      },
        err => {
          this.button12Message = this.unhealthyResponseMessage(err);
        });
        this.sdsService.deleteType(typeId).subscribe(res => {
          this.button12Message = this.healthyResponseMessage(res);
      },
        err => {
          this.button12Message = this.unhealthyResponseMessage(err);
        });
        this.sdsService.deleteType(targetTypeId).subscribe(res => {
          this.button12Message = this.healthyResponseMessage(res);
      },
        err => {
          this.button12Message = this.unhealthyResponseMessage(err);
        });
        this.sdsService.deleteType(targetIntTypeId).subscribe(res => {
          this.button12Message = this.healthyResponseMessage(res);
      },
        err => {
          this.button12Message = this.unhealthyResponseMessage(err);
        });
      });
    });
    this.sdsService.deleteStream(streamIdCompound).subscribe(() => {
      this.sdsService.deleteType(compoundTypeId).subscribe(res => {
        this.button12Message = this.healthyResponseMessage(res);
    },
      err => {
        this.button12Message = this.unhealthyResponseMessage(err);
      });
    });
    this.hasEvents = false;
    this.button12Message = 'All Objects Deleted'
  }

  healthyResponseMessage(res: HttpResponse<any>) {
    console.log(res);
    return `${res.status} (${res.statusText})`;
  }

  unhealthyResponseMessage(err: HttpErrorResponse) {
    console.log(err);
    return `${err.status} (${err.statusText}) [${err.error ? err.error.Reason: 'No error message'}] Op-Id:${err.headers.get('Operation-Id')}`;
  }
}
