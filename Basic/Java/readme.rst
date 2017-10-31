Building a Java client to make REST API calls to the Qi Service
===============================================================

The sample code described in this topic demonstrates how to use Java to store 
and retrieve data from Qi using only the Qi REST API. By examining the code, 
you will see how to establish a connection to Qi, obtain an authorization token, 
obtain a QiNamespace, create a QiType and QiStream, and how to create, read, 
update, and delete values in Qi.

This project is built using Apache Maven. To run the code in this example, you 
must first download and install the Apache Maven software. See 
`Apache Maven Project <https://maven.apache.org/download.cgi>`__ 
for more information. All of the necessary dependencies are specified within 
the pom.xml file.

Summary of steps to run the Java demo
--------------------------------------

1. Clone a local copy of the GitHub repository.
2. Install Maven.
3. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.
4. Replace the configuration strings in ``config.properties``

Java Samples: Building a Client using the Qi REST API
-----------------------------------------------------

This sample is written using only the Qi REST API. The API allows you to
create Qi Service clients in any language that can make HTTP calls. Objects 
are passed between client and server as JSON strings. The sample uses the Gson library 
for the Java client, but you can use any method to create a JSON representation 
of objects.

Instantiate a Qi Client
-----------------------

Each REST API call consists of an HTTP request along with a specific URL and
HTTP method. The URL contains the server name plus the extension
that is specific to the call. Like all REST APIs, the Qi REST API maps
HTTP methods to CRUD operations as shown in the following table:

+---------------+------------------+--------------------+
| HTTP Method   | CRUD Operation   | Content Found In   |
+===============+==================+====================+
| POST          | Create           | Message body       |
+---------------+------------------+--------------------+
| GET           | Retrieve         | URL parameters     |
+---------------+------------------+--------------------+
| PUT           | Update           | Message body       |
+---------------+------------------+--------------------+
| DELETE        | Delete           | URL parameters     |
+---------------+------------------+--------------------+

The constructor for the QiClient class takes the base URL (that is, the
protocol, server address and port number). It also creates a new Gson
serializer/deserializer to convert between Java Objects and JSON.

.. code:: java

    public QiClient(String baseUrl) {
        this.baseUrl =  baseUrl;
        this.mGson = new Gson();
    }   

Configure the Sample:
-----------------------

Included in the sample is a configuration file with placeholders 
that need to be replaced with the proper values. They include information 
for authentication, connecting to the Qi Service, and pointing to a namespace.

The Qi Service is secured using Azure Active Directory. The sample application 
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
value so authentication occurs against the correct tenant. The URL for the Qi 
Service connection must also be changed to reflect the destination address of 
the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create 
a namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` 
page. At the top the add button will create a new namespace after the required 
forms are completed. This namespace is now associated with the logged-in tenant 
and may be used in the sample.

The values to be replaced are in ``config.properties``:

.. code:: java
    resource = https://pihomemain.onmicrosoft.com/ocsapi
    authority = https://login.windows.net/<PLACEHOLDER_REPLACE_WITH_TENANT_NAME>.onmicrosoft.com
    clientId = PLACEHOLDER_REPLACE_WITH_CLIENT_ID
    clientSecret = PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET
    qiServerUrl = PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL
    tenantId = PLACEHOLDER_REPLACE_WITH_TENANT_ID
    namespaceId = PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID

Obtain an Authentication Token
------------------------------

Near the end of the ``QiClient.Java`` file is a method called
``AcquireAuthToken``. The first step in obtaining an authorization token
is to create an authentication context that is related to the Azure
Active Directory instance. The authority is designated by the URI in
``_authority``.

.. code:: java

    if (authContext == null) {
        authContext = new AuthenticationContext(authority);
    }

``AuthenticationContext`` instances are responsible for communicating
with the authority and also for maintaining a local cache of tokens.
Tokens have a fixed lifetime, typically one hour, but can be refreshed
by the authenticating authority for a longer period. If the refresh
period has expired, the credentials must be presented to the authority
again. To streamline development, the ``AcquireToken`` method hides
these details from client programmers. As long as you call
``AcquireToken`` before each HTTP call, you will have a valid token. The
following code shows how this is done:

.. code:: java

    ClientCredential userCred = new ClientCredential(appId, appKey);
    Future<AuthenticationResult> authResult = authContext.acquireToken(resource, userCred, null);
    result = authResult.get();

Create a QiType
----------------

To use Qi, you define QiTypes that describe the kinds of data you want
to store in QiStreams. QiTypes are the model that define QiStreams.
QiTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other QiTypes. For
more information about QiTypes, refer to the `Qi
documentation <https://cloud.osisoft.com/documentation>`__.

