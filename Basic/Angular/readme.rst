AngularJS Samples: Building a Client to make REST API Calls to the Qi Service.
===============================================================================

This sample demonstrates how Qi REST APIs are invoked using AngularJS 1.0.
This sample is still an ASP.Net Web Application so you will use have to 
use Visual Studio to run this application.

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
Directory instance. This sample uses ADAL to authenticate client against
the QI server. Generally, user will need to contact OSISoft dev support
to get their tenant set up to use Qi. The sample code
includes several placeholder strings. You must replace these with the
authentication-related values you received from OSIsoft. The strings are
found in ``app.js``:

.. code:: javascript

		.constant('QI_SAMPLEWEBAPP_EXTERNAL_CLIENTID', 'PLACEHOLDER_REPLACE_WITH_CLIENTID')
		.constant('QI_SERVER_URL', 'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL')
		.constant('QI_SERVER_APPID', PLACEHOLDER_REPLACE_WITH_RESOURCE')


When you run the solution, please click the login button on the top right
to login using your Microsoft account which is setup to use Qi service.

Sample Workflow
------------------------------
Once user is logged in, user can click on the Qi Service tab on the top.
This page has five buttons to show the main functionality of Qi.
1) Create and Insert Button: Creates the namespace, then type, then stream and inserts
WaveData events in the stream.
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

