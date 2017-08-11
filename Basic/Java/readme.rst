Building a Java client to make REST API calls to the Qi Service
===============================================================

The sample code described in this topic demonstrates how to use Java to store 
and retrieve data from Qi using only the Qi REST API. By examining the code, 
you will see how to establish a connection to Qi, obtain an authorization token, 
obtain a QiNamespace, create a QiType and QiStream, and how to create, read, 
update, and delete values in Qi.

This project is built using Apache Maven. To run the code in this example, you 
must first download and install the Apache Maven software. See `Apache Maven Project <https://maven.apache.org/download.cgi>`__ 
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
create Qi Service clients in any language that can make HTTP calls and
does not require access to any OSIsoft libraries (which are only available for
.NET). Objects are passed as JSON strings. The sample uses the Gson library 
for the Java client, but you can use any method to create a JSON representation 
of objects.

Instantiate a Qi Client
-----------------------

Each REST API call consists of an HTTP request along with a specific URL and
HTTP method. The URL consists of the server name plus the extension
that is specific to the call. Like all REST APIs, the Qi REST API maps
HTTP methods to CRUD as shown in the following table:

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
protocol plus server and port number). It also creates a new Gson
serializer/deserializer to convert between Java Objects and JSON.

.. code:: java

    public QiClient(String baseUrl) {
        this.baseUrl =  baseUrl;
        this.mGson = new Gson();
    }   

Configure the Sample:
-----------------------

Included in the sample there is a configuration file with placeholders 
that need to be replaced with the proper values. They include information 
for authentication, connecting to the Qi Service, and pointing to a namespace.

