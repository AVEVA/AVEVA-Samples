// Sample.js
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

var http = require("http");
var restCall = require("request-promise");
var config = require("./config.js");

// retrieve configuration
var SdsServerUrl = config.sdsServerUrl;
var authItems = config.authItems;
var tenantId = config.tenantId;

var checkTokenExpired = function (client) {
    return client.getToken(authItems)
        .catch(function (err) { throw err });
};

var refreshToken = function (res, client) {
    var obj = JSON.parse(res);
    client.token = obj.access_token;
    client.tokenExpires = obj.expires_on;
};

var dumpEvent = function (elem) {
    console.log("Order: " + elem.Order +
        ", Tau: " + elem.Tau +
        ", Radians: " + elem.Radians +
        ", Sin: " + elem.Sin +
        ", Cos: " + elem.Cos +
        ", Tan: " + elem.Tan +
        ", Sinh: " + elem.Sinh +
        ", Cosh: " + elem.Cosh +
        ", Tanh:" + elem.Tanh);
};

var dumpEvents = function (obj) {
    console.log("Total events found: " + obj.length)
    obj.forEach(function (elem, index) {
        if(!elem.Order) {
            elem.Order = 0
        }
        console.log("Order: " + elem.Order +
        ", Tau: " + elem.Tau +
        ", Radians: " + elem.Radians +
        ", Sin: " + elem.Sin +
        ", Cos: " + elem.Cos +
        ", Tan: " + elem.Tan +
        ", Sinh: " + elem.Sinh +
        ", Cosh: " + elem.Cosh +
        ", Tanh:" + elem.Tanh);
    });
};

var dumpViewMap = function (obj) {     
    obj.Properties.forEach(function (elem, index) {
        if(elem.TargetId){
            console.log(elem.SourceId + " => " + elem.TargetId)
        }
        else {
            console.log(elem.SourceId + " => Not mapped")
        }
    });
};

var logError = function (err) {
    if  (typeof (err.statusCode) !== "undefined" && err.statusCode === 302) {
        console.log("Sds Object already present in the Service\n");
    }
    else {
        throw err;
    }
};

