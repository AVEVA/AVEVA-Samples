SDS JavaScript Example using Angular
===================================

Building a client to make REST API calls to the SDS Service
----------------------------------------------------------


The sample code in this topic demonstrates how to invoke SDS REST APIs
using Angular 7. By examining the code, you will see how to establish a connection 
to SDS, obtain an authorization token, create an SdsNamespace, SdsType, and SdsStream, 
and how to create, read, update, and delete values in SDS. Although this example uses 
Angular, other javascript frameworks should also work.


Prerequisites
-------------

You must have the following software installed on your computer:
 - Angular version 7 (available on GitHub/npm)
 - Angular CLI
 - A modern browser (OSIsoft recommends Google Chrome or Mozilla Firefox)
 - This application by default will use Port 4200
 
```
Note: This application is hosted on HTTP.  This is not secure.  You should use a certificate and HTTPS.
```
Developed against Node 10.14.1

Preparation
-----------

The SDS Service is secured by obtaining tokens from our OAuth2 identity provider
to authenticate clients against the SDS server. Contact OSIsoft support
to obtain a tenant for use with SDS. 

The sample code includes several placeholder strings that must be modified 
with values you received from OSIsoft. 

Edit the following values in the src/app/config/oidc.config.json file:

```json
{
    "authority": "https://dat-b.osisoft.com/identity",
    "redirect_uri": "http://localhost:4200/auth-callback/",
    "post_logout_redirect_uri": "http://localhost:4200/",
    "silent_redirect_uri": "http://localhost:4200/auth-callback/",
    "client_id": "REPLACE_WITH_CLIENT_ID"
}
```

Be sure to also configure your Implicit Client with the appropriate redirect URLs via the OCS portal

Also edit the following values in the src/app/config/sdsconfig.json:

```json
{
    "serviceBaseUri": "https://dat-b.osisoft.com",
    "tenantId": "REPLACE_WITH_TENANT_ID",
    "namespaceId": "REPLACE_WITH_NAMESPACE_ID",
    "apiVersion": "v1"
}
```


The application relies on the OAuth2 implicit grant flow.  Upon navigating to the webpage, users will be prompted to login to Azure Active Directory. 
In addition to these credentials, the application must be configured to allow for token retrieval on the user's behalf.  Once this is 
correctly set up, the application will retrieve a bearer token and pass this token along with every request to the SDS Service.  If the this token
is not present, the SDS Service will return 401 Unauthorized for every request.  Users are encouraged to use their browser's development tools
to troubleshoot any issues with authentication.


To run the test please update e2e\src\cred.json with appropriate values.  

Note: this script may run into problems if you have never logged in from the device before to the account you are using.  

To run the test use ng e2e --webdriver-update=false.

Running the example
------------------------------

Install dependencies using ``npm ci``* from within the Angular folder, then run the sample using ``npm start``

*you can use ``npm install`` but this will update the package-lock.json and may introduce new and different sub-dependencies.  

Login using the button in the webpage header

The SDS Services page contains several buttons that demonstrate the main functionality of SDS:

```
Create and Insert: Create the type, then the stream, then inserts WaveData events into the stream.
Retrieve Events: Get the latest event and then get all events from the SdsStream.
Update and Replace: Updates events, adds an additional ten events, then replace all.
SdsStreamViews: Create and demonstrate SdsStreamViews and SdsStreamViewMaps
Cleanup: Deletes the events, stream, streamViews and types.
```


To run the example, click each of the buttons in turn from top to bottom. In most modern browsers, you can view the API calls and results as they occur by pressing **F12**. 


The rest of the sections in this document outline the operation of SDS and the underlying process and technology of the example.


How the example works
----------------------

The sample uses the HttpClient class with an Authentication Interceptor to connect to the SDS Service
endpoint. SDS REST API calls are sent to the SDS Service. The SDS REST API
maps HTTP methods to CRUD operations as in the following table:

HTTP Method |CRUD Operation|Content Found In
-------|-----------|---------
POST          | Create           | message body       
GET           | Retrieve         | URL parameters     
PUT           | Update           | message body       
DELETE        | Delete           | URL parameters     



