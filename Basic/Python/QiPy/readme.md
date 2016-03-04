#Python Samples: Building a Client to make REST API Calls to the Qi Service.

This sample demonstrates how Qi REST APIs are invoked using python.

## Establish a Connection

The sample uses `httplib` module to connect a service endpoint. A new connection is opened as follows:

```python
	conn = httplib.HTTPConnection(url-name)
```
* url-name is the service endpoint (Ex: "localhost:3380"). The connection is used by the `QiClient` class, which encapsulates the REST API and performs authentication.

## Obtain an Authentication Token

The Qi service is secured by obtaining tokens from an Azure Active Directory instance.  A token must be attached to every request made to Qi, in order for the request to succeed.  The sample applications are examples of a *confidential client*. Such clients provide a user ID and secret that are authenticated against the directory. The sample code includes several placeholder strings. You must replace these with the authentication-related values you received from OSIsoft. The strings are found in `Constants.py`:

```python
    #VERY IMPORTANT: edit the following values to reflect the authorization items you were given
    authItems = {'resource' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
                 'authority' : "PLACEHOLDER_REPLACE_WITH_AUTHORITY",#Ex: "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token,
                 'appId' : "PLACEHOLDER_REPLACE_WITH_USER_ID",
                 'appKey' : "PLACEHOLDER_REPLACE_WITH_USER_SECRET"}
    
    QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL"
```

You will need to replace `resource`, `authority`, `appId`, and `appKey`.  The `authItems` array is passed to the `QiClient` constructor.

This Python sample uses raw OAuth 2 calls to obtain an authentication token.  The other samples use libraries from Microsoft that handles token acquisition, caching, and refreshing, but such a library is not available for Python at this time.   

During initialization, `QiClient` makes the following calls:

```python
	self.__getToken()
	if not self.__token:
		return
```

The first call, `__getToken`, makes the OAuth call to the Azure Active Directory instance to get a token, then assigns the value (assuming the application is successfully authenticated) to the member variable `__token`.  Next, QiClient checks to ensure it has an authentication token. Calls would fail in the absence of one, hence the return if no token is found.  This is the code for `__getToken`:

```python
    def __getToken(self):     
        if self.__expiration < (time.time()/100):
            return
            
        response = requests.post(self.__authItems['authority'], 
                                 data = { 'grant_type' : 'client_credentials',
                                         'client_id' : self.__authItems['appId'],
                                            'client_secret' : self.__authItems['appKey'],
                                            'resource' : self.__authItems['resource']
                                            })
        if response.status_code == 200:
            self.__token = response.json()['access_token']
            self.__expiration = response.json()['expires_on']
        else:
            self.__token = ""
            print "Authentication Failure : "+response.reason
```

Authentication tokens do expire, so the token must be periodically refreshed. The first lines of `__getToken` check to see if the token has expired and returns if it has not.  Otherwise, the credentials are submitted to Azure Active Directory to obtain a fresh token.  The `__getToken` method is called before each REST API call, and the token is passed as part of the headers:
```python
def __qi_headers(self):
    return {
        "Authorization" : "bearer %s" % self.__token,
        "Content-type": "application/json", 
        "Accept": "text/plain"
    }
```

Note that the value of the `Authorization` header is the word "bearer", followed by a space, and followed by the token value itself.

## Create a QiType

QiStreams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that the data type must have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a QiType, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.   

Because we are using the Qi REST API, we must build our own type definitions. A type definition in Qi consists of one or more properties.  Each property has its own type.  This can be a simple data type like integer or string, or a previously defined complex QiType. This allows for the creation of nested data types - QiTypes whose properties may be user-defined types.  We have created `QiType` and `QiTypeProperty` classes that match those in the Qi Client Libraries.  Simple types are denoted by an enumeration specified in `QiTypeCode.py`.  The ordinal values in the latter file are those the Qi service expects, so if you wish to create you own classes you must specify these values.

From QiType.py:
```python
	self.__Id = ""
	self.__Name = None
	self.__Description = None
	self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
	self.__Properties = []
```

From QiTypeProperty.py:
```python
    def __init__(self):
            self.__Id = ""
            self.__Name = None
            self.__Description = None
            self.__QiType = None
            self.__IsKey = False
```            	

Type creation is encapsulated by the `createType` method in `QiClient.py`.  Here is how it is called in `test.py`:

```python
	wave = QiType()
	wave.Id = "WaveDataPySample"
	wave.Name = "WaveDataPySample"
	wave.Description = "This is a sample Qi type for storing WaveData type events"
	wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
					   cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

	#create the type in Qi service
	print "Creating the WaveData Qi type in Qi service"
	evtType = client.createType(wave)
```
* Returns the QiType object in a json format
* If a Qi type with the same Id exists, url path of the existing Qi type is returned
* QiType object is passed in json format



## Create a QiStream

An ordered series of events is stored in a QiStream.  We've created a `QiStream` class mirroring the properties of the native Qi service `QiStream` class. All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi service.  You may optionally assign a QiStreamBehavior to the stream.  The value of the stream's `TypeId` property is the value of the QiType `Id` property.  The `CreateStream` method of `QiClient` is similar to `createType`, except that it uses a different URL.  Here is how it is called from the main program:

```python	
	stream = QiStream()
	stream.Id = "WaveStreamPySample"
	stream.Name = "WaveStreamPySample"
	stream.Description = "A Stream to store the WaveData Qi types events"
	stream.TypeId = "WaveDataPySample"
	stream.BehaviorId = None
	evtStream = client.createStream(stream)
```

## Create and Insert Events into the Stream

