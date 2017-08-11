Qi JavaScript Example using AngularJS
======================================

Building a client to make REST API calls to the Qi Service
----------------------------------------------------------

This example demonstrates how Qi REST APIs are invoked using Angular 4 and Typescript.

Prerequisites
-------------

You must have the following software installed on your computer:
 - Node.js and npm (Node package manager)
 - `Angular CLI <https://angular.io/guide/quickstart>`_
 - A modern browser (OSIsoft recommends Google Chrome or Mozilla Firefox)

 Configure the Sample
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
which is situated along the top of the webpage. Two types of keys may be 
created. For a complete explanation of key roles look at the help bar on the 
right side of the page. This sample program covers data creation, deletion and 
retrieval, so an administration key must be used in the configuration file. 
Creating a new key is simple. Enter a name for the key, select ``Administrator 
role``, then click ``Add Key``.

Next, view the key by clicking the small eye icon on the right of the created 
key, located in the list of available keys. A pop-up will appear with the 
tenant ID, client ID and client secret. These must replace the corresponding 
values in the sample's configuration file. 

Along with client ID and secret values, add the tenant name to the authority 
value so authenticaiton occurs against the correct tenant. The URL for the Qi 
Service conneciton must also be changed to reflect the destination address of 
the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create 
a namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` 
page. At the top the add button will create a new namespace after the required 
forms are completed. This namespace is now associated with the logged-in tenant 
and may be used in the sample.

The values to be replaced are in ``config.properties``:

.. code:: javascript
    _resource = https://pihomemain.onmicrosoft.com/historian
    _authority = https://login.windows.net/<PLACEHOLDER_REPLACE_WITH_TENANT_NAME>.onmicrosoft.com
    _clientId = PLACEHOLDER_REPLACE_WITH_CLIENT_ID
    _clientSecret = PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET
    _qiServerUrl = PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL
    _tenantId = PLACEHOLDER_REPLACE_WITH_TENANT_ID
    _namespaceId = PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID

Preparation
-----------

The Qi service is secured by obtaining tokens from an Azure Active
Directory instance. This example uses ADAL (Active Directory Authentication Library) 
to authenticate clients against the QI server. Contact OSIsoft support
to obtain a tenant for use with Qi.

Follow these steps to prepare your environment to run the example:

    1. Clone or download the example from the GitHub repository. If you download the ZIP file, extract the file to a directory on your computer.
    2. From a command prompt, go to the project directory and run ``npm install`` to download the necessary dependencies.
    3. Open the project in the IDE or text editor of your choice.
    4. Go to ``src/app/app.component.ts`` and fill in the ``config`` fields with the values provided by OSIsoft.
    5. To run the sample, open a command prompt and navigate to the project directory and run ``ng serve``. A browser window opens.
    6. In the browser, sign in to a Microsoft account that is configured to use the Qi service.

    If a browser window does not open, start a browser and go to ``localhost:4200``.

Running the example
------------------------------

This Angular app contains six buttons that demonstrate the main functionality of Qi:

	1) **Create Type**: Creates the WaveData type, which determines what kind of data can be written
    to a stream. It is defined by the WaveData class in datasrc.component.ts:

            .. code:: javascript

                    class  WaveData {
                        Order: number;
                        Radians: number;
                        Tau: number;
                        Sin: number;
                        Cos: number;
                        Tan: number;
                        Sinh: number;
                        Cosh: number;
                        Tanh: number
                    }

    2) **Create Stream**: Creates a stream that will contain the events that are written.
    3) **Insert Values**: Writes 100 events to the stream.
    4) **Retrieve Events**: Retrieves 50 events from the stream.
	5) **Create Behavior and Update Stream**: Creates and adds the behavior to the stream.
	6) **Cleanup**: Deletes the events, stream, stream behavior, and type.


To run the example, click each of the buttons in turn from top to bottom. It is recommended that you
open the developer tools in your browser so that you may watch the requests go to and return from Qi.

The rest of the sections in this document outline the operation of Qi and the underlying process and technology of the example.


How the example works
----------------------

The sample uses makes http requests to interact with Qi. Qi REST API calls are sent to the Qi service. The Qi REST API
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

This sample implements an http service that handles composing requests and authorization
in src/adal/authHttp.service.ts(the methods implemented here are then used in qi.rest.service.ts for calls specific to Qi).
For example, the service composes a POST request in the code below:

.. code:: javascript

				post(url: string, body: any, options?: RequestOptionsArgs): Observable<any> {
                    let headers = new Headers();
                    headers.append("Content-Type", 'application/json');
                    let options1 = new RequestOptions({ method: RequestMethod.Post, headers: headers });

                    if (body != null) {
                        options1.body = body;
                    }
                    options1 = options1.merge(options);
                    return this.sendRequest(url, options1);
                }


The ``authHttp`` service makes use of the rxjs module so that the calls to Qi can be made Observable. This allows the user
to handle responses to the REST calls and carry out other instructions that must be done after the calls have returned.
The various methods in ``datasrc.component.ts`` demonstrate the use of the ``qi.rest.service.ts`` calls and show how to encode and
decode the responses.


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

From qi.rest.service.ts:

.. code:: javascript

        export class QiType
        {
            Id:string;
            Name:string;
            Description:string;
            QiTypeCode:QiTypeCode;
            Properties:QiTypeProperty[];
        }

A QiType can be then be created by created by a POST request as follows:

.. code:: javascript

        createType(qiType:QiType):Observable<any> {
            let url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types`;
            return this.authHttp.post(url, JSON.stringify(qiType).toString());
        }

