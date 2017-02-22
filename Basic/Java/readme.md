## Development environment

This project is bulit as a `Maven` project, which requires you to have
Maven installed. All of the necesssary dependencies are specified within
the pom.xml file.

##Steps to Run

1. Clone a local copy of the Git repo.
2. Install Maven
3. If you are using Eclipse, select `File` -> `Import` -> `Maven`-> `Existing maven project` and then select the local copy.

#Java Samples: Building a Client using the Qi REST API

This sample is written using only the Qi REST API. The API allows you to 
create Qi Service clients in any language that can make HTTP
calls and does not require access to any OSIsoft libraries. Objects are
passed as JSON strings. The sample uses the Gson library for the Java
client, but any method of creating a JSON representation of objects will
work.

## Instantiate a Qi Client

The CRUD (Create, Read, Update, Delete) methods encapsulate the Qi REST API. Each call consists of an
HTTP request along with a specific URL and HTTP method. The URL is made up of the server name
plus the extension that is specific to the call. Like all REST APIs, the Qi REST
API maps HTTP methods to CRUD as shown in the following table:


| HTTP Method | CRUD Operation | Content Found In |
|-------------|----------------|------------------|
| POST        | Create         | Message body     |
| GET         | Retrieve       | URL parameters   |
| PUT         | Update         | Message body     |
| DELETE      | Delete         | URL parameters   |

The constructor for the QiClient class takes the base URL (that is, the protocol plus server and port number).

```Java
	public QiClient(String baseUrl)
	{
		mGson = new GsonBuilder().registerTypeAdapter(GregorianCalendar.class, new UTCDateTypeAdapter()).setDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'").create();
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		this.baseUrl =  baseUrl;
		
		try
		{
			url = new URL(this.baseUrl);		
			urlConnection = getConnection(url, "POST");
			urlConnection.setDoOutput(true);
			urlConnection.setRequestMethod("POST");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}
		catch (ProtocolException e)
		{
			e.getMessage();
		}         
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}	
```

## Obtain an Authentication Token

The Qi Service is secured by obtaining tokens from an Azure Active
Directory instance. The sample applications are examples of a
*confidential client*. Confidential clients provide a user ID and secret that
are authenticated against the directory. The sample code includes
several placeholder strings. You must replace the placeholder strings with the
authentication values you received from OSIsoft. The strings are
found at the beginning of the `QiClient.Java` file.


```Java
  static string _resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
  static string _authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
  static string _appId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
  static string _appKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
```

Near the end of the `QiClient.Java` file is a method called
`AcquireAuthToken`. The first step in obtaining an authorization token
is to create an authentication context that is related to the Azure Active
Directory instance. The authority is designated by the
URI in `_authority`.

```Java
    if (_authContext == null)
    {
        _authContext = new AuthenticationContext(_authority);
    }
```

`AuthenticationContext` instances are responsible for communicating with the
authority and also for maintaining a local cache of tokens. Tokens have a fixed
lifetime, typically one hour, but can be refreshed by the
authenticating authority for a longer period. If the refresh period has
expired, the credentials must be presented to the authority again.
To streamline development, the `AcquireToken` method hides these details from client
programmers. As long as you call `AcquireToken` before each HTTP call,
you will have a valid token. The following code shows how this is done:


```Java
   ClientCredential userCred = new ClientCredential(_appId, _appKey);
   Future<AuthenticationResult> authResult = _authContext.acquireToken(_resource, userCred, null);
   result = authResult.get();
```

## Create a Qi Type

Qi data streams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that your data type have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer. 

Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.  

Because the example uses the REST API, you must build your own type definitions. A type definition in Qi consists of one or more properties.  Each property has its own Qi type.  The Qi type can be a simple data type such as an integer or a string, or it can be a complex Qi data type that was defined previously. You can also create nested data types, where proeprties can be
user-defined types. The sample `WaveData` class is a series of simple types. The sample creats `QiType` and `QiTypeProperty` classes that match those in the Qi Libraries. Simple types are denoted by an enumeration specified in `QiTypeCode.Java`. The ordinal values in the latter file are those the Qi Service expects, so if you wish to create you own classes you must specify these values.

`WaveData` has one integer property and a series of double value properties.  To start, then, you create a QiType instance for each of these simple types, as shown here:

```Java
    QiType intType = new QiType();
    intType.Id = "intType";
    intType.QiTypeCode = QiTypeCode.Int32;

    QiType doubleType = new QiType();
    doubleType.Id = "doubleType";
    doubleType.QiTypeCode = QiTypeCode.Double;
```

Now you can create the key property, which is an integer type and is named `Order`.

```Java
    QiTypeProperty orderProperty = new QiTypeProperty();
    orderProperty.Id = "Order";
    orderProperty.QiType = intType;
    orderProperty.IsKey = true;
```
You have specified the ID, used the intType `QiType` you created, and most importantly, set IsKey to `true`.  The double value properties are created in the same way. Shown below is the code for creating the `Radians` property:

