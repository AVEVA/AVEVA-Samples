Python Samples: Building a Client to make REST API Calls to the Qi Service.
===========================================================================

The examples in this topic demonstrate how Qi REST APIs are invoked
using Python.

Establish a Connection
----------------------

The sample in this topic uses ``httplib`` module to connect a service
endpoint. A new connection is opened as follows:

.. code:: python

        conn = httplib.HTTPConnection(url-name)

-  *url-name* is the service endpoint (for example: "localhost:3380").
   The connection is used by the ``QiClient`` class, which encapsulates
   the REST API and performs authentication.

Obtain an Authentication Token
------------------------------

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. For a request to succeed, a token must be attached
to every request made to Qi. The sample applications described here are
examples of a *confidential client*. Such clients provide a user ID and
secret key that are authenticated against the directory. The sample code
includes several placeholder strings. You must replace these strings
with the authentication-related values you received from OSIsoft. The
strings are found in ``Constants.py``:

.. code:: python

        #VERY IMPORTANT: edit the following values to reflect the authorization items you were given
        authItems = {'resource' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
                     'authority' : "PLACEHOLDER_REPLACE_WITH_AUTHORITY",#Ex: "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token,
                     'appId' : "PLACEHOLDER_REPLACE_WITH_USER_ID",
                     'appKey' : "PLACEHOLDER_REPLACE_WITH_USER_SECRET"}
        
        TenantId = PLACEHOLDER_REPLACE_WITH_TENANT_ID
        QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL"

You must replace ``resource``, ``authority``, ``appId``, and ``appKey``
with the appropriate values provided by OSIsoft. The ``authItems`` array
is passed to the ``QiClient`` constructor.

The Python sample in this topic uses raw OAuth 2 calls to obtain an
authentication token. The other samples use libraries from Microsoft
that handles token acquisition, caching, and refreshing, but such a
library is not currently available for Python.

During initialization, ``QiClient`` makes the following calls:

.. code:: python

        self.__getToken()
        if not self.__token:
            return

The first call, ``__getToken``, makes the OAuth call to the Azure Active
Directory instance to get a token, then assigns the value (assuming the
application is successfully authenticated) to the member variable
``__token``. Next, QiClient checks to ensure it has an authentication
token. If a token is not found the call will fail and the call returns.
The following shows the code for ``__getToken``:

.. code:: python

        def __getToken(self):     
            if self.__expiration < (time.time()/100):
                return
                
            response = requests.post(self.__authItems['authority'], 
                                     data = { 'grant_type' : 'client_credentials',
                                             'client_id' : self.__authItems['appId'],
                                                'client_secret' : self.__authItems['appKey'],
                                                'resource' : self.__authItems['resource']
                                                })
            if response.status_code == 200:
                self.__token = response.json()['access_token']
                self.__expiration = response.json()['expires_on']
            else:
                self.__token = ""
                print "Authentication Failure : "+response.reason

Authentication tokens expire after a period of time so the token must be
periodically refreshed. The first lines of ``__getToken`` check whether
the token has expired and returns if it has not. Otherwise, the
credentials are submitted to Azure Active Directory to obtain a fresh
token. The ``__getToken`` method is called before each REST API call,
and the token is passed as part of the headers:

.. code:: python

    def __qi_headers(self):
        return {
            "Authorization" : "bearer %s" % self.__token,
            "Content-type": "application/json", 
            "Accept": "text/plain"
        }

Note that the value of the ``Authorization`` header is the word
"bearer," followed by a space, followed by the token value itself.


Create a Namespace
------------------

A Qi Namespace can be thought of as a container to hold streams, types, and behaviors. 
Namespaces allow you to separate streams or simply have a sandbox in which to test Qi.

.. code:: python

  client.createNamespace(constants.TenantId, sampleNamespace)


Create a QiType
---------------

QiStreams represent open-ended collections of strongly-typed, ordered
events. Qi is capable of storing any data type you care to define. The
only requirement is that the data type must have one or more properties
that constitute an ordered key. While a timestamp is a very common type
of key, any ordered value is permitted. The sample type in this example
uses an integer.

