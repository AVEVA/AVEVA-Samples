#JavaScript Samples: Building a Client to make REST API Calls to the Qi Service.

This sample demonstrates how Qi REST APIs are invoked using JavaScript. It has following dependencies:
* node.js, installation instructions are available at [node.js](https://nodejs.org/en/)
* Request-Promise, HTTP client Request with Promises/A+ compliance. [request-promise](https://www.npmjs.com/package/request-promise)

## Steps to run the sample:
1. Make a local copy of the git repo
2. Install node.js, if you haven't already
3. Install request-promise
    The `request-promise` node package can be installed as follows :
```javascript
npm install request-promise
```
    Add a `-g` option to make the module available globally. If not, install in the same folder as the other js files.
4. Open Command Prompt in Windows
5. Goto folder where js files are located
6. Type the following command to run the test file in the local server
```javascript
node QiTest.js
```
7. Now open a browser client and enter the following URL to trigger the Qi operations
`http://localhost:8080/`
8. Check the console for the updates

## Creating a connection

The sample uses `request-promise` module to connect a service endpoint.
A REST call has the following syntax follows:

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

The Qi Service is secured by obtaining tokens from an Azure Active Directory instance. The sample applications are examples of a *confidential client*. Such clients provide a user ID and secret that are authenticated against the directory. The sample code includes several placeholder strings. You must replace these with the authentication-related values you received from OSIsoft. The strings are found at the beginning of `QiTest.js`:

```javascript
authItems = {'resource' : "RESOURCE-URL",
             'authority' : "https://login.windows.net/AUTHORIZATION-URL/oauth2/token",
             'appId' : "CLIENT-ID",
             'appKey' : "CLIENT-SECRET"}
```

You will need to replace `resource`, `appId`, and `appKey`.  The `authItems` array is passed to the `QiClient` constructor. The following `POST` method us used to fetch the authentication token.

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

The credentials info are passed as form-encoded content.

The javascript sample is unique in that it is using raw OAuth 2 calls to obtain an authentication token. Since OAuth uses HTTP headers, however, it is not hard to do the work yourself if you understand OAuth. Microsoft also provides a Azure AD Authentication library for javascript that can be used with angular.js.

During initialization, `QiClient` sets the QiServerUrl. Then, the first step is to get authentication token by calling,

```javascript
this.getToken()
```

This method in turn calls a request-promise object, which can have a `.then()` and `.catch()` methods associated with it. `.then()` gets executed when the request-promise is resolved (or successful) and `.catch()` if an exception or error is thrown i.e, rejected.

```javascript
var getTokenSuccess = client.getToken(authItems)
                                    .catch(function(err){logError(err)});
var createTypeSuccess = getTokenSuccess.then(...)
```
As seen above, only if `getToken` is successful will the subsequence REST methods be called. This is *NOT* mandatory though for QiService and been designed this way only for the sake of the sample code to execute without any error. QiService returns appropriate error response for all the methods. For example, trying to fetch a non-existent Qi Type. 

Authentication tokens do expire, however, so the token should be periodically refreshed. This is acheieved by checking the `token_expires` property returned by `getToken` response and comparing it with current time. If it is expired, `checkTokenExpired` is called to re-request for an authorization token.

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
```javascript

The token received from `getToken` is then stored and passed as part of the headers
`getHeaders`, in turn, looks like this:

```javascript
 this.getHeaders = function(){
                            return {
                                        "Authorization" : "bearer "+ this.token,
                                        "Content-type": "application/json", 
                                        "Accept": "text/plain"
                                    }
```

Note how the value of the `Authorization` header is the word `bearer`, followed by a space, and followed by the token value itself.

## Creating a Qi type

Qi is capable of storing any data type you care to define.  Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.

A Qi type has the following properties:

```python
        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
        self.__Properties = []
```

The Qi type "Id" is the identifier for a particular type. "Name" is string property for user understanding. "Description" is again a string that describes the Qi type. "QiTypeCode" is used to identify what kind of datatypes the Qi type stores. The file *QiTypeCode.py* has a list of datatypes that can be stored in the Qi.

A Qi types can have multiple properties, which are again Qi types with the exception that they describe only a single datatype and do not contain multiple properties. Atleast one of the Qi type has to be a key, determined by a boolean value, which is used to index the values to be stored. For example, time can be used as key in order store time based data. Qi allows the use of non-time indices, and also permits compound indices.

From QiTypeProperty.py:
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

A Qi type can be created by a POST request as follows:

```javascript
	restCall({
                url : this.url+this.typesBase,
                method: 'POST',
                headers : this.getHeaders(),
                body : JSON.stringify(wave).toString()
            });
```

* Returns the QiType object in a json format
* If a Qi type with the same Id exists, url path of the existing Qi type is returned
* QiType object is passed in json format


## Creating a Qi Stream

Anything in your process that you wish to measure is a stream in Qi, like a point or tag in a chart.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream. The value of the `TypeId` property is the value of the Qi type `Id` property.

```javascript
   QiStream : function(qiStream){
        this.Id = qiStream.Id;
        this.Name = qiStream.Name;
        this.Description = qiStream.Description;
        this.TypeId = qiStream.TypeId;
        if(qiStream.BehaviourId){
            this.BehaviourId = qiStream.BehaviourId;
        }
    }
```

QiStream can be created by a POST request as follows:

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

A single event is a data point in the Stream. An event object cannot be emtpy and should have atleast the key value of the Qi type for the event. Events are passed in json format.

An event can be created using following POST request:

```javascript
restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.insertSingle,
            method : 'POST',
            headers : this.getHeaders(),
            body : JSON.stringify(evt)
        });
```

* qiStream.Id is the stream ID
* body is the event object in json format

Inserting multiple values is similar, but the payload has list of events and the url for POST call varies

```javascript
restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.insertMultiple,
            method : 'POST',
            headers : this.getHeaders(),
            body : JSON.stringify(events)
        });
