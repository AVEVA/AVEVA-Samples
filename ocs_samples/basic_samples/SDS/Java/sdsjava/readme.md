Building a Java client to make REST API calls to the SDS Service
===============================================================

The sample code described in this topic demonstrates how to use Java to store 
and retrieve data from SDS using only the SDS REST API. By examining the code, 
you will see how to establish a connection to SDS, obtain an authorization token, 
obtain an SdsNamespace, create an SdsType and SdsStream, and how to create, read, 
update, and delete values in SDS.

[SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)

This project is built using Apache Maven. To run the code in this example, you 
must first download and install the Apache Maven software. See 
`Apache Maven Project <https://maven.apache.org/download.cgi>`__ 
for more information. All of the necessary dependencies are specified within 
the pom.xml file.

Developed against Maven 3.6.1 and Java 1.8.0_181.

Summary of steps to run the Java demo
--------------------------------------
Using VSCode, Eclipse or any IDE:

1. Clone a local copy of the GitHub repository.

2. Install Maven.

3. *Install the ocs_sample_library_preview to your local Maven repo using "mvn install" from \\library_samples\\Java\\ocs_sample_library_preview\\

4. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.

5. Replace the configuration strings in ``config.properties``


Using a command line:

1. Clone a local copy of the GitHub repository.

2. Download apache-maven-x.x.x.zip from http://maven.apache.org and extract it.

3. Setting environment variables.
   a) For Java JDK
      Variable name - JAVA_HOME
      Variable value - location to the Java JDK in User variables.

      and, also add JDK\bin path to the Path variable in System variables.

   b) For Maven
      Variable name - MAVEN_HOME
      Variable value - location to the extracted folder for the
                       maven ~\apache-maven-x.x.x in User variables.

      and, also add ~\apache-maven-x.x.x\bin path to the Path variable in System variables.

4. *Install the  ocs_sample_library_preview to your local Maven repo using: "mvn install" from \library_samples\Java\ocs_sample_library_preview\

5. Replace the configuration strings in ``config.properties``

. Building and running the project.
   a) cd to your project location.
   b) run "mvn package exec:java" on cmd. or "mvn test" to run the test

*Currently this project is not hosted on the central Maven repo and must be compiled and installed locally.

Java Samples: Building a Client using the SDS REST API
-----------------------------------------------------

This sample is written using the ocs_sample_library_preview library which uses the SDS REST API. The API allows you to
create SDS Service clients in any language that can make HTTP calls. Objects 
are passed between client and server as JSON strings. The sample uses the Gson library 
for the Java client, but you can use any method to create a JSON representation 
of objects.

Instantiate an OCS Client
-----------------------

Each REST API call consists of an HTTP request along with a specific URL and
HTTP method. The URL contains the server name plus the extension
that is specific to the call. Like all REST APIs, the SDS REST API maps
HTTP methods to CRUD operations as shown in the following table:

HTTP Method |CRUD Operation|Content Found In
-------|-----------|---------
POST          | Create           | message body       
GET           | Retrieve         | URL parameters     
PUT           | Update           | message body       
DELETE        | Delete           | URL parameters      


The constructor for the OCSClient class takes the base URL (that is, the
protocol, server address and port number) and the api version. It also creates a new Gson
serializer/deserializer to convert between Java Objects and JSON.  This is all done in a shared baseClient 
that is used amongst the the various services that we can interact with.
```java
public BaseClient() {
    gclientId = getConfiguration("clientId");
    gclientSecret = getConfiguration("clientSecret");
    gresource = getConfiguration("resource");
    gresource = gresource.endsWith("/") ? gresource :  gresource + "/";

    this.baseUrl = gresource;
    this.apiVersion = getConfiguration("apiVersion");
    this.mGson = new Gson();
}
```

Configure the Sample:
-----------------------

Included in the sample is a configuration file with placeholders 
that need to be replaced with the proper values. They include information 
for authentication, connecting to OCS, and pointing to a namespace.

The SDS Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide an 
application ID and secret that are authenticated against the directory. These 
are referred to as client IDs and client secrets, which are associated with 
a given tenant. They are created through the tenant's administration portal. 
The steps necessary to create a new client ID and secret are described below.

