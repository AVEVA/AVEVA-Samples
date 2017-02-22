.NET Samples
============

Building a Client with the Qi REST API
--------------------------------------

This sample demonstrates how to interact with Qi using the Qi REST API. The REST API 
is language independent. Objects are passed as JSON strings. The sample uses the Newtonsoft.Json 
JSON framework, however, any method of creating a JSON representation of objects will work.

HTTP Client
-----------

The sample relies on the System.Net.Http.HttpClient to send and receive REST. The 
System.Net.Http.HttpClientFactory Create method is used to attach a 
System.Net.Http.DelegatingHandler that retrieves and attaches the authorization token to every message.


Authorization Handler
---------------------

The Qi service is secured by Azure Active Directory. For a request to succeed, 
a valid token must be attached to every request sent to Qi. 

The sample includes a simple DelegatingHandler that relies on the 
Microsoft.IdentityModel.Clients.ActiveDirectory assembly to acquire the security token. 
The Authentication Handler accepts a resource, tenant, AAD instance format, 
client identifier and client secret. The handler supports an application identity.

Authentication-related values are received from OSIsoft. The values are provided to 
the sample in the App.Config configuration file as follows:

::

    <!--Configurations-->
    <add key="Namespace" value="Samples" />
    <add key="Tenant" value="PROVIDED_TENANT_ID" />
    <add key="Address" value="https://qi-data.osisoft.com" />

    <!--Credentials-->
    <add key="Resource" value="https://qihomeprod.onmicrosoft.com/historian" />
    <add key="AppId" value="PROVIDED_CLIENT_APPLICATION_ID" />
    <add key="AppKey" value="PROVIDED_CLIENT_APPLICATION_KEY" />


The Authorization context is attached to HttpClient using the 
System.Net.Http.HttpClientFactory Create extension method as follows:

::

  HttpClient client = HttpClientFactory.Create(new WebRequestHandler(),
      new AuthenticationHandler(resource, tenant, aadFormat, appId, appKey));
      
      
Note that Qi returns a status of 302 (Found), when metadata collisions exist. The HttpClient 
auto-redirect, which automatically issues a GET when receiving a 302, will result in an 
unauthorized response. Because HttpClient does not retain the authorization token on a redirect, 
it is recommended that auto redirect be disabled.

In the sample, redirection is managed by invoking GET before POST. POST is invoked only if 
the object is not found.

Create a QiType
---------------

To use Qi, you define QiTypes that describe the kinds of data you want to store in QiStreams. 
QiTypes are the model that define QiStreams.

QiTypes can define simple atomic types, such as integers, floats or strings, or they can 
define complex types by grouping other QiTypes. For more information aabout QiTypes, 
refer to the Qi Documentation.

When working with the Qi Client Libraries, it is strongly recommended that you use the 
QiTypeBuilder. QiTypeBuilder uses reflection to build QiTypes. The QiTypeBuilder exposes 
a number of methods for manipulating types. One of the simplest ways to create a type 
is to use one of its static methods:

::

  QiType type = QiTypeBuilder.CreateQiType<WaveData>();
  
  
When defining the type, specify the key as follows:

::

  public class WaveData
  {
      [QiMember(IsKey = true)]
      public int Order { get; set; }

      public double Tau { get; set; }

      public double Radians { get; set; }

      . . .
  }

Insert Events into the Stream
-----------------------------

The QiClientLibraries sample includes examples of inserting single events, 
updating single events and inserting collections of events.

Retrieve Events
----------------

Many methods permit retrieving events from Qi. This sample demonstrates 
a basic method, called GetWindowValuesAsync. Getting a window of values 
involves specifying the stream and a start and end index.

::

  HttpResponseMessage response =
      client.GetAsync(
              $"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/GetValues?startIndex={0}&endIndex={200}
	  &count={100}")
          .GetAwaiter()
          .GetResult();
  if (!response.IsSuccessStatusCode)
      throw new HttpResponseException(response);
  var retrievedEvents = 
      response.Content.ReadAsAsync<WaveData[]>().GetAwaiter().GetResult();

Index values must be expressed as ISO 8601 strings.

Cleanup
--------

When finished, the sample cleans up its stream, behavior and type. Cleanup becomes significant 
if you run the sample more than once. The sample will encounter collisions if events are left 
in the stream.
