#JavaScript Samples: Building a Client to make REST API Calls to the Qi Service.

This sample demonstrates how Qi REST APIs are invoked using JavaScript. It has following dependencies:
* node.js, installation instructions are available at [node.js](https://nodejs.org/en/)
* Request-Promise, HTTP client Request with Promises/A+ compliance. [request-promise](https://www.npmjs.com/package/request-promise)

## Sample Setup

1. Make a local copy of the git repo
2. Install node.js
3. Install request-promise, using the following command.  Add a `-g` option to make the module available globally, install in the same folder as the other js files:
```javascript
npm install request-promise
```   
4. Open Command Prompt in Windows
5. Goto folder where js files are located
6. Type the following command to run the test file in the local server
```javascript
node QiTest.js
```
7. Now open a browser client and enter the following URL to trigger the Qi operations
`http://localhost:8080/`
8. Check the console for the updates

## Establish a Connection

The sample uses `request-promise` module to connect a service endpoint.  Qi REST API calls are sent to the Qi service.  The Qi REST API maps HTTP methods to CRUD like this:

| HTTP Method | CRUD Operation | Content Found In |
|-------------|----------------|------------------|
| POST        | Create         | message body     |
| GET         | Retrieve       | URL parameters   |
| PUT         | Update         | message body     |
| DELETE      | Delete         | URL parameters   |

The REST calls in this sample are set up as follows:
```javascript
    var restCall = require("request-promise")
	restCall({
                url : 'URL',
                method: 'REST-METHOD',
                headers : {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            "Authorization" : "bearer "+ TOKEN,
                            "Content-type": "application/json", 
                            "Accept": "text/plain"
                },
                form : {    
                            'grant_type' : 'client_credentials',
                            'client_id' : CLIENT-ID,
                            'client_secret' : CLIENT-KEY,
                            'resource' : RESOURCE-URL
                        }
            });
```

* URL - The service endpoint
* REST-METHOD - Denotes the type of REST call
* TOKEN - Authentication token obtained from Azure Oauth2 (explained below)
* CLIENT-ID & CLIENT-KEY - Client credentials provided by service provider
* RESOURCE-URL - Resource string for token acquisition 

`Request-Promise` is used in the current sample in order to execute the REST calls in sequence. It is not mandatory. In fact, the same syntax can be used with `request` module. It adds the Bluebird-powered `.then(...)` method to `request` call objects. This can be used to achieve an `await()` effect. It supports all the features as that of the `request` library, except that callbacks are replaced with promises.

## Obtain an Authentication Token

The Qi service is secured by obtaining tokens from an Azure Active Directory instance.  A token must be attached to every request made to Qi, in order for the request to succeed.  The sample applications are examples of a *confidential client*. Such clients provide a user ID and secret that are authenticated against the directory. The sample code includes several placeholder strings. You must replace these with the authentication-related values you received from OSIsoft. The strings are found in `Constants.js`:

```javascript
	authItems : {'resource' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
			         'authority' : "PLACEHOLDER_REPLACE_WITH_AUTHORITY",//Ex: "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token",
			         'appId' : "PLACEHOLDER_REPLACE_WITH_USER_ID",
			         'appKey' : "PLACEHOLDER_REPLACE_WITH_USER_SECRET"}
	qiServerUrl : "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL";
```

You will need to replace `resource`, `authority`, `appId`, and `appKey`.  The `authItems` array is passed to the `QiClient` constructor. The following `POST` method us used to fetch the authentication token.

```javascript
restCall({
            url : AUTHORITY-URL,
            method: 'POST',
            headers : {
                        'Content-Type': 'application/x-www-form-urlencoded'
            },
            form : {'resource' : "RESOURCE-URL",
                     'authority' : "https://login.windows.net/AUTHORIZATION-URL/oauth2/token",
                     'appId' : "CLIENT-ID",
                     'appKey' : "CLIENT-SECRET"}
        });
```

The credentials are passed as form-encoded content.

This javascript example uses raw OAuth 2 calls to obtain an authentication token.  Microsoft also provides a Azure Active Directory Authentication Library for javascript that can be used with angular.js, which handles the specifics of token acquisition, caching, and refresh.

During initialization, `QiClient` sets the QiServerUrl. Then, the first step is to get authentication token by calling,

```javascript
this.getToken()
```

The token received from `getToken` is included in the headers of each Qi REST API request:
```javascript
 this.getHeaders = function(){
                            return {
                                        "Authorization" : "bearer "+ this.token,
                                        "Content-type": "application/json", 
                                        "Accept": "text/plain"
                                    }
```
Note that the value of the `Authorization` header is the word "bearer", followed by a space, and followed by the token string.

Authentication tokens have an expiration time which can be checked via the `token_expires` property. The sample code handles checking the token expiration and refreshing it as needed.  As mentioned above, Microsoft also provides an authentication library compatible with angular.js that handles token caching and refresh transparently.
```javascript
if(client.tokenExpires < nowSeconds){
                                    return checkTokenExpired(client).then(
                                                            function(res){
                                                                refreshToken(res, client);
                                                                return client.createType(wave);
                                                            }).catch(function(err){logError(err)});
                                }else{
                                    return client.createType(wave);
                                }
```

Note:
The `getToken()` method returns a request-promise object, which can have a `.then()` and a `.catch()` method associated with it. The `.then()` method is executed when the request-promise is resolved (or successful) and `.catch()` is executed if an exception or error is thrown.  This sample follows a pattern of placing REST calls in the `.then()` method after token acquisition (or other dependent REST calls):
```javascript
var getTokenSuccess = client.getToken(authItems)
                                    .catch(function(err){logError(err)});
var createTypeSuccess = getTokenSuccess.then(...<Qi REST call to create a type>...)
```
In the above snippet, the type creation method be called only if token acquisition was successful.  This is not mandatory for interaction with the Qi service - the type creation call could be attempted regardless of token acquisition.  A call to the Qi service with a missing or incorrect token will return with an Unauthorized status code.

## Create a QiType

QiStreams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that the data type must have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a QiType, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.  

A QiType has the following properties: Id, Name, Description, QiTypeCode, and Properties.

The type "Id" is the identifier for a particular type. "Name" and "Description" are optional string properties to describe the type. "QiTypeCode" is used to identify the datatypes stored by the QiType. The file *QiObjects.js* enumerates the available datatypes the qiTypeCodeMap.

A type definition in Qi consists of one or more "Properties."  Each property has its own type.  This can be a simple data type like integer or string, or a previously defined complex QiType. This allows for the creation of nested data types - QiTypes whose properties may be user-defined types.

From QiObjects.js:
```javascript
   QiType : function (qiType){
        if(qiType.Id){
            this.Id = qiType.Id
        }
        if(qiType.Name){
            this.Name = qiType.Name;
        }
        if(qiType.Description){
            this.Description = qiType.Description;
        }
        if(qiType.QiTypeCode){ 
            this.QiTypeCode = qiType.QiTypeCode;
        }
        if(qiType.Properties){
            this.Properties = qiType.Properties;
        }
    }
```            	

A QiType can be created by a POST request as follows:

```javascript
	restCall({
                url : this.url+this.typesBase,
                method: 'POST',
                headers : this.getHeaders(),
                body : JSON.stringify(wave).toString()
            });
```

* Returns the QiType object in a json format
* If a type with the same Id exists, url path of the existing Qi type is returned
* QiType object is passed in json format


## Create a QiStream

An ordered series of events is stored in a QiStream.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi service.  You may optionally assign a QiStreamBehavior to the stream. The value of the `TypeId` property is the value of the QiType `Id` property.
```javascript
   QiStream : function(qiStream){
        this.Id = qiStream.Id;
        this.Name = qiStream.Name;
        this.Description = qiStream.Description;
        this.TypeId = qiStream.TypeId;
        if(qiStream.BehaviorId){
            this.BehaviorId = qiStream.BehaviorId;
        }
    }
```

The local QiStream can be created in the Qi service by a POST request as follows:
```javascript
restCall({
        url : this.url+this.streamsBase,
        method : 'POST',
        headers : this.getHeaders(),
        body : JSON.stringify(qiStream).toString()
    });
```

* QiStream object is passed in json format

## Create and Insert Events into the Stream

A single event is a data point in the stream. An event object cannot be emtpy and should have at least the key value of the Qi type for the event. Events are passed in json format.

An event can be created using the following POST request:
```javascript
restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.insertSingle,
            method : 'POST',
            headers : this.getHeaders(),
            body : JSON.stringify(evt)
        });
```

* qiStream.Id is the stream Id
* body is the event object in json format

Inserting multiple values is similar, but the payload has list of events and the url for POST call varies:
```javascript
restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.insertMultiple,
            method : 'POST',
            headers : this.getHeaders(),
            body : JSON.stringify(events)
        });
```

The Qi REST API provides many more types of data insertion calls beyond those demonstrated in this application.

## Retrieve Events

There are many methods in the Qi REST API allowing for the retrieval of events from a stream.  The retrieval methods take string type start and end values; in our case, these the start and end ordinal indices expressed as strings ("0" and "99", respectively).  The index values must capable of conversion to the type of the index assigned in the QiType.  Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator.  This sample implements only two of the many available retrieval methods - GetWindowValues (getTemplate in `QiClient.js`) and GetRangeValues (`getRangeTemplate` in `QiClient.js`).

```javascript
restCall({
        url : this.url+this.streamsBase+this.getTemplate.format([qiStream.Id,start,end]),
        method : 'GET',
        headers : this.getHeaders()
    });
```
* parameters are the QiStream Id and the starting and ending index values for the desired window
		Ex: For a time index, request url format will be "/{streamId}/Data/GetWindowValues?startIndex={startTime}&endIndex={endTime}

## Update Events

Updating events is handled by PUT REST call as follows:

```javascript
 restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.updateSingle,
            method : 'PUT',
            headers : this.getHeaders(),
            body : JSON.stringify(evt)
        });
```
* the request body has the new event that will update an existing event at the same index

Updating multiple events is similar, but the payload has an array of event objects and url for PUT is slightly different:
```javascript
 restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.updateMultiple,
            method : 'PUT',
            headers : this.getHeaders(),
            body : JSON.stringify(events)
        });
```

##QiStreamBehaviors

With certain data retrieval calls, a QiBoundarytype may be specified.  For example, if GetRangeValues is called with an ExactOrCalculated boundary type, an event at the request start index will be calculated using linear interpolation (default) or based on the QiStreamBehavior associated with the QiStream.  Because our sample QiStream was created without any QiStreamBehavior associated, it should display the default linear interpolation.

The first event returned by the following call will be at index 1 (start index) and calculated via linear interpolation:
```javascript
  client.getRangeValues(stream, 1, 0, 3, False, qiObjs.qiBoundaryType.ExactOrCalculated);
```

To observe how QiStreamBehaviors can change the query results, we will define a new stream behavior object and submit it to the Qi service::
```javascript
    var behavior = new qiObjs.QiBehavior({"Mode":qiObjs.qiStreamMode.Continuous});
    behavior.Id = "evtStreamStepLeading";
    behavior.Mode = qiObjs.qiStreamMode.StepWiseContinuousLeading;
    ...
    client.createBehavior(behavior);
```

By setting the `Mode` property to `StepwiseContinuousLeading` we ensure that any calculated event will have an interpolated index, but every other property will have the value of the previous event.  Now attach this behavior to the existing stream by setting the `BehaviorId` property of the stream and updating the stream definition in the Qi service:
```javascript
	stream.BehaviorId = behavior.Id;
	...
	client.updateStream(stream);
```

The sample repeats the call to `GetRangeValues` with the same parameters as before, allowing you to compare the values of the event at index 1 using different stream behaviors.

## Delete Events

An event at a particular index can be deleted by passing the index value for that data point to following DELETE REST call.  The index values are expressed as string representations of the underlying type.  DateTime index values must be expressed as ISO 8601 strings.

```javascript
restCall({
            url : this.url+this.streamsBase+this.removeSingleTemplate.format([qiStream.Id, index]),
            method : 'DELETE',
            headers : this.getHeaders()
        });
```
* parameters are the stream Id and the index at which to delete an event
			Ex: For a time index, the request url will have the format:
			"/{streamId}/Data/RemoveValue?index={deletionTime}";

Delete can also be performed over a window of key value as follows:
```javascript
 restCall({
            url : this.url+this.streamsBase+this.removeMultipleTemplate.format([qiStream.Id, start, end]),
            method : 'DELETE',
            headers : this.getHeaders()
        });
```
* parameters are the stream Id and the starting and ending index values of the window
			Ex: For a time index, the request url will have the format:
			/{streamId}/Data/RemoveWindowValues?startIndex={startTime}&endIndex={endTime}

## Cleanup: Deleting Types, Behaviors, and Streams

So that it can run repeatedly without name collisions, the sample does some cleanup before exiting. Deleting streams, stream behaviors, and types can be achieved by a DELETE REST call and passing the corresponding Id.  Note: types and behaviors cannot be deleted until any streams referencing them are deleted first.

```javascript
 restCall({
        url : this.url+this.streamsBase+"/"+streamId,
        method : 'DELETE',
        headers : this.getHeaders()
    });
```

```javascript
restCall({
            url : this.url+this.typesBase+"/"+typeId,
            method : 'DELETE',
            headers : this.getHeaders()
        });
```