```

## Retrieve Events

There are many methods that allow for the retrieval of events from a stream.  This sample demonstrates the most basic method of retrieving all the events on a particular time range. In general, the index values must be of the same type as the index assigned in the Qi type.  Compound indices' values are concatenated with a pipe ('|') separator.

```javascript
restCall({
        url : this.url+this.streamsBase+this.getTemplate.format([qiStream.Id,start,end]),
        method : 'GET',
        headers : this.getHeaders()
    });
```

* params has the starting and ending key value of the window
		Ex: For a time index, params will be "endIndex=<*end_time*>&startIndex=<*start_time*>"

## Update Events

Updating events is hanlded by PUT REST call as follows:

```javascript
 restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.updateSingle,
            method : 'PUT',
            headers : this.getHeaders(),
            body : JSON.stringify(evt)
        });
```

* payload has the new value for the event correseponding to the key value that is to be updated

Updating multiple events is similar but the payload has an array of event objects and url for POST call varies

```javascript
 restCall({
            url : this.url+this.streamsBase+"/"+
                    qiStream.Id+this.updateMultiple,
            method : 'PUT',
            headers : this.getHeaders(),
            body : JSON.stringify(events)
        });
```
##Stream Behaviors
Recorded values are returned by `GetWindowValues`.  If you want to get a particular range of values and interpolate events at the endpoints of the range, you may use `GetRangeValues`.  The nature of the interpolation performed is determined by the stream behavior assigned to the stream.  if you do not specify one, a linear interpolation is assumed.  This example demonstrates a stepwise interpolation using stream behaviors.  More sophisticated behavior is possible, including the specification of interpolation behavior at the level of individual event type properties.  This is discussed in the [Qi API Reference](https://qi-docs.readthedocs.org/en/latest/Overview/).  First, before changing the stream's retrieval behavior, call `GetRangeValues` specifying a start index value of 1 (between the first and second events in the stream) and calculated values:

```javascript
  client.getRangeValues(stream, 1, 0, 3, False, qiObjs.qiBoundaryType.ExactOrCalculated);
```

This gives you a calculated event with linear interpolation at index 1.

Now, we define a new stream behavior object and submit it to the Qi Service:

```javascript
    var behaviour = new qiObjs.QiBehaviour({"Mode":qiObjs.qiStreamMode.Continuous});
    behaviour.Id = "evtStreamStepLeading";
    behaviour.Mode = qiObjs.qiStreamMode.StepWiseContinuousLeading;
    ...
    client.createBehaviour(behaviour);
```

By setting the `Mode` property to `StepwiseContinuousLeading` we ensure that any calculated event will have an interpolated index, but every other property will have the value of the recorded event immediately preceding that index.  Now attach this behavior to the existing stream by setting the `BehaviorId` property of the stream and updating the stream definition in the Qi Service:

```javascript
  stream.BehaviourId = behaviour.Id;
  ...
  client.updateStream(stream);
```

The sample repeats the call to `GetRangeValues` with the same parameters as before, allowing you to compare the values of the event at `Order=1`.

## Deleting Events

An event at a particular data point can be deleted by passing the *key* value for that data point to following DELETE REST call:

```javascript
restCall({
            url : this.url+this.streamsBase+this.removeSingleTemplate.format([qiStream.Id, index]),
            method : 'DELETE',
            headers : this.getHeaders()
        });
```

Delete can also be done over a window of key value as follows:

```javascript
 restCall({
            url : this.url+this.streamsBase+this.removeMultipleTemplate.format([qiStream.Id, start, end]),
            method : 'DELETE',
            headers : this.getHeaders()
        });
```

* params has the starting and ending key value of the window
			Ex: For a time index, params:endIndex=<*end_time*>&startIndex=<*start_time*>

## Cleanup: Deleting Types, Behaviors, and Streams

In order to run the sample again in the future without name collisions, the sample does some cleanup at the end. Deleting streams, stream behaviors, and types can be achieved by a DELETE REST call and passing the corresponding ID

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