The Qi Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide a 
application ID and secret that are authenticated against the directory. These 
are referred to as client IDs and a client secrets, which are associated with 
a given tenant. They are created through the tenant's administration portal. 
The steps necessary to create a new cient ID and secret are described below.

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
value so authenticaiton occurs against the correct tenant. The URL for the Qi 
Service conneciton must also be changed to reflect the destination address of 
the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create 
a namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` 
page. At the top the add button will create a new namespace after the required 
forms are completed. This namespace is now associated with the logged-in tenant 
and may be used in the sample.

The values to be replaced are in ``config.properties``:

.. code:: java
    _resource = https://pihomemain.onmicrosof.com/historian
    _authority = https://login.windows.net/<PLACEHOLDER_REPLACE_WITH_TENANT_NAME>.onmicrosoft.com
    _clientId = PLACEHOLDER_REPLACE_WITH_CLIENT_ID
    _clientSecret = PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET
    _qiServerUrl = PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL
    _tenantId = PLACEHOLDER_REPLACE_WITH_TENANT_ID
    _namespaceId = PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID

Obtain an Authentication Token
------------------------------

Near the end of the ``QiClient.Java`` file is a method called
``AcquireAuthToken``. The first step in obtaining an authorization token
is to create an authentication context that is related to the Azure
Active Directory instance. The authority is designated by the URI in
``_authority``.

.. code:: java

    if (_authContext == null) {
        _authContext = new AuthenticationContext(_authority);
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

    ClientCredential userCred = new ClientCredential(_appId, _appKey);
    Future<AuthenticationResult> authResult = _authContext.acquireToken(_resource, userCred, null);
    result = authResult.get();

Create a Qi Type
----------------

Qi data streams represent open-ended collections of strongly-typed,
ordered events. Qi is capable of storing any data type you care to
define. The only requirement is that your data type have one or more
properties that constitute an ordered key. While a timestamp is a very
common type of key, any ordered value is permitted. The sample type uses
an integer as a key.

Each data stream is associated with a Qi type, so that only events
conforming to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

Because the example uses the REST API, you must build your own type
definitions. A type definition in Qi consists of one or more properties.
Each property has its own Qi type. The Qi type can be a simple data type
such as an integer or a string, or it can be a complex Qi data type that
was defined previously. You can also create nested data types, where
proeprties can be user-defined types. The sample ``WaveData`` class is a
series of simple types. The sample creates ``QiType`` and
``QiTypeProperty`` objects that match those in the Qi Libraries. Simple
types are denoted by an enumeration specified in ``QiTypeCode.java``.
The ordinal values in the latter file are those the Qi Service expects,
so if you wish to create you own classes you must use these values.

``WaveData`` has one integer property and a series of double value
properties. To start, then, you create a QiType instance for each of
these simple types, as shown here:

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

You have specified the ID, used the intType ``QiType`` you created, and
most importantly, set IsKey to ``true``. The double value properties are
created in the same way, wihtout setting IsKey. Shown below is the code 
for creating the ``Radians`` property:

.. code:: java

    QiTypeProperty radiansProperty = new QiTypeProperty();
    radiansProperty.Id = "Radians";
    radiansProperty.QiType = doubleType;

After all of the necessary properties are created, you assign them to a
``QiType`` which defines the overall ``WaveData`` class. This is done by
creating an array of ``QiProperty`` instances and assigning it to the
``Properties`` property of ``QiType``:

.. code:: java

    QiType type = new QiType();
    type.Name = "WaveData";
    type.Id = "WaveData";
    type.Description = "This is a sample stream for storing WaveData type events";
    QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
    type.Properties = props;

To nest a user-defined type within another QiType, you begin by defining
the contained type as a ``QiType`` using the methods shown above, then
create a ``QiProperty`` with that type and assign it to the containing
class.

All of the preceeding steps create a type definition locally, but the
definition must be submitted in a REST call before it becomes available
to the Qi Service for the creation of streams. Each request to the
server starts with the base
``/api/Tenants/<tenant_id>/Namespaces/<namespace_id>`` where the tenant
ID and namespace ID are pulled from the configuration file. To create a
type, the URL has the extention ``/Types``, and the body of the request
message is the JSON format serialization of the local ``QiType``. This
is wrapped in the ``createType`` method of ``QiClient``:

.. code:: java

    public String createType(String tenantId, String namespaceId, QiType typeDef) throws QiError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            url = new URL(baseUrl + typesBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) );
            urlConnection = getConnection(url,"POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = mGson.toJson(typeDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK) {
                System.out.println("create type request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED) {
                throw new QiError(urlConnection, "create type request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }

The client calls ``getConnection`` for each request. This method combines
obtaining the token and establishing the connection. After creating the
``HttpURLConnection`` with the proper URL and HTTP method, it calls
``AcquireAuthToken`` and attaches the result to the message as a header.
This ensures that each call always has a valid authentication token.
``getConnection`` takes in the request URL as well as the request type
and returns the opened ``HttpURLConnection``:

.. code:: java

    public static  java.net.HttpURLConnection getConnection(URL url, String method) {
        java.net.HttpURLConnection urlConnection = null;
        AuthenticationResult token = AcquireAuthToken();
        
        try {
            urlConnection = (java.net.HttpURLConnection) url.openConnection();
            urlConnection.setRequestProperty("Accept", "*/*; q=1");
            urlConnection.setRequestMethod(method);
            urlConnection.setUseCaches(false);
            urlConnection.setConnectTimeout(50000);
            urlConnection.setReadTimeout(50000);
            urlConnection.setRequestProperty("Content-Type", "application/json");
            
            urlConnection.setRequestProperty( "Authorization", token.getAccessTokenType()+ " "+ token.getAccessToken());
            if (method == "POST" || method == "PUT" || method == "DELETE") {   
                urlConnection.setChunkedStreamingMode(0);
                urlConnection.setDoOutput(true);     
            } else if(method == "GET") {
                //Do nothing
            }
        } catch(SocketTimeoutException e) {
            e.getMessage();
        } catch (ProtocolException e) {
            e.getMessage();
        }
        catch (IllegalStateException e) {
            e.getMessage();
        } catch(Exception e) {
            e.printStackTrace();
        }

        return urlConnection;
    }

To create a type, you call ``createType``; then you can create a
local object from the returned JSON string, as shown here:

.. code:: java

    String evtTypeString = qiclient.CreateType(type);
    evtType = qiclient.mGson.fromJson(evtTypeString, QiType.class);

Note that if a type already exists with the given type identifier
then that type will be returned\*

Create a Qi Stream
------------------

An ordered series of events is stored in a Qi stream. You have created a
``QiStream`` class that mirrors the properties of the native Qi Service's
``QiStream`` class. All that remains is to create a local QiStream
instance, assign it an ID, assign it a type, and submit it to the Qi
Service. You may optionally assign a stream behavior to the stream. The
code creates a stream named ``sampleStream`` for recording events of the
sample type. The value of the ``TypeId`` property is the value of the
QiType ``Id`` property. The ``createStream`` method of ``QiClient`` is
similar to ``createType``, except that it uses a different URL. Here is
how it is called from the main program:

.. code:: java

    QiStream sampleStream = new QiStream(sampleStreamId, sampleType.getId());
    String streamJson = qiclient.createStream(_tenantId, _namespaceId, sampleStream);
    sampleStream = qiclient.mGson.fromJson(streamJson, QiStream.class);

Note that you set the ``TypeId`` property of the stream that was created
to the value of the Id of the QiType instance that is returned by the
call to ``createType``. Qi types are reference counted (as are
behaviors), so, after a type is assigned to one or more streams, it
cannot be deleted until all streams that use it are deleted.

Create and Insert Events into the Stream
----------------------------------------

The ``WaveData`` class allows you to create events locally. In a
production setting, this class is where you would interface with your
measurements. This sample uses the ``Next`` method to create values and
assign integers from 0..19, incrementing by two, to establish an ordered
collection of ten ``WaveData`` instances. The ``QiClient`` class
provides methods for inserting a single event or an array of events. The
Qi REST API provides many more types of data insertion calls, so
``QiClient`` is by no means complete with respect to the full
capabilities of the Qi Service.

It is possible to pass in a ``WaveData`` instance (or array of
instances), but then the event creation methods would be particular to a
specific class. All serialization and deserialization is handled outside
of the ``QiClient`` class and the results are passed into and out of the
methods. This method allows changing the defintion of the event class
without changing the CRUD methods of the client class to take advantage
of the fact that the Qi Service stores and manipulates arbitrary, user-defined types.

The CRUD methods are all very similar to each another. The REST API URL
templates are predefined strings. Each method populates the template
with the parameters that are specific to the call, adds the protocol,
server, and port of the remote Qi Service, and sets the appropriate HTTP
verb. If the call is unsuccessful, a QiError is thrown. The following
shows the call to insert a single value into a data stream:

.. code:: java

    url = new URL(baseUrl + insertSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
    urlConnection = getConnection(url,"POST");

The main program creates a single ``WaveData`` event with the ``Order``
0 and inserts it. Then, the program creates 19 more sequential events
and inserts them with a single call:

.. code:: java

    // insert a single event
    WaveData evt = WaveData.next(1, 2.0, 0);
    qiclient.insertValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

    // insert an a collection of events
    List<WaveData> events = new ArrayList<WaveData>();
    for (int i = 2; i < 20; i+=2) {
        evt = WaveData.next(1, 2.0, i);
        events.add(evt);
    }
    qiclient.insertValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(events));

Retrieve Events
---------------

There are many methods in the Qi REST API that facilitate the retrieval
of events from a stream. The retrieval methods take string-type start
and end values; in this case, these values are the start and end ordinal
indices expressed as strings ("0" and "18", respectively). The index
values must be capable of conversion to the type of the key value assigned
in the QiType. Timestamp keys are expressed as ISO 8601 format strings.
Compound indices are values concatenated with a pipe ('\|') separator.
``QiClient`` implements four of the available retrieval methods:

Get single value:

.. code:: java

    String jsonSingleValue = qiclient.getSingleValue(_tenantId, _namespaceId, sampleStreamId, "0");
    WaveData data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class);

Get last value inserted:

.. code:: java

    jsonSingleValue = qiclient.getLastValue(_tenantId, _namespaceId, sampleStreamId);
    data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class));

Get window of values:

.. code:: java

    String jsonMultipleValues = qiclient.getWindowValues(_tenantId, _namespaceId, sampleStreamId, "0", "18");
    Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData> type
    ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);

Get range of values:

.. code:: java

    jsonMultipleValues = qiclient.getRangeValues(_tenantId, _namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
    foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);

Update Events vs. Replace Events
--------------------------------

The examples in this section demonstrate updates by taking the values
that were created and replacing them with new values. If you attempt to
update values that do not exist they will be created. The sample updates
the original ten values and then adds another ninety by updating with a
collection of one-hundred values.

After you have modified the client-side events, you submit them to the
Qi Service with ``updateValue`` or ``updateValues`` as shown here:

.. code:: java

    qiclient.updateValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));
    qiclient.updateValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

Note the event or event collection is serialized and passed as a string
into the update method as a parameter.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program replaces all one-hundred values. The calling conventions are
identical to ``updateValue`` and ``updateValues``:

.. code:: java

    qiclient.replaceValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));
    qiclient.replaceValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

Stream Behaviors
----------------

Only recorded values are returned by ``getWindowValues``. To retrieve a
particular range of values and interpolate events at the endpoints of
the range, you can use ``GetRangeValues``. The interpolation performed
is determined by the stream behavior assigned to the stream. If you do
not specify a behavior, linear interpolation is assumed. The example
demonstrates a stepwise interpolation using stream behaviors. More
sophisticated behavior is possible, including the ability to specify
interpolation behavior at the level of individual event type properties.
Interpolation is discussed in the `Qi API
Reference <https://qi-docs.readthedocs.org/en/latest/Overview/>`__.
Before changing the stream's retrieval behavior, the sample calls 
``getRangeValues`` to demonstrate how behavior changes. The first call 
yields three events with linear interpolation at index 1.

