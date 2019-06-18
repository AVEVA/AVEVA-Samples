.NET Samples 
============

Building a Client with the OCS Client Libraries
----------------------------------------------

The sample described in this section makes use of the OSIsoft Cloud Services Client Libraries.   When working in .NET, 
it is recommended that you use the OCS Client Libraries metapackage, OSIsoft.OCSClients. The metapackage is a NuGet package available 
from https://api.nuget.org/v3/index.json. The libraries offer a framework of classes that make client development easier.

[SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)


Developed against DotNet 2.2.300.

Getting Starting
----------------------------

In this example we assume that you have the dotnet core CLI.

To run this example from the commandline run

```
dotnet restore
dotnet run
```

to test this program change directories to the test and run

```
dotnet restore
dotnet test
```


Configure constants for connecting and authentication
-----------------------------------------------------

The SDS Service is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

```json
{
"NamespaceId": "REPLACE_WITH_NAMESPACE_ID",
"TenantId": "REPLACE_WITH_TENANT_ID",
"Resource": "https://dat-b.osisoft.com",
"ClientId": "REPLACE_WITH_APPLICATION_IDENTIFIER",
"ClientKey": "REPLACE_WITH_APPLICATION_SECRET"
}
```



The authentication values are provided to the ``OSIsoft.Identity.AuthenticationHandler``. 
The AuthenticationHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

Set up SDS clients
-----------------

The client example works through two client interfaces: 

* ISdsMetadataService for SdsStream, SdsType, SdsStreamView metadata operations
* ISdsDataService for reading and writing data

The following code block illustrates how to configure clients to use throughout the sample:

```C#
AuthenticationHandler authenticationHandler = new AuthenticationHandler(resource, clientId, clientKey);

SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
var metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
var dataService = sdsService.GetDataService(tenantId, namespaceId);
```
  

Create an SdsType
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want to store in 
SdsStreams. SdsTypes are the model that define SdsStreams.

SdsTypes can define simple atomic types, such as integers, floats or strings, or they 
can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the `SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__.

When working with the SDS Client Libraries, it is strongly recommended that you use 
SdsTypeBuilder. SdsTypeBuilder uses reflection to build SdsTypes. The SdsTypeBuilder exposes 
a number of methods for manipulating types. One of the simplest ways to create a type 
is to use one of its static methods:

```c#
SdsType type = SdsTypeBuilder.CreateSdsType<WaveData>();

// When defining the type, specify the key as follows:
public class WaveData 
{
	[SdsMember(IsKey = true)]
	public int Order { get; set; }
	public double Tau { get; set; }
	public double Radians { get; set; }
	...
}
```
    
To define the SdsType in SDS, use the metadata client as follows:

```c#
SdsType type = config.GetOrCreateTypeAsync(type).GetAwaiter().GetResult();
```

To Create a type with a compound index we create a new type specifying 2 keys and an order for them:

```C#
public class WaveDataCompound
{
		[SdsMember(IsKey = true, Order = 0)]
		public int Order { get; set; }

		[SdsMember(IsKey = true, Order = 1)]
		public int Multiplier { get; set; }

