.NET Samples 
============

Building a Client with the Qi Client Libraries
----------------------------------------------

The sample described in this section makes use of the OSIsoft Qi Client Libraries. When working in .NET, 
it is recommended that you use these libraries. The libraries are available as NuGet packages 
from https://osisoft.myget.org/F/qi/. The packages used are:

* OSIsoft.Contracts, 
* OSIsoft.Data.Core,  
* OSIsoft.Http.Security. 

The libraries offer a framework of classes that make client development easier.

Configure constants for connecting and authentication
-----------------------------------------------------

The Qi Service is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

.. code:: json

{
  "Namespace": "Samples",
  "Tenant": "REPLACE_WITH_TENANT_ID",
  "Address": "https://qi-data.osisoft.com",
  "Resource": "https://qihomeprod.onmicrosoft.com/ocsapi",
  "AppId": "REPLACE_WITH_APPLICATION_IDENTIFIER",
  "AppKey": "REPLACE_WITH_APPLICATION_SECRET"
}



The authentication values are provided to the ``OSIsoft.Http.Security.QiSecurityHandler``. 
The QiSecurityHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

Set up Qi clients
-----------------

The client example works through two client interfaces: 

* IQiMetadataService for QiStream, QiType, QiView and QiStreamBehavior metadata operations
* IQiDataService for reading and writing data

The following code block illustrates how to configure clients to use throughout the sample:

.. code:: cs

    var metadataService = QiService.GetMetadataService(new Uri(address), tenant, namespaceId,
        new QiSecurityHandler(resource, tenant, appId, appKey));

    var dataService = QiService.GetDataService(new Uri(address), tenant, namespaceId,
        new QiSecurityHandler(resource, tenant, appId, appKey));
  
  

Create a QiType
---------------

To use Qi, you define QiTypes that describe the kinds of data you want to store in 
QiStreams. QiTypes are the model that define QiStreams.

QiTypes can define simple atomic types, such as integers, floats or strings, or they 
can define complex types by grouping other QiTypes. For more information about QiTypes, 
refer to the Qi Documentation.

When working with the Qi Client Libraries, it is strongly recommended that you use 
QiTypeBuilder. QiTypeBuilder uses reflection to build QiTypes. The QiTypeBuilder exposes 
a number of methods for manipulating types. One of the simplest ways to create a type 
is to use one of its static methods:

.. code:: cs

	QiType type = QiTypeBuilder.CreateQiType<WaveData>();
 
	// When defining the type, specify the key as follows:
	public class WaveData 
	{
		[QiMember(IsKey = true)]
		public int Order { get; set; }
		public double Tau { get; set; }
		public double Radians { get; set; }
		...
	}
    
To define the QiType in Qi, use the metadata client as follows:

.. code:: cs

	QiType type = config.GetOrCreateTypeAsync(type).GetAwaiter().GetResult();

Create a QiStream
------------------

An ordered series of events is stored in a QiStream. All you have to do
is create a local QiStream instance, give it an Id, assign it a type,
and submit it to the Qi Service. You may optionally assign a
QiStreamBehavior to the stream. The value of the ``TypeId`` property is
the value of the QiType ``Id`` property.

.. code:: cs

      Console.WriteLine("Creating a QiStream");
      var stream = new QiStream
      {
        Id = streamId,
        Name = "Wave Data Sample",
        TypeId = type.Id,
        Description = "This is a sample QiStream for storing WaveData type measurements"
      };


As with the QiType, once a QiStream is created locally, use the metadata client 
to submit it to the Qi Service:

.. code:: cs

	stream = await metadataService.GetOrCreateStreamAsync(stream);

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the Qi type for the
event.  First the event is created locally by instantiating a new WaveData 
object:

.. code:: cs

	return new WaveData
		{
		Order = order,
		Radians = radians,
		Tau = radians / (2 * Math.PI),
		Sin = multiplier * Math.Sin(radians),
		Cos = multiplier * Math.Cos(radians),
		Tan = multiplier * Math.Tan(radians),
		Sinh = multiplier * Math.Sinh(radians),
		Cosh = multiplier * Math.Cosh(radians),
		Tanh = multiplier * Math.Tanh(radians)
		};

