.NET Samples 
============

Building a Client with the Qi Client Libraries
----------------------------------------------

The sample described in this section differs from the other samples in that the clientapplication makes use of the OSIsoft Qi Client Libraries. These libraries are available as NuGet packages from https://osisoft.myget.org/F/qi/. The packages used are ``OSIsoft.Qi.Core``, ``OSIsoft.Qi.Http.Channel``, ``OSIsoft.Qi.Http.Client``, and ``OSIsoft.Qi.Http.Security``. Ultimately, the Qi REST APIs are invoked just like the rest of the samples, but the libraries offer a framework of classes to make client development easier.

Configure constants for authentication
==============================

The Qi service is secured by obtaining tokens from an Azure Active Directory instance. The sample applications are examples of *confidential clients*. Such clients provide a user ID and secret that are authenticated against the directory. The sample code includes several placeholder strings for authentication. You must replace the placeholders with the authentication-related values you received from OSIsoft. The strings are located in the ``Constants.cs`` file.

.. code:: c#

	public const string TenantId = "PLACEHOLDER_REPLACE_WITH_TENANT_ID";
        public const string SecurityResource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        public const string SecurityAppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        public const string SecurityAppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
        public const string QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL";

At the bottom of ``Program.cs`` is a method called ``GetQiSecurityHandler``, which returns a QiSecurityHandler for token acquisition based on the user-configured constants.


Set up Qi client services
=======================

The client example works through several client interfaces:  ``IQiAdministrationService`` for namespace management, ``IQiMetadataService`` for QiStream, QiType, and QiStreamBehavior metadata operations, and ``IQiDataService`` for reading and writing data. These services are accessed via static methods in the QiService class.

To successfully interact with Qi, an ``Authorization`` header must be added to every REST call. The value of this header is the scheme keyword ``Bearer`` followed by a token string that is returned by Azure Active Directory. The OSIsoft.Qi.Http.Security package provides a QiSecurityHandler class that will handle acquiring the appropriate token from Azure Active Directory and adding it to the headers of each request.

The following code block demonstrates setting up an IQiDataService with the QiSecurityHandler and changing the request timeout from the default value of 30 seconds to 1 minute.

.. code-block:: c#

	QiSecurityHandler qiSecurityHandler = new QiSecurityHandler(Constants.SecurityResource, Constants.TenantId, Constants.SecurityAppId, Constants.SecurityAppKey);
        Uri address = new Uri(Constants.QiServerUrl);
        
	IQiDataService qiDataService = QiService.GetDataService(address, Constants.TenantId, namespaceId, qiSecurityHandler);

	qiDataService.GetProxy().Client.Timeout = TimeSpan.FromMinutes(1);              
	
A similar pattern is followed in the sample to set up the IQiAdministrationService and IQiMetadataService.


Create a QiType
===============

Qi is capable of storing any data type you care to define. The only requirement is that the data type must have one or more properties that constitute an ordered key. While a timestamp is a very common type of key, any ordered value is permitted. The sample uses an integer.

QiStreams represent open-ended collections of strongly typed, ordered events.  Each QiStream is associated with a QiType, so that only events that conform to that type can be inserted into the stream. The first step in Qi programming, then, is to define the types for your tenant.

The Qi Client Libraries permit the creation of QiTypes via reflection. For simple types like our sample type, this may not seem like an advantage over the type creation that is illustrated in the REST samples. For more complex types, particularly nested complex types, reflection makes your job far easier.

To take advantage of reflection, the first step is to create a .NET class. The sample definition is contained in ``WaveData.cs``. This class has an ``Order`` property for a key, and properties for radians and the common trigonometric and hyperbolic trigonometric functions of the value of the radians properties. The class illustrates how Qi can store non-traditional custom types. Note the following lines in the code:

.. code:: c#

        [Key]
        public int Order
        {
            get;
            set;
        }

The preceeding code creates an Order property and marks it as the index for this type. The ``Key`` attribute comes from the ``System.ComponentModel.DataAnnotations`` namespace. There are two other ways to specify the key for your custom type. If you use the ``QiMember`` attribute from the ``OSIsoft.Qi`` namespace, set the ``IsKey`` property to true. If you prefer to use data contracts from the ``System.Runtime.Serialization`` namespace, create a ``DataMember`` property whose property name ends in ``id`` (case insensitive). Qi also permits compound indexes.

In ``Program.cs``, a type builder object is created and used to create an instance of the Qi type:

.. code:: c#

	QiTypeBuilder typeBuilder = new QiTypeBuilder();
        QiType sampleType = typeBuilder.Create<WaveData>();

Note that ``Create`` is a generic method, and the type is the class that is defining the desired QiType. While a QiType was created and configured locally, nothing has yet been created in the Qi service. To do so, the type is assigned an identifier and submitted like as in the following code:

.. code:: c#

        sampleType.Id = sampleTypeId;
        sampleType = qiMetadataService.GetOrCreateTypeAsync(sampleType).GetAwaiter().GetResult();