In the sample code, the QiType representing WaveData is defined in the
``getWaveDataType`` method of Program.java. WaveData contains properties
of integer and double atomic types. The function begins by defining a
base QiType for each atomic type.

.. code:: java

    QiType intType = new QiType();
    intType.Id = "intType";
    intType.QiTypeCode = QiTypeCode.Int32;

    QiType doubleType = new QiType();
    doubleType.Id = "doubleType";
    doubleType.QiTypeCode = QiTypeCode.Double;

Now you can create the key property, which is an integer type and is
named ``Order``.

.. code:: java

    QiTypeProperty orderProperty = new QiTypeProperty();
    orderProperty.Id = "Order";
    orderProperty.QiType = intType;
    orderProperty.IsKey = true;

The double value properties are created in the same way, without setting IsKey. 
Shown below is the code for creating the ``Radians`` property:

.. code:: java

    QiTypeProperty radiansProperty = new QiTypeProperty();
    radiansProperty.Id = "Radians";
    radiansProperty.QiType = doubleType;

After all of the necessary properties are created, you assign them to a
``QiType`` which defines the overall ``WaveData`` class. This is done by
creating an array of ``QiTypeProperty`` instances and assigning it to the
``Properties`` property of ``QiType``:

.. code:: java

    QiType type = new QiType();
    type.Name = "WaveData";
    type.Id = "WaveData";
    type.Description = "This is a sample stream for storing WaveData type events";
    QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
    type.Properties = props;


The WaveData type is created in Qi using the ``createType`` method in
QiClient.java.

.. code:: java

    String evtTypeString = qiclient.CreateType(type);
    evtType = qiclient.mGson.fromJson(evtTypeString, QiType.class);

All QiTypes are constructed in a similar manner. Basic QiTypes form the basis for
QiTypeProperties, which are then assigned to a complex user-defined
type. These types can then be used in properties and become part of
another QiType's property list.

Create a QiStream
------------------

A QiStream stores an ordered series of events. To create a
QiStream instance, you simply provide an Id, assign it a type, and
submit it to the Qi service. The ``createStream`` method of QiClient is
similar to createType, except that it uses a different URL. Here is how
it is called from the main program:

.. code:: java

    QiStream sampleStream = new QiStream(sampleStreamId, sampleTypeId);
    String streamJson = qiclient.createStream(tenantId, namespaceId, sampleStream);
    sampleStream = qiclient.mGson.fromJson(streamJson, QiStream.class);

Note that you set the ``TypeId`` property of the stream
to the Id of the QiType previously created.
QiTypes are reference counted, so after 
a type is assigned to one or more streams, it
cannot be deleted until all streams that reference it are deleted.

Create and Insert Values into the Stream
----------------------------------------

A single QiValue is a data point in the stream. It cannot be
empty and must have at least the key value of the QiType for the
event. Events are passed in JSON format and are serialized in
``QiClient.java``, which is then sent along with a POST request.

The main program creates a single ``WaveData`` event with the ``Order``
value of zero and inserts it into the QiStream. Then, the program creates several more sequential events
and inserts them with a single call:

.. code:: java

    // insert a single event
    WaveData evt = WaveData.next(1, 2.0, 0);
    qiclient.insertValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

    // insert an a collection of events
    List<WaveData> events = new ArrayList<WaveData>();
    for (int i = 2; i < 20; i+=2) {
        evt = WaveData.next(1, 2.0, i);
        events.add(evt);
    }
    qiclient.insertValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(events));

Retrieve Values from a Stream
-----------------------------

There are many methods in the Qi REST API that allow for the retrieval of
events from a stream. Many of the retrieval methods accept indexes,
which are passed using the URL. The index values must be capable of
conversion to the type of the index assigned in the QiType.

In this sample, four of the available methods are implemented in
QiClient: ``getLastValue``, ``getValue``, ``getWindowValues``, and ``getRangeValues``.
``getWindowValues`` can be used to retrieve events over a specific index
range. ``getRangeValues`` can be used to retrieve a specified number of
events from a starting index.

Get single value:

.. code:: java

    String jsonSingleValue = qiclient.getValue(tenantId, namespaceId, sampleStreamId, "0");
    WaveData data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class);

Get last value inserted:

.. code:: java

    jsonSingleValue = qiclient.getLastValue(tenantId, namespaceId, sampleStreamId);
    data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class));

Get window of values:

.. code:: java

    String jsonMultipleValues = qiclient.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "18");
    Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData> type
    ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);

Get range of values:

.. code:: java

    jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
    foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);

Updating and Replacing Values
-----------------------------

The examples in this section demonstrate updates by taking the values
that were created and updating them with new values. If you attempt to
update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

