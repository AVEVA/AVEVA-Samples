SDS JavaScript Example using Angular
===================================

Building a client to make REST API calls to the SDS Service
----------------------------------------------------------

This example demonstrates how SDS REST APIs are invoked using Angular 6. Although this example uses Angular, other javascript frameworks should also work.


Prerequisites
-------------

You must have the following software installed on your computer:
 - Angular version 6 (available on GitHub)
 - Angular CLI
 - A modern browser (OSIsoft recommends Google Chrome or Mozilla Firefox)


Preparation
-----------

The SDS Service is secured by obtaining tokens from an Azure Active
Directory instance. This example uses ADAL (Active Directory Authentication Library) 
to authenticate clients against the SDS server. Contact OSIsoft support
to obtain a tenant for use with SDS. 

The sample code includes several placeholder strings that must be modified 
with values you received from OSIsoft. 

Edit the following values in the src/app/app.component.ts file:

:: 

        const config: ISdsConfigSet = {
            ClientID: 'PLACEHOLDER_REPLACE_WITH_CLIENTID',
            SdsEndPoint: 'PLACEHOLDER_REPLACE_WITH_SDS_SERVER_URL',
            SdsResourceURI: 'PLACEHOLDER_REPLACE_WITH_RESOURCE',
            TenantId: 'PLACEHOLDER_REPLACE_WITH_TENANT_ID',
            NamespaceId: 'REPLACE_WITH_NAMESPACE',
            ApiVersion: 'v1-preview'
        };


The application relies on the OAuth2 implicit grant flow.  Upon navigating to the webpage, users will be prompted to login to Azure Active Directory. 
In addition to these credentials, the application must be configured to allow for token retrieval on the user's behalf.  Once this is 
correctly set up, the application will retrieve a bearer token and pass this token along with every request to the SDS Service.  If the this token
is not present, the SDS Service will return 401 Unauthorized for every request.  Users are encouraged to use their browser's development tools
to troubleshoot any issues with authentication.

Running the example
------------------------------

The SDS Services page contains several buttons that demonstrate the main functionality of SDS:

::

    Create and Insert: Create the type, then the stream, then inserts WaveData events into the stream.
    Retrieve Events: Get the latest event and then get all events from the SdsStream.
    Update and Replace: Updates events, adds an additional ten events, then replace all.
    SdsStreamViews: Create and demonstrate SdsStreamViews and SdsStreamViewMaps
    Cleanup: Deletes the events, stream, streamViews and types.


To run the example, click each of the buttons in turn from top to bottom. In most modern browsers, you can view the API calls and results as they occur by pressing **F12**. 


The rest of the sections in this document outline the operation of SDS and the underlying process and technology of the example.


How the example works
----------------------

The sample uses the AuthHttp class to connect to the SDS Service
endpoint. SDS REST API calls are sent to the SDS Service. The SDS REST API
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


Create an SdsType
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want
to store in SdsStreams. SdsTypes are the model that define SdsStreams.
SdsTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>.

In the sample code, the SdsType representing WaveData is defined in the buildWaveDataType method of
datasrc.component.ts. WaveData contains properties of integer and double atomic types. 
The constructions begins by defining a base SdsType for each atomic type and then defining
Properties of those atomic types.

.. code:: javascript

    buildWaveDataType() {
        const doubleType = new SdsType();
        doubleType.Id = 'doubleType';
        doubleType.SdsTypeCode = SdsTypeCode.Double;

        const intType = new SdsType();
        intType.Id = 'intType';
        intType.SdsTypeCode = SdsTypeCode.Int32;

        const orderProperty = new SdsTypeProperty();
        orderProperty.Id = 'Order';
        orderProperty.SdsType = intType;
        orderProperty.IsKey = true;

        const radiansProperty = new SdsTypeProperty();
        radiansProperty.Id = 'Radians';
        radiansProperty.SdsType = doubleType;
        ...

An SdsType can be created by a POST request as follows:

.. code:: javascript

    createType() {
        const type = this.buildWaveDataType();
        this.sdsService.createType(type).subscribe(res => {
        this.button1Message = res.status;
        },
        err => {
            this.button1Message = err;
        });
    }


Create an SdsStream
-----------------

An ordered series of events is stored in an SdsStream. All you have to do
is create a local SdsStream instance, give it an Id, assign it a type,
and submit it to the SDS service. The value of the ``TypeId`` property is
the value of the SdsType ``Id`` property.

.. code:: javascript

    this.stream = new SdsStream();
    this.stream.Id = streamId;
    this.stream.TypeId = typeId;

The local SdsStream can be created in the SDS service by a POST request as
follows:

.. code:: javascript

    this.sdsService.createStream(this.stream)
        .subscribe(res => {
        this.button2Message = res.status;
        },
    err => {
        this.button2Message = err;
        });;

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the SDS type for the
event. Events are passed in json format.

An event can be created using the following POST request:

.. code:: javascript

    insertValue(streamId: string, event: any) {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValue`;
        return this.authHttp.post(url, JSON.stringify(event).toString());
    }

Inserting multiple values is similar, but the payload has list of events
and the url for POST call varies:

.. code:: javascript

    insertValues(streamId: string, events: Array<any>) {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValues`;
        return this.authHttp.post(url, JSON.stringify(events).toString());
        }

The SDS REST API provides many more types of data insertion calls beyond
those demonstrated in this application. Go to the 
SDS documentation<https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html> for more information
on available REST API calls.

Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the SdsType.

This sample implements only two of the many available retrieval methods -
getRangeValues and getLastValue.

.. code:: javascript

    getRangeValues(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
        const url = this.sdsUrl +
            `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
            `/Data/GetRangeValues?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}`;
        return this.authHttp.get(url);
    }


Update Events and Replacing Values
----------------------------------

Updating events is handled by PUT REST call as follows:

.. code:: javascript

    updateValue(streamId: string, event: any) {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValue`;
        return this.authHttp.put(url, JSON.stringify(event).toString());
    }