```Java
    QiTypeProperty radiansProperty = new QiTypeProperty();
    radiansProperty.Id = "Radians";
    radiansProperty.QiType = doubleType;
```
After all of the necessary properties are created, you assign them to a `QiType` which defines the overall `WaveData` class. This is done by created an array of `QiProperty` instances and assigning it to the `Properties` property of `QiType`:

```Java
    QiType type = new QiType();
    type.Name = "WaveData";
    type.Id = "WaveData";
    type.Description = "This is a sample stream for storing WaveData type events";
    QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
    type.Properties = props;
```
To nest a user defined type within another QiType, you begin by defining the contained type as a `QiType` using the methods shown above, then create a `QiProperty` with that type and assign it to the containing class.

All of the preceeding steps create a type definition locally, but the definition must be submitted in a REST call before it becomes available to the Qi Service for the creation of streams. The create call URL has the extention `/Qi/Types`, and the body of the request message is the JSON format serialization of the `QiType` just created. This is wrapped in the `CreateType` method of `QiClient`:

```Java
       	public String CreateType(QiType typeDef)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl + typesBase );
			urlConnection = getConnection(url,"POST");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}        
		catch (Exception e) 
		{
			e.printStackTrace();
		}

		try
		{
			String body = mGson.toJson(typeDef);           
			OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
			OutputStreamWriter writer = new OutputStreamWriter(out);
			writer.write(body);
			writer.close();

			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("type creation request succeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Type creation failed");
			}

			BufferedReader in = new BufferedReader(
					new InputStreamReader(urlConnection.getInputStream()));

			while ((inputLine = in.readLine()) != null) 
			{
				response.append(inputLine);
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}

		return response.toString();
	}
```

After creating the `HttpURLConnection` with the proper URL and HTTP method, you call `AcquireAuthToken` and attach the result to the message as a header. This ensures that each call always has a valid authentication token. The main program calls the method, as shown here:

```Java
   String evtTypeString = qiclient.CreateType(type);
   evtType = qiclient.mGson.fromJson(evtTypeString, QiType.class);
```

You have chosen to return the JSON serialization returned from the Qi Service and deserialize it in the main program, a topic we'll return to when data calls are discussed.

*Note: The various Create methods in Qi return an HTTP status code of 302 (Found) if you attempt to create an entity (in this case, a type definition) that already exists in the system. The client then follows the redirect URI. In the current version of Qi, the call will fail with an HTTP status code of 401 (Unauthorized) rather than succeed following a 302 (Found) result. This will be corrected in future versions.*

## Create a Qi Stream

An ordered series of events is stored in a Qi stream. You have created a `QiStream` class that mirrors the properties of the native Qi Service `QiStream` class. All you have to do now is create a local QiStream instance, assign it an ID, assign it a type, and submit it to the Qi Service. You may optionally assign a stream behavior to the stream. The code creates a stream named `evtStream` for recording events of the sample type. The value of the `TypeId` property is the value of the QiType `Id` property. The `CreateStream` method of `QiClient` is similar to `CreateType`, except that it uses a different URL. Here is how it is called from the main program:

```Java
   QiStream stream = new QiStream("evtStreamJ",evtType.getId());
   String evtStreamString = qiclient.CreateStream(stream);
   evtStream = qiclient.mGson.fromJson(evtStreamString, QiStream.class);
```
Note that you set the `TypeId` property of the stream that was created to the value of the Id of the QiType instance that is returned by the call to `GetOrCreateType`. Qi types are reference counted (as are behaviors), so, after a type is assigned to one or more streams, it cannot be deleted until all streams that use it are deleted.

## Create and Insert Events into the Stream

The `WaveData` class allows you to create events locally. In a production setting, this class is where you would interface with your measurements. You will use the `Next` method to create values and assign integers from 0..99 to establish an ordered collection of `WaveData` instances. The `QiClient` class provides methods for inserting a single event or an array of events. The Qi REST API provides many more types of data insertion calls, so `QiClient` is by no means complete with respect to the full capabilities of the Qi Service.

It is possible to pass in a `WaveData` instance (or array of instances), but then the event creation methods would be particular to a specific class. All serialization and deserialization is handled outside of the `QiClient` class and the results are passed into and out of the methods. This method allows changing the defintion of the event class without changing the CRUD methods of the client class to take advantage of the fact that the Qi Service stores and manipulates arbitrary, user defined types.

The CRUD methods are all very similar to one another. The REST API URL templates are predefined strings. Each method populates the template with the parameters that are specific to the call, adds the protocol, server, and port of the remote Qi Service, and sets the appropriate HTTP verb. If the call is unsuccessful, a QiError is thrown. The following shows the call to create a single event in a data stream:

```Java
        public void CreateEvent(String streamId, String evt)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + insertSingle);
			urlConnection = getConnection(url,"POST");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}      
		catch (Exception e) 
		{
			e.printStackTrace();
		}
		
		try
		{
			OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
			OutputStreamWriter writer = new OutputStreamWriter(out);
			writer.write(evt);
			writer.close();

			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("Event creation request succeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Event creation failed");

			}
		}
		catch (Exception e)
		{
                        e.printStackTrace();
		}
	}

```