Create an SdsType
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want
to store in SdsStreams. SdsTypes are the model that define SdsStreams.
SdsTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html).

In the sample code, the SdsType representing WaveData is defined in the buildWaveDataType method of
datasrc.component.ts. WaveData contains properties of integer and double atomic types. 
The construction begins by defining a base SdsType for each atomic type.

```js
buildWaveDataType() {
    const doubleType = new SdsType();
    doubleType.Id = 'doubleType';
    doubleType.SdsTypeCode = SdsTypeCode.Double;

    const intType = new SdsType();
    intType.Id = 'intType';
    intType.SdsTypeCode = SdsTypeCode.Int32;
```

Next, the WaveData properties are each represented by an SdsTypeProperty.
Each SdsType field in SdsTypeProperty is assigned an integer or double
SdsType. The WaveData Order property represents the type’s key, and its
IsKey property is set to true.

```js
    const orderProperty = new SdsTypeProperty();
    orderProperty.Id = 'Order';
    orderProperty.SdsType = intType;
    orderProperty.IsKey = true;

    const radiansProperty = new SdsTypeProperty();
    radiansProperty.Id = 'Radians';
    radiansProperty.SdsType = doubleType;
    ...
```

An SdsType can be created by a POST request as follows:

```js
createType() {
    const type = this.buildWaveDataType();
    this.sdsService.createType(type).subscribe(res => {
    this.button1Message = res.status;
    },
    err => {
        this.button1Message = err;
    });
}
```

-  Returns the SdsType object in JSON format, or, if an SDS type with the same Id already exists, 
returns the url path of the existing SDS type.
-  The SdsType object is passed in json format

All SdsTypes are constructed in a similar manner. Basic SdsTypes form the basis for
SdsTypeProperties, which are then assigned to a complex user-defined
type. These types can then be used in properties and become part of
another SdsType's property list.


Create an SdsStream
-----------------

An SdsStream stores an ordered series of events. To create a
SdsStream instance, you simply provide an Id, assign it a type, and
submit it to the SDS service.  The value of the ``TypeId`` property is
the value of the SdsType ``Id`` property. The ``SdsStream`` object of SdsClient is
similar to ``SdsType``, except that it uses a different URL. Here is how
it is called from the main program:


```js
this.stream = new SdsStream();
this.stream.Id = streamId;
this.stream.TypeId = typeId;
```

The local SdsStream can be created in the SDS service by a POST request as
follows:

```js
this.sdsService.createStream(this.stream)
    .subscribe(res => {
    this.button2Message = res.status;
    },
err => {
    this.button2Message = err;
    });;
```

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the SDS type for the
event. Events are passed in json format and are serialized before being 
sent along with a POST request.

When inserting single or multiple values, the payload has to be the list of events. 
An event can be created using the following POST request:

```js
insertValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data`;
    return this.authHttp.post(url, JSON.stringify(events).toString());
    }
```

First the event is created locally by populating a new waveData event as follows:

```js
  newWaveDataEvent(order: number, range: number, multiplier: number) {
    const radians = order * Math.PI / 32;

    const waveData = new WaveData();
    waveData.Order = order;
    waveData.Radians = radians;
    waveData.Tau = radians / (2 * Math.PI);
    waveData.Sin = multiplier * Math.sin(radians);
    waveData.Cos = multiplier * Math.cos(radians);
    waveData.Tan = multiplier * Math.tan(radians);
    waveData.Sinh = multiplier * Math.sinh(radians);
    waveData.Cosh = multiplier * Math.cosh(radians);
    waveData.Tanh = multiplier * Math.tanh(radians);

    return waveData;
  }
```

Then use the data service client to submit the event using the insertValues method:

```js
const list: Array<WaveData> = [];
list.push(this.newWaveDataEvent(0, 2.5, 2));
this.sdsService.insertValues(streamId, list)
```

Similarly, we can build a list of objects and insert them in bulk:

```js
const list: Array<WaveData> = [];
for (let i = 0; i < 20; i += 2) {
    list.push(this.newWaveDataEvent(i, 12, 24));
}

