#.NET Samples: Building a Client with the Qi REST API

This sample is written using only the Qi REST API.  This API allows for the creation of Qi Service clients in any language that can make HTTP calls and does not require access to any OSIsoft libraries.  Objects are passed as JSON strings.  We're using the JSON.NET nuget (Newtonsoft.Json id) package, but any method of creating a JSON representation of objects will work.

## Instantiate a Qi Client

We've created a class wrapping an `HttpClient` instance from the `System.Net.Http` namespace and providing methods for the major CRUD operations we wish to perform. The CRUD methods encapsulate the Qi REST API.  Each call consists of an HTTP request with a specific URL and HTTP method.  The URL is the server plus the extension specific to the call.  Like all REST APIs, the Qi REST API maps HTTP methods to CRUD like this:

| HTTP Method | CRUD Operation | Content Found In |
|-------------|----------------|------------------|
| POST        | Create         | message body     |
| GET         | Retrieve       | URL parameters   |
| PUT         | Update         | message body     |
| DELETE      | Delete         | URL parameters   |

The constructor for our QiClient class sets up the HttpClientHandler to prevent auto redirection as will be expained in the next section.  It also takes the base URL (i.e., protocol plus server and port number) and ensures it ends with a forward slash to make our job easier when it comes time to compose the URL for a specific REST call.  Finally, the constructor establishes a thirty second timeout and indicates that the client accepts JSON format responses:

```c#
	public QiClient(string baseUrl)
	{
		_httpClientHandler = new HttpClientHandler
		{
			AllowAutoRedirect = false
		};

		_httpClient = new HttpClient(_httpClientHandler);
		_baseUrl = baseUrl;
		if (_baseUrl.Substring(_baseUrl.Length - 1).CompareTo(@"/") != 0)
		{
			_baseUrl = _baseUrl + "/";
		}

		_httpClient.BaseAddress = new Uri(_baseUrl);
		_httpClient.Timeout = new TimeSpan(0, 0, 30);
		_httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
	}
```

## Obtain an Authentication Token

The Qi service is secured by obtaining tokens from an Azure Active Directory instance.  A token must be attached to every request made to Qi, in order for the request to succeed.  In the previous section, we set AllowAutoRedirect to false for the HttpClientHander; this is because auto redirection strips the token from the request and will always result in an Unauthorized response.  Instead of relying on automatic redirection, this sample will handle redirecting 302 (Found) responses manually.

The sample applications are examples of a *confidential client*.  Such clients provide a user ID and secret that are authenticated against the directory. The sample code includes several placeholder strings.  You must replace these with the authentication-related values you received from OSIsoft.  The strings are found in the `Constants.cs` file.

```c#
	public const string SecurityResource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
	public const string SecurityAuthority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
	public const string SecurityAppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
	public const string SecurityAppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
	public const string QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL";
```

In `QiClient.cs` you will find a method called `AcquireAuthToken`.  The first step in obtaining an authentication token is to create an authentication context related to the Azure Active Directory instance providing tokens.  The authority is designated by the URI in `_authority`.

```c#
	if (_authContext == null)
	{
		_authContext = new AuthenticationContext(Constants.SecurityAuthority);
	}
```

`AuthenticationContext` instances take care of communicating with the authority and also maintain a local cache of tokens.  Tokens have a fixed lifetime, typically one hour, but they can be refreshed by the authenticating authority for a longer period.  If the refresh period has expired, the credentials have to be presented to the authority again.  Happily, the `AcquireToken` method hides these details from client programmers.  As long as you call `AcquireToken` before each HTTP call, you will have a valid token.  Here is how that is done:

```c#
	try
	{
		ClientCredential userCred = new ClientCredential(Constants.SecurityAppId, Constants.SecurityAppKey);
		AuthenticationResult authResult = _authContext.AcquireToken(Constants.SecurityResource, userCred);
		return authResult.AccessToken;
	}
	catch (AdalException)
	{
		return string.Empty;
	}
```


## Create a QiType

QiStreams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that the data type must have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a QiType, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.   