Each data stream is associated with a QiType, so that only events
conforming to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

Because the example uses the Qi REST API, you must build your own type
definitions. A type definition in Qi consists of one or more properties.
Each property has its own type. The type can be a simple data type such
as an integer or string, or a previously defined complex QiType. You can
create nested data types; that is, QiTypes whose properties are
user-defined types. ``QiType`` and ``QiTypeProperty`` classes have been
created that match those in the Qi Client Libraries. Simple types are
denoted by an enumeration specified in ``QiTypeCode.py``. The ordinal
values in the latter file are those the Qi service expects; you must
specify these values if you want to create your own classes.

From QiType.py:

.. code:: python

        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
        self.__Properties = []

From QiTypeProperty.py:

.. code:: python

        def __init__(self):
                self.__Id = ""
                self.__Name = None
                self.__Description = None
                self.__QiType = None
                self.__IsKey = False

Type creation is encapsulated by the ``createType`` method in
``QiClient.py``. The following code shows how the method is called in
``test.py``:

.. code:: python

        wave = QiType()
        wave.Id = "WaveDataPySample"
        wave.Name = "WaveDataPySample"
        wave.Description = "This is a sample Qi type for storing WaveData type events"
        wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                           cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

        #create the type in Qi service
        print "Creating the WaveData Qi type in Qi service"
        evtType = client.createType(wave)

-  Returns the QiType object in JSON format.
-  If a Qi type with the same ID exists, the URL of the existing Qi type
   is returned.
-  The QiType object is passed in JSON format

Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. We've created a
``QiStream`` class mirroring the properties of the native Qi service
``QiStream`` class. All you have to do is create a local QiStream
instance, provide an ID, assign a type, and submit it to the Qi service.
You may optionally assign a QiStreamBehavior to the stream. The value of
the stream's ``TypeId`` property is the value of the QiType ``Id``
property. The ``CreateStream`` method of ``QiClient`` is similar to
``createType``, except that it uses a different URL. The following code
shows how it is called from the main program:

.. code:: python

        stream = QiStream()
        stream.Id = "WaveStreamPySample"
        stream.Name = "WaveStreamPySample"
        stream.Description = "A Stream to store the WaveData Qi types events"
        stream.TypeId = "WaveDataPySample"
        stream.BehaviorId = None
        evtStream = client.createStream(stream)

Create and Insert Events into the Stream
----------------------------------------

A single event is a data point in the Stream. An event object cannot be
emtpy and should have at least the key value of the Qi type for the
event. Events are passed in JSON format. The following code shows the
call to create a single event in a data stream in ``QiClient.py``:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("POST", self.__streamsBase + '/' + qi_stream.Id + self.__insertSingle, 
                     payload, self.__qi_headers())

-  qi\_Stream.Id is the stream ID
-  payload is the event object in JSON format

Inserting multiple values is similar, but the payload has list of events
and the URL for POST call is slightly different:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("POST", self.__streamsBase + '/' + qi_stream.Id + self.__insertMultiple, 
                     payload, self.__qi_headers())

Retrieve Events
---------------

There are many methods in the Qi REST API that allow for the retrieval
of events from a stream. The retrieval methods take string-type start
and end values; in this case, the start and end ordinal indices are
expressed as strings ("0" and "99", respectively). The index values must
be capable of conversion to the type of the index that is assigned in
the QiType. Timestamp keys are expressed as ISO 8601 format strings.
Compound indices are values concatenated with a pipe ('\|') separator.
``QiClient`` implements three of the many available retrieval methods:
``getLastValue``, ``getWindowValues``, and ``getRangeValues``.

``GetWindowValues`` can be used to get events over a specific index
range. ``GetRangeValues`` can be used to obtain a specified number of
events from a starting index point.

Shown below is the code for the ``GetWindowValues`` call:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("GET", self.__streamsBase.format(tenant_id = tenant_id, namespace_id = namespace_id) + '/' + 
                    self.__getTemplate.format(stream_id = qi_stream.Id, 
                                             start = urllib.urlencode({"startIndex": start}), 
                                                end = urllib.urlencode({"endIndex": end})), 
                    headers = self.__qi_headers())

