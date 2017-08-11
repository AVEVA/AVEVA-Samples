JavaScript Samples: Building a Client to make REST API Calls to the Qi Service.
===============================================================================

This sample demonstrates how Qi REST APIs are invoked using JavaScript.
It has following dependencies: \* node.js, installation instructions are
available at `node.js <https://nodejs.org/en/>`__ \* Request-Promise,
HTTP client Request with Promises/A+ compliance.
`request-promise <https://www.npmjs.com/package/request-promise>`__

Sample Setup
------------

1. Make a local copy of the git repo
2. Install node.js
3. Install request-promise, using the following command. Add a ``-g``
   option to make the module available globally, install in the same
   folder as the other js files:

   .. code:: javascript

       npm install request-promise

4. Open Command Prompt in Windows
5. Goto folder where js files are located
6. Type the following command to run the test file in the local server

   .. code:: javascript

       node Sample.js

7. Now open a browser client and enter the following URL to trigger the
   Qi operations ``http://localhost:8080/``
8. Check the console for the updates

Establish a Connection
----------------------

The sample uses ``request-promise`` module to connect a service
endpoint. Qi REST API calls are sent to the Qi service. The Qi REST API
maps HTTP methods to CRUD like this:

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

The REST calls in this sample are set up as follows:

.. code:: javascript

        var restCall = require("request-promise")
        restCall({
                    url : 'URL',
                    method: 'REST-METHOD',
                    headers : {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                "Authorization" : "bearer "+ TOKEN,
                                "Content-type": "application/json", 
                                "Accept": "text/plain"
                    },
                    form : {    
                                'grant_type' : 'client_credentials',
                                'client_Id' : CLIENT-ID,
                                'client_secret' : CLIENT-KEY,
                                'resource' : RESOURCE-URL
                            }
                });

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
for authentication, connecting to the Qi Service, and pointing to a namespace.

