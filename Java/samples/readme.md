#Java Samples: Building a Client with the Qi REST API

This sample is written using only the Qi REST API.  This API allows for the creation of Qi Service clients in any language that can make HTTP calls and does not require access to any OSIsoft libraries.  Objects are passed as JSON strings.  We're using the Gson library for the Java client, but any method of creating a JSON representation of objects will work.

## Instantiate a Qi Client

The CRUD methods encapsulate the Qi REST API.  Each call consists of an HTTP request with a specific URL and HTTP method.  The URL is the server plus the extension specific to the call.  Like all REST APIs, the Qi REST API maps HTTP methods to CRUD like this:

| HTTP Method | CRUD Operation | Content Found In |
|-------------|----------------|------------------|
| POST        | Create         | message body     |
| GET         | Retrieve       | URL parameters   |
| PUT         | Update         | message body     |
| DELETE      | Delete         | URL parameters   |

The constructor for our QiClient class takes the base URL (i.e., protocol plus server and port number).

```Java
	public QiClient(String baseUrl)
	{
	
 	  java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		this.baseUrl =  baseUrl;
		
		try
		{
			url = new URL(this.baseUrl);		
			urlConnection = getConnection(url, "POST");
		}	
	}	
```

## Obtain an Authentication Token

The Qi Service is secured by obtaining tokens from an Azure Active Directory instance.  The sample applications are examples of a *confidential client*.  Such clients provide a user ID and secret that are authenticated against the directory.   The sample code includes several placeholder strings.  You must replace these with the authentication-related values you received from OSIsoft.  The strings are found at the beginning of `QiClient.Java`.

```Java
  static string _resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
  static string _authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
  static string _appId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
  static string _appKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
```

At the bottom of `QiClient.Java` you will find a method called `AcquireAuthToken`.  The first step in obtaining an authorization token is to create an authentication context related to the Azure Active Directory instance providing tokens.  The authority is designated by the URI in `_authority`.
```Java
    if (_authContext == null)
    {
        _authContext = new AuthenticationContext(_authority);
    }
```

`AuthenticationContext` instances take care of communicating with the authority and also maintain a local cache of tokens.  Tokens have a fixed lifetime, typically one hour, but they can be refreshed by the authenticating authority for a longer period.  If the refresh period has expired, the credentials have to be presented to the authority again.  Happily, the `AcquireToken` method hides these details from client programmers.  As long as you call `AcquireToken` before each HTTP call, you will have a valid token.  Here is how that is done:

```Java
   ClientCredential userCred = new ClientCredential(_appId, _appKey);
   Future<AuthenticationResult> authResult = _authContext.acquireToken(_resource, userCred, null);
   result = authResult.get();
```

## Create a Qi Type

Qi data streams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that your data type have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer. 

Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.  

Since we are using the REST API, we must build our own type definitions. A type definition in Qi consists of one or more properties.  Each property has its own Qi type.  This can be a simple data type like integer or string, or a complex Qi data type previously defined. This allows for the creation of nested data types, where proeprties can be user-defined types.  Our sample `WaveData` class is a series of simple types.  We have created `QiType` and `QiTypeProperty` classes that match those in the Qi Libraries.  Simple types are denoted by an enumeration specified in `QiTypeCode.Java`.  The ordinal values in the latter file are those the Qi Service expects, so if you wish to create you own classes you must specify these values.

`WaveData` has one integer property and a series of double value properties.  To start, then, we create a QiType instance for each of these simple types:

```Java
    QiType intType = new QiType();
    intType.Id = "intType";
    intType.QiTypeCode = QiTypeCode.Int32;

    QiType doubleType = new QiType();
    doubleType.Id = "doubleType";
    doubleType.QiTypeCode = QiTypeCode.Double;
```

Now let's create our key property, which is an integer type and is named `Order`.

```Java
    QiTypeProperty orderProperty = new QiTypeProperty();
    orderProperty.Id = "Order";
    orderProperty.QiType = intType;
    orderProperty.IsKey = true;
```
We've specified the id, used the intType `QiType` we created, and most importantly set IsKey to `true`.  The double value properties are created similarly.  Here is the code creating the `Radians` property:

