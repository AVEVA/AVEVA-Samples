'use strict';
angular.module('qisampleApp')
    .controller('qiController', ['$scope', 'QiService', '$timeout', 'adalAuthenticationService', 'QiObjects',
function ($scope, QiService, $timeout, adalService, QiObjects) {
            $scope.error = "";
            $scope.loadingMessage = "Loading...";
            $scope.namespacesList = [];

            $scope.printSelected = null;
            $scope.selectedNSitem = null;
            $scope.namespaceId = "WaveData_SampleNamespace";
            $scope.typeId = "WaveData_SampleType";
            $scope.typeList = [];
            $scope.message = "Click the button";
            $scope.sampleStreamId = "WaveData_SampleStream";
            $scope.step2msg = null;
            $scope.step4Msg = null;
            $scope.step6Msg = null;
            $scope.step3Msg = null;
            $scope.step1msg = null;
            $scope.step5Msg = null;
            $scope.step7Msg = null;
            
            var consoleMsg = "To view the result of this operation, open the console by pressing F12.";
            var bHasTypes = false;
            var sampleNamespaceId = "WaveData_SampleNamespace";
            var sampleTypeId = "WaveData_SampleType";
            var sampleStreamId = "WaveData_SampleStream";
            var sampleBehaviorId = "WaveData_SampleBehavior";

            var doubleType = new QiObjects.QiType({ "Id": "doubleType", "QiTypeCode": QiObjects.qiTypeCodeMap.Double });
            var intType = new QiObjects.QiType({ "Id": "intType", "QiTypeCode": QiObjects.qiTypeCodeMap.Int32 });

            var orderProperty = new QiObjects.QiTypeProperty({ "Id": "Order", "QiType": intType, "IsKey": true });

            var radiansProperty = new QiObjects.QiTypeProperty({ "Id": "Radians", "QiType": doubleType });

            var tauProperty = new QiObjects.QiTypeProperty({ "Id": "Tau", "QiType": doubleType });
            var sinProperty = new QiObjects.QiTypeProperty({ "Id": "Sin", "QiType": doubleType });
            var cosProperty = new QiObjects.QiTypeProperty({ "Id": "Cos", "QiType": doubleType });
            var tanProperty = new QiObjects.QiTypeProperty({ "Id": "Tan", "QiType": doubleType });
            var sinhProperty = new QiObjects.QiTypeProperty({ "Id": "Sinh", "QiType": doubleType });
            var coshProperty = new QiObjects.QiTypeProperty({ "Id": "Cosh", "QiType": doubleType });
            var tanhProperty = new QiObjects.QiTypeProperty({ "Id": "Tanh", "QiType": doubleType });

            var sampleNamespace = new QiObjects.QiNamespace({ "Id": sampleNamespaceId });
            var sampleBehaviorId = "WaveData_SampleBehavior";

            var tenantId = adalService.userInfo.profile.tid;

            var sampleType = new QiObjects.QiType({
                "Id": sampleTypeId, "Name": "WaveDataJs",
                "Description": "This is a sample Qi type for storing WaveData type events",
                "Properties": [orderProperty, tauProperty, radiansProperty, sinProperty,
               cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]
            });

            var sampleStream = new QiObjects.QiStream({
                "Id": sampleStreamId, "Name": "WaveStreamJs",
                "Description": "A Stream to store the WaveData Qi types events",
                "TypeId": sampleTypeId
            });

          

            var sampleBehavior = new QiObjects.QiBehavior({ "Mode": QiObjects.qiStreamMode.Continuous });
            sampleBehavior.Id = sampleBehaviorId;
            sampleBehavior.Mode = QiObjects.qiStreamMode.StepwiseContinuousLeading;

    /*********************************Button Click Functions**************************************/

            $scope.click_Step1 = function () {
                try
                {

                    /*var namespace_Result, type_Result, stream_Result, value_Result, values_Result;
                    namespace_Result = createNameSpace();
                    
                    type_Result = namespace_Result.then(
                      function (res) {
                             return $timeout(function () {return createType(); }, 2000);
                    });

                    stream_Result = type_Result.then(
                      function (res) {
                          return $timeout(function () { return createStream(); }, 2000);
                      });

                    value_Result = stream_Result.then(
                      function (res) {
                          return $timeout(function () { return insertValue(); }, 2000);
                      });

                    values_Result = value_Result.then(
                      function (res) {
                          return $timeout(function () { return insertValues(); }, 2000);
                      });*/
                        
                    cleanMessages();
                    createNameSpace();
                    $timeout(function () { createType(); }, 2000);
                    $timeout(function () { createStream(); }, 5000);
                    $timeout(function () { insertValue(); }, 8000);
                    $timeout(function () { insertValues(); }, 8000);
                    $scope.step1msg = consoleMsg;
                }
                catch (err) {
                    $scope.step1msg = "Create and insert failed. Please open console for detailed error.";
                    console.log(err.message);
                }
            }

            $scope.click_Step2 = function () {
                cleanMessages();
                getValue().then(
                    function(res){
                        $scope.step2msg = "Events successfully recieved";
                    },
                    function(err){
                        $scope.step2msg = "Events recieve failed. Please check logs";
                    });
            }

            $scope.click_Step3 = function () {
                cleanMessages();
                updateValue();
                updateValues();
            }

            
            $scope.click_Step4 = function () {
                cleanMessages();
                getValue().then(
                    function (res) {
                        $scope.step4Msg = "Events successfully recieved";
                    },
                    function (err) {
                        $scope.step4Msg = "Events recieve failed. Please check logs";
                    });
            }

            $scope.click_Step5 = function () {
                cleanMessages();
                createBehavior();
                $scope.step5Msg= "Add Behavior call sent. Please check logs for details."
            }

            $scope.click_Step6 = function () {
                cleanMessages();
                getRangeValue().then(
                    function (res) {
                        $scope.step6Msg = "Events successfully recieved";
                    },
                    function (err) {
                        $scope.step6Msg = "Events recieve failed. Please check logs";
                    });
            }

            $scope.click_Step7 = function () {
                try {
                    cleanMessages();
                    removeValues();
                    $timeout(function () { deleteStream(); }, 3000);
                    $timeout(function () { deleteBehavior(); }, 6000);
                    $timeout(function () { deleteType(); }, 9000);

                    $scope.step7sg = consoleMsg;
                }
                catch (err) {
                    $scope.step7Msg = "Cleanup failed. Please open console for detailed error.";
                    console.log(err);
                }
            }

    /*********************************Helper Functions**************************************/
            //prints all the events in obj
            var dumpEvents = function (obj) {
                var evt = "";
                obj.forEach(function (elem, index) {
                    evt += "Event No. " + index + " : {" + "Order: " + elem.Order +
                        " Tau: " + elem.Tau +
                        " Radians: " + elem.Radians +
                        " Sin: " + elem.Sin +
                        " Cos: " + elem.Cos +
                        " Tan: " + elem.Tan +
                        " Sinh: " + elem.Sinh +
                        " Cosh: " + elem.Cosh +
                        " Tanh:" + elem.Tanh + "}\r\n";
                   
                });
                console.log(evt);
            };

            //sets all the messages to null
            var cleanMessages = function () {
                $scope.step1msg = null;
                $scope.step2Msg = null;
                $scope.step3Msg = null;
                $scope.step4Msg = null;
                $scope.step5msg = null;
                $scope.step6Msg = null;
                $scope.step7Msg = null;
            }

            //tries to get the namespace if it fails, it creates the namespace
            var createNameSpace = function () {
                var nsp = QiObjects.Nam
                var namespace;
                console.log("Creating Namespace...");
                namespace = QiService.getNamespace(tenantId, sampleNamespace.Id)
                namespace.then(function (res1) {
                   
                    if (res1.data.Id == null) {
                        namespace = QiService.getOrCreateNameSpace(tenantId, sampleNamespace)
                            namespace.then(function (res1) {
                            console.log("Namespace created");
                            
                            });
                            return namespace;
                    }
                    else {
                        console.log("Namespace found");
                        return namespace;
                    }
                }, function (error) {
                    namespace = QiService.getOrCreateNameSpace(tenantId, sampleNamespace)
                    namespace.then(function (res1) {
                        console.log("Namespace created");

                    }, function (error) {
                        console.log("Error creating namespace "+ error)
                    });

                });
                return namespace;
                
            };

            //tries to get the type, if it doesn't exist it creates one
            var createType = function () {
                var nsp = QiObjects.Nam
                var type;
                console.log("Creating Type...");
                type = QiService.getType(tenantId, $scope.namespaceId, sampleTypeId)
                type.then(function (res1) {
                    if (res1.data.Id == null) {
                        type = QiService.getorCreateTypes(tenantId, $scope.namespaceId, sampleType)
                        type.then(function (res1) {
                            console.log("Type created");
                        });
                        return type;
                    }

                    else {
                        console.log("Type found");
                        return type;
                    }
                    return type;
                  
                }, function (error) {
                    type = QiService.getorCreateTypes(tenantId, $scope.namespaceId, sampleType)
                    type.then(function (res1) {
                        console.log("Type created");
                        return type;
                    });
                    
                }, function (error) {
                    console.log("Error in create type: " + error);
                });

                return type;

            };

            
            var deleteType= function () {
                var result;
                console.log("Deleting Type...");
                return QiService.deleteType(tenantId, $scope.namespaceId, sampleTypeId).then(function (res1) {
                    console.log("Type Deleted");
                });
            };

            var createStream = function () {
               
                var stream;
                console.log("Creating stream...");
                return QiService.createStream(tenantId, $scope.namespaceId, sampleStream).then(function (res1) {
                    stream = res1.data;
                    if (stream != null) {
                        console.log("Stream Created");
                    }
                });
            };

            var deleteStream = function () {
                var stream;
                console.log("Deleting stream...");
                return QiService.deleteStream(tenantId, $scope.namespaceId, sampleStreamId).then(function (res1) {
                    console.log("Stream Deleted");
                });
            };


            var interval = new Date();
            interval.setHours(0, 1, 0, 0);
            var evt = null;

            var insertValue = function () {
                console.log("Inserting value...");
                evt = QiObjects.NextWave(interval, 2.0, 0);
                return QiService.insertValue(tenantId, sampleNamespaceId, sampleStreamId, evt).then(function (res1) {
                console.log("One event added");
                });

            };

            //creates the events and inserts it
            var insertValues = function () {
                var events = [];
                var evt;
                var i;
                console.log("Inserting values...");
                for (i = 2; i < 200; i += 2)
                {
                    evt = QiObjects.NextWave(interval, 2.0, i);
                    events.push(evt);
                }

                return QiService.insertValues(tenantId, sampleNamespaceId, sampleStreamId, events).then(function (res1) {

                    console.log("Multiple events added");

                });

            };

            var getValue = function () {
                console.log("Getting values...");
                var events = [];
                return QiService.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, "0", "198").then(function (res1) {
                    events = res1.data;
                    var i;

                    console.log("Get Windows Success " + events.length);
                    dumpEvents(events);
                   
                },
                
                function(err){
                    console.log("Get Window Values Failed");
                    return false;
                });
               

            };

            var getRangeValue = function () {
                var events = [];
                console.log("Getting range values..");
                return QiService.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", QiObjects.qiBoundaryType.ExactOrCalculated).then(function (res1) {
                    events = res1.data;
                    var i;

                    console.log("Get Range Values Success " + events.length);
                    dumpEvents(events);

                },

                function (err) {
                    console.log("Get Range Values Failed");
                    return false;
                });
            }

            var updateValue = function () {
                evt = QiObjects.NextWave(interval, 4.0, 0);

                return QiService.updateValue(tenantId, sampleNamespaceId, sampleStreamId, evt).then(function (res1) {
                    console.log("1 Event updated");
                });

            };

            var updateValues = function () {
                var events = [];
                var evt;
                var i;
                for (i = 2; i < 200; i += 2) {
                    evt = QiObjects.NextWave(interval, 2.0, i);
                    events.push(evt);
                }

                return QiService.updateValues(tenantId, sampleNamespaceId, sampleStreamId, events).then(function (res1) {
                    console.log(evt.length + " events updated");
                });

            };

            var createBehavior = function () {
                QiService.createBehavior(tenantId, $scope.namespaceId, sampleBehavior).then(function (res1) {
                    sampleStream.BehaviorId = sampleBehaviorId;
                    return QiService.updateStream(tenantId, $scope.namespaceId, sampleStream).then(function (res1) {
                        console.log("Behavior Added");
                    });
                });

            };

            var deleteBehavior = function () {
                var stream;
                return QiService.deleteBehavior(tenantId, $scope.namespaceId, sampleBehaviorId).then(function (res1) {
                    console.log("Behavior Deleted");
                });
            };

            var removeValues = function () {
               
                QiService.removeValue(tenantId, $scope.namespaceId, sampleStreamId, "0").then(function (res1) {
                    console.log("One event removed")
                   
                 });

                QiService.removeWindowValues(tenantId, $scope.namespaceId, sampleStreamId, "1", "198").then(function (res1) {
                    console.log("All events removed")
                });

            };

            var getType = function () {
                return QiService.getType(tenantId, $scope.namespaceId, sampleType);
            };

            var populateTypes = function () {
                if (bHasTypes = true) {
                    QiService.getTypes(tenantId, $scope.namespaceId).then(function (res1) {
                        $scope.typeList = res1.data;
                    });
                    return true;
                }
                else {
                    return false;
                }
            };

        
    }]);
