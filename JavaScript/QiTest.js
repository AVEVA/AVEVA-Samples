var http = require("http");
var restCall = require("request-promise");

//change these values to the credentials given
var QiServerUrl = "https://qi-data.osisoft.com:3380";
var authItems = {'resource' : "RESOURCE-URL",
	             'authority' : "https://login.windows.net/TENANT-URL/oauth2/token",
	             'appId' : "CLIENT-ID",
	             'appKey' : "CLIENT-KEY"};


var logError = function(err){
								if((typeof(err.statusCode) !== "undefined" && err.statusCode != 302) || 
								(typeof(err.StatusCodeError) !== "undefined" && err.StatusCodeError != 302)){
									//console.log("Error Status : " + (typeof(err.statusCode) !== "undefined" ? err.statusCode:err.StatusCodeError) +", Msg : "+err.message);
									throw err;
								}else{
									console.log("Qi Object already present in the Service\n");
								}
};

var checkTokenExpired = function(client){
								return client.getToken(authItems)
									.catch(function(err){logError(err)});
};

var refreshToken = function(res, client){
								var obj = JSON.parse(res);
								client.token = obj.access_token;
								client.tokenExpires = obj.expires_on;
};

http.createServer(function(request1, response) { 
	if(request1.url == '/favicon.ico'){
		return;
	}
	response.writeHead(200, {"Content-Type": "text/plain"});  
	response.write("Qi Service Operations Begun!\n");
	response.write("Check the console for updates")

	var qiObjs = require("./QiObjects.js");
	var clientObj = require("./QiClient.js");
	
	Object.freeze(qiObjs.qiTypeCodeMap);
	Object.freeze(qiObjs.qiBoundaryType);
	Object.freeze(qiObjs.qiStreamMode);

	var doubleType = new qiObjs.QiType({"Id" : "doubleType", "QiTypeCode" :  qiObjs.qiTypeCodeMap.Double});
	var intType = new qiObjs.QiType({"Id" : "intType", "QiTypeCode" :  qiObjs.qiTypeCodeMap.Int32});

	var orderProperty = new qiObjs.QiTypeProperty({"Id" : "Order", "QiType" : intType, "IsKey" : true});

	var radiansProperty = new qiObjs.QiTypeProperty({"Id" : "Radians", "QiType" : doubleType});

	var tauProperty = new qiObjs.QiTypeProperty({"Id" : "Tau", "QiType" : doubleType});
	var sinProperty = new qiObjs.QiTypeProperty({"Id" : "Sin", "QiType" : doubleType});
	var cosProperty = new qiObjs.QiTypeProperty({"Id" : "Cos", "QiType" : doubleType});
	var tanProperty = new qiObjs.QiTypeProperty({"Id" : "Tan", "QiType" : doubleType});
	var sinhProperty = new qiObjs.QiTypeProperty({"Id" : "Sinh", "QiType" : doubleType});
	var coshProperty = new qiObjs.QiTypeProperty({"Id" : "Cosh", "QiType" : doubleType});
	var tanhProperty = new qiObjs.QiTypeProperty({"Id" : "Tanh", "QiType" : doubleType});

	//create a QiType for WaveData Class
	var wave = new qiObjs.QiType({"Id" : "WaveDataJs", "Name" : "WaveDataJs", 
					"Description" : "This is a sample Qi type for storing WaveData type events",
					"Properties" : [orderProperty, tauProperty, radiansProperty, sinProperty, 
	               cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]});

	var client = new clientObj.QiClient(QiServerUrl);


	var getTokenSuccess = client.getToken(authItems)
									.catch(function(err){logError(err)});
	var nowSeconds;
	var checkTokenExpired;
	

	var createTypeSuccess = getTokenSuccess.then(
									function(res){
										console.log("\nCreating a QiType : "+ wave.Name);
										refreshToken(res, client);
										nowSeconds = Date.now()/1000;
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.createType(wave);
																	}).catch(function(err){logError(err)});
										}else{
											return client.createType(wave);
										}
									})
									.catch(function(err){logError(err)});

	var listTypesSuccess = createTypeSuccess.then(
											//if create types successful, call GET method to list all types
											function(res){
												console.log("Create Qi Type successful");
												if(client.tokenExpires < nowSeconds){
													return checkTokenExpired(client).then(
																			function(res){
																				refreshToken(res, client);
																				return client.getTypes();
																			}).catch(function(err){logError(err)});
												}else{
													return client.getTypes();
												}
											})
											.catch(function(err){logError(err)});

	//create a stream object
	var stream = new qiObjs.QiStream({"Id":"WaveStreamJs", "Name":"WaveStreamJs",
										"Description":"A Stream to store the WaveData Qi types events", 
										"TypeId":"WaveDataJs"});

	var createStreamSuccess = listTypesSuccess.then(
													//POST method to create a stream
													function(res){
														console.log("\nListing all the Qi Types in the QiService under the tenant")
														var obj = JSON.parse(res);
														obj.forEach(function(elem, index){
																console.log("Qi Type "+ index +" :"+elem.Name);
															});
														console.log("");

														if(client.tokenExpires < nowSeconds){
															return checkTokenExpired(client).then(
																					function(res){
																						refreshToken(res, client);
																						return client.createStream(stream);
																					}).catch(function(err){logError(err)});
														}else{
															return client.createStream(stream);
														}
													}).catch(function(err){logError(err)});

	var listStreamsSuccess = createStreamSuccess.then(
													//if stream creation is successful, list all the streams in the Qi service
													function(res){
														console.log("Create Stream successful");
														if(client.tokenExpires < nowSeconds){
															return checkTokenExpired(client).then(
																					function(res){
																						refreshToken(res, client);
																						return client.getStreams();
																					}).catch(function(err){logError(err)});
														}else{
															return client.getStreams();
														}
													}).catch(function(err){logError(err)});
	
	//creating an event
	var interval = new Date();
	interval.setHours(0,1,0,0);
	var evt = qiObjs.NextWave(interval, 2.0, 0);

	var insertValueSuccess = listStreamsSuccess.then(
													//GET all streams successful
													//insert a value into the stream
													function(res){
														console.log("\nListing all the QiStreams in the Qi Service under the tenant");
														var obj = JSON.parse(res);
														obj.forEach(function(elem, index){
															console.log("Qi Stream "+ index + " : "+elem.Name);
														});
														console.log("");

														console.log("Inserting a single event");
														if(client.tokenExpires < nowSeconds){
															return checkTokenExpired(client).then(
																					function(res){
																						refreshToken(res, client);
																						return client.insertEvent(stream, evt);
																					}).catch(function(err){logError(err)});
														}else{
															return client.insertEvent(stream, evt);
														}
													}).catch(function(err){logError(err)});

	//create multiple events and insert
	var events = [];
	var evt1 = null;
	for (var i = 1; i < 200; i+=2) {
		evt1 = qiObjs.NextWave(interval, 2.0, i);
		events.push(evt1);
	};

	var insertMultipleSuccess = insertValueSuccess.then(
														//insert randomly generated values
														function(res){
															console.log("Single event insert successful");
															console.log("");
															
															console.log("Artificially generating 100 events and inserting them into the Qi Service");
															if(client.tokenExpires < nowSeconds){
																return checkTokenExpired(client).then(
																						function(res){
																							refreshToken(res, client);
																							return client.insertEvents(stream, events);
																						}).catch(function(err){logError(err)});
															}else{
																return client.insertEvents(stream, events);
															}
														}).catch(function(err){logError(err)});

	var listEvents = insertMultipleSuccess.then(
												function(res){
													//if insert passed list all events
													console.log("Multiple events insertion successful");
													console.log("");

													console.log("Retrieveing all the events in the Qi stream");
													if(client.tokenExpires < nowSeconds){
														return checkTokenExpired(client).then(
																				function(res){
																					refreshToken(res, client);
																					return client.getWindowValues(stream, 0, 99);
																				}).catch(function(err){logError(err)});
													}else{
														return client.getWindowValues(stream, 0, 99);
													}
												}).catch(function(err){logError(err)});

	var foundEvents;
	var updateEvent = listEvents.then(
									//if list events passed
									//test update of single event
									function(res){
										//list all the events
										var obj = JSON.parse(res);
										foundEvents = obj;
										obj.forEach(function(elem, index){
											console.log("Event No. "+ index + " : "+JSON.stringify(elem));
										});

										console.log("\nUpdate a single event at index 1");
										evt = foundEvents[0];
										evt = qiObjs.NextWave(interval, 4.0, 0);
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.updateEvent(stream, evt);
																	}).catch(function(err){logError(err)});
										}else{
											return client.updateEvent(stream, evt);
										}
									}).catch(function(err){logError(err)});

	var newEvents = [];
	var updateEvents = updateEvent.then(
									//if update event passed
									//test update of events
									function(res){
										console.log("Single event update successful");
										
										console.log("\nUpdate multiple events");
										for (var i = 1; i < 100; i++) {
											evt1 = qiObjs.NextWave(interval, 4.0, i);
											newEvents.push(evt1);
										};
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.updateEvents(stream, newEvents);
																	}).catch(function(err){logError(err)});
										}else{
											return client.updateEvents(stream, newEvents);
										}
									}).catch(function(err){logError(err)});

	listEvents = updateEvents.then(
									function(res){
										//if insert passed list all events
										console.log("Multiple events update successful");
										console.log("");

										console.log("Retrieveing all the events in the Qi stream");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.getWindowValues(stream, 0, 99);
																	}).catch(function(err){logError(err)});
										}else{
											return client.getWindowValues(stream, 0, 99);
										}
									}).catch(function(err){logError(err)});

	//
	var getRangeEvents = listEvents.then(
									function(res){
										//if insert passed list all events
										//list all the events
										var obj = JSON.parse(res);
										foundEvents = obj;
										obj.forEach(function(elem, index){
											console.log("Event No. "+ index + " : "+JSON.stringify(elem));
										});

										console.log("\nRetrieving three events without a stream behaviour");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.getRangeValues(stream, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
																	}).catch(function(err){logError(err)});
										}else{
											return client.getRangeValues(stream, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
										}
									}).catch(function(err){logError(err)});

	//stream behaviour tests
	var behaviour = new qiObjs.QiBehaviour({"Mode":qiObjs.qiStreamMode.Continuous});
	behaviour.Id = "evtStreamStepLeading";
	behaviour.Mode = qiObjs.qiStreamMode.StepwiseContinuousLeading;

	var createBehaviourSuccess = getRangeEvents.then(
									function(res){
										var obj = JSON.parse(res);
										foundEvents = obj;
										obj.forEach(function(elem, index){
											console.log("Event No. "+ index + " : "+JSON.stringify(elem));
										});
										console.log("\nCreating Qistream behaviour");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.createBehaviour(behaviour);
																	}).catch(function(err){logError(err)});
										}else{
											return client.createBehaviour(behaviour);
										}
									}).catch(function(err){logError(err)});

	//update stream with the behaviour
	var updateStream = createBehaviourSuccess.then(
									function(res){
										console.log("\nUpdating Qi stream with the new behaviour ");
										stream.BehaviourId = behaviour.Id;
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.updateStream(stream);
																	}).catch(function(err){logError(err)});
										}else{
											return client.updateStream(stream);
										}
									}).catch(function(err){logError(err)});

	getRangeEvents = updateStream.then(
									function(res){
										console.log("\nRetrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.getRangeValues(stream, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
																	}).catch(function(err){logError(err)});
										}else{
											return client.getRangeValues(stream, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated);
										}
									}).catch(function(err){logError(err)});

	var deleteEvent = getRangeEvents.then(
									function(res){
										var obj = JSON.parse(res);
										foundEvents = obj;
										obj.forEach(function(elem, index){
											console.log("Event No. "+ index + " : "+JSON.stringify(elem));
										});
										//delete an event
										console.log("\nDeleting event at index 0");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.deleteEvent(stream, 0);
																	}).catch(function(err){logError(err)});
										}else{
											return client.deleteEvent(stream, 0);
										}
									}).catch(function(err){logError(err)});

	var deleteWindowEvents = deleteEvent.then(
									function(res){
										console.log("\nDeleting all the events");
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.deleteWindowEvents(stream, 0, 99);
																	}).catch(function(err){logError(err)});
										}else{
											return client.deleteWindowEvents(stream, 0, 99);
										}
									}).catch(function(err){logError(err)});

	var deleteStream = deleteWindowEvents.then(
									function(res){
										console.log("\nDeleting Qi Stream "+ stream.Name);
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.deleteStream(stream.Id);
																	}).catch(function(err){logError(err)});
										}else{
											return client.deleteStream(stream.Id);
										}
									}).catch(function(err){logError(err)});

	var deleteType = deleteStream.then(
									function(res){
										console.log("\nDeleting QiType "+ wave.Name);
										if(client.tokenExpires < nowSeconds){
											return checkTokenExpired(client).then(
																	function(res){
																		refreshToken(res, client);
																		return client.deleteType(wave.Id);
																	}).catch(function(err){logError(err)});
										}else{
											return client.deleteType(wave.Id);
										}
									}).catch(function(err){logError(err)});

	//One catch to rule all the errors
	var finalCatch = deleteType.then(
											function(res){
												console.log("Test successful!");
												process.exit(1);
											})
										.catch(
												function(err){
													console.log(err.message);
												});

	response.end();
}).listen(8080);
console.log("Server is listening at http://localhost:8080/");