Then use the data service client to submit the event using the InsertValueAsync method:

.. code:: cs

 await dataService.InsertValueAsync(stream.Id, wave);

Similarly, we can build a list of objects and insert them in bulk by calling 
InsertValuesAsync:

.. code:: cs

	var waves = new List<WaveData>();
	for (var i = 2; i <= 18; i += 2)
	{
		waves.Add(GetWave(i, 200, 2));
	}
	await dataService.InsertValuesAsync(stream.Id, waves);


Retrieve Values from a Stream
-----------------------------

There are many methods in the Qi REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the QiType.

.. code:: cs

  IEnumerable<WaveData> retrieved = 
     client.GetWindowValuesAsync<WaveData>(stream.Id, "0", "20").GetAwaiter().GetResult();

Update Events and Replacing Values
----------------------------------

Updating events is handled using the data service client as follows:

.. code:: cs

	await dataService.UpdateValueAsync(stream.Id, updatedWave);

Updates can be made in bulk by passing a collection of WaveData objects:

.. code:: cs

	var updatedCollection = new List<WaveData>();
	for (int i = 2; i < 40; i = i+2)
	{
		updatedCollection.Add(GetWave(i, 400, 4));
	}
	await dataService.UpdateValuesAsync(stream.Id, updatedCollection);

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValue`` and ``updateValues``:

.. code:: cs

	await dataService.ReplaceValueAsync<WaveData>(streamId, replaceEvent);	

	await dataService.ReplaceValuesAsync<WaveData>(streamId, allEvents);

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

.. code:: cs

	// create a Discrete stream behavior
	var behavior = new QiStreamBehavior
	{
		Id = behaviorId,
		Mode = QiStreamMode.Discrete
	};	
	behavior = await metadataService.GetOrCreateBehaviorAsync(behavior);

	// update the stream
	stream.BehaviorId = behavior.Id;
	await metadataService.CreateOrUpdateStreamAsync(stream);

The sample repeats the call to ``getRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
``Order=1``.

QiViews
-------

A QiView provides a way to map Stream data requests from one data type 
to another. You can apply a View to any read or GET operation. QiView 
is used to specify the mapping between source and target types.

Qi attempts to determine how to map Properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, Qi will map the properties automatically.

.. code:: cs

      var autoViewData = await dataService.GetRangeValuesAsync<WaveDataTarget>(stream.Id, "1", 3, QiBoundaryType.ExactOrCalculated, autoViewId);

To map a property that is beyond the ability of Qi to map on its own, 
you should define a QiViewProperty and add it to the QiView's Properties collection.

.. code:: cs

	// create explicit mappings 
	var vp1 = new QiViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
	var vp2 = new QiViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
	var vp3 = new QiViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
	var vp4 = new QiViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

    var manualView = new QiView()
	{
		Id = manualViewId,
		SourceTypeId = typeId,
		TargetTypeId = targetIntTypeId,
		Properties = new List<QiViewProperty>() { vp1, vp2, vp3, vp4 }
	};

	await metadataService.CreateOrUpdateViewAsync(manualView);

QiViewMap
---------

When a QiView is added, Qi defines a plan mapping. Plan details are retrieved as a QiViewMap. 
The QiViewMap provides a detailed Property-by-Property definition of the mapping.
The QiViewMap cannot be written, it can only be retrieved from Qi.

.. code:: cs

	var manualViewMap = await metadataService.GetViewMapAsync(manualViewId);

Delete Values from a Stream
---------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Code from both functions
is shown below:

.. code:: cs

	await dataService.RemoveValueAsync(stream.Id, 0);

	await dataService.RemoveWindowValuesAsync(stream.Id, 1, 40);


As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to '1' and '40'
are removed from the stream.

Cleanup: Deleting Types, Behaviors, Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream
behaviors, views and types can be achieved using the metadata 
client and passing the corresponding object Id:

.. code:: cs

	await metadataService.DeleteStreamAsync(streamId);
	await metadataService.DeleteTypeAsync(typeId);