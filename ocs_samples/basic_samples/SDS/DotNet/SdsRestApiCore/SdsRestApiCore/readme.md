.NET Samples using API Calls
============

Developed against DotNet 2.2.105.

Building a Client with the rest calls directly
----------------------------------------------

The sample does not makes use of the OSIsoft Cloud Services Client Libraries.   When working in .NET, 
it is generally recommended that you use the OCS Client Libraries metapackage, OSIsoft.OCSClients. The metapackage is a NuGet package available 
from https://api.nuget.org/v3/index.json. The libraries offer a framework of classes that make client development easier.

[SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)


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

The sample authenticates your clientId and ClientKey to open access to the API:
```C#
SdsSecurityHandler securityHandler = new SdsSecurityHandler(resource, clientId, clientKey);
HttpClient httpClient = new HttpClient(securityHandler)
    {
        BaseAddress = new Uri(resource)
    };
```
The TenantId and NamespaceId will be used in the constructing of the various API calls used throughout the sample:
```C#
response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}...
```

Create an SdsType
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want to store in 
SdsStreams. SdsTypes are the model that define SdsStreams.

SdsTypes can define simple atomic types, such as integers, floats or strings, or they 
can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the `SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__.

To create an SdsType with a rest call:
```C#
SdsType waveType = BuildWaveDataType(TypeId);
response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveType.Id}",
                        new StringContent(JsonConvert.SerializeObject(waveType)));
```

Create an SdsStream
------------------

An ordered series of events is stored in an SdsStream. All you have to do
is create a local SdsStream instance, give it an Id, assign it a type,
and submit it to the SDS Service. The value of the ``TypeId`` property is
the value of the SdsType ``Id`` property.
```C#
 Console.WriteLine("Creating a SdsStream");
                SdsStream waveStream = new SdsStream
                {
                    Id = StreamId,
                    Name = "WaveStream",
                    TypeId = waveType.Id
                };
```

Once an SdsStream is created locally, structure the API call:
```C#
response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
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
                Tanh = multiplier * Math.Tanh(radians),
            };
```
Then submit the event using the proper API call:
```C#
response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(singleWaveList)));
```
Similarly, we can build a list of objects and insert them in bulk by sending multiple waves in the API call:
```C#
List<WaveData> waves = new List<WaveData>();
                for (int i = 2; i < 20; i += 2)
                {
                    WaveData newEvent = GetWave(i, 2, 2.0);
                    waves.Add(newEvent);
                }
response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(waves)));
```
Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the SdsType.
```C#
response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex={waves[waves.Count - 1].Order}");
List<WaveData> retrievedList = JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
```
The values can be retrieved in the form of a table (in this case with headers):
```C#
response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex={waves[waves.Count - 1].Order}&form=tableh");
```
You can retrieve a sample of your data to show the overall 
trend. In addition to the start and end index, we also 
provide the number of intervals and a sampleBy parameter. Intervals parameter 
determines the depth of sampling performed and will affect how many values
are returned. SampleBy allows you to select which property within your data you want the samples to be based on.

```C#
response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Sampled?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count-1].Order}&intervals={4}&sampleBy={nameof(WaveData.Sin)}");
var retrievedSamples = JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
```

Update Events and Replacing Values
----------------------------------

Updating events is handled using the API client as follows:
```C#
response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(updateWave)));
```

Updates can be made in bulk by passing a collection of WaveData objects:
```C#
List<WaveData> updateWaves = new List<WaveData>();
for (int i = 0; i < 40; i += 2)
{
    WaveData newEvent = GetWave(i, 4, 4.0);
    updateWaves.Add(newEvent);
}

response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(updateWaves)));
```

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
as follows:
```C#
response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?allowCreate=false",
                new StringContent(JsonConvert.SerializeObject(replaceSingleWaveList)));

response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?allowCreate=false",
                new StringContent(JsonConvert.SerializeObject(replaceEvents)));
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
SdsStreamPropertyOverride propertyOverride = new SdsStreamPropertyOverride
    {
        SdsTypePropertyId = "Radians",
        InterpolationMode = SdsInterpolationMode.Discrete
    };

var propertyOverrides = new List<SdsStreamPropertyOverride>() { propertyOverride };

 // update the stream
waveStream.PropertyOverrides = propertyOverrides;
response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
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
response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Transform?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}&streamViewId={AutoStreamViewId}");
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
                    Id = ManualStreamViewId,
                    SourceTypeId = TypeId,
                    TargetTypeId = TargetIntTypeId,
                    Properties = new List<SdsStreamViewProperty>() { vp1, vp2, vp3, vp4 }
                };

                response =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}",
                    new StringContent(JsonConvert.SerializeObject(autoStreamView)));
                CheckIfResponseWasSuccessful(response);
```
You can also use a streamview to change a Stream's type.
```C#
response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Type?streamViewId={AutoStreamViewId}", null);
```
SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS.
```C#
response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}/Map");

response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}/Map");
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
response = await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?index=0");

response = await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex=40");
```
As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to '0' and '40'
are removed from the stream.

Cleanup: Deleting Types, StreamViews and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream views and 
types can be achieved using the metadata client and passing the corresponding 
object Id:

```C#
// Delete the stream, types and streamViews
RunInTryCatch(httpClient.DeleteAsync, $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}");
RunInTryCatch(httpClient.DeleteAsync,($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TypeId}"));
```

----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNetAPI)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

----------------

Tested against DotNet 2.2.105.

For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