The BuildWaveDataType method in datasrc.component.ts demonstrates how to properly construct a QiType in the proper format.


Create a QiStream
-----------------

An ordered series of events is stored in a QiStream. 
To create a local QiStream instance, you provide an Id, assign a type,
and submit it to the Qi service. You may optionally assign a
QiStreamBehavior to the stream. The value of the ``TypeId`` property is
the value of the QiType ``Id`` property.

.. code:: javascript

        export class QiStream
            {
              Id:string;
              Name:string;
              Description:string;
              TypeId:string;
              BehaviorId:string;
            }

The local QiStream can be created in the Qi service by a POST request as
follows:

.. code:: javascript

    createStream(qiStream: QiStream): Observable<any> {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams`;
        return this.authHttp.post(url, JSON.stringify(qiStream).toString());
    }

Create and Insert Events into the Stream
----------------------------------------

A single event is a data point in the stream. An event object cannot be
empty and should have at least the key value of the Qi type for the
event. Events are passed in JSON format.

Events can be written using the following POST request:

.. code:: javascript

    insertValues(streamId: string, events: Array<any>) {
        let url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/InsertValues`;
        return this.authHttp.post(url, JSON.stringify(events).toString());
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
example implements only one of the many available retrieval methods - GetRangeValues.

.. code:: javascript

    getRangeValues(streamId: string, start, count, boundary: QiBoundaryType): Observable<any> {
        let url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}/Data/GetRangeValues?startIndex=${start}&count=${count}&boundaryType=${boundary}`;
        return this.authHttp.get(url);
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

The first event returned by the following call will be at index 3 (start
index) and calculated via linear interpolation:

.. code:: javascript

      retrieveWaveDataEvents() {
        this.hasEvents = false;
        this.qiService.getRangeValues(streamId, "3", 50, QiBoundaryType.ExactOrCalculated)
        .map(res => res.json())
        .subscribe(res => {
            this.events = res as WaveData[];
            this.hasEvents = true;
            this.button4Message = `Found ${this.events.length} events`
        });
      }

To see how QiStreamBehaviors can change the query results, the following example
defines a new stream behavior object and submits it to the Qi service. It then updates the
stream to use the newly created behavior:

.. code:: javascript

        createBehaviorAndUpdateStream() {
            let behavior = new QiStreamBehavior();
            behavior.Id = behaviorId;
            behavior.Name = "SampleBehavior";
            behavior.Mode = QiStreamMode.Discrete;
            this.qiService.createBehavior(behavior).subscribe(() => {
              this.stream.BehaviorId = behaviorId;
              this.qiService.updateStream(this.stream).subscribe(res => {
                this.button5Message = res.status;
              });
            })
        }

Setting the ``Mode`` property to ``Discrete``
ensures that only values that were explicitly written will be returned. We
attached this behavior to the existing stream by setting the
``BehaviorId`` property of the stream and updating the stream definition.

The sample suggests you repeat the call to ``GetRangeValues`` with the same
parameters as before, allowing you to compare the values of the event at
index 3 using different stream behaviors.


Cleanup: Deleting Types, Behaviors, and Streams
-----------------------------------------------

So that it can run repeatedly without name collisions, the example performs
some cleanup before exiting. Deleting streams, stream behaviors, and
types can be achieved by a DELETE REST call and passing the
corresponding Id. Note: types and behaviors cannot be deleted until any
streams referencing them are deleted first.

Note: An event at a particular index can be deleted by passing the index value
for that data point to a DELETE REST call. Rather than delete individual events,
though, the sample deletes the entire stream. Deleting a stream also deletes all of the
events that have been written to that stream. The various deletion calls for Qi can be
seen in the documentation.

.. code:: javascript

    deleteType(typeId: string): Observable<any> {
        let url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Types/${typeId}`;
        return this.authHttp.delete(url);
    }

.. code:: javascript

    deleteStream(streamId: string): Observable<any> {
        const url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Streams/${streamId}`;
        return this.authHttp.delete(url);
    }

.. code:: javascript

    deleteBehavior(behaviorId:string) {
        let url = this.qiUrl + `/api/Tenants/${this.tenantId}/Namespaces/${this.namespaceId}/Behaviors/${behaviorId}`;
        return this.authHttp.delete(url);
    }
 