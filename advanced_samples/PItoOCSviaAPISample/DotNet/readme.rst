
PI to OCS Samples 
============

The purpose of this sample code is to demonstrate the use of the AF SDK and the OSIsoft Cloud Services (OCS) 
client libraries to copy data from a PI Data Archive into OCS. This illustrates the definition and creation
of appropriate Sds Stream Types and streams to represent PI data and the subsequent transmission of the data
itself. The project is a complete (very simple) command line application that takes a PIPoint name search 
mask (e.g. sinu*), a start time and an endtime and writes all the data found for the points and time range
into OCS.

Building a client with the Sds Client Libraries
----------------------------------------------

The sample described in this section makes use of the OSIsoft Sds Client Libraries to write data to OCS.
When working in .NET, it is recommended that you use these libraries. The libraries are available 
as NuGet packages from https://api.nuget.org/v3/index.json. The packages used are:

* OSIsoft.Contracts
* OSIsoft.Models
* OSIsoft.Http.Client  
* OSIsoft.Http.Security 

The libraries offer a framework of classes that make client development easier.

Configure constants for connecting and authentication
-----------------------------------------------------

OSIsoft Cloud Services is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an app.config configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from the OCS Portal. 

::
   <appSettings>	  
     <add key="address" value="https://dat-a.osisoft.com" />
     <add key="accountId" value="REPLACE_WITH_ACCOUNT_ID" />
     <add key="resource" value="https://qihomeprod.onmicrosoft.com/ocsapi" />
     <add key="clientId" value="REPLACE_WITH_CLIENT_IDENTIFIER" />
     <add key="clientSecret" value="REPLACE_WITH_CLIENT_SECRET" />
	 ...
   </appSettings>
	
The authentication values are provided to the ``OSIsoft.Http.Security.SdsSecurityHandler``. 
The SdsSecurityHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

Other Configuration
-------------------
   <appSettings>
     ...	 
     <add key="namespaceId" value="REPLACE_WITH_NAMESPACE_ID" />
     <add key="PIDataArchive" value="REPLACE_WITH_SERVER_NAME" />
   </appSettings>

Set up Sds clients
-----------------

The client example works through two client interfaces: 

* ISdsMetadataService for SdsStream, SdsType, SdsView and SdsStreamBehavior metadata operations
* ISdsDataService for reading and writing data

The following code block illustrates how to configure clients to use throughout the sample:

```csharp
	SdsSecurityHandler securityHandler = new SdsSecurityHandler(resource, tenant, clientId, clientKey);

	SdsService sdsService = new SdsService(new Uri(address), securityHandler);
	var metadataService = sdsService.GetMetadataService(tenant, namespaceId);
	var dataService = sdsService.GetDataService(tenant, namespaceId);
   ```
Create SdsTypes
---------------

To use Sds, you define SdsTypes that describe the kinds of data you want to store in 
SdsStreams. SdsTypes are the model that define SdsStreams.

PI point data can generally be represented as as a SdsType with a DateTime index and some
other value property. The PI to OCS via OMF sample defines five different possible values 
property kinds in five different SdsTypes. The value properties are integer, float, string,
time and blob (byte array).

When working with the Sds Client Libraries, it is strongly recommended that you use 
SdsTypeBuilder. SdsTypeBuilder uses reflection to build SdsTypes. The SdsTypeBuilder exposes 
a number of methods for manipulating types. One of the simplest ways to create a type 
is to use one of its static methods as is done below for the type representing an integer PIPoint:

```csharp

	IntegerSdsType = SdsTypeBuilder.CreateSdsType<IntegerData>();
    IntegerSdsType.Id = "PIIntegerValueAndTimestamp";
    IntegerSdsType.Name = "PIIntegerValueAndTimestamp";
    IntegerSdsType.Description = "Represents simple time series data with an integer value";
 
	public class IntegerData
    {
        [SdsMember(IsKey = true, Order = 0)]
        public DateTime Timestamp { get; set; }
        public Int64 Value { get; set; }
    }
  ```  
This type is then defined in OCS by using the metadataService as follows:

```csharp
	metadataService.CreateOrUpdateTypeAsync(IntegerSdsType).GetAwaiter().GetResult();
```
Note that this simple Sds Type does not include the IsGood property of a PIPoint and does not handle
system digital states written when IsGood == false. It also does not contain a field for annotations.
These fields could be added to the type by simply adding properties to the underlying class (IntegerData).

Create SdsStreams
------------------

In OSIsoft Cloud Services, an ordered series of events is stored in a SdsStream. In this
sample, a PI point maps directly to a SdsStream. All the data written to a single SdsStream 
is read from a single PI point.

As with the SdsTypes, SdsStreams can be created in OCS via the client library as is done in the sample code
in the method CreateStreamBasedOnPIPoints. One thing to note is that there are restrictions as to the format
and characters used for a unique StreamID and we have provided an example method to compose StreamIDs that
comply with these rules based on the PI Server and PIPoint name: GetStreamId(AFSDK.PI.PIPoint point).

	
Read PI point data
----------------------------------------

PI point data is read from a configured PI server using the OSIsoft AF SDK client. Further documentation
is available either as part of installation kit of AF SDK or at : https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/1a02af4c-1bec-4804-a9ef-3c7300f5e2fc.htm

In this example command line application the data to be read is specified by passing the following command line parameters:
a search mask for the PIPoint name, the start time and end time of the data range to be retrieved.



Write PI point data to OSIsoft Cloud Services
----------------------------------------

A single PI point event translates to a single event in a SdsStream. The events for an individual stream can be
sent in bulk and this is done in the example, sending all values retrieved for a single PIPoint:

```csharp

	private static void WriteDataForIntegerStream(ISdsDataService data, List<AFValue> afValues, string streamId)
    {
        var dataList = new List<StreamTypes.IntegerData>();
		dataList.AddRange(afValues.Where(val => val.IsGood).Select(val => new StreamTypes.IntegerData()
		{
			Timestamp = val.Timestamp,
			Value = val.ValueAsInt32()
		}));
		data.UpdateValuesAsync(streamId, dataList).GetAwaiter().GetResult();
    }
```
As previously mentioned this sample selects only good values and does not consider annotations. If these are relevant
to a particular analysis they could be included by modifying this method (and the ones for the other types) along 
with ReadDataFromPIAndWriteToOcs to retrieve and send the additional information.