Now, you can define a new stream behavior object and submit it to the Qi
Service, as shown here:

.. code:: java

    QiStreamBehavior behavior = new QiStreamBehavior();
    behavior.setId(sampleBehaviorId);
    behavior.setMode(QiStreamMode.Discrete);
    String behaviorString = qiclient.createBehavior(_tenantId, _namespaceId, behavior);
    behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class));
    

In the sample, the behavior is updated to discrete, meaning that if an index
does not correspond to a real value in the stream then ``null`` is
returned by the Qi Service. Now attach this behavior to the
existing stream by setting the ``BehaviorId`` property of the stream and
updating the stream definition in the Qi Service:

.. code:: java

    sampleStream.setBehaviorId(sampleBehaviorId);
    qiclient.updateStream(_tenantId, _namespaceId, sampleStreamId, sampleStream);

The sample repeats the call to ``getRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
``Order=1``.

Delete Events
-------------

As with insertion, deletion of events is managed by specifying a single
index or a range of index values over the type's key property. The
following removes the single event whose ``Order`` property has the
value 0, then removes any event in the range 1..198:

.. code:: java

    qiclient.removeValue(_tenantId, _namespaceId, sampleStreamId, "0");
    qiclient.removeWindowValues(_tenantId, _namespaceId, sampleStreamId, "1", "198");