this.sdsService.insertValues(streamId, list)
```

The SDS REST API provides many more types of data insertion calls beyond
those demonstrated in this application. Refer to the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html) for 
more information on available REST API calls.

Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API that allow the retrieval of
events from a stream. Many of the retrieval methods accept indexes,
which are passed using the URL. The index values must be capable of
conversion to the type of the index assigned in the SdsType. Below are 
some of the available methods which have been implemented in SdsClient: 

<h5>Get Window Values</h5>

``getWindowValues`` is used for retrieving events over a specific index range. 
Here is the request:

```js
  getWindowValues (streamId: string, start, end, filter: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data?startIndex=${start}&endIndex=${end}&filter=${filter}`;
    return this.authHttp.get(url, this.options);
  }
```

- *start* and *end* (inclusive) represent the indices for the retrieval. 
- The namespace ID and stream ID must be provided to the function call.
- A JSON object containing a list of the found values is returned. 
 Ex: For a time index, request url format will be
    "/{streamId}/Data?startIndex={startTime}&endIndex={endTime}


Here is how it is called:

```js
this.sdsService.getWindowValues(streamId, 0, 40, 'Radians%20lt%203')
```

<h5>Get Range Values</h5>

``getRangeValues`` is a method in ``SdsClient`` used for retrieving a 
specified number of events from a starting index. The starting index is 
the ID of the ``SdsTypeProperty`` that corresponds to the key value of 
the WaveData type. Here is the request:

```js
getRangeValues(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
    const url = this.sdsUrl +
        `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
        `/Data/Transform?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}`;
    return this.authHttp.get(url);
}
```

- *skip* is the increment by which the retrieval will happen.
- *count* is how many values you wish to have returned.
- *reverse* is a boolean that when ``true`` causes the retrieval to work 
backwards from the starting point.
- *boundary\_type* is a ``SdsBoundaryType`` value that determines the 
behavior if the starting index cannot be found. Refer the to the 
[SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html) for more information about SdsBoundaryTypes.

The ``getRangeValues`` method is called as shown :

```js
this.sdsService.getRangeValues(streamId, '1', 40, SdsBoundaryType.ExactOrCalculated)
```

You can also retreive the values in the form of a table (in this case with headers).
Here is the request:

```js
  getRangeValuesHeaders(streamId: string, start, count, boundary: SdsBoundaryType, streamViewId: string = ''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Transform?startIndex=${start}&count=${count}&boundaryType=${boundary}&streamViewId=${streamViewId}&form=tableh`;
    return this.authHttp.get(url, this.options);
  }
```

- *start* and *end* (inclusive) represent the indices for the retrieval.
- The namespace ID and stream ID must be provided to the function call.
- *form* specifies the organization of a table, the two available 
formats are table and header table

Here is how it is called:

```js
this.sdsService.getRangeValuesHeaders(streamId, '1', 40, SdsBoundaryType.ExactOrCalculated)
```

<h5>Get Sampled Values</h5>

Sampling allows retrieval of a representative sample of data between a start and end 
index.  Sampling is driven by a specified property or properties of the 
stream's Sds Type. Property types that cannot be interpolated do not 
support sampling requests. Strings are an example of a property that 
cannot be interpolated. For more information see 
[Interpolation.](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/SDS_Types.html#interpolation) Here is the request:

```js
  getSampledValues (streamId: string, start, end, intervals, sampleBy, filter: string = '', streamViewId=''): Observable<any> {
    const url = this.sdsUrl +
      `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
      `/Data/Sampled?startIndex=${start}&endIndex=${end}&intervals=${intervals}&sampleBy=${sampleBy}&filter=${filter}&streamViewId=${streamViewId}`;
    return this.authHttp.get(url, this.options);
  }
```
-  Parameters are the SdsStream Id, the starting and ending index
   values for the desired window, the number of intervals to select 
   from, the property or properties to use when sampling, an 
   optional filter by expression, and an optional streamViewId. 
- Note: This method, implemented for example purposes in ``SdsClient``, 
    does not include support for SdsBoundaryTypes. For more 
    information about SdsBoundaryTypes and how to implement them with 
    sampling, refer to the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)

Here is how it is called:

```js
this.sdsService.getSampledValues(streamId, 0, 40, 4, "sin")
```

Update Events and Replacing Values
----------------------------------

<h5>Updating Events</h5>

When updating single or multiple events, the payload has to be an array of event objects. 
Updating events is handled by the following PUT request. The request body has the new 
event that will update an existing event at the same index:


```js
updateValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
}
```

This is called as follows:
```js
const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 2.5, 5));
    }
    this.sdsService.updateValues(streamId, list)
