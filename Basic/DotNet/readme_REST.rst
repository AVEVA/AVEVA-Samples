.NET Samples
============

Building a Client with the Qi REST API
--------------------------------------

This sample is written using only the Qi REST API. The API allows for
the creation of Qi Service clients in any language that can make HTTP
calls and does not require access to any OSIsoft libraries. Objects are
passed as JSON strings. The sample uses the JSON.NET NuGet (Newtonsoft.Json
id) package, however, any method of creating a JSON representation of objects
will work.

Instantiate a Qi Client
=======================

A class has been provided that wraps an ``HttpClient`` instance from the
``System.Net.Http`` namespace and provides methods for the major CRUD (create, read, update and delete) 
operations. The CRUD methods encapsulate the Qi REST
API. Each call consists of an HTTP request with a specific URL and HTTP
method. The URL consists of the server plus the extension that is specific to the call.
Like all REST APIs, the Qi REST API maps HTTP methods to CRUD as in the following table:

+---------------+------------------+--------------------+
| HTTP Method   | CRUD Operation   | Content Found In   |
+===============+==================+====================+
| POST          | Create           | message body       |
+---------------+------------------+--------------------+
| GET           | Retrieve         | URL parameters     |
+---------------+------------------+--------------------+
| PUT           | Update           | message body       |
+---------------+------------------+--------------------+
| DELETE        | Delete           | URL parameters     |
+---------------+------------------+--------------------+

The constructor for the QiClient class configures the HttpClientHandler to
prevent auto redirection (which will be expained in the next section.) It
also takes the base URL (that is, the protocol plus the server and port number) and
ensures that it ends with a forward slash to make it easier to compose the URL for a specific REST call. Finally, the
constructor establishes a thirty-second timeout and indicates that the
client accepts JSON format responses:

.. code:: c#

        public QiClient(string baseUrl)
        {
            _httpClientHandler = new HttpClientHandler
            {
                AllowAutoRedirect = false
            };

            _httpClient = new HttpClient(_httpClientHandler);
            _baseUrl = baseUrl;
            if (_baseUrl.Substring(_baseUrl.Length - 1).CompareTo(@"/") != 0)
            {
                _baseUrl = _baseUrl + "/";
            }

            _httpClient.BaseAddress = new Uri(_baseUrl);
            _httpClient.Timeout = new TimeSpan(0, 0, 30);
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }

Obtain an Authentication Token
==============================

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. For a request to succeed, a token must be attached to every request that is made to
Qi. In the previous section, 
AllowAutoRedirect was set to false for the HttpClientHander; this is because
auto redirection strips the token from the request, which
results in an unauthorized response. Instead of relying on automatic
redirection, this sample handles redirecting 302 (Found) responses
manually.

The sample applications are examples of a *confidential client*. Such
clients provide a user ID and secret that are authenticated against the
directory. The sample code includes several placeholder strings. You
must replace these placeholders with the authentication-related values you received
from OSIsoft. The strings are found in the ``Constants.cs`` file.

.. code:: c#

        public const string SecurityResource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        public const string SecurityAuthority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        public const string SecurityAppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        public const string SecurityAppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
        public const string QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL";

In ``QiClient.cs`` is a method called ``AcquireAuthToken``.
To obtain an authentication token, the first step is to create an
authentication context that is related to the Azure Active Directory instance
pthat is roviding tokens. The authority is designated by the URI in
``_authority``.

.. code:: c#

        if (_authContext == null)
        {
            _authContext = new AuthenticationContext(Constants.SecurityAuthority);
        }

``AuthenticationContext`` instances are responsible for communicating with the
authority and also maintain a local cache of tokens. Tokens have a fixed
lifetime (typically one hour); however, they can be refreshed by the
authenticating authority for a longer period. If the refresh period has
expired, the credentials must be presented to the authority again.
The ``AcquireToken`` method hides these details from client
programmers. As long as you call ``AcquireToken`` before each HTTP call,
you will have a valid token. Here is the code:

.. code:: c#

        try
        {
            ClientCredential userCred = new ClientCredential(Constants.SecurityAppId, Constants.SecurityAppKey);
            AuthenticationResult authResult = _authContext.AcquireToken(Constants.SecurityResource, userCred);
            return authResult.AccessToken;
        }
        catch (AdalException)
        {
            return string.Empty;
        }

Create a QiType
===============

QiStreams represent open-ended collections of strongly-typed, ordered
events. Qi is capable of storing any data type you care to define. The
only requirement is that the data type must have one or more properties
that constitute an ordered key. While a timestamp is a very common type
of key, any ordered value is permitted. This sample type uses an integer.