The index values are expressed as string representations of the
underlying type. DateTime index values must be expressed as ISO 8601
strings.

Get Methods
-----------

There are a number of additional methods included ``QiClient`` to help
you get started using the Qi REST API. These cover getting a single
``QiType``, getting multiple ``QiType``\ s associated with a namespace,
getting a single ``QiStream``, getting multiple ``QiStream``\ s
associated with a namespace, getting a ``QiBehavior``, and getting
multiple ``QiBehavior``\ s assoiated with a namespace. All the get
methods are very similar in syntax. Below is an example of retrieving a
specific stream associated with your namespace as well as getting
multiple streams:

.. code:: java

    // get a single stream
    String stream = qiclient.getStream(_tenantId, _namespaceId, sampleStreamId);
    QiStream = qiclient.mGson.fromJson(returnedStream, QiStream.class));
    // get multiple streams
    String returnedStreams = qiclient.getStreams(_tenantId, _namespaceId, "","0", "100");
    Type streamListType = new TypeToken<ArrayList<QiStream>>(){}.getType();
    ArrayList<QiStream> streams = qiclient.mGson.fromJson(returnedStreams, streamListType);

This demonstrates the procedure for getting types, streams and behaviors
from the Qi Service. When getting more than one, you must provide a
query string used to filter results, a skip value and the total number
of requested types, streams or behaviors.

Cleanup: Deleting Types and Streams
-----------------------------------

You should try running the sample more than once. To avoid collisions
with types and streams, the sample program deletes the stream, stream
behavior, and Qi type it created before terminating, thereby resetting
your tenant environment to the state it was in before running the
sample. The stream is removed first so that the reference count on the
type goes to zero:

.. code:: java

    qiclient.deleteStream(_tenantId, _namespaceId, sampleStreamId);
    qiclient.deleteBehavior(_tenantId, _namespaceId, sampleBehaviorId);

Note that the ID of the stream is passed, not the stream object.
Similarly, the following code deletes the type from the Qi Service:

.. code:: java

    qiclient.deleteType(_tenantId, _namespaceId, sampleTypeId);