The Qi Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide a 
application ID and secret that are authenticated against the directory. These 
are referred to as client IDs and a client secrets, which are associated with 
a given tenant. They are created through the tenant's administration portal. 
The steps necessary to create a new cient ID and secret are described below.

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
so authenticaiton occurs against the correct tenant. The URL for the Qi Service 
conneciton must also be changed to reflect the destination address of the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create a 
namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` page. 
At the top the add button will create a new namespace after the required forms are 
completed. This namespace is now associated with the logged-in tenant and may be 
used in the sample.

The values to be replaced are in ``config.js``:

.. code:: javascript

        authItems : {'resource' : "https://pihomemain.onmicrosoft.com/historian",
                         'authority' : "PLACEHOLDER_REPLACE_WITH_AUTHORITY", //Ex: "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token",
                         'clientId' : "PLACEHOLDER_REPLACE_WITH_USER_ID",
                         'clientSecret' : "PLACEHOLDER_REPLACE_WITH_USER_SECRET"}
        qiServerUrl : "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL",
		tenantId: "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
		namespaceId: "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID"

Obtain an Authentication Token
------------------------------

This javascript example uses raw OAuth 2 calls to obtain an
authentication token. Microsoft also provides a Azure Active Directory
Authentication Library for javascript that can be used with angular.js,
which handles the specifics of token acquisition, caching, and refresh.

During initialization, ``QiClient`` sets the QiServerUrl. Then, the
first step is to get an authentication token by calling,

.. code:: javascript

    this.getToken(authItems)

The token received from ``getToken`` is included in the headers of each
Qi REST API request:

.. code:: javascript

     this.getHeaders = function(){
                                return {
                                            "Authorization" : "bearer "+ this.token,
                                            "Content-type": "application/json", 
                                            "Accept": "text/plain"
                                        }

Note that the value of the ``Authorization`` header is the word
"bearer", followed by a space, and followed by the token string.

Authentication tokens have an expiration time which can be checked via
the ``token_expires`` property. The sample code handles checking the
token expiration and refreshing it as needed. As mentioned above,
Microsoft also provides an authentication library compatible with
angular.js that handles token caching and refresh transparently.

.. code:: javascript

    if (client.tokenExpires < nowSeconds) {
                return checkTokenExpired(client)
				.then(
                    function (res) {
                        refreshToken(res, client);
                        return client.createType(tenantId, sampleNamespaceId, sampleType);
                    })
				.catch(function (err) { logError(err); });

Note: The ``checkTokenExpired`` method returns a request-promise object, which
can have a ``.then()`` and a ``.catch()`` method associated with it. The
``.then()`` method is executed when the request-promise is resolved (or
successful) and ``.catch()`` is executed if an exception or error is
thrown. This sample follows a pattern of placing REST calls in the
``.then()`` method after token acquisition (or other dependent REST
calls):

.. code:: javascript

    var getTokenSuccess = client.getToken(authItems)
                                        .catch(function(err){logError(err)});
    var createTypeSuccess = getTokenSuccess.then(...<Qi REST call to create a type>...)

In the above snippet, the type creation method is called only if token
acquisition was successful. This is not mandatory for interaction with
the Qi service - the type creation call could be attempted regardless of
token acquisition. A call to the Qi service with a missing or incorrect
token will return with an Unauthorized status code.

Create a QiType
---------------

QiStreams represent open-ended collections of strongly-typed, ordered
events. Qi is capable of storing any data type you care to define. The
only requirement is that the data type must have one or more properties
that constitute an ordered key. While a timestamp is a very common type
of key, any ordered value is permitted. Our sample type uses an integer.

Each data stream is associated with a QiType, so that only events
conforming to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

A QiType has the following properties: Id, Name, Description,
QiTypeCode, and Properties.

The type "Id" is the identifier for a particular type. "Name" and
"Description" are optional string properties to describe the type.
"QiTypeCode" is used to identify the datatypes stored by the QiType. The
file *QiObjects.js* enumerates the available datatypes the
qiTypeCodeMap.

A type definition in Qi consists of one or more "Properties". Each
property has its own type. This can be a simple data type like integer
or string, or a previously defined complex QiType. This allows for the
creation of nested data types - QiTypes whose properties may be
user-defined types.

From QiObjects.js:

.. code:: javascript

       QiType : function (qiType){
            if(qiType.Id){
                this.Id = qiType.Id
            }
            if(qiType.Name){
                this.Name = qiType.Name;
            }
            if(qiType.Description){
                this.Description = qiType.Description;
            }
            if(qiType.QiTypeCode){ 
                this.QiTypeCode = qiType.QiTypeCode;
            }
            if(qiType.Properties){
                this.Properties = qiType.Properties;
            }
        }

A QiType can be created by a POST request as follows:

.. code:: javascript

        restCall({
                    url : this.url+this.typesBase.format([tenantId, namespaceId]),
                    method: 'POST',
                    headers : this.getHeaders(),
                    body : JSON.stringify(wave).toString()
                });

-  Returns the QiType object in a json format
-  If a type with the same Id exists, url path of the existing Qi type
   is returned
-  QiType object is passed in json format

Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. All you have to do
is create a local QiStream instance, give it an Id, assign it a type,
and submit it to the Qi service. You may optionally assign a
QiStreamBehavior to the stream. The value of the ``TypeId`` property is
the value of the QiType ``Id`` property.

.. code:: javascript

       QiStream : function(qiStream){
            this.Id = qiStream.Id;
            this.Name = qiStream.Name;
            this.Description = qiStream.Description;
            this.TypeId = qiStream.TypeId;
            if(qiStream.BehaviorId){
                this.BehaviorId = qiStream.BehaviorId;
            }
        }

The local QiStream can be created in the Qi service by a POST request as
follows:

.. code:: javascript

    restCall({
            url : this.url+this.streamsBase.format([tenantId, namespaceId]),
            method : 'POST',
            headers : this.getHeaders(),
            body : JSON.stringify(qiStream).toString()
        });

-  QiStream object is passed in json format

Create and Insert Events into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
emtpy and should have at least the key value of the Qi type for the
event. Events are passed in json format.

An event can be created using the following POST request:

.. code:: javascript

    restCall({
                url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+
                        qiStream.Id+this.insertSingleValueBase,
                method : 'POST',
                headers : this.getHeaders(),
                body : JSON.stringify(evt)
            });

-  qiStream.Id is the stream Id
-  body is the event object in json format

Inserting multiple values is similar, but the payload has list of events
and the url for POST call varies:

.. code:: javascript

    restCall({
                url : this.url+this.streamsBase+"/"+
                        qiStream.Id+this.insertMultipleValuesBase,
                method : 'POST',
                headers : this.getHeaders(),
                body : JSON.stringify(events)
            });

The Qi REST API provides many more types of data insertion calls beyond
those demonstrated in this application. Go to the 
`Qi documentation<https://cloud.osisoft.com/documentation>`_ for more information
on available REST API calls.

Retrieve Values
---------------

There are many methods in the Qi REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these the start and end ordinal indices
expressed as strings ("0" and "198", respectively). The index values must
capable of conversion to the type of the index assigned in the QiType.
Timestamp keys are expressed as ISO 8601 format strings. Compound
indices are values concatenated with a pipe ('\|') separator. This
sample implements only two of the many available retrieval methods -
getWindowValues (getTemplate in ``QiClient.js``) and getRangeValues
(``getRangeTemplate`` in ``QiClient.js``).

