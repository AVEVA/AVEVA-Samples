Python Sample: Building a Client to make REST API Calls to the Qi Service
===========================================================================

The sample code in this topic demonstrates how to invoke Qi REST APIs 
using Python.

The sections that follow provide a brief description of the process from beginning to end. 

Establish a Connection
----------------------

The sample in this topic uses the ``http.client`` module to connect a service
endpoint. A new connection is opened as follows:

.. code:: python

        connection = http.HTTPSConnection(url)

-  *url* is the service endpoint (for example: ``https://qi-data.osisoft.com``).
   The connection is used by the ``QiClient`` class, which encapsulates
   the Qi REST API.

Obtain an Authentication Token
------------------------------

The Qi service is secured by Azure Active Directory. For a request to succeed, a token must be obtained 
and attached to every request made to Qi. The sample applications are examples of a confidential client. 
Confidential clients provide a user Id and secret that are authenticated against the directory. The 
sample code includes several placeholder strings; you must replace the placeholder strings with the 
values you received from OSIsoft. The strings are found in ``config.ini``:

.. code:: python

  [Configuraitons] 
  Namespace = Samples

  [Access]
  Address = https://qi-data.osisoft.com
  Tenant = REPLACE_WITH_TENANT_ID

  [Credentials]
  Resource = https://qihomeprod.onmicrosoft.com/historian
  AppId = REPLACE_WITH_APPLICATION_IDENTIFIER
  AppKey = REPLACE_WITH_APPLICATION_SECRET
    

In your own code, you must replace ``Tenant``, ``Resource``, ``AppId``, and ``AppKey``. You might also want 
to replace the ``Namespace``. The QiClient usea the information to acquire and attach the appropriate 
authentication token to requests.

Some of the other Qi samples use Azure Active Directory libraries to manage token acquisition, caching, 
and refreshing; however, those libraries are not available in Python, so this sample acquires the 
token directly and performs rudimentry caching and refreshing. The sample must be adjusted appropriately 
if token timing is changed. Before invoking each request, QiClient makes the following call to 
acquire the token:

.. code:: python

  self.__getToken()
    
Acquire a QiNamespace
----------------------

In Qi, a namespace provides isolation within a Tenant. Each namespace has its 
own collection of Streams, Types, and Behaviors. 


Create a QiType
---------------

To use Qi, you define QiTypes that describe the kinds of data you want to store in QiStreams. 
QiTypes are the model that define QiStreams. QiTypes can define simple atomic types, such as integers, 
floats or strings, or they can define complex types by grouping other QiTypes. For more information
about QiTypes, refer to the Qi Documentation.

In the sample, the QiType representing WaveData is defined in the getWaveDataType method of test.py. 

WaveData contains properties of integer and double atomic types. The ``getWaveDataType`` function begins by 
defining a base QiType for each atomic type. Next, the WaveData properties are each represented 
by a QiTypeProperty. Each QiTypeProperty’s QiType field is assigned an integer or double QiType. 
The WaveData QiType is defined as a collection of the QiTypeProperties.
The WaveData Order property represents the type’s key, and its IsKey property is set to true.
The WaveData type is created in Qi using the ``createType`` method in QiClient.py. 


Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. To create a local QiStream instance, you simply 
give it an Id, assign it a type, and submit it to the Qi service. The CreateStream method of 
QiClient is similar to createType, except that it uses a different URL. 
Here is how it is called from the main program:


Create and Insert Events into the Stream
----------------------------------------

A single event is a data point in the Stream. An event object cannot be emtpy and should have 
at least the key value of the Qi type for the event. Events are passed in JSON format. 
Here is the call to create a single event in a data stream in QiClient.py:

.. code:: python

  pathAndQuery = "/Qi/{tenant_id}/{namespace_id}/Streams/{stream_id}/Data".format(tenant_id = 
                  tenant_id, namespace_id = namespace_id, stream_id = stream_id) + "InsertValue"

  payload = json.dumps(value, cls = Encoder)

  connection = http.HTTPSConnection(self.url)
  connection.request("POST", pathAndQuery, payload, self.__qi_headers())

  response = connection.getresponse()
  connection.close()

Inserting multiple values is similar; however, the payload has a collection of events 
and InsertValue is plural (InsertValues) in the URL.

Retrieve events
---------------

There are many methods in the Qi REST API that allow the retrieval of events from a stream. 
Many of the retrieval methods accept indexes, which are passed using the uri. The index 
values must be capable of conversion to the type of the index assigned in the QiType.

In this sample, three of the available methods are implemented in QiClient: getLastValue, 
getWindowValues, and getRangeValues. getWindowValues can be used to get events over 
a specific index range. getRangeValues can be used to get a specified number of 
events from a starting index.

Here is what the getWindowValues call looks like:

.. code:: python

  path = "/Qi/{tenant_id}/{namespace_id}/Streams/{stream_id}/Data".format(tenant_id = 
          tenant_id, namespace_id = namespace_id, stream_id = stream_id)
  query - "GetWindowValues?{start}&{end}".format(
  start = urllib.parse.urlencode({"startIndex": start}),
  end = urllib.parse.urlencode({"endIndex": end}))

  pathAndQuery = "{path}/{query}".format(path = path, query = query)

  connection = http.HTTPSConnection(self.url)
  connection.request("GET", pathAndQuery, self.__qi_headers())

  response = connection.getresponse()
  connection.close()


Cleanup: Deleting Types, Behaviors, and Streams
-----------------------------------------------

So that the program can run repeatedly without collisions, the sample performs some cleanup 
before exiting. Deleting streams, stream behaviors, and types can be achieved by a DELETE REST 
call and passing the corresponding Id. 

Note: types and behaviors cannot be deleted until any streams referencing them are deleted first.


