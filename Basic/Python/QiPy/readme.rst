Building a Python client to make REST API calls to the Qi Service
==================================================================

The sample code in this topic demonstrates how to invoke Qi REST APIs
using Python. By examining the code, you will see how to establish a connection 
to Qi, obtain an authorization token, create a QiNamespace, QiType, and QiStream, 
and how to create, read, update, and delete values in Qi.

The sections that follow provide a brief description of the process from
beginning to end.

Python Version:
---------------

Two versions of the sample code are provided, one targets environments running Python 2.x 
and the other targets those running Python 3.x.  Please use the sample that is appropriate 
to your environment.  You can determine which version of Python you are running by typing 
the following at the command line:

.. code::

	python -V

To Run this Sample:
-------------------
1. Clone the GitHub repository
2. Open the folder with your favorite IDE
3. Update ``config.ini`` with the credentials provided by OSIsoft
4. Run ``program.py``

Establish a Connection
----------------------

The sample code uses the ``requests`` module, which 
exposes simple methods for specifying request types to a given
destination address. The client calls the requests method by passing a destination
URL, payload, and headers. The server's response is stored.

.. code:: python

    response = requests.post(url, data=payload, headers=client_headers)

-  *url* is the service endpoint (for example:
   ``https://qi-data.osisoft.com``). The connection is used by the
   ``QiClient`` class.

Each call to the Qi REST API consists of an HTTP request along with a specific 
URL and HTTP method. The URL consists of the server name plus the extension that 
is specific to the call. Like all REST APIs, the Qi REST API maps HTTP
methods to CRUD operations as shown in the following table:

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

Configure the Sample:
-----------------------

Included in the sample there is a configuration file with placeholders that 
need to be replaced with the proper values. They include information for 
authentication, connecting to the Qi Service, and pointing to a namespace.

The Qi Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide an application ID 
and secret that are authenticated against the directory. These are referred to as client 
IDs and client secrets, which are associated with a given tenant. They are created through 
the tenant's administration portal. The steps necessary to create a new client ID and secret 
are described below.

First, log on to the `Cloud Portal <https://cloud.osisoft.com>`__ with admin credentials 
and navigate to the ``Client Keys`` page under the ``Manage`` tab, which is situated along 
the top of the webpage. Two types of keys may be created. For a complete explanation of 
key roles look at the help bar on the right side of the page. This sample program covers 
data creation, deletion and retrieval, so an administration key must be used in the 
configuration file. Creating a new key is simple. Enter a name for the key, select 
``Administrator role``, then click ``Add Key``.

Next, view the key by clicking the small eye icon on the right of the created key, 
located in the list of available keys. A pop-up will appear with the tenant ID, client 
ID and client secret. These must replace the corresponding values in the sample's 
configuration file. 

Along with the client ID and secret values, add the tenant name to the authority value 
so authentication occurs against the correct tenant. The URL for the Qi Service 
connection must also be changed to reflect the destination address of the requests. 

Finally, a valid namespace ID for the tenant must be given. To create a 
namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` page. 
At the top the add button will create a new namespace after the required forms are 
completed. This namespace is now associated with the logged-in tenant and may be 
used in the sample.

The values to be replaced are in ``config.ini``:

.. code:: python

    [Configurations]
    Namespace = REPLACE_WITH_NAMESPACE

    [Access]
    Address = REPLACE_WITH_QI_SERVER_URL
    Tenant = REPLACE_WITH_TENANT_ID

    [Credentials]
    Resource = https://pihomemain.onmicrosof.com/ocsapi
    Authority = https://login.windows.net/<PLACEHOLDER_REPLACE_WITH_TENANT_NAME>.onmicrosoft.com
    ClientId = REPLACE_WITH_CLIENT_IDENTIFIER
    ClientSecret = REPLACE_WITH_CLIENT_SECRET

Obtain an Authentication Token
------------------------------

The Azure Active Directory python library ``adal`` provides a simple way
to authenticate and obtain bearer tokens. Within each
request to Qi, the headers are provided by a function that is also
responsible for refreshing the token. An authentication context is created 
and a token is acquired from that context.

.. code:: python

    context = adal.AuthenticationContext(self.__authority,
       validate_authority=True)
    token = context.acquire_token_with_client_credentials(self.__resource, 
       self.__clientId, self.__clientSecret)

Acquire a QiNamespace
---------------------

In Qi, a namespace provides isolation within a Tenant. Each namespace
has its own collection of Streams, Types, and Behaviors. It is not
possible to programmatically create or delete a namespace. If you are a
new user, be sure to go to the `Cloud
Portal <http://cloud.osisoft.com>`__ and create a namespace using your
tenant login credentials provided by OSIsoft. You must provide the
namespace ID of a valid namespace in ``config.ini`` for the sample to
function properly.

Each QiClient is associated with the tenant passed as an argument to the
constructor. There is a one-to-one correspondence between them. However,
multiple namespaces may be allocated to a single tenant, so you will see
that each function in ``QiClient.py`` takes in a namespace ID as an
argument.

Create a QiType
---------------

To use Qi, you define QiTypes that describe the kinds of data you want
to store in QiStreams. QiTypes are the model that define QiStreams.
QiTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other QiTypes. For
more information about QiTypes, refer to the `Qi
documentation <https://cloud.osisoft.com/documentation>`__.

In the sample code, the QiType representing WaveData is defined in the
``getWaveDataType`` method of program.py. WaveData contains properties
of integer and double atomic types. The function begins by defining a
base QiType for each atomic type.

.. code:: python

    intType = QiType()
    intType.Id = "intType"
    intType.QiTypeCode = QiTypeCode.Int32

Next, the WaveData properties are each represented by a QiTypeProperty.
Each QiType field in QiTypeProperty is assigned an integer or double
QiType. The WaveData Order property represents the type’s key, and its
IsKey property is set to true.

.. code:: python

    orderProperty = QiTypeProperty()
    orderProperty.Id = "Order"
    orderProperty.QiType = intType
    orderProperty.IsKey = True

The WaveData QiType is defined as a collection of the QiTypeProperties.

.. code:: python

    #create a QiType for WaveData Class
    wave = QiType()
    wave.Id = sampleTypeId
    wave.Name = "WaveDataPySample"
    wave.Description = "This is a sample Qi type for storing WaveData type events"
    wave.QiTypeCode = QiTypeCode.Object
    wave.Properties = [orderProperty, tauProperty, radiansProperty, 
                       sinProperty, cosProperty, tanProperty, sinhProperty, 
                       coshProperty, tanhProperty]

The WaveData type is created in Qi using the ``createType`` method in
QiClient.py.

.. code:: python

    type = getWaveDataType(sampleTypeId)
    type = client.createType(namespaceId, type)

All QiTypes are constructed in a similar manner. Basic QiTypes form the basis for
QiTypeProperties, which are then assigned to a complex user-defined
type. These types can then be used in properties and become part of
another QiType's property list.

Create a QiStream
-----------------

A QiStream stores an ordered series of events. To create a
QiStream instance, you simply provide an Id, assign it a type, and
submit it to the Qi service. The ``createStream`` method of QiClient is
similar to createType, except that it uses a different URL. Here is how
it is called from the main program:

.. code:: python

    stream = QiStream()
    stream.Id = sampleStreamId
    stream.Name = "WaveStreamPySample"
    stream.Description = "A stream to store the WaveData events"
    stream.TypeId = type.Id
    stream.BehaviorId = None
    stream = client.createStream(namespaceId, stream)

Create and Insert Values into the Stream
----------------------------------------

A single QiValue is a data point in the stream. It cannot be
empty and must have at least the key value of the QiType for the
event. Events are passed in JSON format and are serialized in
``QiClient.py``, which is then sent along with a POST request.

.. code:: python

    payload = json.dumps(value, cls=Encoder)
    response = requests.post(self.__uri 
                   + self.__insertValuePath.format(tenant_id=self.__tenant, 
                     namespaceId=namespaceId,
                     stream_id=stream_id), data=payload, 
                     headers=self.__qiHeaders())

You use a similar process to insert multiple values; however, the payload has a
collection of events and InsertValue is plural ``insertValues`` in the
URL. See the sample code for an example.

Retrieve Values from a Stream
-----------------------------

There are many methods in the Qi REST API that allow the retrieval of
events from a stream. Many of the retrieval methods accept indexes,
which are passed using the URL. The index values must be capable of
conversion to the type of the index assigned in the QiType.

In this sample, four of the available methods are implemented in
QiClient: ``getLastValue``, ``getValue``, ``getWindowValues``, and ``getRangeValues``.
``getWindowValues`` can be used to retrieve events over a specific index
range. ``getRangeValues`` can be used to retrieve a specified number of
events from a starting index.

Here is how to use ``getWindowValues``:

.. code:: python

    def getWindowValues(self, namespaceId, stream_id, start, end):

*start* and *end* (inclusive) represent the starting and ending indices for the
retrieval. Additionally, the namespace ID and stream ID must
be provided to the function call. A JSON object containing a list of the
found values is returned. In the sample the call is:

.. code:: python

    events = client.getWindowValues(namespaceId, stream.Id, 0, 40)

Optionally, you can retrieve a range of values from a start index using the
``getRangeValues`` method in ``QiClient``. The starting index is the ID
of the ``QiTypeProperty`` that corresponds to the key value of the
WaveData type. In this case, it is ``Order``. Following is the
declaration of getRangeValues in QiClient.py:

.. code:: python

    def getRangeValues(self, namespaceId, stream_id, start, skip, 
        count, reverse, boundary_type):

*skip* is the increment by which the retrieval will happen. *count* is
how many values you wish to have returned. *reverse* is a boolean that
when ``true`` causes the retrieval to work backwards from the starting
point. Finally, *boundary\_type* is a ``QiBoundaryType`` value that
determines the behavior if the starting index cannot be found. Refer the
to the `Qi documentation <https://cloud.osisoft.com/documentation>`__
for more information about QiBoundaryTypes.

The ``getRangeValues`` method is called as shown here in
program.py:

.. code:: python

    events = client.getRangeValues(namespaceId, stream.Id, 
             "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)

Updating and Replacing Values
-----------------------------

Values can be updated or replaced after they are inserted into a stream. The
distinction between updating and replacing operations is that updating inserts a
value if none exists previously, but replacing does not. The sample
demonstrates this behavior by first inserting ten values into the
stream, then updating and adding ten more values using the update
methods. Afterwards, it replaces all twenty values using the replace
methods.

Here are the calls that accomplish these steps:

Update values:

.. code:: python

    # update one value
    event = nextWave(start, span, 4.0, 0)
    client.updateValue(namespaceId, stream.Id, event)
    # update multiple values
    updatedEvents = []
    for i in range(2, 40, 2):
        event = nextWave(start + datetime.timedelta(seconds=i * 0.2), span, 4.0, i)
        updatedEvents.append(event)
    client.updateValues(namespaceId, stream.Id, updatedEvents)

Replace values:

.. code:: python

    # replace one value
    event = nextWave(start, span, 10.0, 0)
    client.replaceValue(namespaceId, stream.Id, event)
    # replace multiple values
    replacedEvents = []
    for i in range(2, 40, 2):
        event = nextWave(start + datetime.timedelta(seconds=i * 0.2), span, 10.0, i)
        replacedEvents.append(event)
    client.replaceValues(namespaceId, stream.Id, replacedEvents)

Changing Stream Behavior
------------------------

When retrieving a value, the behavior of a stream can be altered
using the ``QiStreamBehavior`` class. A stream is updated with a behavior,
which changes how "get" operations are performed when an index falls between,
before, or after existing values. The default behavior is continuous, so
any indices not in the stream are interpolated using the previous
and next values.

In the sample, the behavior is updated to discrete, meaning that if an index
does not correspond to a real value in the stream then ``null`` is
returned by the Qi Service. The following shows how this is done in the
code:

.. code:: python

    # create the behavior
    discreteBehavior = QiStreamBehavior()
    discreteBehavior.Id = sampleBehaviorId
    discreteBehavior.Mode = QiStreamMode.Discrete
    discreteBehavior = client.createBehavior(namespaceId, discreteBehavior)
    # update the stream
    stream.BehaviorId = discreteBehavior.Id
    client.updateStream(namespaceId, stream)

The process consists of two steps. First, the behavior must be created, then the
stream must be updated. Note that the sample retrieves three data points
before and after updating the stream to show that it has changed. See
the `Qi documentation <https://cloud.osisoft.com/documentation>`__ for
more information about QiStreamBehaviors.

QiViews
-------

A QiView provides a way to map stream data requests from one data type 
to another. You can apply a QiView to any read or GET operation. QiView 
is used to specify the mapping between source and target types.

Qi attempts to determine how to map Properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, Qi will map the properties automatically.

.. code:: python

        rangeWaves = client.getRangeValues(namespaceId, stream.Id, WaveDataTarget, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated, automaticView.Id)

To map a property that is beyond the ability of Qi to map on its own, 
you should define a QiViewProperty and add it to the QiVeiw’s Properties collection.

.. code:: python

        vp2 = QiViewProperty()
        vp2.SourceId = "Sin"
        vp2.TargetId = "SinInt"
        ...
        manualView = QiView()
        manualView.Id = sampleViewIntId
        manualView.Name = "SampleIntView"
        manualView.TargetTypeId = waveIntegerType.Id
        manualView.SourceTypeId = waveType.Id
        manualView.Properties = [vp1, vp2, vp3, vp4]

QiViewMap
---------

When a QiView is added, Qi defines a plan mapping. Plan details are retrieved as a QiViewMap. 
The QiViewMap provides a detailed Property-by-Property definition of the mapping.
The QiVeiwMap cannot be written, it can only be retrieved from Qi.

.. code:: python

        viewMap2 = client.getViewMap(namespaceId, manualView.Id)


Deleting Values from a Stream
-----------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Below are the
declarations of both functions:

.. code:: python

    # remove a single value from the stream
    def removeValue(self, namespaceId, stream_id, index):
    # remove multiple values from the stream
    def removeWindowValues(self, namespaceId, stream_id, index):

Here is how the methods are used in the sample:

.. code:: python

    client.removeValue(namespaceId, stream.Id, 0)
    client.removeWindowValues(namespaceId, stream.Id, 0, 40)

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to Order=0 and Order=40
are removed from the stream.


Additional Methods
------------------

Notice that there are more methods provided in QiClient than are discussed in this
document, including get methods for types, behaviors, and streams.
Each has both a single get method and a multiple get method, which
reflect the data retrieval methods covered above. Below are the function declarations:

.. code:: python

    def getType(self, namespaceId, type_id):
    def getTypes(self, namespaceId):
    def getBehavior(self, namespaceId, behavior_id):
    def getBehaviors(self, namespaceId, skip, count):
    def getStream(self, namespaceId, stream_id):
    def getStreams(self, namespaceId, query, skip, count):

For a complete list of HTTP request URLs refer to the `Qi
documentation <https://cloud.osisoft.com/documentation>`__.

Cleanup: Deleting Types, Behaviors, Views and Streams
-----------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream
behaviors, and types can be achieved by a DELETE REST call and passing
the corresponding Id. The following calls are made in the sample code.

.. code:: python

    client.deleteStream(namespaceId, sampleStreamId)
    client.deleteType(namespaceId, sampleTypeId)
    client.deleteBehavior(namespaceId, sampleBehaviorId)
    client.deleteView(namespaceId, sampleViewId)

*Note: Types and behaviors cannot be deleted until any streams
referencing them are deleted first. Their references are counted so
deletion will fail if any streams still reference them.*