.. code:: javascript

    restCall({
            url : this.url+this.streamsBase+this.getSingleValueBase.format([qiStream.Id,start,end]),
            method : 'GET',
            headers : this.getHeaders()
        });

-  parameters are the QiStream Id and the starting and ending index
   values for the desired window Ex: For a time index, request url
   format will be
   "/{streamId}/Data/GetWindowValues?startIndex={startTime}&endIndex={endTime}

Update Events
-------------

Updating events is handled by PUT REST call as follows:

.. code:: javascript

     restCall({
                url : this.url+this.streamsBase+"/"+
                        qiStream.Id+this.updateSingleValueBase,
                method : 'PUT',
                headers : this.getHeaders(),
                body : JSON.stringify(evt)
            });

-  the request body has the new event that will update an existing event
   at the same index

Updating multiple events is similar, but the payload has an array of
event objects and url for PUT is slightly different:

.. code:: javascript

     restCall({
                url : this.url+this.streamsBase+"/"+
                        qiStream.Id+this.updateMultipleValuesBase,
                method : 'PUT',
                headers : this.getHeaders(),
                body : JSON.stringify(events)
            });

QiStreamBehaviors
-----------------

With certain data retrieval calls, a QiBoundarytype may be specified.
For example, if getRangeValues is called with an ExactOrCalculated
boundary type, an event at the request start index will be calculated
using linear interpolation (default) or based on the QiStreamBehavior
associated with the QiStream. Because our sample QiStream was created
without any QiStreamBehavior associated, it should display the default
linear interpolation.

The first event returned by the following call will be at index 1 (start
index) and calculated via linear interpolation:

.. code:: javascript

      client.getRangeValues(tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, "False", qiObjs.qiBoundaryType.ExactOrCalculated)

To observe how QiStreamBehaviors can change the query results, we will
define a new stream behavior object and submit it to the Qi service::

.. code:: javascript

        var behavior = new qiObjs.QiBehavior({"Mode": qiObjs.qiStreamMode.StepWiseContinuousLeading;});
        behavior.Id = "evtStreamStepLeading";
		sampleBehavior.ExtrapolationMode = qiObjs.qiBoundaryType.Continuous;
        ...
        client.createBehavior(behavior);

By setting the ``Mode`` property to ``StepwiseContinuousLeading`` we
ensure that any calculated event will have an interpolated index, but
every other property will have the value of the previous event. Setting
the extrapolation mode defines how the stream responds to requests for
and index that proceeds or follows all of the data in the stream. Finally,
attach this behavior to the existing stream by setting the
``BehaviorId`` property of the stream and updating the stream definition
in the Qi service:

.. code:: javascript

        stream.BehaviorId = behavior.Id;
        ...
        client.updateStream(stream);

The sample repeats the call to ``GetRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
index 1 using different stream behaviors.

Delete Events
-------------

An event at a particular index can be deleted by passing the index value
for that data point to following DELETE REST call. The index values are
expressed as string representations of the underlying type. DateTime
index values must be expressed as ISO 8601 strings.

.. code:: javascript

    restCall({
                url : this.url+this.streamsBase+this.removeSingleValueBase.format([qiStream.Id, index]),
                method : 'DELETE',
                headers : this.getHeaders()
            });

-  parameters are the stream Id and the index at which to delete an
   event Ex: For a time index, the request url will have the format:
   "/{streamId}/Data/RemoveValue?index={deletionTime}";

Delete can also be performed over a window of key value as follows:

.. code:: javascript

     restCall({
                url : this.url+this.streamsBase+this.removeMultipleValuesBase.format([qiStream.Id, start, end]),
                method : 'DELETE',
                headers : this.getHeaders()
            });

-  parameters are the stream Id and the starting and ending index values
   of the window Ex: For a time index, the request url will have the
   format:
   /{streamId}/Data/RemoveWindowValues?startIndex={startTime}&endIndex={endTime}

Cleanup: Deleting Types, Behaviors, and Streams
-----------------------------------------------

So that it can run repeatedly without name collisions, the sample does
some cleanup before exiting. Deleting streams, stream behaviors, and
types can be achieved by a DELETE REST call and passing the
corresponding Id. Note: types and behaviors cannot be deleted until any
streams referencing them are deleted first.

.. code:: javascript

     restCall({
            url : this.url+this.streamsBase+"/"+streamId,
            method : 'DELETE',
            headers : this.getHeaders()
        });

.. code:: javascript

    restCall({
                url : this.url+this.typesBase+"/"+typeId,
                method : 'DELETE',
                headers : this.getHeaders()
            });
