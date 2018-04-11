Qi JavaScript Example using Angular
===================================

Building a client to make REST API calls to the Qi Service
----------------------------------------------------------

This example demonstrates how Qi REST APIs are invoked using Angular 4.0. Although this example uses Angular, other javascript frameworks should also work.


Prerequisites
-------------

You must have the following software installed on your computer:
 - Angular version 4 (available on GitHub) or greater
 - Angular CLI version 1.1.2 or greater
 - A modern browser (OSIsoft recommends Google Chrome or Mozilla Firefox)


Preparation
-----------

The Qi Service is secured by obtaining tokens from an Azure Active
Directory instance. This example uses ADAL (Active Directory Authentication Library) 
to authenticate clients against the QI server. Contact OSIsoft support
to obtain a tenant for use with Qi. 

The sample code includes several placeholder strings that must be modified 
with values you received from OSIsoft. 

Edit the following values in the src/app/app.component.ts file:

:: 

    const config: IQiConfigSet = {
        Subscription: 'REPLACE_WITH_AZURE_SUBSCRIPTION',
        ClientID: 'REPLACE_WITH_APPLICATION_ID',
        SystemEndpoint: 'REPLACE_WITH_SYSTEM_ENDPOINT',
        SystemResourceURI: 'REPLACE_WITH_SYSTEM_RESOURCE_URI',
        QiEndPoint: 'REPLACE_WITH_QI_ENDPOINT',
        QiResourceURI: 'REPLACE_WITH_QI_RESOURCE_URI',
        TenantId: 'REPLACE_WITH_TENANT_ID',
        NamespaceId: 'REPLACE_WITH_NAMESPACE'
    } 

The application relies on the OAuth2 implicit grant flow.  Upon navigating to the webpage, users will be prompted to login to Azure Active Directory. 
In addition to these credentials, the application must be configured to allow for token retrieval on the user's behalf.  Once this is 
correctly set up, the application will retrieve a bearer token and pass this token along with every request to the Qi Service.  If the this token
is not present, the Qi Service will return 401 Unauthorized for every request.  Users are encouraged to use their browser's development tools
to troubleshoot any issues with authentication.

Running the example
------------------------------

The Qi Services page contains several buttons that demonstrate the main functionality of Qi:

::

    Create and Insert: Create the type, then the stream, then inserts WaveData events into the stream.
    Retrieve Events: Get the latest event and then get all events from the QiStream.
    Update and Replace: Updates events, adds an additional ten events, then replace all.
    Add Behavior: Creates and adds the behavior to the streams
    QiViews: Create and demonstrate QiViews and QiViewMaps
    Cleanup: Deletes the events, stream, stream behavior, views and types.


To run the example, click each of the buttons in turn from top to bottom. In most modern browsers, you can view the API calls and results as they occur by pressing **F12**. 


The rest of the sections in this document outline the operation of Qi and the underlying process and technology of the example.


How the example works
----------------------

The sample uses the AuthHttp class to connect to the Qi Service
endpoint. Qi REST API calls are sent to the Qi Service. The Qi REST API
maps HTTP methods to CRUD operations as in the following table:

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


Create a QiType
---------------

To use Qi, you define QiTypes that describe the kinds of data you want
to store in QiStreams. QiTypes are the model that define QiStreams.
QiTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other QiTypes. For
more information about QiTypes, refer to the Qi
documentation <https://cloud.osisoft.com/documentation>.

In the sample code, the QiType representing WaveData is defined in the buildWaveDataType method of
datasrc.component.ts. WaveData contains properties of integer and double atomic types. 
The constructions begins by defining a base QiType for each atomic type and then defining
Properties of those atomic types.

.. code:: javascript

    buildWaveDataType() {
        const doubleType = new QiType();
        doubleType.Id = 'doubleType';
        doubleType.QiTypeCode = QiTypeCode.Double;

        const intType = new QiType();
        intType.Id = 'intType';
        intType.QiTypeCode = QiTypeCode.Int32;

        const orderProperty = new QiTypeProperty();
        orderProperty.Id = 'Order';
        orderProperty.QiType = intType;
        orderProperty.IsKey = true;

        const radiansProperty = new QiTypeProperty();
        radiansProperty.Id = 'Radians';
        radiansProperty.QiType = doubleType;
        ...

A QiType can be created by a POST request as follows:

.. code:: javascript

    createType() {
        const type = this.buildWaveDataType();
        this.qiService.createType(type).subscribe(res => {
        this.button1Message = res.status;
        },
        err => {
            this.button1Message = err;
        });
    }


Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. All you have to do
is create a local QiStream instance, give it an Id, assign it a type,
and submit it to the Qi service. You may optionally assign a
QiStreamBehavior to the stream. The value of the ``TypeId`` property is
the value of the QiType ``Id`` property.

.. code:: javascript

    this.stream = new QiStream();
    this.stream.Id = streamId;
    this.stream.TypeId = typeId;

The local QiStream can be created in the Qi service by a POST request as
follows:

.. code:: javascript

    this.qiService.createStream(this.stream)
        .subscribe(res => {
        this.button2Message = res.status;
        },
    err => {
        this.button2Message = err;
        });;

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the Qi type for the
event. Events are passed in json format.

An event can be created using the following POST request:

.. code:: javascript

    insertValue(streamId: string, event: any) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValue`;
        return this.authHttp.post(url, JSON.stringify(event).toString());
    }

Inserting multiple values is similar, but the payload has list of events
and the url for POST call varies:

.. code:: javascript

    insertValues(streamId: string, events: Array<any>) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValues`;
        return this.authHttp.post(url, JSON.stringify(events).toString());
        }