Because we are using the Qi REST API, we must build our own type definitions. A type definition in Qi consists of one or more properties.  Each property has its own type.  This can be a simple data type like integer or string, or a previously defined complex QiType. This allows for the creation of nested data types - QiTypes whose properties may be user-defined types.  Our sample `WaveData` class is a series of simple types.  We have created `QiType` and `QiTypeProperty` classes that match those in the Qi Client Libraries.  Simple types are denoted by an enumeration specified in `QiTypeCode.cs`.  The ordinal values in the latter file are those the Qi service expects, so if you wish to create you own classes you must specify these values.

`WaveData` has one integer property and a series of double value properties.  To start, then, we create a QiType instance for each of these simple types:

```c#
	QiType intType = new QiType();
	intType.Id = "intType";
	intType.QiTypeCode = QiTypeCode.Int32;

	QiType doubleType = new QiType();
	doubleType.Id = "doubleType";
	doubleType.QiTypeCode = QiTypeCode.Double;
```

Now let's create our key property, which is an integer type and is named `Order`.

```C#
	QiTypeProperty orderProperty = new QiTypeProperty();
	orderProperty.Id = "Order";
	orderProperty.QiType = intType;
	orderProperty.IsKey = true;
```
We've specified the id, used the intType `QiType` we created, and most importantly set IsKey to `true`.  The double value properties are created similarly.  Here is the code creating the `Radians` property:

```c#
	QiTypeProperty radiansProperty = new QiTypeProperty();
	radiansProperty.Id = "Radians";
	radiansProperty.QiType = doubleType;
```
Once all the necessary properties are created, it is necessary to assign them to a `QiType` defining the overall `WaveData` class.  This is done by created an array of `QiProperty` instances and assigning it to the `Properties` property of `QiType`:

```C#
	QiType type = new QiType();
	type.Name = "WaveData";
	type.Id = "WaveDataType";
	type.Description = "This is a type for WaveData events";
	QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
	type.Properties = props;
```
If you wanted to nest a user defined type within another QiType, you would begin by defining the contained type as a `QiType` using the methods illustrated above, then create a `QiProperty` with that type and assign it to the containing class.

All this creates a type definition locally which must be submitted in a REST call before it becomes available to the Qi service for the creation of streams. The create call URL has the extention `/Qi/Types`, and the body of the request message is the JSON format serialization of the `QiType` just created.  Creation of other Qi objects is performed similarly.  The specifics of object creation are wrapped in the generic `CreateQiObjectAsync<T>` method of `QiClient`.  `CreateQiObjectAsync` also handles the manual redirection of 302 (Found) responses, as referenced in the sections on creating a Qi client and obtaining an authentication token.

Note that the methods in `QiClient` are asynchronous, but the application itself is a simple console application.  `Main` is a static method, so it cannot take advantage of `await`, hence our use of `Result` above, and `Wait` for methods that do not return a value.  A more complicated client application could use the asynchronous methods to greater advantage.


## Create a QiStream

An ordered series of events is stored in a QiStream.  We've created a `QiStream` class mirroring the properties of the native Qi service `QiStream` class. All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi service.  You may optionally assign a QiStreamBehavior to the stream.  This is the code to create a stream named `evtStream` for recording events of our sample type.  The value of the `TypeId` property is the value of the QiType `Id` property.  The `CreateStream` method of `QiClient` is similar to `CreateType`, except that it uses a different URL.  Here is how it is called from the main program:

```c#
	QiStream stream = new QiStream("evtStream", evtType.Id);
	string evtStreamString = qiclient.CreateStream(stream).Result;
	QiStream evtStream = JsonConvert.DeserializeObject<QiStream>(evtStreamString);
```
Note that we set the `TypeId` property of the stream to the value of the Id of the QiType created earlier. Types and behaviors are reference counted; a type or behavior cannot be deleted until all streams using it are also deleted.

## Create and Insert Events into the Stream

The `WaveData` class allows us to create events locally.  In an actual production setting, this is where you would interface with your measurements.  We'll use the `Next` method to create values, and assign integers from 0-99 to establish an ordered collection of `WaveData` instances.  Our `QiClient` class provides methods for inserting a single event or an array of events.  The Qi REST API provides many more types of data insertion calls in addition to those demonstrated in this application.

