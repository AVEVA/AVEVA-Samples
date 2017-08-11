.NET Samples 
============

Building a Client with the Qi Client Libraries
----------------------------------------------

The sample described in this section makes use of the OSIsoft Qi Client Libraries. OSIsoft recommends you use these libraries when creating .NET applications. The OSIsoft Qi Client Libraries are available as NuGet packages 
from `OSIsoft <https://osisoft.pkgs.visualstudio.com/_packaging/qilibrariescore/nuget/v3/index.json/>`_.

The included packages used are as follows:

* OSIsoft.Data.Core
* OSIsoft.Contracts
* OSIsoft.Data.Http.Server
* OSIsoft.Http.Client
* OSIsoft.Http.Security

The libraries offer a framework of classes that make client development significantly easier.

The sections that follow describe each of the major sections of the sample and how they work.

Configure the Sample:
-----------------------

Included in the sample there is a configuration file called appsettings.json with placeholders 
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
tenant ID, client ID and client secret. These must replace the AppId and AppKey 
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

::

    {
		"Namespace": "ENTER YOUR NAMESPACE ID",
		"Tenant": "ENTER YOUR TENANT ID",
		"Address": "ENTER PROVIDED ADDRESS",
		"Resource": "ENTER RESOURCE",
		"AppId": "ENTER CLIENT APPLICATION ID",
		"AppKey": "ENTER CLIENT APPLICATION KEY"
	}
	
Configure constants for connecting and authentication
-----------------------------------------------------

The authentication values are provided to the ``OSIsoft.Http.Security.QiSecurityHandler``. 
The ``QiSecurityHandler`` is a ``DelegatingHandler`` that is attached to an ``HttpClient`` pipeline.

Set up Qi clients
-----------------

The client example works using two client interfaces: 

* ``IQiMetadataService`` for QiStream, QiType, and QiStreamBehavior metadata operations
* ``IQiDataService`` for reading and writing data

The following code block illustrates how to configure clients in the sample:

::

  var admin = QiService.GetAdministrationService(new Uri(address), tenant, 
  new QiSecurityHandler(resource, tenant, appId, appKey));
  var metadatService = QiService.GetMetadataService(new Uri(address), tenant, namespaceId, 
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

::

  QiType type = QiTypeBuilder.CreateQiType<WaveData>();
  When defining the type, specify the key as follows:
  public class WaveData 
  {
      [QiMember(IsKey = true)]
      public int Order { get; set; }

      public double Tau { get; set; }

      public double Radians { get; set; }

      . . .
  }
  
  
To create the QiType in Qi, use the metadata client as follows:

::

  QiType type = await metadataService.GetOrCreateTypeAsync(type);

Create a QiStream
------------------

An ordered series of events is stored in a QiStream. Stream creation involves creating 
a local QiStream instance, giving it an Id, assigning it a type, and submitting it to the Qi service.

:: 

  await metadataService.GetOrCreateStreamAsync(stream);

Insert Events into the Stream
-----------------------------

The QiClientLibraries sample includes examples of inserting single events, updating 
single events and inserting collections of events.

::

  await dataService.InsertValueAsync(stream.Id, wave);

Retrieve Events
---------------

Many methods permit retrieving events from Qi. This sample demonstrates a basic 
method called GetWindowValuesAsync. Getting a window of values involves specifying 
the stream and a start and end index.

::

  IEnumerable<WaveData> retrieved = 
     await dataService.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200");

Cleanup
-------

When the sample code completes, it deletes its stream, behavior, and type. Cleaning up becomes significant 
if you run the sample more than one time. The sample will encounter collisions when events are left in the stream.



