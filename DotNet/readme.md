#.NET Samples: Building a Client with the Qi Libraries

This sample differs from the other samples in that the client makes use of the OSIsoft Qi libraries, which are available as nuget packages from **placeholder**.  Ultimately, the Qi REST APIs are invoked just like the rest of the samples, but the libraries offer a framework of classes to make client development easier.

## Instantiate a Qi Client

The client works through the `IQiServer` interface.  You instantiate it through a client factory on which you set a timeout for REST calls.  You must add two headers to every REST call, a `QiTenant` whose value is your tenant id and a `Bearer` authentication header whose value is the token returned by Azure Active Directory.  Here's the code:

```c#
    QiHttpClientFactory<IQiServer> clientFactory = new QiHttpClientFactory<IQiServer>();
    clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);
    clientFactory.OnCreated((p) => p.DefaultHeaders.Add("QiTenant", "sampletenant"));
    IQiServer qiclient = clientFactory.CreateChannel(new Uri(server));
```

## Obtain an Authentication Token

The sample code includes several placeholder strings.  You must replace these with the authentication-related values you received from OSIsoft **placeholder**.

## Create a Qi Type

Qi is capable of storing any data type you care to define.  Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.  

The Qi Libraries permit the creation of Qi Types via reflection.  For simple types like our sample type, this may not seem like an advantage over the type creation illustrated in the REST samples.  For more complex types, particularly when you wish to nest complex types, reflection makes your job far easier!

The first step to taking advantage of reflection is to create a .NET class.  Our sample definition is in `SimpleEvent.cs`.  Note the lines

```c#
    [Key]
    public DateTime Timestamp
    {
        get;
        set;
    }
```

This creates a timestamp property and marks it as the index for this type.  The `Key` attribute comes from the `System.ComponentModel.DataAnnotations` namespace.  Remember, Qi allows the use of non-time indices, and also permits compound indices.

Now, back in the client code, we create a type builder object and use it to create an instance of the Qi type:

```c#
    QiTypeBuilder typeBuilder = new QiTypeBuilder();
    QiType evtType = typeBuilder.Create<SimpleEvent>();
```

Note that `Create` is a generic method, and the type is the name of the class defining the type.  After you have a type, you set the `Id` property.  While we've created and configured a QiType object locally, we haven't created anything in the Qi Service, so you must submit it like this:

```c#
    qiclient.GetOrCreateType(evtType);
```

## Create a Qi Stream

Anything in your process that you wish to measure is a stream in Qi, like a point or tag in the classic Pi Archive.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream.  This is the code to create a stream named `evtStream` for recording events of our sample type.  The value of the `TypeId` property is the value of the QiType `Id` property.

```c#
    QiStream sampleStream = new QiStream();
    sampleStream.Name = "evtStream";
    sampleStream.Id = "evtStream";
    sampleStream.TypeId = "SimpleEvent";
    sampleStream.Description = "This is a sample stream for storing SimpleEvent type measurements";
    QiStream strm = qiclient.GetOrCreateStream(sampleStream);
```
Qi types are reference counted (as are behaviors), so once a type is assigned to one or more streams, it cannot be deleted until all streams using it are deleted.

## Create and Insert Events into the Stream

The `SimpleEvent` class allows us to create events locally.  In an actual production setting, this is where you would interface with your measurements.  We'll use the `Random` class to create values, and assign timestamps for a range 100 seconds into the past.  There are a number of methods you can use.  A single event can be inserted using InsertValue<T> or InsertValueAsync<T> (all Async methods use .NET TPL, see <https://msdn.microsoft.com/en-us/library/hh191443.aspx>).  You can also submit a collection of events using `InsertValues<T>` or `InsertValuesAsync<T>`.  There is also an overloaded version of InsertValues that takes an `IDictionary`.  Here is an edited version of the insertion code:

```c#
      SimpleEvent evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");
      DateTime start = DateTime.UtcNow.AddSeconds(-100.0);
      evt.Timestamp = start;
      qiclient.InsertValue("evtStream", evt);

      List<SimpleEvent> events = new List<SimpleEvent>();
      for (int i = 1; i < 100; i++)
      {
        evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");
        evt.Timestamp = start.AddSeconds((double)i);
        events.Add(evt);
      }
      qiclient.InsertValues<SimpleEvent>("evtStream", events);
```

## Retrieve Events

There are many methods that allow for the retrieval of events from a stream.  This sample demonstrates the most basic method of retrieving all the events on a particular time range.  The retrieval methods take start and end values; in our case, these are timestamp values converted to a round-trip format.  In general, the index values must be of the same type as the index assigned in the QiType.  Compound indices are values concatenated with a pipe ('|') separator.  You can get a collection of events on a time range like this:

```c#
IEnumerable<SimpleEvent> foundEvts = qiclient.GetWindowValues<SimpleEvent>("evtStream", start.ToString("o"), DateTime.UtcNow.ToString("o"));
```

Keep in mind that with an IEnumerable instance, there are a variety of LINQ and extension methods allowing you to manipulate the events locally.

## Update Events

We'll demonstrate updates by taking the values we created and converting them from Celsius to Fahrenheit (remember to update the units of measure!).  Once you've modified the events client-side, you submit them to the Qi Service with `UpdateValue<T>` or `UpdateValues<T>`, or their asynchronous equivalents:

```c#
    qiclient.UpdateValue<SimpleEvent>("evtStream", evt);
    qiclient.UpdateValues<SimpleEvent>("evtStream", events);
```

## Delete Events

As with insertion, deletion of events is managed by a range over the type's index.  In our case, this is a time range.  

```c#
    qiclient.RemoveValue<DateTime>("evtStream", evt.Timestamp);
    qiclient.RemoveWindowValues("evtStream", foundEvts.First<SimpleEvent>().Timestamp.ToString("o"), foundEvts.Last<SimpleEvent>().Timestamp.ToString("o"));
```
This isn't as imposing as it appears here.  In the sample code, we retrieved the events, obtaining a collection, `foundEvents`.  We also manipulated a single event, `evt`.  We get the timestamp values from these objects and convert them to strings using the `o` predefined format string to create a round-trip time string.  The singular remove method is a generic whose type is the type of the event type's index property (for us, a `DateTime`).

## Bonus: Deleting Types and Streams

You might want to run the sample more than once.  To avoid collisions with types and streams, the sample program deletes the stream and Qi type it created before terminating.  The stream goes first so that the reference count on the type goes to zero:

```c#
qiclient.DeleteStream("evtStream")
```

Note that we've passed the id of the stream, not the stream object.  Similarly

```c#
qiclient.DeleteType("SimpleEvent");
```

deletes the type from the Qi Service.  The `IQiServer` instance doesn't need any cleanup.  REST runs on HTTP, which is stateless, so the Qi Service is not maintaining a connection with the client.