Each data stream is associated with a QiType, so that only events
that conform to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

Because the sample uses the Qi REST API, type
definitions must be created. A type definition in Qi consists of one or more properties.
Each property has its own type. The type can be a simple data type such as
integer or string, or a previously defined complex QiType. You can 
also create nested data types: QiTypes whose properties can be
user-defined types. The sample ``WaveData`` class is a series of simple
types. ``QiType`` and ``QiTypeProperty`` classes have been created that
match those in the Qi Client Libraries. Simple types are denoted by an
enumeration specified in ``QiTypeCode.cs``. The ordinal values in the
latter file are those the Qi service expects, so you must specify these values if you wish to create
you own classes.

``WaveData`` contains one integer property and a series of double value
properties. To start, then, you create a QiType instance for each of
the following simple types:

.. code:: c#

        QiType intType = new QiType();
        intType.Id = "intType";
        intType.QiTypeCode = QiTypeCode.Int32;

        QiType doubleType = new QiType();
        doubleType.Id = "doubleType";
        doubleType.QiTypeCode = QiTypeCode.Double;

You can now create the key property, which is an integer type and is named
``Order``:

.. code:: c#

        QiTypeProperty orderProperty = new QiTypeProperty();
        orderProperty.Id = "Order";
        orderProperty.QiType = intType;
        orderProperty.IsKey = true;

Thus far, you have specified the ID, used the intType ``QiType`` that was created, and most
importantly, set IsKey to ``true``. The double value properties are
created in a similar manner. The code for creating the ``Radians`` property is shown below:

.. code:: c#

        QiTypeProperty radiansProperty = new QiTypeProperty();
        radiansProperty.Id = "Radians";
        radiansProperty.QiType = doubleType;

After all of the properties are created, it is necessary to assign
them to a ``QiType``, defining the overall ``WaveData`` class. This is
done by creating an array of ``QiProperty`` instances and assigning it to
the ``Properties`` property of ``QiType``, as shown here:

.. code:: c#

        QiType type = new QiType();
        type.Name = "WaveData";
        type.Id = "WaveDataType";
        type.Description = "This is a type for WaveData events";
        QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
        type.Properties = props;

To nest a user-defined type within another QiType, you
define the contained type as a ``QiType`` using the
methods illustrated above, then create a ``QiProperty`` with that type
and assign it to the containing class.

All this creates a type definition locally which must be submitted in a
REST call before it becomes available to the Qi service for the creation
of streams. The create call URL has the extention ``/Qi/Types``, and the
body of the request message is the JSON format serialization of the
``QiType`` that was just created. Creation of other Qi objects is performed
similarly. The specifics of object creation are wrapped in the generic
``CreateQiObjectAsync<T>`` method of ``QiClient``.
``CreateQiObjectAsync`` also handles the manual redirection of 302
(Found) responses, as described in the sections about creating a Qi client
and obtaining an authentication token.

Note that the methods in ``QiClient`` are asynchronous, but the
application itself is a simple console application. ``Main`` is a static
method, so it cannot take advantage of ``await``, hence the use of
``Result`` above, and ``Wait`` for methods that do not return a value. A
more complicated client application could use the asynchronous methods
to greater advantage.

Create a QiStream
=================

An ordered series of events is stored in a QiStream. The 
``QiStream`` class mirrors the properties of the native Qi service
``QiStream`` class. All you have to do is create a local QiStream
instance, assign it an ID, specify a type, and submit it to the Qi
service. You may optionally assign a QiStreamBehavior to the stream.
The following code shows how to create a stream named ``evtStream`` for recording
events of our sample type. The value of the ``TypeId`` property is the
value of the QiType ``Id`` property. The ``CreateStream`` method of
``QiClient`` is similar to ``CreateType``, except that it uses a
different URL. The code below shows how it is called from the main program:

.. code:: c#

        QiStream stream = new QiStream("evtStream", evtType.Id);
        string evtStreamString = qiclient.CreateStream(stream).Result;
        QiStream evtStream = JsonConvert.DeserializeObject<QiStream>(evtStreamString);

Note that ``TypeId`` property of the stream is set to the value of
the ID of the QiType that was created earlier. Types and behaviors are reference
counted; a type or behavior cannot be deleted until all streams that use it
are also deleted.

Create and Insert Events into the Stream
========================================

