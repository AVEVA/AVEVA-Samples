var http = require("http");
var restCall = require("request-promise");
var config = require("./config.js");

// retrieve configuration
var QiServerUrl = config.qiServerUrl;
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
        console.log("Qi Object already present in the Service\n");
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

    response.write("---------------------------------------------------------------\n");
    response.write("________  .__ _______             .___               __        \n");
    response.write("\\_____  \\ |__|\\      \\   ____   __| _/____          |__| ______\n");
    response.write(" /  / \\  \\|  |/   |   \\ /  _ \\ / __ |/ __ \\         |  |/  ___/\n");
    response.write("/   \\_/.  \\  /    |    (  <_> ) /_/ \\  ___/         |  |\\___ \\ \n");
    response.write("\\_____\\ \\_/__\\____|__  /\\____/\\____ |\\___  > /\\ /\\__|  /____  >\n");
    response.write("       \\__>          \\/            \\/    \\/  \\/ \\______|    \\/ \n");
    response.write("---------------------------------------------------------------\n");
    response.write("Qi Service Operations Begun!\n");
    response.write("Check the console for updates")

    var qiObjs = require("./QiObjects.js");
    var clientObj = require("./QiClient.js");
    var waveDataObj = require("./WaveData.js");

    var sampleNamespaceId = config.namespaceId;
    var sampleTypeId = "WaveData_SampleType";
    var sampleStreamId = "WaveData_SampleStream";
    var sampleBehaviorId = "WaveData_SampleBehavior";
    var sampleViewId = "WaveData_SampleView"
    var targetTypeId = "targetTypeId";
    var targetIntegerTypeId = "targetIntegerTypeId"
    var manualViewId = "WaveData_ManualView"

    Object.freeze(qiObjs.qiTypeCode);
    Object.freeze(qiObjs.qiBoundaryType);
    Object.freeze(qiObjs.qiStreamMode);

    // define basic QiTypes
    var doubleType = new qiObjs.QiType({ "Id": "doubleType", "QiTypeCode": qiObjs.qiTypeCode.Double });
    var intType = new qiObjs.QiType({ "Id": "intType", "QiTypeCode": qiObjs.qiTypeCode.Int32 });

    // define properties
    var orderProperty = new qiObjs.QiTypeProperty({ "Id": "Order", "QiType": intType, "IsKey": true });
    var radiansProperty = new qiObjs.QiTypeProperty({ "Id": "Radians", "QiType": doubleType });
    var tauProperty = new qiObjs.QiTypeProperty({ "Id": "Tau", "QiType": doubleType });
    var sinProperty = new qiObjs.QiTypeProperty({ "Id": "Sin", "QiType": doubleType });
    var cosProperty = new qiObjs.QiTypeProperty({ "Id": "Cos", "QiType": doubleType });
    var tanProperty = new qiObjs.QiTypeProperty({ "Id": "Tan", "QiType": doubleType });
    var sinhProperty = new qiObjs.QiTypeProperty({ "Id": "Sinh", "QiType": doubleType });
    var coshProperty = new qiObjs.QiTypeProperty({ "Id": "Cosh", "QiType": doubleType });
    var tanhProperty = new qiObjs.QiTypeProperty({ "Id": "Tanh", "QiType": doubleType });

    //create a QiType for WaveData Class
    var sampleType = new qiObjs.QiType({
        "Id": sampleTypeId, "Name": "WaveDataJs",
        "Description": "This is a sample Qi type for storing WaveData type events",
        "QiTypeCode" : qiObjs.qiTypeCode.Object,
        "Properties": [orderProperty, tauProperty, radiansProperty, sinProperty,
            cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]
    });

    var client = new clientObj.QiClient(QiServerUrl);

    var getClientToken = client.getToken(authItems)
        .catch(function (err) { throw err });

    var nowSeconds = function () { return Date.now() / 1000; };

    // create a QiType
    console.log("\nCreating a QiType")
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

    //create a QiStream
    console.log("Creating a QiStream")
    var sampleStream = new qiObjs.QiStream({
        "Id": sampleStreamId, "Name": "WaveStreamJs",
        "Description": "A Stream to store the WaveData Qi types events",
        "TypeId": sampleTypeId
        });

    var createStream = createType.then(
        function (res) {
            // create QiStream
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

    // QiStreamBehaviors
    var getRangeEvents = printReplaceEvents.then(
        function (res) {
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // create a QiBehavior    
    var sampleBehavior = new qiObjs.QiBehavior({ "Mode": qiObjs.qiStreamMode.Discrete });
    sampleBehavior.Id = sampleBehaviorId;
    sampleBehavior.ExtrapolationMode = qiObjs.qiBoundaryType.Continuous;

    var printDefaultBehavior = getRangeEvents.then(
        function (res){
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("\nQiStreamBehaviors determine whether Qi interpolates or extrapolates data at the requested index location");
            console.log("\nDefault (Continuous) stream behavior, requesting data starting at index location '1', Qi will interpolate this value:");
            obj.forEach(function (elem) {
                console.log("Order: " + elem.Order +
                            ", Radians: " + elem.Radians);
            });
    });

    var createBehavior = printDefaultBehavior.then(
        function (res) {
            // create behavior
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createBehavior(tenantId, sampleNamespaceId, sampleBehavior);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.createBehavior(tenantId, sampleNamespaceId, sampleBehavior);
            }
        }
    ).catch(function (err) { logError(err); });

    // update stream
    var updateStream = createBehavior.then(
        function (res) {
            sampleStream.BehaviorId = sampleBehaviorId;
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
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
            }
        }
    ).catch(function (err) { logError(err); });

    // print stepwise results
    var printResultEvent = getRangeEvents.then(
        function (res) {
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("\nDiscrete stream behavior, Qi does not interpolate and returns the data starting at the next index location containing data:");
            obj.forEach(function (elem) {
                console.log("Order: " + elem.Order +
                            ", Radians: " + elem.Radians);
        });
        return obj;
    });

    // QiViews
    var viewMessage = printResultEvent.then(  
        function(res){ 
            console.log("\nQiViews")
            console.log("Here is some of our data as it is stored on the server:");
            res.forEach(function (elem) {
                console.log("Sin: " + elem.Sin +
                            ", Cos: " + elem.Cos  +
                            ", Tan: " + elem.Tan);
            });
    });
   
    // create properties for our target types
    var orderTargetProperty = new qiObjs.QiTypeProperty({ "Id": "OrderTarget", "QiType": intType, "IsKey": true });
    var radiansTargetProperty = new qiObjs.QiTypeProperty({ "Id": "RadiansTarget", "QiType": doubleType });
    var tauTargetProperty = new qiObjs.QiTypeProperty({ "Id": "TauTarget", "QiType": doubleType });
    var sinTargetProperty = new qiObjs.QiTypeProperty({ "Id": "SinTarget", "QiType": doubleType });
    var cosTargetProperty = new qiObjs.QiTypeProperty({ "Id": "CosTarget", "QiType": doubleType });
    var tanTargetProperty = new qiObjs.QiTypeProperty({ "Id": "TanTarget", "QiType": doubleType });
    var sinhTargetProperty = new qiObjs.QiTypeProperty({ "Id": "SinhTarget", "QiType": doubleType });
    var coshTargetProperty = new qiObjs.QiTypeProperty({ "Id": "CoshTarget", "QiType": doubleType });
    var tanhTargetProperty = new qiObjs.QiTypeProperty({ "Id": "TanhTarget", "QiType": doubleType });

    var sinInt = new qiObjs.QiTypeProperty({ "Id": "SinInt", "QiType": intType });
    var cosInt = new qiObjs.QiTypeProperty({ "Id": "CosInt", "QiType": intType });
    var tanInt = new qiObjs.QiTypeProperty({ "Id": "TanInt", "QiType": intType });

    // build additional types to define our targets
    var integerType = new qiObjs.QiType({
        "Id": targetIntegerTypeId, 
        "Name": "WaveDataTargetIntegersJs",
        "Description": "This is a sample Qi type for storing a view of WaveData's sin, cos and tan properties as Integers",
        "QiTypeCode" : qiObjs.qiTypeCode.Object,
        "Properties": [orderTargetProperty, tanInt, cosInt, sinInt]
    });

    var targetType = new qiObjs.QiType({
        "Id": targetTypeId, 
        "Name": "WaveDataTargetJs",
        "Description": "This is a sample Qi type for storing a view of WaveData type events",
        "QiTypeCode" : qiObjs.qiTypeCode.Object,
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

    // build a view to map our sample type to our target type, as the properties are in the same order and of the same type Qi will do the mapping automatically
    var autoView = new qiObjs.QiView({
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
 
    // create QiViewProperties to explicitly map source property to target property 
    var sinViewProperty = new qiObjs.QiViewProperty({ "SourceId": "Sin", "TargetId": "SinInt" });
    var cosViewProperty = new qiObjs.QiViewProperty({ "SourceId": "Cos", "TargetId": "CosInt" });
    var tanViewProperty = new qiObjs.QiViewProperty({ "SourceId": "Tan", "TargetId": "TanInt" });
    
    // build a view using QiViewProperties
    var manualView = new qiObjs.QiView({
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
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated, autoView.Id);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated, autoView.Id);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // print results
    var dumpViewEvent = getRangeViewEvents.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nSpecifying a view with a QiType of the same shape returns values that are automatically mapped to the target QiType's properties:");
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
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated, manualViewId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated, manualViewId);
            }
        }
    ).catch(function (err) { logError(err); });
    
    // print results
    var dumpIntegerViewEvent = getRangeIntegerViewEvents.then(
            function (res) {
                var obj = JSON.parse(res);
                console.log("\nQiViews can also convert certain types of data, here we return integers where the original values were doubles:");
                obj.forEach(function (elem) {
                    console.log("SinInt: " + elem.SinInt +
                                ", CosInt: " + elem.CosInt  +
                                ", TanInt: " + elem.TanInt);
            });
        }
    ).catch(function (err) { logError(err);});

    // request maps
    var getAutoQiViewMap = dumpIntegerViewEvent.then(
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
    var dumpMapResult = getAutoQiViewMap.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nWe can query Qi to return the QiViewMap for our QiView, here is the one generated automatically:");
            dumpViewMap(obj);
        }
    ).catch(function (err) { logError(err);});

    var getManualQiViewMap = dumpMapResult.then(
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
    dumpMapResult = getManualQiViewMap.then(
        function (res) {
            var obj = JSON.parse(res);
            console.log("\nHere is our explicit mapping, note QiViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
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
           console.log("\nDeleting values from the QiStream");
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
    }).finally(
            // delete the behavior
        function () {
            console.log("Deleting the behavior");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteBehavior(tenantId, sampleNamespaceId, sampleBehaviorId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteBehavior(tenantId, sampleNamespaceId, sampleBehaviorId);
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
console.log("Qi endpoint at " + QiServerUrl);