First, log on to the `Cloud Portal <http://cloud.osisoft.com>`__ with admin 
credentials and navigate to the ``Client Keys`` page under the ``Manage`` tab, 
which is situated along the top of the webpage. Two types of keys may be 
created. For a complete explanation of key roles look at the help bar on the 
right side of the page. This sample program covers data creation, deletion and 
retrieval, so an administration key must be used in the configuration file. 
Creating a new key is simple. Enter a name for the key, select ``Administrator 
role``, then click ``Add Key``.

Next, view the key by clicking the small eye icon on the right of the created 
key, located in the list of available keys. A pop-up will appear with the 
tenant ID, client ID and client secret. These must replace the corresponding 
values in the sample's configuration file. 

Along with client ID and secret values, add the tenant name to the authority 
value so authentication occurs against the correct tenant. The URL for the SDS 
Service connection must also be changed to reflect the destination address of 
the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create 
a namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` 
page. At the top the add button will create a new namespace after the required 
forms are completed. This namespace is now associated with the logged-in tenant 
and may be used in the sample.

The values to be replaced are in ``config.properties``:

'''
resource = https://dat-b.osisoft.com
clientId = REPLACE_WITH_APPLICATION_IDENTIFIER
clientSecret = REPLACE_WITH_APPLICATION_SECRET
tenantId = REPLACE_WITH_TENANT_ID
namespaceId = REPLACE_WITH_NAMESPACE_ID
apiVersion = v1
'''

Obtain an Authentication Token
------------------------------

Near the end of the ``BaseClient.Java`` file is a method called
``AcquireAuthToken``. The first step in obtaining an authorization token
is to connect to the Open ID discovery endpoint and get a URI for obtaining the token.
Thereafter, the token based on ``clientId`` and ``clientSecret`` is retrieved.

The token is cached, but as tokens have a fixed lifetime, typically one hour. It can be refreshed
by the authenticating authority for a longer period. If the refresh
period has expired, the credentials must be presented to the authority
again. To streamline development, the ``AcquireToken`` method hides
these details from client programmers. As long as you call
``AcquireToken`` before each HTTP call, you will have a valid token. 

Create an SdsType
----------------

To use SDS, you define SdsTypes that describe the kinds of data you want
to store in SdsStreams. SdsTypes are the model that define SdsStreams.
SdsTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the `SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__.

In the sample code, the SdsType representing WaveData is defined in the
``getWaveDataType`` method of Program.java. WaveData contains properties
of integer and double atomic types. The function begins by defining a
base SdsType for each atomic type.

```java
SdsType intType = new SdsType();
intType.Id = "intType";
intType.SdsTypeCode = SdsTypeCode.Int32;

SdsType doubleType = new SdsType();
doubleType.Id = "doubleType";
doubleType.SdsTypeCode = SdsTypeCode.Double;
```

Now you can create the key property, which is an integer type and is
named ``Order``.

```java
SdsTypeProperty orderProperty = new SdsTypeProperty();
orderProperty.Id = "Order";
orderProperty.SdsType = intType;
orderProperty.IsKey = true;
```

The double value properties are created in the same way, without setting IsKey. 
Shown below is the code for creating the ``Radians`` property:

```java
SdsTypeProperty radiansProperty = new SdsTypeProperty();
radiansProperty.Id = "Radians";
radiansProperty.SdsType = doubleType;
```

After all of the necessary properties are created, you assign them to a
``SdsType`` which defines the overall ``WaveData`` class. This is done by
creating an array of ``SdsTypeProperty`` instances and assigning it to the
``Properties`` property of ``SdsType``:

```java
SdsType type = new SdsType();
type.Name = "WaveData";
type.Id = "WaveData";
type.Description = "This is a sample stream for storing WaveData type events";
SdsTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
type.Properties = props;
```


The WaveData type is created in SDS using the ``createType`` method in
SdsClient.java.

```java
String evtTypeString = ocsClient.Types.CreateType(type);
evtType = ocsClient.mGson.fromJson(evtTypeString, SdsType.class);
```

All SdsTypes are constructed in a similar manner. Basic SdsTypes form the basis for
SdsTypeProperties, which are then assigned to a complex user-defined
type. These types can then be used in properties and become part of
another SdsType's property list.