After you have modified the client-side events, you submit them to the
Qi Service with ``updateValue`` or ``updateValues`` as shown here:

.. code:: java

    qiclient.updateValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));
    qiclient.updateValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValue`` and ``updateValues``:

.. code:: java

    qiclient.replaceValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));
    qiclient.replaceValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

Changing Stream Behavior
------------------------

When retrieving a value, the behavior of a stream can be altered
using ``QiStreamBehaviors``. A stream is updated with a behavior,
which changes how "get" operations are performed when an index falls between,
before, or after existing values. The default behavior is continuous, so
any indices not in the stream are interpolated using the previous
and next values.

In the sample, the behavior is updated to discrete, meaning that if an index
does not correspond to a real value in the stream then ``null`` is
returned by the Qi Service. The following shows how this is done in the
code:

.. code:: java

	// create the behavior
    QiStreamBehavior behavior = new QiStreamBehavior();
    behavior.setId(sampleBehaviorId);
    behavior.setMode(QiStreamMode.Discrete);
    String behaviorString = qiclient.createBehavior(tenantId, namespaceId, behavior);
    behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class));
    
	// update the stream
    sampleStream.setBehaviorId(sampleBehaviorId);
    qiclient.updateStream(tenantId, namespaceId, sampleStreamId, sampleStream);

The sample repeats the call to ``getRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
``Order=1``.

QiViews
-------

A QiView provides a way to map stream data requests from one data type 
to another. You can apply a view to any read or GET operation. QiView 
is used to specify the mapping between source and target types.

Qi attempts to determine how to map properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, Qi will map the properties automatically.

.. code:: java

        jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStream.getId(), "1", 0, 3, false, QiBoundaryType.ExactOrCalculated, sampleViewId);

To map a property that is beyond the ability of Qi to map on its own, 
you should define a QiViewProperty and add it to the QiView\’s Properties collection.

.. code:: java

         QiViewProperty vp2 = new QiViewProperty();
         vp2.setSourceId("Sin");
         vp2.setTargetId("SinInt");
        ...
         QiView manualView = new QiView();
         manualView.setId(sampleManualViewId);
         manualView.setName("SampleManualView");
         manualView.setDescription("This is a view mapping SampleType to SampleTargetType");
         manualView.setSourceTypeId(sampleTypeId);
         manualView.setTargetTypeId(integerTargetTypeId);
         manualView.setProperties(props);

QiViewMap
---------

When a QiView is added, Qi defines a plan mapping. Plan details are retrieved as a QiViewMap. 
The QiViewMap provides a detailed Property-by-Property definition of the mapping.
The QiViewMap cannot be written, it can only be retrieved from Qi.

.. code:: java

         String jsonViewMap = qiclient.getViewMap(tenantId, namespaceId, sampleManualViewId);


Deleting Values from a Stream
-----------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Below are the
declarations of both functions:

.. code:: java

    qiclient.removeValue(tenantId, namespaceId, sampleStreamId, "0");
    qiclient.removeWindowValues(tenantId, namespaceId, sampleStreamId, "2", "40");

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to Order=2 and Order=40
are removed from the stream.

Additional Methods
------------------

Notice that there are more methods provided in QiClient than are discussed in this
document, including get methods for types, behaviors, and streams.
Each has both a single get method and a multiple get method, which
reflect the data retrieval methods covered above.  Below is an example demonstrating getStream 
and getStreams: 

.. code:: java

    // get a single stream
    String stream = qiclient.getStream(tenantId, namespaceId, sampleStreamId);
    QiStream = qiclient.mGson.fromJson(returnedStream, QiStream.class));
    // get multiple streams
    String returnedStreams = qiclient.getStreams(tenantId, namespaceId, "","0", "100");
    Type streamListType = new TypeToken<ArrayList<QiStream>>(){}.getType();
    ArrayList<QiStream> streams = qiclient.mGson.fromJson(returnedStreams, streamListType);

For a complete list of HTTP request URLs refer to the `Qi
documentation <https://cloud.osisoft.com/documentation>`__.

Cleanup: Deleting Types, Behaviors, Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream
behaviors, views and types can be achieved by a DELETE REST call and passing
the corresponding Id.

.. code:: java

    qiclient.deleteStream(tenantId, namespaceId, sampleStreamId);
    qiclient.deleteBehavior(tenantId, namespaceId, sampleBehaviorId);
	qiclient.deleteView(tenantId, namespaceId, sampleViewId);

Note that the IDs of the objects are passed, not the object themselves.
Similarly, the following code deletes the type from the Qi Service:

.. code:: java

    qiclient.deleteType(tenantId, namespaceId, sampleTypeId);