If an identifier is not specified, the Qi service automatically assigns one, which will be included in the returned QiType. The ID is required for stream creation, so be sure to capture the returned QiType instance.

Create a QiStream
=================

An ordered series of events is stored in a QiStream. Stream creation involves creating a local QiStream instance, giving it an ID, assigning it a type, and submitting it to the Qi service. You may optionally assign a QiStreamBehavior to the stream. The following code shows how to create a stream named ``evtStream`` for recording events of the sample type. The value of the ``TypeId`` property is set to the value of the QiType ``Id`` property for the QiType created in the previous step.

.. code:: c#

        QiStream sampleStream = new QiStream()
        {
            Name = "Wave Data Sample Stream",
            Id = sampleStreamId,
            TypeId = sampleTypeId,
            Description = "This is a sample QiStream for storing WaveData type measurements"
        };
		
        sampleStream = qiMetadataService.GetOrCreateStreamAsync(sampleStream).GetAwaiter().GetResult();

Note that QiTypes and QiStreamBehaviors are reference counted; a type or behavior cannot be deleted until all streams using it are also deleted.

Create and Insert Events into the Stream
========================================

The ``WaveData`` class allows you to create events locally. In a production environment, this is the class where you would interface with your measurements. The ``Next`` method is used to create values and assign integers from 0-99 to establish an ordered collection of ``WaveData`` instances. There are a number of methods you can use to insert values into the Qi service. A single event can be inserted using ``InsertValueAsync<T>``.  You can also submit a collection of events using ``InsertValuesAsync<T>``. Here is the insertion code from this sample:

.. code:: c#

        TimeSpan span = new TimeSpan(0, 1, 0);
        WaveData waveDataEvent = WaveData.Next(span, 2.0, 0);
        
        qiDataService.InsertValueAsync(sampleStreamId, waveDataEvent).GetAwaiter().GetResult();
       
        List<WaveData> waveDataEvents = new List<WaveData>();
        for (int i = 2; i < 200; i += 2)
        {
            waveDataEvent = WaveData.Next(span, 2.0, i);
            waveDataEvents.Add(waveDataEvent);
        }

        qiDataService.InsertValuesAsync(sampleStreamId, waveDataEvents).GetAwaiter().GetResult();
		

Retrieve Events
===============

There are many methods that permit retrieving events from a stream. This sample demonstrates the most basic method of retrieving all the events in a particular index range. The retrieval methods take string type start and end values; in this case, the start and end ordinal indices are expressed as strings ("0" and "99", respectively). The index values must capable of being converted to the type of the index that is assigned in the QiType. Timestamp keys are expressed as ISO 8601 format strings. Compound indices are values concatenated with a pipe ('\|') separator. You can get a collection of events over an index range like this:

.. code:: c#

        IEnumerable<WaveData> foundEvents = qiDataService.GetWindowValuesAsync<WaveData>(sampleStreamId, "0", "198").GetAwaiter().GetResult();

Keep in mind that with an IEnumerable instance, there are a variety of LINQ and extension methods that allow you to manipulate the events locally.


Update Events
=============

Updates can best be demonstrated by taking the values that were created and replacing them with new values. After you have modified the events on the client, you submit them to the Qi service with ``UpdateValueAsync<T>`` or ``UpdateValuesAsync<T>``:

.. code:: c#

        waveDataEvent = foundEvents.First();
        waveDataEvent = WaveData.Next(span, 4.0, waveDataEvent.Order);
        qiDataService.UpdateValueAsync(sampleStreamId, waveDataEvent).GetAwaiter().GetResult();

        // update the collection of events (same span, multiplier of 4, retain order)
        waveDataEvents = new List<WaveData>();
        foreach (WaveData evnt in waveDataEvents)
        {
            waveDataEvent = WaveData.Next(span, 4.0, evnt.Order);
            waveDataEvents.Add(waveDataEvent);
        }

        qiDataService.UpdateValuesAsync(sampleStreamId, waveDataEvents).GetAwaiter().GetResult();

		
Delete Events
=============

As with reading data, deletion is managed using the index. It is possible to delete data at a particular index or set of indexes, or over an index range.

.. code:: c#

        qiDataService.RemoveValueAsync(sampleStreamId, 0).GetAwaiter().GetResult();
        qiDataService.RemoveWindowValuesAsync(sampleStreamId, 2, 198).GetAwaiter().GetResult();

Deleting Types, Behaviors and Streams
=================================

You should run the sample more than once. To avoid collisions with types, behaviors, and streams, the sample program deletes the metadata objects that were created before terminating. The stream goes first so that the reference count on the type and behavior go to zero:

.. code:: c#

        qiMetadataService.DeleteStreamAsync(sampleStreamId)).GetAwaiter().GetResult();
	qiMetadataService.DeleteBehaviorAsync(sampleBehaviorId)).GetAwaiter().GetResult();
	qiMetadataService.DeleteTypeAsync(sampleTypeId)).GetAwaiter().GetResult();