http.createServer(function (request1, response) {
    if (request1.url === '/favicon.ico') {
        return;
    }
    response.writeHead(200, { "Content-Type": "text/plain" });

    response.write("------------------------------------------------------------------------------------\n");
    response.write("  _________    .___      _______             .___               __        \n");
    response.write(" /   _____/  __| _/______\\      \\   ____   __| _/____          |__| ______\n");
    response.write(" \\_____  \\  / __ |/  ___//   |   \\ /  _ \\ / __ |/ __ \\         |  |/  ___/\n");
    response.write(" /        \\/ /_/ |\\___ \\/    |    (  <_> ) /_/ \\  ___/         |  |\\___ \\ \n");
    response.write("/_______  /\\____ /____  >____|__  /\\____/\\____ |\\___  > /\\ /\\__|  /____  >\n");
    response.write("        \\/      \\/    \\/        \\/            \\/    \\/  \\/ \\______|    \\/ \n");
    response.write("------------------------------------------------------------------------------------\n");
    response.write("Sds Service Operations Begun!\n");
    response.write("Check the console for updates")

    var sdsObjs = require("./SdsObjects.js");
    var clientObj = require("./SdsClient.js");
    var waveDataObj = require("./WaveData.js");

    var sampleNamespaceId = config.namespaceId;
    var sampleTypeId = "WaveData_SampleType";
    var sampleStreamId = "WaveData_SampleStream";
    var sampleViewId = "WaveData_SampleView"
    var targetTypeId = "targetTypeId";
    var targetIntegerTypeId = "targetIntegerTypeId"
    var manualViewId = "WaveData_ManualView"

    Object.freeze(sdsObjs.sdsTypeCode);
    Object.freeze(sdsObjs.sdsBoundaryType);
    Object.freeze(sdsObjs.sdsStreamMode);

    // define basic SdsTypes
    var doubleType = new sdsObjs.SdsType({ "Id": "doubleType", "SdsTypeCode": sdsObjs.sdsTypeCode.Double });
    var intType = new sdsObjs.SdsType({ "Id": "intType", "SdsTypeCode": sdsObjs.sdsTypeCode.Int32 });

    // define properties
    var orderProperty = new sdsObjs.SdsTypeProperty({ "Id": "Order", "SdsType": intType, "IsKey": true });
    var radiansProperty = new sdsObjs.SdsTypeProperty({ "Id": "Radians", "SdsType": doubleType });
    var tauProperty = new sdsObjs.SdsTypeProperty({ "Id": "Tau", "SdsType": doubleType });
    var sinProperty = new sdsObjs.SdsTypeProperty({ "Id": "Sin", "SdsType": doubleType });
    var cosProperty = new sdsObjs.SdsTypeProperty({ "Id": "Cos", "SdsType": doubleType });
    var tanProperty = new sdsObjs.SdsTypeProperty({ "Id": "Tan", "SdsType": doubleType });
    var sinhProperty = new sdsObjs.SdsTypeProperty({ "Id": "Sinh", "SdsType": doubleType });
    var coshProperty = new sdsObjs.SdsTypeProperty({ "Id": "Cosh", "SdsType": doubleType });
    var tanhProperty = new sdsObjs.SdsTypeProperty({ "Id": "Tanh", "SdsType": doubleType });

    //create an SdsType for WaveData Class
    var sampleType = new sdsObjs.SdsType({
        "Id": sampleTypeId, "Name": "WaveDataJs",
        "Description": "This is a sample Sds type for storing WaveData type events",
        "SdsTypeCode" : sdsObjs.sdsTypeCode.Object,
        "Properties": [orderProperty, tauProperty, radiansProperty, sinProperty,
            cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]
    });

    var client = new clientObj.SdsClient(SdsServerUrl);

    var getClientToken = client.getToken(authItems)
        .catch(function (err) { throw err });

    var nowSeconds = function () { return Date.now() / 1000; };

    // create an SdsType
    console.log("\nCreating an SdsType")
    var createType = getClientToken.then(
        function (res) {
            refreshToken(res, client);
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createType(tenantId, sampleNamespaceId, sampleType);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.createType(tenantId, sampleNamespaceId, sampleType);
            }
        }
    ).catch(function (err) { logError(err); });

    //create an SdsStream
    console.log("Creating an SdsStream")
    var sampleStream = new sdsObjs.SdsStream({
        "Id": sampleStreamId, "Name": "WaveStreamJs",
        "Description": "A Stream to store the WaveDatan Sds types events",
        "TypeId": sampleTypeId
        });

    var createStream = createType.then(
        function (res) {
            // create SdsStream
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createStream(tenantId, sampleNamespaceId, sampleStream);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.createStream(tenantId, sampleNamespaceId, sampleStream);
            }
    }).catch(function (err) { logError(err); });

    // insert data
    console.log("Inserting data")
    var interval = new Date();
    interval.setHours(0, 1, 0, 0);
    var evt = null;

    // insert a single event
    var insertValue = createStream.then(
        function (res) {
            evt = waveDataObj.NextWave(interval, 2.0, 0);
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.insertEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.insertEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
            }
        }
    ).catch(function (err) { logError(err); });

    // insert multiple events
    var events = [];
    var evt1 = null;
    var evtCount = 2;
    var mutliplier = 2;
    var callback = null;
    var totalEvents = 20;

    var buildEvents = function () {
        if (evtCount < totalEvents) {
            evt1 = waveDataObj.NextWave(interval, mutliplier, evtCount);
            events.push(evt1);
            evtCount += 2;
            buildEvents();
        } else {
            callback();
        }
    };

    var createRandomEvents = insertValue.then(
        function (res) {
            var prom = new Promise(function (resolve, reject) {
                callback = resolve;
                buildEvents();
            });
            return prom;
        }
    ).catch(function (err) { logError(err); });

    var insertMultipleValues = createRandomEvents.then(
        function () {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.insertEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.insertEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
            }
        }
    ).catch(function (err) { logError(err); });

    // get last event 
    var getLastValue = insertMultipleValues.then(
        function(res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function(res) {
                        refreshToken(res, client);
                        console.log("Getting latest event")
                        return client.getLastValue(tenantId, sampleNamespaceId, sampleStreamId);
                    }).catch(function(err) { logError(err); });
            } else {
                return client.getLastValue(tenantId, sampleNamespaceId, sampleStreamId);
            }
        }
    ).catch(function(err) { logError(err); });

    var printLastValue = getLastValue.then(
        function(res){
            var lastEvent = JSON.parse(res)
            dumpEvent(lastEvent)
        }
    ).catch(function (err) { logError(err); });

    // get all events
    var getWindowEvents = printLastValue.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        console.log("\nGetting all events")
                        return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }
    ).catch(function (err) { logError(err); });

    var printWindowEvents = getWindowEvents.then(
        function(res){
            var allEvents = JSON.parse(res)
            dumpEvents(allEvents)
            return allEvents
        }
    ).catch(function (err) { logError(err); });

    // update one event

    var updateEvent = printWindowEvents.then(
        function (res) {
            // update the first value
            evt = res[0];
            evt = waveDataObj.NextWave(interval, 4.0, 0);
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        console.log("\nUpdating events")
                        return client.updateEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
            }
        }
    ).catch(function (err) { logError(err); });

    // if updating single value successful, then create a list of new values to insert
    createRandomEvents = updateEvent.then(
        function (res) {
            mutliplier = 4.0;
            events = [];
            evtCount = 2;
            var prom = new Promise(function (resolve, reject) {
                callback = resolve;
                totalEvents = 40
                buildEvents();
            });
            return prom;
        }
    ).catch(function (err) { logError(err); });

    // if creating a list of new values successful, then update values in the stream
    var updateEvents = createRandomEvents.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.updateEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
            }
        }
    ).catch(function (err) { logError(err); });

    // get updated events
    getWindowEvents = updateEvents.then(
        function (res) {
            console.log("Getting updated events");
            // get updated values
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }
    ).catch(function (err) { logError(err); });

    var printUpdateEvents = getWindowEvents.then(
        function(res){
            var updatedEvents = JSON.parse(res)
            dumpEvents(updatedEvents)
            return updatedEvents
        }
    ).catch(function (err) { logError(err); });

    // replace events
    var currentEvents;
    var replaceEvent = printUpdateEvents.then(
        function (res) {
            console.log("\nReplacing events");
            var replaceEvent = res[0];
            currentEvents = res;
            replaceEvent.sinProperty = 1/2;
            replaceEvent.cosProperty = Math.sqrt(3)/2;
            replaceEvent.tanProperty = 1;

            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.replaceEvent(tenantId, sampleNamespaceId, sampleStreamId, replaceEvent)
                    }).catch(function (err) { logError(err); });
            } else {
                return client.replaceEvent(tenantId, sampleNamespaceId, sampleStreamId, replaceEvent)
            }
        }
    ).catch(function (err) { logError(err); });

    var replaceEvents = replaceEvent.then(
        function (res) {
            var replaceEvents = currentEvents;
            replaceEvents.forEach(function (elem) {
                elem.Sin = 5.0* 1.0/2.0;
                elem.Cos = 5.0* Math.sqrt(3.0)/2.0;
                elem.Tan = 5.0* 1.0;
            });
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.replaceEvents(tenantId, sampleNamespaceId, sampleStreamId, replaceEvents)
                    }).catch(function (err) { logError(err); });
            } else {
                return client.replaceEvent(tenantId, sampleNamespaceId, sampleStreamId, replaceEvents)
            }
        }
    ).catch(function (err) { logError(err); });
    
    // get replaced events
    var getReplacedEvents = replaceEvents.then(
        function (res) {
            console.log("Getting replaced events");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }
    ).catch(function (err) { logError(err); });


    var printReplaceEvents = getReplacedEvents.then(
        function(res){
            var updatedEvents = JSON.parse(res)
            dumpEvents(updatedEvents)
        }
    ).catch(function (err) { logError(err); });

    // Property Overrides
    var getRangeEvents = printReplaceEvents.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // create a Property Override    
    var propertyOverride = new sdsObjs.SdsPropertyOverride({ "SdsTypePropertyId": "Radians", "InterpolationMode": sdsObjs.sdsStreamMode.Discrete });
    var propertyOverrides = [propertyOverride]

    var printDefaultBehavior = getRangeEvents.then(
        function (res){
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("\nSds can interpolate or extrapolate data at an index location where data does not explicitly exist.");
            console.log("\nDefault (Continuous) requesting data starting at index location '1', where we have not entered data, Sds will interpolate a value for each property:");
            obj.forEach(function (elem) {
                console.log("Order: " + elem.Order +
                            ", Radians: " + elem.Radians + ", Cos : " + elem.Cos);
            });
    });

    // update stream
    var updateStream = printDefaultBehavior.then(
        function (res) {
            sampleStream.PropertyOverrides = propertyOverrides;
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.updateStream(tenantId, sampleNamespaceId, sampleStream);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateStream(tenantId, sampleNamespaceId, sampleStream);
            }
        }
    ).catch(function (err) { logError(err); });

    getRangeEvents = updateStream.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated);
            }
        }
    ).catch(function (err) { logError(err); });

    // print stepwise results
    var printResultEvent = getRangeEvents.then(
        function (res) {
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("\nWe can override this behavior on a property by property basis, here we override the Radians property instructing Sds not to interpolate.");
            console.log("\nSds will now return the default value for the data type:");
            obj.forEach(function (elem) {
                console.log("Order: " + elem.Order +
                            ", Radians: " + elem.Radians + ", Cos: " + elem.Cos);
        });
        return obj;
    });

    // SdsViews
    var viewMessage = printResultEvent.then(  
        function(res){ 
            console.log("\nSdsViews")
            console.log("Here is some of our data as it is stored on the server:");
            res.forEach(function (elem) {
                console.log("Sin: " + elem.Sin +
                            ", Cos: " + elem.Cos  +
                            ", Tan: " + elem.Tan);
            });
    });
   
    // create properties for our target types
    var orderTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "OrderTarget", "SdsType": intType, "IsKey": true });
    var radiansTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "RadiansTarget", "SdsType": doubleType });
    var tauTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "TauTarget", "SdsType": doubleType });
    var sinTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "SinTarget", "SdsType": doubleType });
    var cosTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "CosTarget", "SdsType": doubleType });
    var tanTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "TanTarget", "SdsType": doubleType });
    var sinhTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "SinhTarget", "SdsType": doubleType });
    var coshTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "CoshTarget", "SdsType": doubleType });
    var tanhTargetProperty = new sdsObjs.SdsTypeProperty({ "Id": "TanhTarget", "SdsType": doubleType });

    var sinInt = new sdsObjs.SdsTypeProperty({ "Id": "SinInt", "SdsType": intType });
    var cosInt = new sdsObjs.SdsTypeProperty({ "Id": "CosInt", "SdsType": intType });
    var tanInt = new sdsObjs.SdsTypeProperty({ "Id": "TanInt", "SdsType": intType });

    // build additional types to define our targets
    var integerType = new sdsObjs.SdsType({
        "Id": targetIntegerTypeId, 
        "Name": "WaveDataTargetIntegersJs",
        "Description": "This is a sample Sds type for storing a view of WaveData's sin, cos and tan properties as Integers",
        "SdsTypeCode" : sdsObjs.sdsTypeCode.Object,
        "Properties": [orderTargetProperty, tanInt, cosInt, sinInt]
    });

    var targetType = new sdsObjs.SdsType({
        "Id": targetTypeId, 
        "Name": "WaveDataTargetJs",
        "Description": "This is a sample Sds type for storing a view of WaveData type events",
        "SdsTypeCode" : sdsObjs.sdsTypeCode.Object,
        "Properties": [orderTargetProperty, tauTargetProperty, radiansTargetProperty, sinTargetProperty,
            cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty],
    });

    // create target types on server
    var createTargetType = viewMessage.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createType(tenantId, sampleNamespaceId, targetType);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.createType(tenantId, sampleNamespaceId, targetType);
            }
        }
    ).catch(function (err) { logError(err); });

    var createTargetIntegerType = createTargetType.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createType(tenantId, sampleNamespaceId, integerType);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.createType(tenantId, sampleNamespaceId, integerType);
            }
        }
    ).catch(function (err) { logError(err); });

    // build a view to map our sample type to our target type, as the properties are in the same order and of the same type Sds will do the mapping automatically
    var autoView = new sdsObjs.SdsView({
        "Id": sampleViewId, 
        "Name": "MapSampleTypeToATargetType",     
        "TargetTypeId" : targetTypeId,
        "SourceTypeId" : sampleTypeId
        });
    
    // create view on the server    
    var createAutoView = createTargetIntegerType.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createView(tenantId, sampleNamespaceId, autoView);
                        }).catch(function (err) { logError(err); });
            } else {
                return client.createView(tenantId, sampleNamespaceId, autoView);
            }
        }
    ).catch(function (err) { logError(err); });
 
    // create SdsViewProperties to explicitly map source property to target property 
    var sinViewProperty = new sdsObjs.SdsViewProperty({ "SourceId": "Sin", "TargetId": "SinInt" });
    var cosViewProperty = new sdsObjs.SdsViewProperty({ "SourceId": "Cos", "TargetId": "CosInt" });
    var tanViewProperty = new sdsObjs.SdsViewProperty({ "SourceId": "Tan", "TargetId": "TanInt" });
    
    // build a view using SdsViewProperties
    var manualView = new sdsObjs.SdsView({
        "Id": manualViewId, 
        "Name": "MapSampleTypeToATargetType",     
        "TargetTypeId" : targetIntegerTypeId,
        "SourceTypeId" : sampleTypeId,
        "Properties" : [sinViewProperty, cosViewProperty, tanViewProperty]
    });
    
    // create the view on the server
    var createManualView = createAutoView.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createView(tenantId, sampleNamespaceId, manualView);
                    }).catch(function (err) { logError(err); });
            } else {
                    return client.createView(tenantId, sampleNamespaceId, manualView);
            }
        }
    ).catch(function (err) { logError(err); });

    // get range of values specifying our view
    var getRangeViewEvents = createManualView.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated, autoView.Id);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated, autoView.Id);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // print results
    var dumpViewEvent = getRangeViewEvents.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nSpecifying a view with an SdsType of the same shape returns values that are automatically mapped to the target SdsType's properties:");
            obj.forEach(function (elem) {
                console.log("SinTarget: " + elem.SinTarget +
                            ", CosTarget: " + elem.CosTarget  +
                            ", TanTarget: " + elem.TanTarget);
            });
        }
    ).catch(function (err) { logError(err);});

    // get range of values specifying our integer view
    var getRangeIntegerViewEvents = getRangeViewEvents.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated, manualViewId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated, manualViewId);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // print results
    var dumpIntegerViewEvent = getRangeIntegerViewEvents.then(
            function (res) {
                var obj = JSON.parse(res);
                console.log("\nSdsViews can also convert certain types of data, here we return integers where the original values were doubles:");
                obj.forEach(function (elem) {
                    console.log("SinInt: " + elem.SinInt +
                                ", CosInt: " + elem.CosInt  +
                                ", TanInt: " + elem.TanInt);
            });
        }
    ).catch(function (err) { logError(err);});

    // request maps
    var getAutoSdsViewMap = dumpIntegerViewEvent.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getViewMap(tenantId, sampleNamespaceId, sampleViewId);
                    }).catch(function (err) { logError(err); });
            } else {
                    return client.getViewMap(tenantId, sampleNamespaceId, sampleViewId);
            }
        }
    ).catch(function (err) { logError(err); });

    // print map
    var dumpMapResult = getAutoSdsViewMap.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nWe can query Sds to return the SdsViewMap for our SdsView, here is the one generated automatically:");
            dumpViewMap(obj);
        }
    ).catch(function (err) { logError(err);});

    var getManualSdsViewMap = dumpMapResult.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getViewMap(tenantId, sampleNamespaceId, manualViewId);
                    }).catch(function (err) { logError(err); });
            } else {
                    return client.getViewMap(tenantId, sampleNamespaceId, manualViewId);
            }
        }
    ).catch(function (err) { logError(err); });

    // print map
    dumpMapResult = getManualSdsViewMap.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nHere is our explicit mapping, note SdsViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
            dumpViewMap(obj);
        }
    ).catch(function (err) { logError(err);});   
                
    //tags, metadata and search
    var createTags = dumpMapResult.then( 
        function(res) {
           console.log("\nLet's add some Tags and Metadata to our stream:");
           var tags = [ "waves", "periodic", "2018", "validated" ];
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.updateTags(tenantId, sampleNamespaceId, sampleStreamId, tags);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateTags(tenantId, sampleNamespaceId, sampleStreamId, tags);
            }
        }
    ).catch(function (err) { logError(err); });

    var createMetadata = createTags.then( 
        function(res) {
           var metadata = {Region: "North America", Country: "Canada", Province: "Quebec"};
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.updateMetadata(tenantId, sampleNamespaceId, sampleStreamId, metadata);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateTags(tenantId, sampleNamespaceId, sampleStreamId, metadata);
            }
        }
    ).catch(function (err) { logError(err); });

    var getTags = createMetadata.then( 
        function(res) {
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getTags(tenantId, sampleNamespaceId, sampleStreamId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getTags(tenantId, sampleNamespaceId, sampleStreamId);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // print tags
    var printTags = getTags.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nTags now associated with " + sampleStreamId + ":");
            obj.forEach(function (elem, index) {
                    console.log(elem)               
            });
        }
    ).catch(function (err) { logError(err);});   

    // get metadata
    var getMetadata = printTags.then( 
        function(res) {
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getMetadata(tenantId, sampleNamespaceId, sampleStreamId, "");
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getMetadata(tenantId, sampleNamespaceId, sampleStreamId, "");
            }
        }
    ).catch(function (err) { logError(err); });

    // print metadata
    var printMetadata = getMetadata.then(
        function (res) {
            console.log("\nMetadata now associated with " + sampleStreamId + ":");
            var obj = JSON.parse(res);
            console.log("Metadata key Region: " + obj["Region"])
            console.log("Metadata key Country: " + obj["Country"])
            console.log("Metadata key Province: " + obj["Province"])                           
        }
    ).catch(function (err) { logError(err);});   

    // allow time for search indexing
    var pauseForSearchIndexing = printMetadata.then(
        function (res) {
            console.log("\nPausing to allow for search indexing...")
            return new Promise(resolve => setTimeout(resolve, 15000));
        }
    ).catch(function (err) { logError(err);}); 
    

    var searchForStream = pauseForSearchIndexing.then( 
        function(res) {
           console.log("\nWe can also use our tags to search for streams, let's search for streams tagged with 'periodic':");
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getStreams(tenantId, sampleNamespaceId, "periodic");
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getStreams(tenantId, sampleNamespaceId, "periodic");
            }
        }
    ).catch(function (err) { logError(err); });

    // print search result
    var printResult = searchForStream.then(
        function (res) {
            var obj = JSON.parse(res);
            if(obj)
            {
                obj.forEach(function (elem) {
                    console.log(elem.Id)
                })
            }                           
        }
    ).catch(function (err) { logError(err);});

    //delete an event
    var deleteOneEvent = printResult.then( 
        function(res) {
           console.log("\nDeleting values from the SdsStream");
           if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteEvent(tenantId, sampleNamespaceId, sampleStreamId, 0);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteEvent(tenantId, sampleNamespaceId, sampleStreamId, 0);
            }
        }
    ).catch(function (err) { logError(err); });

    // delete all events
    var deleteWindowEvents = deleteOneEvent.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteWindowEvents(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteWindowEvents(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }
    ).catch(function (err) { logError(err); });

    // One catch to rule all the errors
    var testFinished = deleteWindowEvents.then(
        function (res) {
            console.log("All values deleted successfully!");
        }
    ).catch(function (err) { logError(err) });

    // cleanup of namespace 
    var cleanup = testFinished
    .finally(
        // delete the stream
        function () {
            console.log("Cleaning up");
			console.log("Deleting the stream");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteStream(tenantId, sampleNamespaceId, sampleStreamId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteStream(tenantId, sampleNamespaceId, sampleStreamId);
            }
    }).finally( 
        function () {
            console.log("Deleting the views");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        client.deleteView(tenantId, sampleNamespaceId, sampleViewId);
                        return client.deleteView(tenantId, sampleNamespaceId, manualViewId);
                    }).catch(function (err) { logError(err); });
            } else {
                client.deleteView(tenantId, sampleNamespaceId, sampleViewId);
                return client.deleteView(tenantId, sampleNamespaceId, manualViewId);
            }
    }).finally(
        // delete the types
        function () {
            console.log("Deleting the types");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        client.deleteType(tenantId, sampleNamespaceId, targetIntegerTypeId);
                        client.deleteType(tenantId, sampleNamespaceId, targetTypeId);
                        return client.deleteType(tenantId, sampleNamespaceId, sampleTypeId);
                    }).catch(function (err) { logError(err); });
            } else {
                client.deleteType(tenantId, sampleNamespaceId, targetIntegerTypeId);
                client.deleteType(tenantId, sampleNamespaceId, targetTypeId);
                return client.deleteType(tenantId, sampleNamespaceId, sampleTypeId);
            }
    }).then(
        function () {
            console.log("done");
    }).catch(
        // log the call that failed
        function (err) {
            console.log("An error occured!\n" + err);
    });
    
    response.end();

}).listen(8080);
console.log("Server is listening at http://localhost:8080/");
console.log("Sds endpoint at " + SdsServerUrl);
