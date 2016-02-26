#.NET Samples: Building a Client with the Qi Client Libraries

This sample differs from the other samples in that the client
application makes use of the OSIsoft Qi Client Libraries. These
libraries are available as nuget packages from
https://osisoft.myget.org/F/qi/. The packages used are
``OSIsoft.Qi.Core``, ``OSIsoft.Qi.Http.Channel``, and
``OSIsoft.Qi.Http.Client``. Ultimately, the Qi REST APIs are invoked
just like the rest of the samples, but the libraries offer a framework
of classes to make client development easier.

Instantiate a Qi Client
=======================

The client works through the ``IQiServer`` interface, which is
instantiated through a client factory. The timeout for REST calls may be
set in the factory OnCreated action.

In order to successfully interact with Qi, an ``Authorization`` header
must be added to every REST call. The value of this header is the scheme
keyword ``Bearer`` followed by a token string returned by Azure Active
Directory. This code ensures an up to date token is added to each
request:

.. code:: c#

        QiHttpClientFactory<IQiServer> clientFactory = new QiHttpClientFactory<IQiServer>();
        clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);

        IQiServer qiclient = clientFactory.CreateChannel(new Uri(server));
        IQiClientProxy proxy = (IQiClientProxy)qiclient;
        proxy.OnBeforeInvoke((handler)=>{
            string token = AcquireAuthToken();
            if (proxy.Client.DefaultHeaders.Contains("Authorization"))
            {
                 proxy.Client.DefaultHeaders.Remove("Authorization");
            }
            proxy.Client.DefaultHeaders.Add("Authorization", new AuthenticationHeaderValue("Bearer", token).ToString());
        });
        

The cast of the client object to ``IQiClientProxy`` provides access to
the ``OnBeforeInvoke`` action. Because security tokens expire, we give
the authentication libraries a chance to refresh the token before every
call. The lambda implementing this calls ``AcquireAuthToken``, which
we'll describe in the next section, then turns to the ``DefaultHeaders``
collection. This collection will throw an exception if more than one
``Authorization`` header is added, so any existing header is removed
before attaching the new one.

Obtain an Authentication Token
==============================

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. The sample applications are examples of
*confidential clients*. Such clients provide a user ID and secret that
are authenticated against the directory. The sample code includes
several placeholder strings for authentication. You must replace these
with the authentication-related values you received from OSIsoft. The
strings are located in the ``Constants.cs`` file.

.. code:: c#

            public const string SecurityResource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
            public const string SecurityAuthority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
            public const string SecurityAppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
            public const string SecurityAppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
            public const string QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL";

At the bottom of ``Program.cs`` you will find a method called
``AcquireAuthToken``. The first step in obtaining an authorization token
is to create an authentication context related to the Azure Active
Directory instance providing tokens. The authority is designated by the
URI in ``SecurityAuthority``.

.. code:: c#

        if (_authContext == null)
        {
            _authContext = new AuthenticationContext(Constants.SecurityAuthority);
        }

``AuthenticationContext`` instances take care of communicating with the
authority and also maintain a local cache of tokens. Tokens have a fixed
lifetime of one hour, but they can be refreshed by the authenticating
authority for a longer period. If the refresh period has expired,
credentials must be presented to the authority again. Happily, the
``AcquireToken`` method hides these details from client programmers. As
long as ``AcquireToken`` is called before each HTTP call, you will have
a valid token. Here is how that is done:

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

The result returned by ``AcquireAuthToken`` is the value, ``token``,
attached to the client object as shown in the previous section:

.. code:: c#

        clientFactory.OnCreated((p)=>p.DefaultHeaders.Add("Authorization", new AuthenticationHeaderValue("Bearer", token).ToString()));

Create a QiType
===============

QiStreams represent open-ended collections of strongly-typed, ordered
events. Qi is capable of storing any data type you care to define. The
only requirement is that the data type must have one or more properties
that constitute an ordered key. While a timestamp is a very common type
of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a QiType, so that only events
conforming to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

The Qi Client Libraries permit the creation of QiTypes via reflection.
For simple types like our sample type, this may not seem like an
advantage over the type creation illustrated in the REST samples. For
more complex types, particularly nested complex types, reflection makes
your job far easier!

The first step to taking advantage of reflection is to create a .NET
class. Our sample definition is in ``WaveData.cs``. This class has an
``Order`` property for a key, and properties for radians and the common
trigonometric and hyperbolic trigonometric functions of the value of the
radians properties. The class illustrates how Qi can store
non-traditional custom types. Note the lines

.. code:: c#

        [Key]
        public int Order
        {
            get;
            set;
        }

This creates an Order property and marks it as the index for this type.
The ``Key`` attribute comes from the
``System.ComponentModel.DataAnnotations`` namespace. There are two other
ways to specify the key for your custom type. If you use the
``QiMember`` attribute from the ``OSIsoft.Qi`` namespace, set the
``IsKey`` property to true. If you prefer to use data contracts from the
``System.Runtime.Serialization`` namespace, create a ``DataMember``
property whose property name ends in ``id`` (case insensitive). Qi also
permits compound indices.