The Qi REST API provides many more types of data insertion calls beyond
those demonstrated in this application. Go to the 
Qi documentation<https://cloud.osisoft.com/documentation> for more information
on available REST API calls.

Retrieve Values from a Stream
-----------------------------

There are many methods in the Qi REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the QiType.

This sample implements only two of the many available retrieval methods -
getRangeValues and getLastValue.

.. code:: javascript

    getRangeValues(streamId: string, start, count, boundary: QiBoundaryType, viewId: string = ''): Observable<any> {
        const url = this.qiUrl +
            `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
            `/Data/GetRangeValues?startIndex=${start}&count=${count}&boundaryType=${boundary}&viewId=${viewId}`;
        return this.authHttp.get(url);
    }


Update Events and Replacing Values
----------------------------------

Updating events is handled by PUT REST call as follows:

.. code:: javascript

    updateValue(streamId: string, event: any) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValue`;
        return this.authHttp.put(url, JSON.stringify(event).toString());
    }

-  the request body has the new event that will update an existing event
   at the same index

Updating multiple events is similar, but the payload has an array of
event objects and url for PUT is slightly different:

.. code:: javascript

    updateValues(streamId: string, events: Array<any>) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValues`;
        return this.authHttp.put(url, JSON.stringify(events).toString());
    }

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValue`` and ``updateValues``:

.. code:: javascript

    replaceValue(streamId: string, event: any) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValue`;
        return this.authHttp.put(url, JSON.stringify(event).toString());
    }

    replaceValues(streamId: string, events: Array<any>) {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValues`;
        return this.authHttp.put(url, JSON.stringify(events).toString());
    }


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

.. code:: javascript

    const behavior = new QiStreamBehavior();
    behavior.Id = behaviorId;
    behavior.Name = 'SampleBehavior';
    behavior.Mode = QiStreamMode.Discrete;
    this.qiService.createBehavior(behavior).subscribe(() => {
        this.stream.BehaviorId = behaviorId;
        this.qiService.updateStream(this.stream).subscribe
        ...

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

.. code:: javascript

    this.qiService.getRangeValues(streamId, '3', 5, QiBoundaryType.ExactOrCalculated, autoViewId)

To map a property that is beyond the ability of Qi to map on its own, 
you should define a QiViewProperty and add it to the QiView’s Properties collection.

.. code:: javascript

    const manualView = new QiView();
    manualView.Id = manualViewId;
    manualView.Name = "WaveData_AutoView";
    manualView.Description = "This view uses Qi Types of different shapes, mappings are made explicitly with QiViewProperties."
    manualView.SourceTypeId = typeId;
    manualView.TargetTypeId = targetIntTypeId;

    const viewProperty0 = new QiViewProperty();
    viewProperty0.SourceId = 'Order';
    viewProperty0.TargetId = 'OrderTarget';

    const viewProperty1 = new QiViewProperty();
    viewProperty1.SourceId = 'Sinh';
    viewProperty1.TargetId = 'SinhInt';

QiViewMap
---------

When a QiView is added, Qi defines a plan mapping. Plan details are retrieved as a QiViewMap. 
The QiViewMap provides a detailed Property-by-Property definition of the mapping.
The QiViewMap cannot be written, it can only be retrieved from Qi.

.. code:: javascript

    getViewMap(viewId: string): Observable<any> {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Views/${viewId}/Map`;
        return this.authHttp.get(url);
    }

Delete Values from a Stream
---------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Code from both functions
is shown below:

.. code:: javascript

    deleteValue(streamId: string, index): Observable<any> {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
        return this.authHttp.delete(url);
    }

    deleteWindowValues(streamId: string, start, end): Observable<any> {
        const url = this.qiUrl +
        `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
        `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
        return this.authHttp.delete(url);
    }

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to start and end
are removed from the stream.

Cleanup: Deleting Types, Behaviors, Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream
behaviors, views and types can be achieved by a DELETE REST call and passing
the corresponding Id.

.. code:: javascript

    deleteValue(streamId: string, index): Observable<any> {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
        return this.authHttp.delete(url);
    }

.. code:: javascript

    deleteWindowValues(streamId: string, start, end): Observable<any> {
        const url = this.qiUrl +
        `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
        `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
        return this.authHttp.delete(url);
    }