```Java
    QiTypeProperty radiansProperty = new QiTypeProperty();
    radiansProperty.Id = "Radians";
    radiansProperty.QiType = doubleType;
```
Once all the necessary properties are created, it is necessary to assign them to a `QiType` defining the overall `WaveData` class.  This is done by created an array of `QiProperty` instances and assigning it to the `Properties` property of `QiType`:

```Java
    QiType type = new QiType();
    type.Name = "WaveData";
    type.Id = "WaveData";
    type.Description = "This is a sample stream for storing WaveData type events";
    QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
    type.Properties = props;
```
If you wanted to nest a user defined type within another QiType, you would begin by defining the contained type as a `QiType` using the methods illustrated above, then create a `QiProperty` with that type and assign it to the containing class.

All this creates a type definition locally, but it has to be submitted in a REST call before it becomes available to the Qi Service for the creation of streams. The create call URL has the extention `/Qi/Types`, and the body of the request message is the JSON format serialization of the `QiType` just created.  This is wrapped in the `CreateType` method of `QiClient`:

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
		}catch (IllegalStateException e) {
			e.getMessage();
		}        
		catch (Exception e) {
			e.printStackTrace();
		}



		try{
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

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}



		}catch (Exception e){

			e.printStackTrace();

		}

		return response.toString();


	}
```

After creating the `HttpURLConnection` with the proper URL and HTTP method, we call `AcquireAuthToken` and attach the result to the message as a header.  This ensures that each call always has a valid authentication token. The main program calls the method like this.

```Java
   String evtTypeString = qiclient.CreateType(type);
   evtType = qiclient.mGson.fromJson(evtTypeString, QiType.class);
```

We've chosen to return the JSON serialization returned from the Qi Service and deserialize it in the main program, a topic we'll return to when we discuss data calls.
*Note: The various Create methods in Qi will return an HTTP status code of 302 (Found) if you attempt to create an entity (in this case, a type definition) that exists in the system. The client then follows the redirect URI. In the current version of the Qi, this will fail with an HTTP status code of 401 (Unauthorized) rather than succeed following a 302 (Found) result.  This will be corrected in future versions.*

## Create a Qi Stream

An ordered series of events is stored in a Qi stream.  We've created a `QiStream` class mirroring the properties of the native Qi Service `QiStream` class. All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream.  This is the code to create a stream named `evtStream` for recording events of our sample type.  The value of the `TypeId` property is the value of the QiType `Id` property.  The `CreateStream` method of `QiClient` is similar to `CreateType`, except that it uses a different URL.  Here is how it is called from the main program:

```Java
   QiStream stream = new QiStream("evtStreamJ",evtType.getId());
   String evtStreamString = qiclient.CreateStream(stream);
   evtStream = qiclient.mGson.fromJson(evtStreamString, QiStream.class);
```
Note that we set the `TypeId` property of the stream we created to the value of the Id of the QiType instance returned by the call to `GetOrCreateType`. Qi types are reference counted (as are behaviors), so once a type is assigned to one or more streams, it cannot be deleted until all streams using it are deleted.

## Create and Insert Events into the Stream

The `WaveData` class allows us to create events locally.  In an actual production setting, this is where you would interface with your measurements.  We'll use the `Next` method to create values, and assign integers from 0..99 to establish an ordered collection of `WaveData` instances.  Our `QiClient` class provides methods for inserting a single event or an array of events.  The Qi REST API provides many more types of data insertion calls, so `QiClient` is by no means complete with respect to the full capabilities of the Qi Service.

It would be possible to pass in a `WaveData` instance (or array of instances), but then our event creation methods would be particular to a specific class. We've made the decision to handle all serialization and deserialization outside the `QiClient` class and pass the results into and out of the methods.  This allows us to change the defintion of the event class without changing the CRUD methods of our client class to take advantage of the fact that the Qi Service stores and manipulates arbitrary, user defined types.

Our CRUD methods are all very similar.  The REST API URL templates are predefined strings.  Each method fills in the template with the parameters specific to the call, adds the protocol, server, and port of the remote Qi Service, and sets the appropriate HTTP verb.  If the call is unsuccessful, a QiError is thrown.  Here is the call to create a single event in a data stream:

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
		}catch (IllegalStateException e) {
			e.getMessage();
		}      
		catch (Exception e) {
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



		}catch (Exception e){
             e.printStackTrace();


		}
	}
```

