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

var dumpEvents = function (obj) {
    obj.forEach(function (elem, index) {
        console.log("Event No. " + index + " : {" + "Order: " + elem.Order +
            " Tau: " + elem.Tau +
            " Radians: " + elem.Radians +
            " Sin: " + elem.Sin +
            " Cos: " + elem.Cos +
            " Tan: " + elem.Tan +
            " Sinh: " + elem.Sinh +
            " Cosh: " + elem.Cosh +
            " Tanh:" + elem.Tanh + "}");
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
    response.write("Qi Service Operations Begun!\n");
    response.write("Check the console for updates")

    var qiObjs = require("./QiObjects.js");
    var clientObj = require("./QiClient.js");
    var waveDataObj = require("./WaveData.js");

    var sampleNamespaceId = config.namespaceId;
    var sampleTypeId = "WaveData_SampleType";
    var sampleStreamId = "WaveData_SampleStream";
    var sampleBehaviorId = "WaveData_SampleBehavior";

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
        "Properties": [orderProperty, tauProperty, radiansProperty, sinProperty,
            cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]
    });

    var client = new clientObj.QiClient(QiServerUrl);

    var getClientToken = client.getToken(authItems)
        .catch(function (err) { throw err });

    var nowSeconds = function () { return Date.now() / 1000; };

    // if get token successful, then create a QiType
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
        })
        .catch(function (err) { logError(err); });

    //create a stream object
    var sampleStream = new qiObjs.QiStream({
        "Id": sampleStreamId, "Name": "WaveStreamJs",
        "Description": "A Stream to store the WaveData Qi types events",
        "TypeId": sampleTypeId
    });

    // if getting all types successful, list types, then create a QiStream
    var createStream = createType.then(
        function (res) {
            console.log("Type creation successful");
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

    //creating an event
    var interval = new Date();
    interval.setHours(0, 1, 0, 0);
    var evt = null;

    // if getting all streams successful, list streams, then insert a value
    var insertValue = createStream.then(
        function (res) {
            console.log("Stream creation successful");
            // insert value
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
        }).catch(function (err) { logError(err); });

    // create multiple events and insert
    var events = [];
    var evt1 = null;
    // minimize delay to hurry up the generation
    var delay = 50;
    var evtCount = 2;
    var mutliplier = 2;
    var callback = null;

    var loopDelay = function () {
        setTimeout(function () {
            if (evtCount < 200) {
                evt1 = waveDataObj.NextWave(interval, mutliplier, evtCount);
                events.push(evt1);
                process.stdout.clearLine();
                process.stdout.cursorTo(0);
                process.stdout.write("Total random events " + evtCount);
                evtCount += 2;
                loopDelay();
            } else {
                callback();
            }
        }, delay);
    };

    // if inserting one value successful, then create a list of random values
    var createRandomEvents = insertValue.then(
        function (res) {
            console.log("Single event insert successful");
            console.log("Artificially generating 99 events and inserting them into the Qi Service");
            console.log("Generating random events...");
            var prom = new Promise(function (resolve, reject) {
                callback = resolve;
                loopDelay();
            });
            return prom;

        }).catch(function (err) { logError(err); });

    // if creating a list of values successful, then insert the generated values
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
        }).catch(function (err) { logError(err); });

    // if insertin multiple values successful, then get the last value to be added
    var getLastValue = insertMultipleValues.then(
        function(res) {
            // if insert passed list all events
            console.log("\nMultiple events insertion successful");
            // get last value
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function(res) {
                        refreshToken(res, client);
                        return client.getLastValue(tenantId, sampleNamespaceId, sampleStreamId);
                    }).catch(function(err) { logError(err); });
            } else {
                return client.getLastValue(tenantId, sampleNamespaceId, sampleStreamId);
            }
        }).catch(function(err) { logError(err); });

    // if getting last value successful, then get the values in stream using get window
    var getWindowEvents = getLastValue.then(
        function (res) {
            console.log("Get last value successful");
            // get window of values
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }).catch(function (err) { logError(err); });


    // if getting window of values successful, then update a single value in stream
    var foundEvents;
    var updateEvent = getWindowEvents.then(
        function (res) {
            // list found values
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("Event window retrieval successful");
            dumpEvents(obj);
            // update the first value
            evt = foundEvents[0];
            evt = waveDataObj.NextWave(interval, 4.0, 0);
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.updateEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.updateEvent(tenantId, sampleNamespaceId, sampleStreamId, evt);
            }
        }).catch(function (err) { logError(err); });

    // if updating single value successful, then create a list of new values to insert
    createRandomEvents = updateEvent.then(
        function (res) {
            console.log("Single event update successful");
            console.log("Creating new events...");
            mutliplier = 4.0;
            events = [];
            evtCount = 2;
            var prom = new Promise(function (resolve, reject) {
                callback = resolve;
                loopDelay();
            });
            return prom;
        }).catch(function (err) { logError(err); });

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
        }).catch(function (err) { logError(err); });

    // if updating values in the stream successful, then get the update values using get window of values
    getWindowEvents = updateEvents.then(
        function (res) {
            // if insert passed list all events
            console.log("\nMultiple events update successful");
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
        }).catch(function (err) { logError(err); });

    // if getting updated values successful, list updated values, then get three values using get range of values
    var getRangeEvents = getWindowEvents.then(
        function (res) {
            // list updated events
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("Event window retrieval successful");
            dumpEvents(obj);
            // get range of values
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
            }
        }).catch(function (err) { logError(err); });

    // create a QiBehavior
    var sampleBehavior = new qiObjs.QiBehavior({ "Mode": qiObjs.qiStreamMode.StepwiseContinuousLeading });
    sampleBehavior.Id = sampleBehaviorId;
    sampleBehavior.ExtrapolationMode = qiObjs.qiBoundaryType.Continuous;

    // if getting a range of values successful, list found values, then create a QiBehavior
    var createBehavior = getRangeEvents.then(
        function (res) {
            // list found values
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("Event range retrieval successful");
            dumpEvents(obj);
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
        }).catch(function (err) { logError(err); });

    // if creating a behavior successful, then update stream with the behavior
    var updateStream = createBehavior.then(
        function (res) {
            console.log("Behavior creation successful");
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
        }).catch(function (err) { logError(err); });

    // if updating stream behavior successful, get a range of values
    getRangeEvents = updateStream.then(
        function (res) {
            console.log("Stream update successful");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
            }
        }).catch(function (err) { logError(err); });

    // if getting range of values successful, then delete one event
    var deleteEvent = getRangeEvents.then(
        function (res) {
            var obj = JSON.parse(res);
            foundEvents = obj;
            console.log("Retrieval of three events with a stepwise stream behavior in effect successful -- compare to last retrieval");
            dumpEvents(obj);
            //delete an event
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteEvent(tenantId, sampleNamespaceId, sampleStreamId, 0);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteEvent(tenantId, sampleNamespaceId, sampleStreamId, 0);
            }
        }).catch(function (err) { logError(err); });

    // if deleting one event successful, then delete multiple events
    var deleteWindowEvents = deleteEvent.then(
        function (res) {
            console.log("Single event deletion successful");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteWindowEvents(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteWindowEvents(tenantId, sampleNamespaceId, sampleStreamId, 0, 198);
            }
        }).catch(function (err) { logError(err); });

    // One catch to rule all the errors
    var testFinished = deleteWindowEvents.then(function (res) {
        console.log("Multiple events deletion successful");
        console.log("\n------Test successful!------");
    }).catch(function (err) { logError(err) });

    // cleanup of namespace 
    var cleanup = testFinished
        .finally(
        // delete the stream
        function () {
            console.log("Cleaning up...");
			console.log("Deleting stream");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteStream(tenantId, sampleNamespaceId, sampleStreamId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteStream(tenantId, sampleNamespaceId, sampleStreamId);
            }
        })
        .finally(
        // delete the type
        function () {
            console.log("Deleting type");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteType(tenantId, sampleNamespaceId, sampleTypeId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteType(tenantId, sampleNamespaceId, sampleTypeId);
            }
        })
        .finally(
        // delete the behavior
        function () {
            console.log("Deleting behavior");
            if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client).then(
                    function (res) {
                        refreshToken(res, client);
                        return client.deleteBehavior(tenantId, sampleNamespaceId, sampleBehaviorId);
                    }).catch(function (err) { logError(err); });
            } else {
                return client.deleteBehavior(tenantId, sampleNamespaceId, sampleBehaviorId);
            }
        })
        .then(
        function () {
            console.log("Behavior deletion successful");
            console.log("------Sample Finished-------");
        })
        .catch(
        // log the call that failed
        function (err) {
            console.log("An error occured!\n" + err);
        });

    response.end();
}).listen(8080);
console.log("Server is listening at http://localhost:8080/");
