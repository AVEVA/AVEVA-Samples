AngularJS Samples: Building a Client to make REST API Calls to the Qi Service.
===============================================================================

This example demonstrates how Qi REST APIs are invoked using AngularJS 1.0.
The example is an ASP.Net Web Application; you must 
use Visual Studio to run this application.

Establish a Connection
----------------------

The sample uses the ``request-promise`` module to connect to a service
endpoint. Qi REST API calls are sent to the Qi service. The Qi REST API
maps HTTP methods to CRUD (Create, Read, Update, Delete) as in the following table:

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

The REST calls in this example are configured as follows:

.. code:: javascript

				var deferred = $q.defer();

                $http({
                    url: 'URL',
                    method: 'REST-METHOD',
                    data: JSON.stringify(qiStream).toString()
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;


-  URL - The service endpoint
-  REST-METHOD - Denotes the type of REST call
-  DATA - Object in the JSON format

Authenticating with Qi
------------------------------

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. This example uses ADAL (Active Directory Authentication Library ) 
to authenticate clients against
the QI server. Generally, users must contact OSIsoft support
to obtain a tenant to use Qi. 

The sample code
includes several placeholder strings. You must replace these strings with the
authentication-related values you received from OSIsoft. The strings are
found in ``app.js``:

.. code:: javascript

		.constant('QI_SAMPLEWEBAPP_EXTERNAL_CLIENTID', 'PLACEHOLDER_REPLACE_WITH_CLIENTID')
		.constant('QI_SERVER_URL', 'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL')
		.constant('QI_SERVER_APPID', 'PLACEHOLDER_REPLACE_WITH_RESOURCE')


When you run the example, click the login button at the top right of the screen
to log in using a Microsoft account that is configured to use the Qi service.


Sample Workflow
------------------------------

After you are logged in, click the Qi Service tab at the top of the screen.
The page displayed has five buttons that show the main functionality of Qi:

	1) Create and Insert Button: Creates the namespace, then the type, then the stream, then inserts WaveData events into the stream.
	2) Update Button: Updates the events 
	3) Retrieve Button: Gets all the events
	4) Add Behavior: Creates and adds the behavior to the streams
	5) Cleanup: Deletes the events, stream, behavior, type.

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

A type definition in Qi consists of one or more "Properties." Each
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
                    url : this.url+this.typesBase,
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
is create a local QiStream instance, give it an id, assign it a type,
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

    createStream: function(tenantId, nameSpaceId, qiStream){

                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams";
                $http({
                    url: myurl,
                    method: 'POST',
                    data: JSON.stringify(qiStream).toString()
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
    }

-  QiStream object is passed in json format

Create and Insert Events into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
emtpy and should have at least the key value of the Qi type for the
event. Events are passed in json format.

An event can be created using the following POST request:

.. code:: javascript

   insertValue: function (tenantId, nameSpaceId, qiStreamId, evt) {

            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId+ "/Data/InsertValue";
            $http({
                url: myurl,
                method: 'POST',
                data: JSON.stringify(evt).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
    }

-  qiStreamId is the stream Id
-  data is the event object in json format

Inserting multiple values is similar, but the payload has list of events
and the url for POST call varies:

.. code:: javascript

    //insert an array of events
        insertValues: function (tenantId, nameSpaceId, qiStreamId, events) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/InsertValues";
            $http({
                url: myurl,
                method: 'POST',
                data: JSON.stringify(events).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
    }

The Qi REST API provides many more types of data insertion calls beyond
those demonstrated in this application.

Retrieve Events
---------------

There are many methods in the Qi REST API allowing for the retrieval of
events from a stream. The retrieval methods take string type start and
end values; in our case, these the start and end ordinal indices
expressed as strings ("0" and "99", respectively). The index values must
capable of conversion to the type of the index assigned in the QiType.
Timestamp keys are expressed as ISO 8601 format strings. Compound
indices are values concatenated with a pipe ('\|') separator. This
sample implements only two of the many available retrieval methods -
GetWindowValues (getTemplate in ``QiClient.js``) and GetRangeValues
(``getRangeTemplate`` in ``QiClient.js``).

.. code:: javascript

    getWindowValues: function (tenantId, nameSpaceId, qiStreamId, start, end) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/GetWindowValues?startIndex="
                + start + "&endIndex=" + end;
            $http({
                url: myurl,
                method: 'GET'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

-  parameters are the QiStream Id and the starting and ending index
   values for the desired window Ex: For a time index, request url
   format will be
   "/{streamId}/Data/GetWindowValues?startIndex={startTime}&endIndex={endTime}

Update Events
-------------

Updating events is handled by PUT REST call as follows:

.. code:: javascript

     updateValue: function (tenantId, nameSpaceId, qiStreamId, evt) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/UpdateValue";
            $http({
                url: myurl,
                method: 'PUT',
                data: JSON.stringify(evt).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

-  the request body has the new event that will update an existing event
   at the same index

Updating multiple events is similar, but the payload has an array of
event objects and url for PUT is slightly different:

.. code:: javascript

      //update an array of events
        updateValues: function (tenantId, nameSpaceId, qiStreamId, events) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/UpdateValues";
            $http({
                url: myurl,
                method: 'PUT',
                data: JSON.stringify(events).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

QiStreamBehaviors
-----------------

With certain data retrieval calls, a QiBoundarytype may be specified.
For example, if GetRangeValues is called with an ExactOrCalculated
boundary type, an event at the request start index will be calculated
using linear interpolation (default) or based on the QiStreamBehavior
associated with the QiStream. Because our sample QiStream was created
without any QiStreamBehavior associated, it should display the default
linear interpolation.

The first event returned by the following call will be at index 1 (start
index) and calculated via linear interpolation:

.. code:: javascript

      QiClient.getRangeValues(stream, 1, 0, 3, False, qiObjs.qiBoundaryType.ExactOrCalculated);

To observe how QiStreamBehaviors can change the query results, we will
define a new stream behavior object and submit it to the Qi service::

.. code:: javascript

        var behavior = new qiObjs.QiBehavior({"Mode":qiObjs.qiStreamMode.Continuous});
        behavior.Id = "evtStreamStepLeading";
        behavior.Mode = qiObjs.qiStreamMode.StepWiseContinuousLeading;
        ...
        QiClient.createBehavior(behavior);

By setting the ``Mode`` property to ``StepwiseContinuousLeading`` we
ensure that any calculated event will have an interpolated index, but
every other property will have the value of the previous event. Now
attach this behavior to the existing stream by setting the
``BehaviorId`` property of the stream and updating the stream definition
in the Qi service:

.. code:: javascript

        stream.BehaviorId = behavior.Id;
        ...
        QiClient.updateStream(stream);

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

    removeValue: function (tenantId, nameSpaceId, qiStreamId, index) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/RemoveValue?index=" + index;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

-  parameters are the stream Id and the index at which to delete an
   event Ex: For a time index, the request url will have the format:
   "/{streamId}/Data/RemoveValue?index={deletionTime}";

Delete can also be performed over a window of key value as follows:

.. code:: javascript

     removeWindowValues: function (tenantId, nameSpaceId, qiStreamId, start, end) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/RemoveWindowValues?startIndex="
                + start + "&endIndex=" + end;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

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

     deleteStream: function (tenantId, nameSpaceId, streamId) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + streamId;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        }

.. code:: javascript

    deleteType: function (tenantId, nameSpaceId, typeId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/" + typeId;
                $http({
                    url: myurl,
                    method: 'DELETE',
                    data: { Id: typeId }
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
        }