Create an SdsStream
------------------

A SdsStream stores an ordered series of events. To create a
SdsStream instance, you simply provide an Id, assign it a type, and
submit it to the SDS service. The ``createStream`` method of SdsClient is
similar to createType, except that it uses a different URL. Here is how
it is called from the main program:

```java
SdsStream sampleStream = new SdsStream(sampleStreamId, sampleTypeId);
String streamJson = ocsClient.Streams.createStream(tenantId, namespaceId, sampleStream);
sampleStream = ocsClient.mGson.fromJson(streamJson, SdsStream.class);
```

Note that you set the ``TypeId`` property of the stream
to the Id of the SdsType previously created.
SdsTypes are reference counted, so after 
a type is assigned to one or more streams, it
cannot be deleted until all streams that reference it are deleted.

Create and Insert Values into the Stream
----------------------------------------

A single SdsValue is a data point in the stream. It cannot be
empty and must have at least the key value of the SdsType for the
event. Events are passed in JSON format and are serialized in
``SdsClient.java``, which is then sent along with a POST request.

The main program creates a single ``WaveData`` event with the ``Order``
value of zero and inserts it into the SdsStream. Then, the program creates several more sequential events
and inserts them with a single call:

```java
// insert a single event
List<WaveData> event = new ArrayList<WaveData>();
WaveData evt = WaveData.next(1, 2.0, 0);
event.add(evt);
ocsClient.Streams.insertValues(tenantId, namespaceId, sampleStreamId, sdsclient.mGson.toJson(event));

// insert an a collection of events
List<WaveData> events = new ArrayList<WaveData>();
for (int i = 2; i < 20; i+=2) {
evt = WaveData.next(1, 2.0, i);
events.add(evt);
}
ocsClient.Streams.insertValues(tenantId, namespaceId, sampleStreamId, sdsclient.mGson.toJson(events));
```

Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API that allow for the retrieval of
events from a stream. Many of the retrieval methods accept indexes,
which are passed using the URL. The index values must be capable of
conversion to the type of the index assigned in the SdsType.

In this sample, five of the available methods are implemented in
StreamsClient: ``getLastValue``, ``getValue``, ``getWindowValues``, ``getRangeValues``, and ``getSampledValues``.
``getWindowValues`` can be used to retrieve events over a specific index
range. ``getRangeValues`` can be used to retrieve a specified number of
events from a starting index. ``getSampledValues`` can retrieve a sample of your data to show the overall 
trend. In addition to the start and end index, we also 
provide the number of intervals and a sampleBy parameter. Intervals parameter 
determines the depth of sampling performed and will affect how many values
are returned. SampleBy allows you to select which property within your data you want the samples to be based on.

Get single value:

```java
String jsonSingleValue = ocsClient.Streams.getValue(tenantId, namespaceId, sampleStreamId, "0");
WaveData data = ocsClient.mGson.fromJson(jsonSingleValue, WaveData.class);
```

Get last value inserted:

```java
jsonSingleValue = ocsClient.Streams.getLastValue(tenantId, namespaceId, sampleStreamId);
data = ocsClient.mGson.fromJson(jsonSingleValue, WaveData.class));
```

Get window of values:

```java
String jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "18");
Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData> type
ArrayList<WaveData> foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
```

Get range of values:

```java
jsonMultipleValues = ocsClient.Streams.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, SdsBoundaryType.ExactOrCalculated);
foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);   
```

Get sampled values:

```java
jsonMultipleValues = ocsClient.Streams.getSampledValues(tenantId, namespaceId, sampleStreamId, "0", "40", 4, "Sin");
foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
```

Updating and Replacing Values
-----------------------------

The examples in this section demonstrate updates by taking the values
that were created and updating them with new values. If you attempt to
update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

After you have modified the client-side events, you submit them to the
SDS Service with ``updateValues`` as shown here:

```java
ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvent));
ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvents));
```

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValues``:

```java
ocsClient.Streams.replaceValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvent));
ocsClient.Streams.replaceValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvents));
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

```java
// Create a Discrete stream PropertyOverride indicating that we do not want SDS to calculate a value for Radians and update our stream 
SdsStreamPropertyOverride propertyOverride = new SdsStreamPropertyOverride();
propertyOverride.setSdsTypePropertyId("Radians");
propertyOverride.setInterpolationMode(SdsInterpolationMode.Discrete);
List<SdsStreamPropertyOverride> propertyOverrides = new ArrayList<SdsStreamPropertyOverride>();
propertyOverrides.add(propertyOverride);

// update the stream   		 	
sampleStream.setPropertyOverrides(propertyOverrides);
ocsClient.Streams.updateStream(tenantId, namespaceId, sampleStreamId, sampleStream);
```

The process consists of two steps. First, the Property Override must be created, then the
stream must be updated. Note that the sample retrieves three data points
before and after updating the stream to show that it has changed. See
the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html) for
more information about SDS Property Overrides.

SdsStreamViews
-------

A SdsStreamView provides a way to map stream data requests from one data type 
to another. You can apply a stream view to any read or GET operation. SdsStreamView 
is used to specify the mapping between source and target types.

SDS attempts to determine how to map properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, SDS will map the properties automatically.

```java
jsonMultipleValues = ocsClient.Streams.getRangeValues(tenantId, namespaceId, sampleStream.getId(), "1", 0, 3, false, SdsBoundaryType.ExactOrCalculated, sampleStreamViewId);
```

To map a property that is beyond the ability of SDS to map on its own, 
you should define an SdsStreamViewProperty and add it to the SdsStreamView's Properties collection.

```java
SdsStreamViewProperty vp2 = new SdsStreamViewProperty();
vp2.setSourceId("Sin");
vp2.setTargetId("SinInt");
...
SdsStreamView manualStreamView = new SdsStreamView();
manualStreamView.setId(sampleManualStreamViewId);
manualStreamView.setName("SampleManualStreamView");
manualStreamView.setDescription("This is a StreamView mapping SampleType to SampleTargetType");
manualStreamView.setSourceTypeId(sampleTypeId);
manualStreamView.setTargetTypeId(integerTargetTypeId);
manualStreamView.setProperties(props);
```

SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS.

```java
String jsonStreamViewMap = ocsClient.Streams.getStreamViewMap(tenantId, namespaceId, sampleStreamViewId);
```


Deleting Values from a Stream
-----------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Below are the
declarations of both functions:

```java
ocsClient.Streams.removeValue(tenantId, namespaceId, sampleStreamId, "0");
ocsClient.Streams.removeWindowValues(tenantId, namespaceId, sampleStreamId, "2", "40");
```

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to Order=2 and Order=40
are removed from the stream.

Additional Methods
------------------

Notice that there are more methods provided in SdsClient than are discussed in this
document, including get methods for types, and streams.
Each has both a single get method and a multiple get method, which
reflect the data retrieval methods covered above.  Below is an example demonstrating getStream 
and getStreams: 

```java
// get a single stream
String stream = ocsClient.Streams.getStream(tenantId, namespaceId, sampleStreamId);
SdsStream = ocsClient.mGson.fromJson(returnedStream, SdsStream.class));
// get multiple streams
String returnedStreams = ocsClient.Streams.getStreams(tenantId, namespaceId, "","0", "100");
Type streamListType = new TypeToken<ArrayList<SdsStream>>(){}.getType();
ArrayList<SdsStream> streams = ocsClient.mGson.fromJson(returnedStreams, streamListType);
```

For a complete list of HTTP request URLs refer to the `SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__.

Cleanup: Deleting Types, Stream Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream, stream views and 
types can be achieved by a DELETE REST call and passing
the corresponding Id.

```java
ocsClient.Streams.deleteStream(tenantId, namespaceId, sampleStreamId);
ocsClient.Streams.deleteStreamView(tenantId, namespaceId, sampleStreamViewId);
```

Note that the IDs of the objects are passed, not the object themselves.
Similarly, the following code deletes the type from the SDS Service:

```java
ocsClient.Types.deleteType(tenantId, namespaceId, sampleTypeId);
```

-------------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) 

--------------

Tested against Maven 3.6.1 and Java 1.8.0_212.

For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OCS page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)