Update Events
-------------

Updating events is handled by ``PUT`` REST call as shown below:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("PUT", self.__streamsBase + '/' + qi_stream.Id + self.__updateSingle, 
                     payload, self.__qi_headers())

-  payload is the new event with an index value specifying the existing
   event to overwrite.

Updating multiple events is similar but the payload has an array of
event objects and URL for POST is slightly different:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("PUT", self.__streamsBase.format(tenant_id = tenant_id, namespace_id = namespace_id) + 
        '/' + qi_stream.Id + self.__updateMultiple, payload, self.__qi_headers())

QiStreamBehaviors
-----------------

You can specify a QiBoundarytype for certain data retrieval calls. For
example, if ``GetRangeValues`` is called with an ``ExactOrCalculated``
boundary type, an event at the request start index will be calculated
using linear interpolation (default) or based on the QiStreamBehavior
associated with the QiStream. Because the example QiStream was created
without an associated ``QiStreamBehavior``, it displays the default
linear interpolation.

The first event returned by the following call will be at index 1 (start
index) and calculated using linear interpolation:

.. code:: python

        foundEvents = client.getRangeValues("WaveStreamPy", "1", 0, 3, False, QiBoundaryType.ExactOrCalculated.value)

To see how QiStreamBehaviors can change the query results, the following
code defines a new stream behavior object and submits it to the Qi
service:

.. code:: python

        behaviour = QiStreamBehaviour()
        behaviour.Id = "evtStreamStepLeading";
        behaviour.Mode = QiStreamMode.StepwiseContinuousLeading.value
        behaviour = client.createBehaviour(behaviour)

Setting the ``Mode`` property to ``StepwiseContinuousLeading`` ensures
that any calculated event will have an interpolated index, but every
other property will have the value of the previous event. The following
code attaches this behavior to the existing stream by setting the
``BehaviorId`` property of the stream and updating the stream definition
in the Qi service:

.. code:: python

        evtStream.BehaviourId = behaviour.Id
        client.updateStream(evtStream)

The example repeats the call to ``GetRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
index 1 using different stream behaviors.

Delete Events
-------------

An event at a particular index can be deleted by passing the index value
for that data point to the following DELETE REST call. The index values
are expressed as string representations of the underlying type. DateTime
index values must be expressed as ISO 8601 strings.

Deleting a single value is done using the QiClient's ``removeValue``
method:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("DELETE", self.__streamsBase + '/' + self.__removeSingleTemplate.format(stream_id = qi_stream.Id, param = params), 
                     headers = self.__qi_headers())

Delete can also be done over a range of index values, as in the
following ``removeValues`` method:

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request("DELETE", self.__streamsBase.format(tenant_id = tenant_id, namespace_id = namespace_id) + '/' + 
                    self.__removeMultipleTemplate.format(stream_id = qi_stream.Id, 
                    start = urllib.urlencode({"startIndex": start}),
                    end = urllib.urlencode({"endIndex": end})), 
                    headers = self.__qi_headers())

Cleanup: Deleting Types, Behaviors, and Streams
-----------------------------------------------

To prevent name collisions if the sample program is run repeadly, some
cleanup is required before exiting. Deleting streams, stream behaviors,
and types is done using a ``DELETE`` REST call and passing the
corresponding ID. Note that types and behaviors cannot be deleted until
any streams that reference those types and behaviors are deleted first.

.. code:: python

        conn.request("DELETE", self.__streamsBase.format(tenant_id = tenant_id, namespace_id = namespace_id) 
        + '/' + stream_id, headers = self.__qi_headers())
        response = conn.getresponse()

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request('DELETE', self.__typesBase.format(tenant_id = tenant_id, namespace_id = namespace_id) 
        + '/' +  type_id, headers = self.__qi_headers())

.. code:: python

        conn = http.HTTPSConnection(self.url)
        conn.request('DELETE', self.__behaviorBase.format(tenant_id = tenant_id, namespace_id = namespace_id)
        + '/' +  behaviorId, headers = self.__qi_headers())

