#.NET Samples: Building a Client with the Qi Libraries

This sample differs from the other samples in that the client makes use of the OSIsoft Qi libraries, which are available as nuget packages from **placeholder**.  The packages used are `OSIsoft.Qi.Core`, `OSIsoft.Qi.Http.Channel`, and `OSIsoft.Qi.Http.Client`. Ultimately, the Qi REST APIs are invoked just like the rest of the samples, but the libraries offer a framework of classes to make client development easier.

## Instantiate a Qi Client

The client works through the `IQiServer` interface.  You instantiate it through a client factory on which you set a timeout for REST calls.  You must add an `Authorization` header to every REST call. The value of this header is the scheme keyword `Bearer` followed by the token returned by Azure Active Directory.  Here's the code:

```c#
    QiHttpClientFactory<IQiServer> clientFactory = new QiHttpClientFactory<IQiServer>();
    clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);

    IQiServer qiclient = clientFactory.CreateChannel(new Uri(server));
    IQiClientProxy proxy = (IQiClientProxy)qiclient;
    proxy.OnBeforeInvoke((handler)=>{
        string token = AcquireAuthToken();
        if (proxy.Client.DefaultHeaders.Contains("Authorization"))
        {
             proxy.Client.DefaultHeaders.Remove("Authorization");
        }
        proxy.Client.DefaultHeaders.Add("Authorization", new AuthenticationHeaderValue("Bearer", token).ToString());
    });
    
```

The cast of the client object to `IQiClientProxy` gives you access to the `OnBeforeInvoke` delegate. Since security tokens expire, we give the authentication libraries a chance to refresh the token, if needed, before every call. The lambda implementing this calls `AcquireAuthToken`, which we'll describe in the next section, then turns to the `DefaultHeaders` collection.  This collection will throw an exception if you try to add more than one `Authorization` header, so we remove any existing header before attaching the new one.

## Obtain an Authentication Token

The Qi Service is secured by obtaining tokens from an Azure Active Directory instance.  The sample applications are examples of a *confidential client*.  Such clients provide a user ID and secret that are authenticated against the directory.   The sample code includes several placeholder strings.  You must replace these with the authentication-related values you received from OSIsoft.  The strings are found at the beginning of `Program.cs`.

```c#
        static string _resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        static string _authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        static string _appId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        static string _appKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
```

At the bottom of `Program.cs` you will find a method called `AcquireAuthToken`.  The first step in obtaining an authorization token is to create an authentication context related to the Azure Active Directory instance providing tokens.  The authority is designated by the URI in `_authority`.

```c#
    if (_authContext == null)
    {
        _authContext = new AuthenticationContext(_authority);
    }
```

`AuthenticationContext` instances take care of communicating with the authority and also maintain a local cache of tokens.  Tokens have a fixed lifetime, typically one hour, but they can be refreshed by the authenticating authority for a longer period.  If the refresh period has expired, the credentials have to be presented to the authority again.  Happily, the `AcquireToken` method hides these details from client programmers.  As long as you call `AcquireToken` before each HTTP call, you will have a valid token.  Here is how that is done:

```c#
    try
    {
        ClientCredential userCred = new ClientCredential(_appId, _appKey);
        AuthenticationResult authResult = _authContext.AcquireToken(_resource, userCred);
        return authResult.AccessToken;
    }
    catch (AdalException)
    {
        return string.Empty;
    }
```

The result returned by `AcquireAuthToken` is the value, `token`, attached to the client object in the line you saw in the previous section:

```c#
    clientFactory.OnCreated((p)=>p.DefaultHeaders.Add("Authorization", new AuthenticationHeaderValue("Bearer", token).ToString()));
```

The current version of the Qi Libraries do not permit you to attach a header prior to making a call on the client.  This does not matter for our sample, but a long-lived client would run into trouble when the token expired.  The proper pattern is to call `AcquireAuthToken` before each call and attach the token returned.  Future versions of the Qi Libraries will support this.

## Create a Qi Type

Qi data streams represent open-ended collections of strongly-typed, ordered events. Qi is capable of storing any data type you care to define.  The only requirement is that your data type have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.  

The Qi Libraries permit the creation of Qi Types via reflection.  For simple types like our sample type, this may not seem like an advantage over the type creation illustrated in the REST samples.  For more complex types, particularly when you wish to nest complex types, reflection makes your job far easier!

The first step to taking advantage of reflection is to create a .NET class.  Our sample definition is in `WaveData.cs`.  This class has an `Order` property for a key, and properties for radians and the common trigonometric and hyperbolic trigonometric functions of the value of the radians properties.  The class illustrates how Qi can store non-traditional custom types. Note the lines

```c#
    [Key]
    public int Order
    {
        get;
        set;
    }
```

This creates an Order property and marks it as the index for this type.  The `Key` attribute comes from the `System.ComponentModel.DataAnnotations` namespace.  There are two other ways to specify the key for your custom type.  If you use the `QiMember` attribute from the `OSIsoft.Qi` namespace, set the `IsKey` property to true.  If you prefer to use data contracts from the `System.Runtime.Serialization` namespace, create a `DataMember` property whose property name ends in `id` (case insensitive). Qi also permits compound indices.

