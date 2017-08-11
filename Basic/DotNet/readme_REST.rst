.NET Samples
============

Building a Client with the Qi REST API
--------------------------------------

This sample demonstrates how to interact with Qi using the Qi REST API. The REST API 
is language independent. Objects are passed as JSON strings. The sample uses the Newtonsoft.Json 
JSON framework, however, any method of creating a JSON representation of objects will work.

HTTP Client
-----------

The sample relies on the System.Net.Http.HttpClient with a HttpClientHandler to send and receive REST.


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
define complex types by grouping other QiTypes. For more information about QiTypes, 
refer to the Qi Documentation.

::
  
The sample mimics some of the functionality of the Qi Client Libraries by defining its own QiClient
and its own classes to represent QiTypes, QiStreams, QiStreamBehaviors, etc. When making rest calls to create them, instances of
these classes are converted to a JSON string and sent as the content of an HTTP request. For example, the sample defines
a QiStream as such:

    public class QiType
    {
        public string Id
        {
            get;
            set;
        }

        public string Name
        {
            get;
            set;
        }

        public string Description
        {
            get;
            set;
        }
		
		. . .
    }

The BuildWaveDataType method in the sample further demonstrates how to construct the object that will be sent to Qi.
::

Insert Events into the Stream
-----------------------------

The sample makes use of Qi calls to insert either one event or several events at a time.  The following method demonstrates inserting one event:

	public async Task InsertValue<T>(string streamId, T data)
	{
		var requestUri = string.Format(DataRequestBase + "/InsertValue", _tenantId, _namespaceId, streamId);
		var response = await _client.PostAsync(requestUri,
			new StringContent(JsonConvert.SerializeObject(data)));

		if (!response.IsSuccessStatusCode)
		{
			throw new HttpRequestException($"Error: InsertValue request returned with response code {response.StatusCode}");
		}
	}

Retrieve Events
----------------

Many methods permit retrieving events from Qi. This sample demonstrates 
a basic method, called GetWindowValuesAsync. Getting a window of values 
involves specifying the stream and a start and end index.

::

	public async Task<List<T>> GetWindowValues<T>(string streamId, string startIndex, string endIndex)
	{
		var requestUri = string.Format(DataRequestBase + "/GetWindowValues?startIndex={3}&endIndex={4}",
			_tenantId, _namespaceId, streamId, startIndex, endIndex);
		var response = await _client.GetAsync(requestUri);

		if (!response.IsSuccessStatusCode)
		{
			throw new HttpRequestException($"Error: GetWindowValues request returned with response code {response.StatusCode}");
		}

		var contentAsString = await response.Content.ReadAsStringAsync();
		return JsonConvert.DeserializeObject<List<T>>(contentAsString);
	}

Index values must be expressed as ISO 8601 strings.

Cleanup
--------

When finished, the sample cleans up its stream, behavior and type. Cleanup becomes significant 
if you run the sample more than once. The sample will encounter collisions if events are left 
in the stream.