```

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

<h5>Replacing Events</h5>

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values.

```js
replaceValues(streamId: string, events: Array<any>) {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data?allowCreate=false`;
    return this.authHttp.put(url, JSON.stringify(events).toString());
}
```

This is called as follows:
```js
const list: Array<WaveData> = [];
    for (let i = 0; i < 40; i += 2) {
      list.push(this.newWaveDataEvent(i, 1.5, 10));
    }
    this.sdsService.replaceValues(streamId, list
```

Property Overrides
------------------

SDS has the ability to override certain aspects of an SDS Type at the SDS Stream level.  
Meaning we apply a change to a specific SDS Stream without changing the SDS Type or the
read behavior of any other SDS Streams based on that type.  

In the sample, the InterpolationMode is overridden to a value of Discrete for the property Radians. 
Now if a requested index does not correspond to a real value in the stream then ``null``, 
or the default value for the data type, is returned by the SDS Service. 
The following shows how this is done in the code:

```js
const propertyOverride = new SdsStreamPropertyOverride();
propertyOverride.SdsTypePropertyId = "Radians";
propertyOverride.InterpolationMode = SdsStreamMode.Discrete;
this.stream.PropertyOverrides = [propertyOverride];
this.sdsService.updateStream(this.stream)
```

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

```js
this.sdsService.getRangeValues(streamId, '3', 5, SdsBoundaryType.ExactOrCalculated, autoStreamViewId)
```

To map a property that is beyond the ability of SDS to map on its own, 
you should define an SdsStreamViewProperty and add it to the SdsStreamView’s Properties collection.

```js
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
```

SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS.

```js
getStreamViewMap(streamViewId: string): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/StreamViews/${streamViewId}/Map`;
    return this.authHttp.get(url);
}
```

Delete Values from a Stream
---------------------------

There are two methods in the sample that illustrate removing values from
a stream of data. The first method deletes only a single value. The second method 
removes a window of values, much like retrieving a window of values.
Removing values depends on the value's key type ID value. If a match is
found within the stream, then that value will be removed. Code from both functions
is shown below:

```js
deleteValue(streamId: string, index): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data?index=${index}`;
    return this.authHttp.delete(url);
}

deleteWindowValues(streamId: string, start, end): Observable<any> {
    const url = this.sdsUrl +
    `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
    `/Data?startIndex=${start}&endIndex=${end}`;
    return this.authHttp.delete(url);
}
```

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to start and end
are removed from the stream.

Cleanup: Deleting Types, Stream Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream views and types can be 
achieved by a DELETE REST call and passing the corresponding Id.

```js
deleteValue(streamId: string, index): Observable<any> {
    const url = this.sdsUrl + `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data?index=${index}`;
    return this.authHttp.delete(url);
}
```

```js
deleteWindowValues(streamId: string, start, end): Observable<any> {
    const url = this.sdsUrl +
    `/api/${this.apiVersion}/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}` +
    `/Data?startIndex=${start}&endIndex=${end}`;
    return this.authHttp.delete(url);
}
```


Test
------------------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSangJS)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

Note this samaple  sometimes fails in automation due to automation issues.  Testing manually, locally it is normally ok... 

 Automated test uses Node10.16.0 x64

For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OCS page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
