SDS JavaScript Example using NodeJS
===================================

Building a Client to make REST API Calls to the SDS Service.
----------------------------------------------------------

This sample demonstrates how SDS REST APIs are invoked using JavaScript.
By examining the code, you will see how to establish a connection to SDS, 
obtain an authorization token, obtain an SdsNamespace, create an SdsType 
and SdsStream, and how to create, read, update, and delete values in SDS.
It has following dependencies: \* node.js, installation instructions are
available at `node.js <https://nodejs.org/en/>`__ \* Request-Promise,
HTTP client Request with Promises/A+ compliance.
`request-promise <https://www.npmjs.com/package/request-promise>`__

Sample Setup
------------

1. Make a local copy of the git repo
2. Install node.js
3. Install rquest and request-promise, using the following command. Add a ``-g``
   option to make the module available globally, install in the same
   folder as the other js files:

```
npm install request
npm install request-promise
```

4. Open Command Prompt in Windows
5. Goto folder where js files are located
6. Type the following command to run the test file in the local server

```
node Sample.js
```

7. Now open a browser client and enter the following URL to trigger the
   SDS operations ``http://localhost:8080/``
8. Check the console for the updates

Establish a Connection
----------------------

The sample uses ``request-promise`` module to connect a service
endpoint. Each REST API call consists of an HTTP request along with a specific URL and
HTTP method. The URL contains the server name plus the extension
that is specific to the call. Like all REST APIs, the SDS REST API maps
HTTP methods to CRUD operations as shown in the following table:

HTTP Method |CRUD Operation|Content Found In
-------|-----------|---------
POST          | Create           | message body       
GET           | Retrieve         | URL parameters     
PUT           | Update           | message body       
DELETE        | Delete           | URL parameters     

The REST calls in this sample are set up as follows:

```js
var restCall = require("request-promise")
restCall({
    url: authItems["authority"],
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    form: {
        'grant_type': 'client_credentials',
        'client_id': authItems['clientId'],
        'client_secret': authItems['clientSecret'],
        'resource': authItems['resource']
    }
});
```

-  URL - The service endpoint
-  REST-METHOD - Denotes the type of REST call
-  TOKEN - Authentication token obtained from Azure Oauth2 (explained
   below)
-  CLIENT-ID & CLIENT-KEY - Client credentials provided by service
   provider
-  RESOURCE-URL - Resource string for token acquisition

``Request-Promise`` is used in the current sample in order to execute
the REST calls in sequence. It is not mandatory. In fact, the same
syntax can be used with ``request`` module. It adds the Bluebird-powered
``.then(...)`` method to ``request`` call objects. This can be used to
achieve an ``await()`` effect. It supports all the features as that of
the ``request`` library, except that callbacks are replaced with
promises.

Configure the Sample:
-----------------------

Included in the sample there is a configuration file with placeholders 
that need to be replaced with the proper values. They include information 
for authentication, connecting to the SDS Service, and pointing to a namespace.

The SDS Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide a 
application ID and secret that are authenticated against the directory. These 
are referred to as client IDs and a client secrets, which are associated with 
a given tenant. They are created through the tenant's administration portal. 
The steps necessary to create a new client ID and secret are described below.

First, log on to the `Cloud Portal <http://cloud.osisoft.com>`__ with admin 
credentials and navigate to the ``Client Keys`` page under the ``Manage`` tab,
which is situated along the top of the webpage. Two types of keys may be created. 
For a complete explanation of key roles look at the help bar on the right side of 
the page. This sample program covers data creation, deletion and retrieval, so an 
administration key must be used in the configuration file. Creating a new key is 
simple. Enter a name for the key, select ``Administrator role``, then click ``Add Key``.

Next, view the key by clicking the small eye icon on the right of the created key, 
located in the list of available keys. A pop-up will appear with the tenant ID, client 
ID and client secret. These must replace the corresponding  values in the sample's 
configuration file. 

Along with client ID and secret values, add the tenant name to the authority value 
so authentication occurs against the correct tenant. The URL for the SDS Service 
connection must also be changed to reflect the destination address of the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create a 
namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` page. 
At the top the add button will create a new namespace after the required forms are 
completed. This namespace is now associated with the logged-in tenant and may be 
used in the sample.

The values to be replaced are in ``config.js``:

```js
authItems : {'resource' : "https://sdshomeprod.onmicrosoft.com/ocsapi",
                    'authority' : "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token",
                    'clientId' : "PLACEHOLDER_REPLACE_WITH_APPLICATION_IDENTIFIER",
                    'clientSecret' : "PLACEHOLDER_REPLACE_WITH_APPLICATION_SECRET"}
