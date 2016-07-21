Qi JavaScript Example using AngularJS
======================================

Building a client to make REST API calls to the Qi Service
----------------------------------------------------------

This example demonstrates how Qi REST APIs are invoked using AngularJS 1.0.
Because the example is an ASP.Net Web Application, you must 
use Visual Studio to run it.

Prerequisites
-------------

You must have the following software installed on your computer:
 - AngularJS version 1 (available on GitHub)
 - Microsoft Visual Studio 2015
 - A browser (such as Microsoft Internet Explorer)


Preparation
-----------

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. This example uses ADAL (Active Directory Authentication Library) 
to authenticate clients against the QI server. Contact OSIsoft support
to obtain a tenant for use with Qi. 

The sample code includes several placeholder strings that must be modified 
with values you received from OSIsoft. 

Follow these steps to prepare your environment to run the example:

 1. Clone or download the example from the GitHub repository. If you download the ZIP file, extract the file to a directory on your computer.
 2. Start Visual Studio and select **File > Open > Project/Solution**.
 3. Navigate to the directory in which the example was downloaded, select the file: ``qiSampleApp.sln`` and then click **Open**.
 4. In Visual Studio, use the Solution Explorer window to find and select the file: ``app.js``.
 5. Modify the following values within ``app.js`` using the values that were provided by OSIsoft:
 
 .. code:: javascript
 
  .constant('QI_SERVER_URL', 'QI_URL')
  .constant('QI_SERVER_APPID', 'QI_APP_ID_URL')
  .constant('QI_SAMPLEWEBAPP_EXTERNAL_CLIENTID', 'PLACEHOLDER_REPLACE_WITH_CLIENTID')
  .constant('QI_SERVER_URL', 'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL')
  .constant('QI_SERVER_APPID', 'PLACEHOLDER_REPLACE_WITH_RESOURCE')

 6. In Visual Studio, run the example by clicking **Start**.
 7. Click the **Login** button in the top-right corner of the screen and log in using a Microsoft account that is configured to use the Qi service.
 8. After you are logged in, click the **Qi Service** tab at the top of the screen.
 

Running the example
------------------------------

The Qi Services page contains five buttons that demonstrate the main functionality of Qi:

	1) **Create and Insert**: Creates the namespace, then the type, then the stream, then inserts WaveData events into the stream.
	2) **Update**: Updates the events 
	3) **Retrieve**: Gets all the events
	4) **Add Behavior**: Creates and adds the behavior to the streams
	5) **leanup**: Deletes the events, stream, behavior, and type type.

To run the example, click each of the buttons in turn from top to bottom. In most modern browsers, you can view the API calls and results as they occur by pressing **F12**. 

Messages to look for:

  After clicking ``Create and Insert``, look for the following messages:

::  

    Creating Namespace
    Namespace found
    Creating Type...
    Type created
    Creating stream...
    Inserting values...


  After clicking ``Retrieve Events`` button, look for:

::

    All events removed
    Deleting stream...
    Stream Deleted
    Behavior Deleted
    Deleting Type...
    Type Deleted


  After clicking the ``Retrieve Events``, look for:

::

    All events removed
    Deleting stream...
    Stream Deleted
    Behavior Deleted
    Deleting Type...
    Type Deleted


  
  After clicking ``Add Behavior``, look for:

::

    All events removed
    Deleting stream...
    Stream Deleted
    Behavior Deleted
    Deleting Type...
    Type Deleted
    

  After clicking ``Range Events``, look for:

::

    All events removed
    Deleting stream...
    Stream Deleted
    Behavior Deleted
    Deleting Type...
    Type Deleted


  After clicking Create and Insert button, look for:

::

    All events removed
    Deleting stream...
    Stream Deleted
    Behavior Deleted
    Deleting Type...
    Type Deleted
    
    

The rest of the sections in this document outline the operation of Qi and the underlying process and technology of the example.


How the example works
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


Create a QiType
---------------

QiStreams represent open-ended collections of strongly-typed, ordered
events. Qi is capable of storing any data type you care to define. The
only requirement is that the data type must have one or more properties
that constitute an ordered key. While a timestamp is a very common type
of key, any ordered value is permitted. This example uses an integer type.

Each data stream is associated with a QiType, so that only events
conforming to that type can be inserted into the stream. The first step
in Qi programming, then, is to define the types for your tenant.

A QiType has the following properties: 

- Id
- Name
- Description
- QiTypeCode
- Properties.

The ``Id`` property is the identifier for a particular type. ``Name`` and
``Description`` are optional string properties that describe the type.
``QiTypeCode`` is used to identify the datatypes that are stored by the QiType. The
file *QiObjects.js* enumerates the available datatypes in the
qiTypeCodeMap.

A type definition in Qi consists of one or more *Properties*. Each
property has its own type. The type can be a simple data type such as integer
or string, or a previously defined complex QiType, which allows the
creation of nested data types; that is, QiTypes whose properties may be
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

-  Returns the QiType object in JSON format
-  If a type with the same Id apready exists, the URL path of the existing Qi type
   is returned.
-  The QiType object is passed in JSON format.


Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. 
To create a local QiStream instance, you provide an ID, assign a type,
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
event. Events are passed in JSON format.

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

Inserting multiple values is similar, but the payload has a list of events
and the URL for the POST call varies:

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

There are many methods in the Qi REST API that allow for the retrieval of
events from a stream. The retrieval methods take string-type start and
end values; in our case, these start and end ordinal indices
are expressed as strings ("0" and "99", respectively). The index values must
be capable of conversion to the type of the index assigned in the QiType.
Timestamp keys are expressed as ISO 8601 format strings. Compound
indices are values concatenated with a pipe ('\|') separator. This
example implements only two of the many available retrieval methods -
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
   values for the desired window Ex: For a time index, request URL
   format will be:
   
   ``"/{streamId}/Data/GetWindowValues?startIndex={startTime}&endIndex={endTime}``

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
   at the same index.

Updating multiple events is similar, but the payload contains an array of
event objects and the URL for PUT is slightly different:

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
For example, if ``GetRangeValues`` is called with an ExactOrCalculated
boundary type, an event at the request start index will be calculated
using linear interpolation (default) or based on the QiStreamBehavior
associated with the QiStream. Because our sample QiStream was created
without any QiStreamBehavior associated, it should display the default
linear interpolation.

The first event returned by the following call will be at index 1 (start
index) and calculated via linear interpolation:

.. code:: javascript

      QiClient.getRangeValues(stream, 1, 0, 3, False, qiObjs.qiBoundaryType.ExactOrCalculated);

To see how QiStreamBehaviors can change the query results, the following example
defines a new stream behavior object and submits it to the Qi service:

.. code:: javascript

        var behavior = new qiObjs.QiBehavior({"Mode":qiObjs.qiStreamMode.Continuous});
        behavior.Id = "evtStreamStepLeading";
        behavior.Mode = qiObjs.qiStreamMode.StepWiseContinuousLeading;
        ...
        QiClient.createBehavior(behavior);

Setting the ``Mode`` property to ``StepwiseContinuousLeading`` 
ensures that any calculated event has an interpolated index, but
every other property has the value of the previous event. Now
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
   
   ``"/{streamId}/Data/RemoveValue?index={deletionTime}";``

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

-  Parameters are the stream Id and the starting and ending index values
   of the window. Example: For a time index, the request URL will have the following
   format:
   
   ``/{streamId}/Data/RemoveWindowValues?startIndex={startTime}&endIndex={endTime}``

Cleanup: Deleting Types, Behaviors, and Streams
-----------------------------------------------

So that it can run repeatedly without name collisions, the examples performs
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