		public double Tau { get; set; }
```


Create an SdsStream
------------------

An ordered series of events is stored in an SdsStream. All you have to do
is create a local SdsStream instance, give it an Id, assign it a type,
and submit it to the SDS Service. The value of the ``TypeId`` property is
the value of the SdsType ``Id`` property.

```C#
Console.WriteLine("Creating an SdsStream");
var stream = new SdsStream
{
	Id = streamId,
	Name = "Wave Data Sample",
	TypeId = type.Id,
	Description = "This is a sample SdsStream for storing WaveData type measurements"
};
```


As with the SdsType, once an SdsStream is created locally, use the metadata client 
to submit it to the SDS Service:

```C#
stream = await metadataService.GetOrCreateStreamAsync(stream);
```

To create an SdsStream with a secondary index we define this when creating the stream.  In the snippet below we find the property that we are making a secondary index and then we assign it:

```C#
SdsStreamIndex measurementIndex = new SdsStreamIndex()
{
	SdsTypePropertyId = type.Properties.First(p => p.Id.Equals("Radians")).Id
};
SdsStream secondary = new SdsStream()
{
	Id = streamIdSecondary,
	TypeId = type.Id,
	Indexes = new List<SdsStreamIndex>()
	{
		measurementIndex
	}
};
```

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the SDS type for the
event.  First the event is created locally by instantiating a new WaveData 
object:

```C#
return new WaveData
	{
	Order = order,
	Radians = radians,
	Tau = radians / (2 * Math.PI),
	Sin = multiplier * Math.Sin(radians),
	Cos = multiplier * Math.Cos(radians),
	Tan = multiplier * Math.Tan(radians),
	Sinh = multiplier * Math.Sinh(radians),
	Cosh = multiplier * Math.Cosh(radians),
	Tanh = multiplier * Math.Tanh(radians)
	};
```

Then use the data service client to submit the event using the InsertValueAsync method:

```C#
await dataService.InsertValueAsync(stream.Id, wave);
```

Similarly, we can build a list of objects and insert them in bulk by calling 
InsertValuesAsync:

```C#
var waves = new List<WaveData>();
for (var i = 2; i <= 18; i += 2)
{
	waves.Add(GetWave(i, 200, 2));
}
await dataService.InsertValuesAsync(stream.Id, waves);
```


Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the SdsType.

```C#
IEnumerable<WaveData> retrieved = 
		client.GetWindowValuesAsync<WaveData>(stream.Id, "0", "20").GetAwaiter().GetResult();
```
	
SDS can retreive the values in the form of a table (in this case with headers)

```C#
SdsTable tableEvents = await tableService.GetWindowValuesAsync(stream.Id, "0", "180");
```
	
	
SDS can retreive interpolated values.  In this case we are asking for values at 5, 14, 23, and 32.  We onlt have values stored at the even numbers, so the odd numbers will be interpolated for.

```C#
IEnumerable<WaveData> retrievedInterpolated = await dataService.GetValuesAsync<WaveData>(stream.Id, "5", "32", 4);
```
	
When retreiving events you can also filter on what is being returned, so you only get the events you are interested in.

```C#
IEnumerable<WaveData> retrievedInterpolatedFiltered = (await dataService.GetWindowFilteredValuesAsync<WaveData>(stream.Id, "0", "180", SdsBoundaryType.ExactOrCalculated, "Radians lt 50"));
```

SDS can be used to retrieve a sample of your data to show the overall 
trend. In addition to the start and end index, we also 
provide the number of intervals and a sampleBy parameter. Intervals parameter 
determines the depth of sampling performed and will affect how many values
are returned. SampleBy allows you to select which property within your data you want the samples to be based on.

```C#
IEnumerable<WaveData> sampledValues = await dataService.GetSampledValuesAsync<WaveData>(stream.Id, "0", "40", 4, new[] {nameof(WaveData.Sin)});
```

Update Events and Replacing Values
----------------------------------

Updating events is handled using the data service client as follows:

```C#
await dataService.UpdateValueAsync(stream.Id, updatedWave);
```

Updates can be made in bulk by passing a collection of WaveData objects:

```C#
var updatedCollection = new List<WaveData>();
for (int i = 2; i < 40; i = i+2)
{
	updatedCollection.Add(GetWave(i, 400, 4));
}
await dataService.UpdateValuesAsync(stream.Id, updatedCollection);
```

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValue`` and ``updateValues``:

```C#
await dataService.ReplaceValueAsync<WaveData>(streamId, replaceEvent);	

await dataService.ReplaceValuesAsync<WaveData>(streamId, allEvents);
```

Property Overrides
------------------

SDS has the ability to override certain aspects of an SDS Type at the SDS Stream level.  
Meaning we apply a change to a specific SDS Stream without changing the SDS Type or the
read behavior of any other SDS Streams based on that type.  

In the sample, the InterpolationMode is overridden to a value of Discrete for the property Radians. 
Now if a requested index does not correspond to a real value in the stream, null, 
or the default value for the data type, is returned by the SDS Service. 
The following shows how this is done in the code:

```C#            
// create a Discrete stream PropertyOverride indicating that we do not want SDS to calculate a value for Radians and update our stream 
var propertyOverride = new SdsStreamPropertyOverride()
	{
	SdsTypePropertyId = "Radians",
	InterpolationMode = SdsInterpolationMode.Discrete
	};
var propertyOverrides = new List<SdsStreamPropertyOverride>() {propertyOverride};

// update the stream
stream.PropertyOverrides = propertyOverrides;
await metadataService.CreateOrUpdateStreamAsync(stream);
```

The process consists of two steps. First, the Property Override must be created, then the
stream must be updated. Note that the sample retrieves three data points
before and after updating the stream to show that it has changed. See
the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html) for
more information about SDS Property Overrides.

SdsStreamViews
-------

An SdsStreamView provides a way to map Stream data requests from one data type 
to another. You can apply a Stream View to any read or GET operation. SdsStreamView 
is used to specify the mapping between source and target types.

SDS attempts to determine how to map Properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, SDS will map the properties automatically.

```C#
var autoStreamViewData = await dataService.GetRangeValuesAsync<WaveDataTarget>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, autoStreamViewId);
```

To map a property that is beyond the ability of SDS to map on its own, 
you should define an SdsStreamViewProperty and add it to the SdsStreamView's Properties collection.

```C#
// create explicit mappings 
var vp1 = new SdsStreamViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
var vp2 = new SdsStreamViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
var vp3 = new SdsStreamViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
var vp4 = new SdsStreamViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

var manualStreamView = new SdsStreamView()
{
	Id = manualStreamViewId,
	SourceTypeId = typeId,
	TargetTypeId = targetIntTypeId,
	Properties = new List<SdsStreamViewProperty>() { vp1, vp2, vp3, vp4 }
};

await metadataService.CreateOrUpdateStreamViewAsync(manualStreamView);
```

You can also use a streamview to change a Stream's type.


```C#
await metadataService.UpdateStreamTypeAsync(stream.Id, manualStreamView);
```

SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS. 

```C#
var manualStreamViewMap = await metadataService.GetStreamViewMapAsync(manualStreamViewId);
```

Delete Values from a Stream
---------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Code from both functions
is shown below:

```C#
await dataService.RemoveValueAsync(stream.Id, 0);

await dataService.RemoveWindowValuesAsync(stream.Id, 1, 40);
```

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to '1' and '40'
are removed from the stream.

Cleanup: Deleting Types, StreamViews and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream views and 
types can be achieved using the metadata client and passing the corresponding 
object Id:

```C#
await metadataService.DeleteStreamAsync(streamId);
await metadataService.DeleteTypeAsync(typeId);
```

------------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

-----------

Tested against DotNet 2.2.105.

For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