The ``WaveData`` class allows you to create events locally. In a
production environment, this is the class where you would interface your
measurements. The ``Next`` method is used to create values and assign
integers from 0-99 to establish an ordered collection of ``WaveData``
instances. The ``QiClient`` class provides methods for inserting a
single event or an array of events. The Qi REST API provides many more
types of data-insertion calls in addition to those shown in this
sample application.

It would be possible to pass in a ``WaveData`` instance (or array of
instances) into the event creation methods, but then the methods would
be particular to that specific class. A decision was made to handle
all serialization and deserialization outside the ``QiClient`` class and
to pass the results into and out of the event creation methods. This allows
changing the definition of the event class without changing the CRUD
methods of the client class. In this way we are able to take advantage
of the fact that the Qi service stores and manipulates arbitrary, user
defined types.

The CRUD methods are all very similar. The Qi REST API URL templates are
predefined strings. Each method fills in the template with the
parameters that are specific to the call, adds the protocol, server, and port of
the remote Qi Service, and sets the appropriate HTTP verb. If the call
is not successful, a QiError is thrown. The following code shows the call to create a
single event in a data stream:

.. code:: c#

        public async Task CreateEventAsync(string streamId, string singleEvent)
        {
            string requestUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.InsertSingleBaseUrl;
            await InsertEventDataIntoStreamAsync(requestUrl, singleEvent);
        }

The main program creates a single ``WaveData`` event with the ``Order``
0 and inserts it. Then it creates 99 more sequential events and inserts
them with a single call:

.. code:: c#

        TimeSpan span = new TimeSpan(0, 1, 0);
        WaveData evt = WaveData.Next(span, 2.0, 0);

        qiclient.CreateEventAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();

        List<WaveData> events = new List<WaveData>();
        for (int i = 2; i < 200; i += 2)
        {
            evt = WaveData.Next(span, 2.0, i);
            events.Add(evt);
            Thread.Sleep(400);
        }

        qiclient.CreateEventsAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();

Retrieve Events
===============

There are many methods in the Qi REST API that permit the retrieval of
events from a stream. The retrieval methods take string-type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings ("0" and "99", respectively). The index values must
be capable of conversion to the type of the index that is assigned in the QiType.
Timestamp keys are expressed as ISO 8601 format strings. Compound
indices are values concatenated with a pipe ('\|') separator.
``QiClient`` implements only two of the many available retrieval
methods:

.. code:: c#

        public async Task<string> GetWindowValuesAsync(string streamId, string startIndex, string endIndex)

        public async Task<string> GetRangeValuesAsync(string streamId, string startIndex, int skip, int count, bool reverse, QiBoundaryType boundaryType)

'GetWindowValuesAsync' is used to retrieve events over a specific index
range. 'GetRangeValuesAsync' is used to retrieve a specified number of
events from a starting index point:

.. code:: c#

        string jCollection = qiclient.GetWindowValuesAsync("evtStream", "0", "198").Result;
        WaveData[] foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
        
        jCollection = qiclient.GetRangeValuesAsync("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
        foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);

Update Events
=============

Updates can be demonstrated by taking the values that were created and replacing
them with new values. After you have modified the events on the client side, you
submit them to the Qi service with ``UpdateValueAsync`` or
``UpdateValuesAsync``, as shown here:

.. code:: c#

        qiclient.UpdateValueAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();
        qiclient.UpdateValuesAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();

Note that you are serializing the event or event collection and passing
the string into the update method as a parameter.

Delete Events
=============

As with insertion, the deletion of events is managed by specifying a single
index or a range of index values over the type's key property. The code below shows
the removal of a single event whose ``Order`` property has the value 0,
and then the removal of any event in the range 1-99:

.. code:: c#

        qiclient.RemoveValueAsync("evtStream", "0").Wait();
        qiclient.RemoveWindowValuesAsync("evtStream", "1", "99").Wait();

Index values are expressed as string representations of the
underlying type. DateTime index values must be expressed as ISO 8601
strings.

Bonus: Deleting Types and Streams
=================================

You should run the sample more than once. To avoid collisions
with types and streams, the sample program deletes the stream and type
it created before terminating. The stream goes first so that the
reference count on the type goes to zero:

.. code:: c#

        qiclient.DeleteStreamAsync("evtStream");

Note that the id of the stream is passed, not the stream object.
Similarly, the following code deletes the type from the Qi service

.. code:: c#

        qiclient.DeleteTypeAsync(evtType.Id);

Recall that ``evtType`` is the
QiType instance that is returned by the Qi service when the type was created.