sdsServerUrl : "PLACEHOLDER_REPLACE_WITH_SDS_SERVER_URL",
tenantId: "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
namespaceId: "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
apiVersion: "v1-preview"
```

Obtain an Authentication Token
------------------------------

This javascript example uses raw OAuth 2 calls to obtain an
authentication token. Microsoft also provides a Azure Active Directory
Authentication Library for javascript that can be used with angular.js,
which handles the specifics of token acquisition, caching, and refresh.

During initialization, ``SdsClient`` sets the SdsServerUrl. Then, the
first step is to get an authentication token by calling,

```js
this.getToken(authItems)
```

The token received from ``getToken`` is included in the headers of each
SDS REST API request:

```js
this.getHeaders = function(){
                        return {
                                    "Authorization" : "bearer "+ this.token,
                                    "Content-type": "application/json", 
                                    "Accept": "*/*; q=1"
                                }
```

Note that the value of the ``Authorization`` header is the word
"bearer", followed by a space, and followed by the token string.

Authentication tokens have an expiration time which can be checked via
the ``token_expires`` property. The sample code handles checking the
token expiration and refreshing it as needed. As mentioned above,
Microsoft also provides an authentication library compatible with
angular.js that handles token caching and refresh transparently.

```js
if (client.tokenExpires < nowSeconds) {
            return checkTokenExpired(client)
            .then(
                function (res) {
                    refreshToken(res, client);
                    return client.createType(tenantId, sampleNamespaceId, sampleType);
                })
            .catch(function (err) { logError(err); });
```

Note: The ``checkTokenExpired`` method returns a request-promise object, which
can have a ``.then()`` and a ``.catch()`` method associated with it. The
``.then()`` method is executed when the request-promise is resolved (or
successful) and ``.catch()`` is executed if an exception or error is
thrown. This sample follows a pattern of placing REST calls in the
``.then()`` method after token acquisition (or other dependent REST
calls):

```js
var getClientToken = client.getToken(authItems)
    .catch(function (err) { throw err });
var createType = getClientToken.then(...<SDS REST call to create a type>...)
```


In the above snippet, the type creation method is called only if token
acquisition was successful. This is not mandatory for interaction with
the SDS service - the type creation call could be attempted regardless of
token acquisition. A call to the SDS service with a missing or incorrect
token will return with an Unauthorized status code.

Create an SdsType
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want
to store in SdsStreams. SdsTypes are the model that define SdsStreams.
SdsTypes can define simple atomic types, such as integers, floats, or
strings, or they can define complex types by grouping other SdsTypes. For
more information about SdsTypes, refer to the `SDS
documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__.

In the sample code, the SdsType representing WaveData is defined in the 
Sample.js. WaveData contains properties of integer and double atomic types. 
The constructions begins by defining a base SdsType for each atomic type and then defining
Properties of those atomic types.

```js
// define basic SdsTypes
var doubleType = new sdsObjs.SdsType({ "Id": "doubleType", "SdsTypeCode": sdsObjs.sdsTypeCode.Double });
var intType = new sdsObjs.SdsType({ "Id": "intType", "SdsTypeCode": sdsObjs.sdsTypeCode.Int32 });

// define properties
var orderProperty = new sdsObjs.SdsTypeProperty({ "Id": "Order", "SdsType": intType, "IsKey": true });
```

An SdsType can be created by a POST request as follows:

```js
restCall({
    url: this.url + this.typesBase.format([tenantId, namespaceId]) + "/" + type.Id,
    method: 'POST',
    headers: this.getHeaders(),
    body: JSON.stringify(type).toString()
});
```

-  Returns the SdsType object in a json format
-  If a type with the same Id exists, url path of the existing SDS type
   is returned
-  SdsType object is passed in json format

Create an SdsStream
-----------------

A SdsStream stores an ordered series of events. To create a
SdsStream instance, you simply provide an Id, assign it a type, and
submit it to the SDS service.  The value of the ``TypeId`` property is
the value of the SdsType ``Id`` property. The ``SdsStream`` object of SdsClient is
similar to ``SdsType``, except that it uses a different URL. Here is how
it is called from the main program:

```js
var sampleStream = new sdsObjs.SdsStream({
    "Id": sampleStreamId, 
"Name": "WaveStreamJs",
    "Description": "A Stream to store the WaveDatan Sds types events",
    "TypeId": sampleTypeId
    });
```

The local SdsStream can be created in the SDS service by a POST request as
follows:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" + stream.Id,
    method: 'POST',
    headers: this.getHeaders(),
    body: JSON.stringify(stream).toString()
});
```

-  SdsStream object is passed in json format

Create and Insert Values into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the SDS type for the
event. Events are passed in json format.

When inserting single or multiple values, the payload has to be a list of events.
An event can be created using the following POST request:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
        streamId + this.insertValuesBase,
    method: 'POST',
    headers: this.getHeaders(),
    body: JSON.stringify(events)
});
```