Now, back in ``Program.cs``, we create a type builder object and use it
to create an instance of the Qi type:

.. code:: c#

        QiTypeBuilder typeBuilder = new QiTypeBuilder();
        evtType = typeBuilder.Create<WaveData>();

Note that ``Create`` is a generic method, and the type is the class
defining the desired QiType. While we've created and configured a QiType
object locally, we have not yet created anything in the Qi service. In
order to do so, the type is assigned an identifier and submitted like
this:

.. code:: c#

        evtType.Id = "WaveType";
        QiType tp = qiclient.GetOrCreateType(evtType);

If no identifier is specified, the Qi service will automatically assign
one, which will be included in the returned QiType. The id is required
for stream creation, so be sure to capture the returned QiType instance.

Create a QiStream
=================

An ordered series of events is stored in a QiStream. Stream creation
involves creating a local QiStream instance, giving it an id, assigning
it a type, and submitting it to the Qi service. You may optionally
assign a QiStreamBehavior to the stream. This is the code to create a
stream named ``evtStream`` for recording events of our sample type. The
value of the ``TypeId`` property is the value of the QiType ``Id``
property.

.. code:: c#

        QiStream sampleStream = new QiStream();
        sampleStream.Name = "evtStream";
        sampleStream.Id = "evtStream";
        sampleStream.TypeId = tp.Id;
        sampleStream.Description = "This is a sample stream for storing WaveData type measurements";
        QiStream strm = qiclient.GetOrCreateStream(sampleStream);

Note that we set the ``TypeId`` property of the stream we created to the
value of the id of the QiType instance returned by the call to
``GetOrCreateType``. Types and behaviors are reference counted; a type
or behavior cannot be deleted until all streams using it are also
deleted.

Create and Insert Events into the Stream
========================================

The ``WaveData`` class allows us to create events locally. In an actual
production setting, this is where you would interface with your
measurements. We'll use the ``Next`` method to create values, and assign
integers from 0-99 to establish an ordered collection of ``WaveData``
instances. There are a number of methods you can use to insert values
into the Qi service. A single event can be inserted using
``InsertValue<T>`` or ``InsertValueAsync<T>`` (all Async methods use
.NET TPL, see https://msdn.microsoft.com/en-us/library/hh191443.aspx).
You can also submit a collection of events using ``InsertValues<T>`` or
``InsertValuesAsync<T>``. There is also an overloaded version of
``InsertValues`` that takes an ``IDictionary``. Here is the insertion
code from this sample:

.. code:: c#

        TimeSpan span = new TimeSpan(0, 0, 1);
        WaveData evt = WaveData.Next(span, 2.0, 0);

        qiclient.InsertValue("evtStream", evt);

        List<WaveData> events = new List<WaveData>();
        for (int i = 1; i < 100; i++)
        {
            evt = WaveData.Next(span, 2.0, i);
            events.Add(evt);
        }
        
        qiclient.InsertValues("evtStream", events);

Retrieve Events
===============

There are many methods that allow for the retrieval of events from a
stream. This sample demonstrates the most basic method of retrieving all
the events in a particular index range. The retrieval methods take
string type start and end values; in our case, these the start and end
ordinal indices expressed as strings ("0" and "99", respectively). The
index values must capable of conversion to the type of the index
assigned in the QiType. Timestamp keys are expressed as ISO 8601 format
strings. Compound indices are values concatenated with a pipe ('\|')
separator. You can get a collection of events over an index range like
this:

.. code:: c#

        IEnumerable<WaveData> foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "99");

Keep in mind that with an IEnumerable instance, there are a variety of
LINQ and extension methods allowing you to manipulate the events
locally.

Update Events
=============

We'll demonstrate updates by taking the values we created and replacing
them with new values. Once you've modified the events client-side, you
submit them to the Qi service with ``UpdateValue<T>`` or
``UpdateValues<T>``, or their asynchronous equivalents:

.. code:: c#

        qiclient.UpdateValue("evtStream", evt);
        qiclient.UpdateValues("evtStream", newEvents);

Delete Events
=============

As with reading data, deletion is managed via the index. It is possible
to delete data at a particular index or set of indices, or over an index
range.

.. code:: c#

        qiclient.RemoveValue("evtStream", 0);
        qiclient.RemoveWindowValues("evtStream", 1, 99);

Bonus: Deleting Types and Streams
=================================

You might want to run the sample more than once. To avoid collisions
with types and streams, the sample program deletes the stream and type
it created before terminating. The stream goes first so that the
reference count on the type goes to zero:

.. code:: c#

        qiclient.DeleteStream("evtStream")

Note that we've passed the id of the stream, not the stream object.
Similarly, the following deletes the type from the Qi service:

.. code:: c#

        qiclient.DeleteType(tp.Id);

The ``IQiServer`` instance doesn't need any cleanup. REST runs on HTTP,
which is stateless, so the Qi service is not maintaining a connection
with the client.