The main program creates a single `WaveData` event with the `Order` 0 and inserts it.  Then it creates 99 more sequential events and inserts them with a single call:

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

There are many methods in the Qi REST API allowing for the retrieval of events from a stream.  The retrieval methods take string type start and end values; in our case, these the start and end ordinal indices expressed as strings ("0" and "99", respectively).  The index values must capable of conversion to the type of the index assigned in the QiType.  Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator.  `QiClient` implements one of the available retrieval methods:

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

We'll demonstrate updates by taking the values we created and replacing them with new values.  Once you've modified the events client-side, you submit them to the Qi Service with `UpdateValue` or `UpdateValues`:

```Java
   qiclient.updateValue(evtStream.getId(), qiclient.mGson.toJson(evt));
   qiclient.updateValues(evtStream.getId(),qiclient.mGson.toJson(events));
```

Note that we are serializing the event or event collection and passing the string into the update method as a parameter.
##Stream Behaviors
Only recorded values are returned by `GetWindowValues`.  If you want to get a particular range of values and interpolate events at the endpoints of the range, you may use `GetRangeValues`.  The nature of the interpolation performed is determined by the stream behavior assigned to the stream.  if you do not specify one, a linear interpolation is assumed.  This example demonstrates a stepwise interpolation using stream behaviors.  More sophisticated behavior is possible, including the specification of interpolation behavior at the level of individual event type properties.  This is discussed in the [Qi API Reference](https://qi-docs.readthedocs.org/en/latest/Overview/).  First, before changing the stream's retrieval behavior, call `GetRangeValues` specifying a start index value of 1 (between the first and second events in the stream) and calculated values:

```Java      
          jCollection = qiclient.getRangeValues("evtStreamJ", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
          foundEvents = qiclient.mGson.fromJson(jCollection, listType);
```

This gives you a calculated event with linear interpolation at index 1.

Now, we define a new stream behavior object and submit it to the Qi Service:

```Java
  QiStreamBehavior behavior = new QiStreamBehavior();
  behavior.setId("evtStreamStepLeading") ;
  behavior.setMode(QiStreamMode.StepwiseContinuousLeading);
  String behaviorString = qiclient.CreateBehavior(behavior);
  behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class);
```

By setting the `Mode` property to `StepwiseContinuousLeading` we ensure that any calculated event will have an interpolated index, but every other property will have the value of the recorded event immediately preceding that index.  Now attach this behavior to the existing stream by setting the `BehaviorId` property of the stream and updating the stream definition in the Qi Service:

```Java#
   evtStream.setBehaviorId("evtStreamStepLeading");
   qiclient.UpdateStream("evtStreamJ", evtStream);
```

The sample repeats the call to `GetRangeValues` with the same parameters as before, allowing you to compare the values of the event at `Order=1`.

## Delete Events

As with insertion, deletion of events is managed by specifying a single index or a range of index values over the type's key property. Here we are removing the single event whose `Order` property has the value 0, then removing any event on the range 1..99:    

```Java
   qiclient.removeValue(evtStream.getId(), "0");
   qiclient.removeWindowValues(evtStream.getId(), "1", "99");
```
The index values are expressed as string representations of the underlying type.  DateTime index values must be expressed as ISO 8601 strings.

## Cleanup: Deleting Types and Streams

You might want to run the sample more than once.  To avoid collisions with types and streams, the sample program deletes the stream, stream behavior and Qi type it created before terminating, thereby resetting your tenant environment to the state before running the sample.  The stream goes first so that the reference count on the type goes to zero:

```Java
   qiclient.deleteStream("evtStreamJ");
    qiclient.DeleteBehavior("evtStreamStepLeading");
```

Note that we've passed the id of the stream, not the stream object.  Similarly

```Java
   qiclient.deleteType("evtType.getId()");
```

deletes the type from the Qi Service.  Recall that `evtType` is the QiType instance returned by the Qi Service when the type was created. 