A single event is a data point in the Stream. An event object cannot be emtpy and should have atleast the key value of the Qi type for the event. Events are passed in json format. Here is the call to create a single event in a data stream in `QiClient.py`:
```python
	conn = http.HTTPSConnection(self.url)
	conn.request("POST", self.__streamsBase + '/' + qi_stream.Id + self.__insertSingle, 
				 payload, self.__qi_headers())
```
* qi_Stream.Id is the stream ID
* payload is the event object in json format

Inserting multiple values is similar, but the payload has list of events and the url for POST call is slightly different:
```python
	conn = http.HTTPSConnection(self.url)
	conn.request("POST", self.__streamsBase + '/' + qi_stream.Id + self.__insertMultiple, 
				 payload, self.__qi_headers())
```

## Retrieve Events

There are many methods in the Qi REST API allowing for the retrieval of events from a stream.  The retrieval methods take string type start and end values; in our case, these the start and end ordinal indices expressed as strings ("0" and "99", respectively).  The index values must capable of conversion to the type of the index assigned in the QiType.  Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator.  `QiClient` implements three of the many available retrieval methods: `getLastValue`, `getWindowValues`, and `getRangeValues`. 

'GetWindowValues' can be used to get events over a specific index range.  'GetRangeValues' can be used to get a specified number of events from a starting index point.

Here is what the `GetWindowValues` call looks like:

```python
	conn = http.HTTPSConnection(self.url)
	conn.request("GET", self.__streamsBase + '/' + 
					self.__getTemplate.format(stream_id = qi_stream.Id, 
											 start = urllib.urlencode({"startIndex": start}), 
												end = urllib.urlencode({"endIndex": end})), 
					headers = self.__qi_headers())
```


## Update Events

Updating events is handled by PUT REST call as follows:

```python
	conn = http.HTTPSConnection(self.url)
	conn.request("PUT", self.__streamsBase + '/' + qi_stream.Id + self.__updateSingle, 
				 payload, self.__qi_headers())
```
* payload is the new event with an index value specifying the existing event to overwrite.

Updating multiple events is similar but the payload has an array of event objects and url for POST is slightly different:
```python
	conn = http.HTTPSConnection(self.url)
	conn.request("PUT", self.__streamsBase + '/' + qi_stream.Id + self.__updateMultiple, 
				 payload, self.__qi_headers())
```

##QiStreamBehaviors

With certain data retrieval calls, a QiBoundarytype may be specified.  For example, if GetRangeValues is called with an ExactOrCalculated boundary type, an event at the request start index will be calculated using linear interpolation (default) or based on the QiStreamBehavior associated with the QiStream.  Because our sample QiStream was created without any QiStreamBehavior associated, it should display the default linear interpolation.

The first event returned by the following call will be at index 1 (start index) and calculated via linear interpolation:
```python
	foundEvents = client.getRangeValues("WaveStreamPy", "1", 0, 3, False, QiBoundaryType.ExactOrCalculated.value)
```

To observe how QiStreamBehaviors can change the query results, we will define a new stream behavior object and submit it to the Qi service:
```python
	behaviour = QiStreamBehaviour()
	behaviour.Id = "evtStreamStepLeading";
	behaviour.Mode = QiStreamMode.StepwiseContinuousLeading.value
	behaviour = client.createBehaviour(behaviour)
```

By setting the `Mode` property to `StepwiseContinuousLeading` we ensure that any calculated event will have an interpolated index, but every other property will have the value of the previous event.  Now attach this behavior to the existing stream by setting the `BehaviorId` property of the stream and updating the stream definition in the Qi service:
```python
	evtStream.BehaviourId = behaviour.Id
	client.updateStream(evtStream)
```

The sample repeats the call to `GetRangeValues` with the same parameters as before, allowing you to compare the values of the event at index 1 using different stream behaviors.

## Delete Events

An event at a particular index can be deleted by passing the index value for that data point to following DELETE REST call.  The index values are expressed as string representations of the underlying type.  DateTime index values must be expressed as ISO 8601 strings.

Deleting a single value is done via the QiClient's removeValue method:
```python
	conn = http.HTTPSConnection(self.url)
	conn.request("DELETE", self.__streamsBase + '/' + self.__removeSingleTemplate.format(stream_id = qi_stream.Id, param = params), 
				 headers = self.__qi_headers())
```

Delete can also be done over a window of index values, as in the removeValues method:
```python
	conn = http.HTTPSConnection(self.url)
	conn.request("DELETE", self.__streamsBase + '/' + 
					self.__removeMultipleTemplate.format(stream_id = qi_stream.Id, 
					start = urllib.urlencode({"startIndex": start}),
					end = urllib.urlencode({"endIndex": end})), 
					headers = self.__qi_headers())
```


## Cleanup: Deleting Types, Behaviors, and Streams

So that it can run repeatedly without name collisions, the sample does some cleanup before exiting. Deleting streams, stream behaviors, and types can be achieved by a DELETE REST call and passing the corresponding Id.  Note: types and behaviors cannot be deleted until any streams referencing them are deleted first.

```python
	conn.request("DELETE", self.__streamsBase + '/' + stream_id, headers = self.__qi_headers())
	response = conn.getresponse()
```

```python
	conn = http.HTTPSConnection(self.url)
	conn.request('DELETE', self.__typesBase + '/' +  type_id, headers = self.__qi_headers())
```

```python
	conn = http.HTTPSConnection(self.url)
	conn.request('DELETE', self.__behaviorBase + '/' +  behaviorId, headers = self.__qi_headers())
```
