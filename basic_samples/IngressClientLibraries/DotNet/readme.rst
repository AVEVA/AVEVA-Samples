.NET Samples 
============

Building a Client with the Ingress Client Libraries
---------------------------------------------------

The sample described in this section makes use of the OSIsoft Ingress Client Libraries. When working in .NET, 
it is recommended that you use these libraries. The libraries are available as NuGet packages. The packages used are:

* OSIsoft.Contracts.Ingress
* OSIsoft.Models.Ingress
* OSIsoft.Identity.AuthenticationHandler

The libraries offer a framework of classes that make client development easier.

Configure constants for connecting and authentication
-----------------------------------------------------

The Ingress Service is secured by obtaining tokens from the Identity Server. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the server. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

::

	{
		"TenantId": "REPLACE_WITH_TENANT_ID",
		"NamespaceId": "REPLACE_WITH_NAMESPACE_ID",
		"Address": "https://dat-b.osisoft.com",
		"ClientId": "REPLACE_WITH_CLIENT_IDENTIFIER",
		"ClientSecret": "REPLACE_WITH_CLIENT_SECRET"
	}



The authentication values are provided to the ``OSIsoft.Identity.AuthenticationHandler``. 
The AuthenticationHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

Other Configuration
-------------------

The aforementioned appsettings.json file has placeholders for the names of the topic
and subscription, as well as a client Id to map to the topic. You must fill in those values as well.

Set up IngressService
----------------------

The example works through one interface: 

* IIngressService for Topic and Subscription object operations

The following code block illustrates how to configure the IngressService to use throughout the sample:

.. code:: cs

	AuthenticationHandler authenticationHandler = new AuthenticationHandler(address, clientId, clientSecret);

	IngressService baseIngressService = new IngressService(new Uri(address), null, HttpCompressionMethod.None, authenticationHandler);
	IIngressService ingressService = baseIngressService.GetIngressService(tenantId, namespaceId);
  
Mapped clients
---------------

The same clients obtained from the Identity Server are used to send OMF messages to a topic. A client may only be mapped to one topic per namespace. 
It is recommended that the client you wish to map to the topic be different from the client used too authenticate. 

Create a Topic
--------------

A Topic is used to aggregate data received from clients and make it available for consumption 
via a Subscription. A topic must contain at least one client Id. Client Ids may be added to 
or removed from an existing topic. First, we create the Topic locally by instantiating 
a new Topic object:

.. code:: cs

	Topic topic = new Topic()
	{
		TenantId = tenantId,
		NamespaceId = namespaceId,
		Name = "REPLACE_WITH_TOPIC_NAME",
		Description = "This is a sample Topic",
		ClientIds = new List<string>() { mappedClientId }
	};

Then use the Ingress client to create the Topic in OCS:

.. code:: cs

	Topic createdTopic = await ingressService.CreateOrUpdateTopicAsync(topic);

Create a Subscription
---------------------

A Subscription is used to consume data from a Topic. There are two types of 
Subscriptions: Standard Subscription and OCS Data Store Subscriptions. This 
section only talks about an OCS Data Store Subscription. An OCS Data Store 
Subscription pulls the data from the Topics and sends it to Sds. First, we 
create the Subscription locally by instantiating a new Subscription object:

.. code:: cs

	Subscription subscription = new Subscription()
	{
		TenantId = tenantId,
		NamespaceId = namespaceId,
		Name = "REPLACE_WITH_SUBSCRIPTION_NAME",
		Description = "This is a sample OCS Data Store Subscription",
		Type = SubscriptionType.Sds,
		TopicId = createdTopic.Id,
		TopicTenantId = createdTopic.TenantId,
		TopicNamespaceId = createdTopic.NamespaceId
	};
	
Then use the Ingress client to create the Subscription in OCS:

.. code:: cs

	Subscription createdSubscription = await ingressService.CreateOrUpdateSubscriptionAsync(subscription);
	
At this point, we are ready to send OMF data to OCS, and consume it as well. To learn how to do this, click 
here: https://github.com/osisoft/OMF-Samples/tree/master/Tutorials/CSharp_Sds

Cleanup: Deleting Types, Stream Views, and Streams
-----------------------------------------------------

In order to prevent a bunch of unused resources from being left behind, this 
sample performs some cleanup before exiting. Deleting Subscriptions and Topics 
can be achieved using the Ingress client and passing the corresponding object Ids:

.. code:: cs

	await ingressService.DeleteSubscriptionAsync(createdSubscription.Id);
	await ingressService.DeleteTopicAsync(createdTopic.Id);