It would be possible to pass in a `WaveData` instance (or array of instances) into the event creation methods, but then the methods would be particular to that specific class. We've made the decision to handle all serialization and deserialization outside the `QiClient` class and pass the results into and out of the event creation methods.  This allows us to change the defintion of the event class without changing the CRUD methods of our client class.  In this way we are able to take advantage of the fact that the Qi service stores and manipulates arbitrary, user defined types.

Our CRUD methods are all very similar.  The Qi REST API URL templates are predefined strings.  Each method fills in the template with the parameters specific to the call, adds the protocol, server, and port of the remote Qi Service, and sets the appropriate HTTP verb.  If the call is unsuccessful, a QiError is thrown.  Here is the call to create a single event in a data stream:

```c#
	public async Task CreateEventAsync(string streamId, string singleEvent)
	{
		string requestUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.InsertSingleBaseUrl;
		await InsertEventDataIntoStreamAsync(requestUrl, singleEvent);
	}
```

The main program creates a single `WaveData` event with the `Order` 0 and inserts it.  Then it creates 99 more sequential events and inserts them with a single call:

```c#
	TimeSpan span = new TimeSpan(0, 1, 0);
	WaveData evt = WaveData.Next(span, 2.0, 0);

	qiclient.CreateEventAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();

	List<WaveData> events = new List<WaveData>();
	for (int i = 2; i < 200; i += 2)
	{
		evt = WaveData.Next(span, 2.0, i);
		events.Add(evt);
		Thread.Sleep(400);
	}

	qiclient.CreateEventsAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();
```

## Retrieve Events

There are many methods in the Qi REST API allowing for the retrieval of events from a stream.  The retrieval methods take string type start and end values; in our case, these the start and end ordinal indices expressed as strings ("0" and "99", respectively).  The index values must capable of conversion to the type of the index assigned in the QiType.  Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator.  `QiClient` implements only two of the many available retrieval methods:

```c#
	public async Task<string> GetWindowValuesAsync(string streamId, string startIndex, string endIndex)

	public async Task<string> GetRangeValuesAsync(string streamId, string startIndex, int skip, int count, bool reverse, QiBoundaryType boundaryType)
```

'GetWindowValuesAsync' can be used to get events over a specific index range.  'GetRangeValuesAsync' can be used to get a specified number of events from a starting index point:

```c#
	string jCollection = qiclient.GetWindowValuesAsync("evtStream", "0", "198").Result;
	WaveData[] foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
	
	jCollection = qiclient.GetRangeValuesAsync("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
	foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
```

## Update Events

We'll demonstrate updates by taking the values we created and replacing them with new values.  Once you've modified the events client-side, you submit them to the Qi service with `UpdateValueAsync` or `UpdateValuesAsync`:

```c#
	qiclient.UpdateValueAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();
	qiclient.UpdateValuesAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();
```

Note that we are serializing the event or event collection and passing the string into the update method as a parameter.

## Delete Events

As with insertion, deletion of events is managed by specifying a single index or a range of index values over the type's key property. Here we are removing the single event whose `Order` property has the value 0, then removing any event on the range 1-99:    

```c#
	qiclient.RemoveValueAsync("evtStream", "0").Wait();
	qiclient.RemoveWindowValuesAsync("evtStream", "1", "99").Wait();
```
The index values are expressed as string representations of the underlying type.  DateTime index values must be expressed as ISO 8601 strings.

## Bonus: Deleting Types and Streams

You might want to run the sample more than once.  To avoid collisions with types and streams, the sample program deletes the stream and type it created before terminating.  The stream goes first so that the reference count on the type goes to zero:

```c#
	qiclient.DeleteStreamAsync("evtStream");
```

Note that we've passed the id of the stream, not the stream object.  Similarly

```c#
	qiclient.DeleteTypeAsync(evtType.Id);
```

deletes the type from the Qi service.  Recall that `evtType` is the QiType instance returned by the Qi service when the type was created. 