-  the request body has the new event that will update an existing event
   at the same index

Updating multiple events is similar, but the payload has an array of
event objects and url for PUT is slightly different:

.. code:: javascript

    updateValues(streamId: string, events: Array<any>) {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/UpdateValues`;
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
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValue`;
        return this.authHttp.put(url, JSON.stringify(event).toString());
    }

    replaceValues(streamId: string, events: Array<any>) {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/ReplaceValues`;
        return this.authHttp.put(url, JSON.stringify(events).toString());
    }


Property Overrides
------------------

SDS has the ability to override certain aspects of an SDS Type at the SDS Stream level.  
Meaning we apply a change to a specific SDS Stream without changing the SDS Type or the
read behavior of any other SDS Streams based on that type.  

In the sample, the InterpolationMode is overridden to a value of Discrete for the property Radians. 
Now if a requested index does not correspond to a real value in the stream then ``null``, 
or the default value for the data type, is returned by the SDS Service. 
The following shows how this is done in the code:

.. code:: javascript

	const propertyOverride = new SdsStreamPropertyOverride();
	propertyOverride.SdsTypePropertyId = "Radians";
	propertyOverride.InterpolationMode = SdsStreamMode.Discrete;
	this.stream.PropertyOverrides = [propertyOverride];
	this.sdsService.updateStream(this.stream)

The process consists of two steps. First, the Property Override must be created, then the
stream must be updated. Note that the sample retrieves three data points
before and after updating the stream to show that it has changed. See
the `SDS documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__ for
more information about SDS Property Overrides.

SdsStreamViews
-------

An SdsStreamView provides a way to map Stream data requests from one data type 
to another. You can apply a StreamView to any read or GET operation. SdsStreamView 
is used to specify the mapping between source and target types.

SDS attempts to determine how to map Properties from the source to the 
destination. When the mapping is straightforward, such as when 
the properties are in the same position and of the same data type, 
or when the properties have the same name, SDS will map the properties automatically.

.. code:: javascript

    this.sdsService.getRangeValues(streamId, '3', 5, SdsBoundaryType.ExactOrCalculated, autoStreamViewId)

To map a property that is beyond the ability of SDS to map on its own, 
you should define an SdsStreamViewProperty and add it to the SdsStreamView’s Properties collection.

.. code:: javascript

    const manualStreamView = new SdsStreamView();
    manualStreamView.Id = manualStreamViewId;
    manualStreamView.Name = "WaveData_AutoStreamView";
    manualStreamView.Description = "This StreamView uses SDS Types of different shapes, mappings are made explicitly with SdsStreamViewProperties."
    manualStreamView.SourceTypeId = typeId;
    manualStreamView.TargetTypeId = targetIntTypeId;

    const streamViewProperty0 = new SdsStreamViewProperty();
    streamViewProperty0.SourceId = 'Order';
    streamViewProperty0.TargetId = 'OrderTarget';

    const streamViewProperty1 = new SdsStreamViewProperty();
    streamViewProperty1.SourceId = 'Sinh';
    streamViewProperty1.TargetId = 'SinhInt';

SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS.

.. code:: javascript

    getStreamViewMap(streamViewId: string): Observable<any> {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}/Map`;
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
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
        return this.authHttp.delete(url);
    }

    deleteWindowValues(streamId: string, start, end): Observable<any> {
        const url = this.sdsUrl +
        `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
        `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
        return this.authHttp.delete(url);
    }

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to start and end
are removed from the stream.

Cleanup: Deleting Types, Stream Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream views and types can be 
achieved by a DELETE REST call and passing the corresponding Id.

.. code:: javascript

    deleteValue(streamId: string, index): Observable<any> {
        const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/RemoveValue?index=${index}`;
        return this.authHttp.delete(url);
    }

.. code:: javascript

    deleteWindowValues(streamId: string, start, end): Observable<any> {
        const url = this.sdsUrl +
        `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
        `/Data/RemoveWindowValues?startIndex=${start}&endIndex=${end}`;
        return this.authHttp.delete(url);
    }