-  sdsStream.Id is the stream Id
-  body is the list of event objects in json format

First the event is created locally by populating a newWave event as follows:

```js
NextWave: function(interval, multiplier, order) {
        
        radians = order * Math.PI/32 +1;

        newWave = new this.WaveData();
        newWave.Order = order;
        newWave.Radians = radians;
        newWave.Tau = radians / (2 * Math.PI);
        newWave.Sin = multiplier * Math.sin(radians);
        newWave.Cos = multiplier * Math.cos(radians);
        newWave.Tan = multiplier * Math.tan(radians);
        newWave.Sinh = multiplier * Math.sinh(radians);
        newWave.Cosh = multiplier * Math.cosh(radians);
        newWave.Tanh = multiplier * Math.tanh(radians);

        return newWave;
    }
```

Then use the data service client to submit the event using the insertValues method:

```js
client.insertEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
```

Similarly, we can build a list of objects and insert them in bulk:

```js
    //variable initialization

    var buildEvents = function () {
        if (evtCount < totalEvents) {
            evt1 = waveDataObj.NextWave(200, mutliplier, evtCount);
            events.push(evt1);
            evtCount += 2;
            buildEvents();
        } else {
            callback();
        }
    };

    //wrapper for build events

    client.insertEvents(tenantId, sampleNamespaceId, sampleStreamId, events);
```


The SDS REST API provides many more types of data insertion calls beyond
those demonstrated in this application. Go to the 
`SDS documentation <https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html>`__ for more information
on available REST API calls.

Retrieve Values from a Stream
-----------------------------

There are many methods in the SDS REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these are the start and end ordinal indices
expressed as strings. The index values must
capable of conversion to the type of the index assigned in the SdsType.

This sample implements only a few of the many available retrieval methods.

<h5>Getting Window Values</h5>

Allows retrieval of events over a specific index range. Here is the request:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getWindowValuesBase.format([streamId, start, end]),
    method: 'GET',
    headers: this.getHeaders()
});
```

-  *start* and *end* (inclusive) represent the starting and ending indices for the
    retrieval. Additionally, the namespace ID and stream ID must
    be provided to the function call. A JSON object containing a list of the
    found values is returned. Ex: For a time index, request url
    format will be
    "/{streamId}/Data?startIndex={startTime}&endIndex={endTime}


Here is how it is called:

```js
client.getWindowValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 180);
```

<h5>Get Range Values</h5>

For retrieving a specified number of events from a starting index. 
This method in ``SdsClient`` allows retrieval of a range of values 
from a start index. The starting index is the ID of the ``SdsTypeProperty`` 
that corresponds to the key value of the WaveData type.
Following is the http request of getRangeValues:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getRangeValuesBase.format([streamId, start, skip, count, reverse, boundaryType, streamView]),
    method: 'GET',
    headers: this.getHeaders()
});
```

*skip* is the increment by which the retrieval will happen. *count* is
how many values you wish to have returned. *reverse* is a boolean that
when ``true`` causes the retrieval to work backwards from the starting
point. Finally, *boundary\_type* is a ``SdsBoundaryType`` value that
determines the behavior if the starting index cannot be found. Refer the
to the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)
for more information about SdsBoundaryTypes.

Here is how it is called:

```js
client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", sdsObjs.sdsBoundaryType.ExactOrCalculated);
```

<h5>Getting Table Form</h5>

You can retreive the values in the form of a table (in this case with headers).
Here is how to use it:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getWindowValuesBase.format([streamId, start, end,""]) +"&form=tableh",
    method: 'GET',
    headers: this.getHeaders()
});
```

-  *start* and *end* (inclusive) represent the starting and ending indices for the
    retrieval. Additionally, the namespace ID and stream ID must
    be provided to the function call. 

Here is how it is called:

```js
client.getWindowValuesTable(tenantId, sampleNamespaceId, sampleStreamId, 0, 180);
```

<h5>Getting Sampled Values</h5>

Sampling allows retrieval of a representative sample of data between a start and end 
index.  Sampling is driven by a specified property or properties of the 
stream's Sds Type. Property types that cannot be interpolated do not 
support sampling requests. Strings are an example of a property that 
cannot be interpolated. For more information see 
[Interpolation.](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/SDS_Types.html#interpolation) Here is how the http request is made:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getSamplesBase.format([streamId, start, end, intervals, sampleBy, filter, streamViewId]),
    method: 'GET',
    headers: this.getHeaders()
});
```
-  parameters are the SdsStream Id, the starting and ending index
   values for the desired window, the number of intervals to select 
   from, the property or properties to use when sampling, an 
   optional filter by expression, and an optional streamViewId. 