Now, back in the client code, we create a type builder object and use it to create an instance of the Qi type:

```c#
    QiTypeBuilder typeBuilder = new QiTypeBuilder();
    evtType = typeBuilder.Create<WaveData>();
```

Note that `Create` is a generic method, and the type is the name of the class defining the type.  While we've created and configured a QiType object locally, we haven't created anything in the Qi Service, so you must submit it like this:

```c#
    QiType tp = qiclient.GetOrCreateType(evtType);
```
The Qi Service will assign a unique name and id to the QiType that is returned, and you will need the id when you create a stream, so be sure to capture the returned QiType instance.

*Note: In the current version of the Qi, calls to GetOrCreateX when the entity (in this case, type definition) exists will fail with an HTTP status code of 401 (Unauthorized) rather than succeed following a 302 (Found) result.  This will be corrected in future versions.*

## Create a Qi Stream

An ordered series of events is stored in a Qi stream.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream.  This is the code to create a stream named `evtStream` for recording events of our sample type.  The value of the `TypeId` property is the value of the QiType `Id` property.

```c#
    QiStream sampleStream = new QiStream();
    sampleStream.Name = "evtStream";
    sampleStream.Id = "evtStream";

    sampleStream.TypeId = tp.Id;
    sampleStream.Description = "This is a sample stream for storing WaveData type measurements";
    QiStream strm = qiclient.GetOrCreateStream(sampleStream);
```
Note that we set the `TypeId` property of the stream we created to the value of the Id of the QiType instance returned by the call to `GetOrCreateType`. Qi types are reference counted (as are behaviors), so once a type is assigned to one or more streams, it cannot be deleted until all streams using it are deleted.

## Create and Insert Events into the Stream

The `WaveData` class allows us to create events locally.  In an actual production setting, this is where you would interface with your measurements.  We'll use the `Next` method to create values, and assign integers from 0..99 to establish an ordered collection of `WaveData` instances.  There are a number of methods you can use to insert values into the Qi Service.  A single event can be inserted using `InsertValue<T>` or `InsertValueAsync<T>` (all Async methods use .NET TPL, see <https://msdn.microsoft.com/en-us/library/hh191443.aspx>).  You can also submit a collection of events using `InsertValues<T>` or `InsertValuesAsync<T>`.  There is also an overloaded version of `InsertValues` that takes an `IDictionary`.  Here is an edited version of the insertion code:

```c#
    TimeSpan span = new TimeSpan(0, 0, 1);
    WaveData evt = WaveData.Next(span, 2.0, 0);

    qiclient.InsertValue("evtStream", evt);

    List<WaveData> events = new List<WaveData>();
    for (int i = 1; i < 100; i++)
    {
        evt = WaveData.Next(span, 2.0, i);
        events.Add(evt);
    }
    qiclient.InsertValues<WaveData>("evtStream", events);
```

## Retrieve Events

There are many methods that allow for the retrieval of events from a stream.  This sample demonstrates the most basic method of retrieving all the events on a particular time range.  The retrieval methods take string type start and end values; in our case, these the start and end ordinal indices expressed as strings ("0" and "99", respectively).  The index values must capable of conversion to the type of the index assigned in the QiType.  Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('|') separator.  You can get a collection of events on a time range like this:

```c#
    IEnumerable<WaveData> foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "99");
```

Keep in mind that with an IEnumerable instance, there are a variety of LINQ and extension methods allowing you to manipulate the events locally.

## Update Events

We'll demonstrate updates by taking the values we created and replacing them with new values.  Once you've modified the events client-side, you submit them to the Qi Service with `UpdateValue<T>` or `UpdateValues<T>`, or their asynchronous equivalents:

```c#
    qiclient.UpdateValue<WaveData>("evtStream", evt);
    qiclient.UpdateValues<WaveData>("evtStream", newEvents);
```

## Delete Events

As with insertion, deletion of events is managed by a range over the type's index.    

```c#
    qiclient.RemoveValue<int>("evtStream", 0);
    qiclient.RemoveWindowValues<int>("evtStream", 1, 99);
```
The type of the index property is specified as the type of the generic method.

## Bonus: Deleting Types and Streams

You might want to run the sample more than once.  To avoid collisions with types and streams, the sample program deletes the stream and Qi type it created before terminating.  The stream goes first so that the reference count on the type goes to zero:

```c#
    qiclient.DeleteStream("evtStream")
```

Note that we've passed the id of the stream, not the stream object.  Similarly

```c#
    qiclient.DeleteType(evtType.Id);
```

deletes the type from the Qi Service.  Recall that `evtType` is the QiType instance returned by the Qi Service when the type was created. The `IQiServer` instance doesn't need any cleanup.  REST runs on HTTP, which is stateless, so the Qi Service is not maintaining a connection with the client.