The main program creates a single `WaveData` event with the `Order` 0 and inserts it. Then, the program creates 99 more sequential events and inserts them with a single call:

```Java#
   WaveData evt = WaveData.next(1, 2.0, 0);
   qiclient.CreateEvent(evtStream.getId(), qiclient.mGson.toJson(evt));
   List<WaveData> events = new ArrayList<WaveData>();
   // how to insert an a collection of events
   for (int i = 1; i < 100; i++)
   {
     evt = WaveData.next(1, 2.0, i); 
     events.add(evt);
   }
   qiclient.CreateEvents(evtStream.getId(), qiclient.mGson.toJson(events));
```

## Retrieve Events

There are many methods in the Qi REST API that facilitate the retrieval of events from a stream. The retrieval methods take string-type start and end values; in this case, these values are the start and end ordinal indices expressed as strings ("0" and "99", respectively). The index values must be capable of conversion to the type of the index assigned in the QiType. Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator. `QiClient` implements one of the available retrieval methods:

```Java
    public String GetWindowValues (String streamId, String startIndex, String endIndex)throws QiError
```
You can use this to get a collection of events on a time range like this:

```Java
    String jCollection = qiclient.GetWindowValues(evtStream.getId(), "0", "99");
    Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType();
    ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jCollection, listType);
```

## Update Events

The examples in this section demonstrate updates by taking the values that were created and replacing them with new values. After you have modified the client-side events, you submit them to the Qi Service with `UpdateValue` or `UpdateValues` as shown here:

```Java
    qiclient.updateValue(evtStream.getId(), qiclient.mGson.toJson(evt));
    qiclient.updateValues(evtStream.getId(),qiclient.mGson.toJson(events));
```

Note the event or event collection is serialized and passed as a string into the update method as a parameter.

##Stream Behaviors
Only recorded values are returned by `GetWindowValues`. To retrieve a particular range of values and interpolate events at the endpoints of the range, you can use `GetRangeValues`. The interpolation performed is determined by the stream behavior assigned to the stream. If you do not specify a behavior, linear interpolation is assumed. The example demonstrates a stepwise interpolation using stream behaviors. More sophisticated behavior is possible, including the ability to specify interpolation behavior at the level of individual event type properties. Interpolation is discussed in the [Qi API Reference](https://qi-docs.readthedocs.org/en/latest/Overview/). Before changing the stream's retrieval behavior, you should first call `GetRangeValues`, specifying a start index value of 1 (between the first and second events in the stream) and calculated values:

```Java      
          jCollection = qiclient.getRangeValues("evtStreamJ", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
          foundEvents = qiclient.mGson.fromJson(jCollection, listType);
```

The code yields a calculated event with linear interpolation at index 1.

Now, you can define a new stream behavior object and submit it to the Qi Service, as shown here:

```Java
    QiStreamBehavior behavior = new QiStreamBehavior();
    behavior.setId("evtStreamStepLeading") ;
    behavior.setMode(QiStreamMode.StepwiseContinuousLeading);
    String behaviorString = qiclient.CreateBehavior(behavior);
    behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class);
```

By setting the `Mode` property to `StepwiseContinuousLeading` you ensure that any calculated event will have an interpolated index, but every other property will have the value of the recorded event immediately preceding that index. Now attach this behavior to the existing stream by setting the `BehaviorId` property of the stream and updating the stream definition in the Qi Service:

```Java#
    evtStream.setBehaviorId("evtStreamStepLeading");
    qiclient.UpdateStream("evtStreamJ", evtStream);
```

The sample repeats the call to `GetRangeValues` with the same parameters as before, allowing you to compare the values of the event at `Order=1`.

## Delete Events

As with insertion, deletion of events is managed by specifying a single index or a range of index values over the type's key property. The following removes the single event whose `Order` property has the value 0, then removes any event in the range 1..99:

```Java
    qiclient.removeValue(evtStream.getId(), "0");
    qiclient.removeWindowValues(evtStream.getId(), "1", "99");
```
The index values are expressed as string representations of the underlying type. DateTime index values must be expressed as ISO 8601 strings.

## Cleanup: Deleting Types and Streams

You should try running the sample more than once. To avoid collisions with types and streams, the sample program deletes the stream, stream behavior, and Qi type it created before terminating, thereby resetting your tenant environment to the state it was in before running the sample. The stream is removed first so that the reference count on the type goes to zero:

```Java
    qiclient.deleteStream("evtStreamJ");
    qiclient.DeleteBehavior("evtStreamStepLeading");
```

Note that the ID of the stream is passed, not the stream object. Similarly, the following code deletes the type from the Qi Service:

```Java
    qiclient.deleteType("evtType.getId()");
```

Recall that `evtType` is the QiType instance that is returned by the Qi Service when the type was created. 