- Note: This method, implemented for example purposes in ``SdsClient``, 
    does not include support for SdsBoundryTypes. For more 
    information about SdsBoundaryTypes and how to implement them with 
    sampling, refer to the [SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)

Here is how it is called:

```js
client.getSampledValues(tenantId, sampleNamespaceId, sampleStreamId, 0, 40, 4, "sin");
```

Update Events and Replacing Values
----------------------------------
Values can be updated or replaced after they are inserted into a stream. The
distinction between updating and replacing operations is that updating inserts a
value if none exists previously, but replacing does not. The sample
demonstrates this behavior by first inserting ten values into the
stream, then updating and adding ten more values using the update
methods. Afterwards, it replaces all twenty values using the replace
methods.

When updating single or multiple events, the payload has to be an array of event objects. 
Updating events is handled by PUT REST call as follows:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
    streamId + this.updateValuesBase,
    method: 'PUT',
    headers: this.getHeaders(),
    body: JSON.stringify(events)
});
```
-  the request body has the new event that will update an existing event
   at the same index

If you attempt to update values that do not exist they will be created. The sample updates
the original ten values and then adds another ten values by updating with a
collection of twenty values.

In contrast to updating, replacing a value only considers existing
values and will not insert any new values into the stream. The sample
program demonstrates this by replacing all twenty values. The calling conventions are
identical to ``updateValues``:

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
    streamId + this.replaceValuesBase,
    method: 'PUT',
    headers: this.getHeaders(),
    body: JSON.stringify(events)
});
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
// Create a Discrete stream PropertyOverride indicating that we do not want SDS to calculate a value for Radians and update our stream 
var propertyOverride = new sdsObjs.SdsPropertyOverride({ "SdsTypePropertyId": "Radians", "InterpolationMode": sdsObjs.sdsStreamMode.Discrete });
var propertyOverrides = [propertyOverride]

// update the stream
sampleStream.PropertyOverrides = propertyOverrides;
return client.updateStream(tenantId, sampleNamespaceId, sampleStream);
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
client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, start, skip, count, reverse, sdsObjs.sdsBoundaryType.ExactOrCalculated, autoStreamView.Id)
```

To map a property that is beyond the ability of SDS to map on its own, 
you should define an SdsStreamViewProperty and add it to the SdsStreamView’s Properties collection.

```js
var sinStreamViewProperty = new sdsObjs.SdsStreamViewProperty({ "SourceId": "Sin", "TargetId": "SinInt" });
...
var manualStreamView = new sdsObjs.SdsStreamView({
    "Id": manualStreamViewId, 
    "Name": "MapSampleTypeToATargetType",     
    "TargetTypeId" : targetIntegerTypeId,
    "SourceTypeId" : sampleTypeId,
    "Properties" : [sinStreamViewProperty, cosStreamViewProperty, tanStreamViewProperty]
});
```
You can also use a streamview to change a Stream's type.

```js
client.updateStreamType(tenantId, namespaceId, streamId, streamViewId)
```


SdsStreamViewMap
---------

When an SdsStreamView is added, SDS defines a plan mapping. Plan details are retrieved as an SdsStreamViewMap. 
The SdsStreamViewMap provides a detailed Property-by-Property definition of the mapping.
The SdsStreamViewMap cannot be written, it can only be retrieved from SDS.

```js
var sdsStreamViewMap = client.getStreamViewMap(tenantId, sampleNamespaceId, manualStreamViewId);
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
    restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.removeSingleValueBase.format([streamId, index]),
    method: 'DELETE',
    headers: this.getHeaders()
});

restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.removeMultipleValuesBase.format([streamId, start, end]),
    method: 'DELETE',
    headers: this.getHeaders()
});
```

As when retrieving a window of values, removing a window is
inclusive; that is, both values corresponding to start and end
are removed from the stream.

Cleanup: Deleting Types, Stream Views and Streams
-----------------------------------------------------

In order for the program to run repeatedly without collisions, the sample
performs some cleanup before exiting. Deleting streams, stream views and types can 
be achieved by a DELETE REST call and passing the corresponding Id.

```js
restCall({
    url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" + streamId,
    method: 'DELETE',
    headers: this.getHeaders()
});
```

```js
restCall({
    url: this.url + this.typesBase.format([tenantId, namespaceId]) + "/" + typeId,
    method: 'DELETE',
    headers: this.getHeaders()
});
```

----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSnodeJS)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

--------



For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OCS page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)