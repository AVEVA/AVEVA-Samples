.NET Samples 
============

Building a Client with the Ingress Client Libraries
---------------------------------------------------

The sample described in this section makes use of the OSIsoft Ingress Client Libraries. When working in .NET, 
it is recommended that you use these libraries. The libraries are available as NuGet packages. The packages used are:

* OSIsoft.Omf
* OSIsoft.OmfIngress
* OSIsoft.Identity.AuthenticationHandler

The libraries offer a framework of classes that make client development easier.

Configure constants for connecting and authentication
-----------------------------------------------------

The Ingress Service is secured by obtaining tokens from the Identity Server. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the server. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. The application requires two Client Credential Clients, one to manage OMF Ingress connetions and one to send data from a mock device. For information on how to obtain these client IDs and secrets, see the [Client Credential Client Documentation](https://ocs-docs.osisoft.com/Documentation/Identity/Identity_ClientCredentialClient.html).

```
	{
        "TenantId": "REPLACE_WITH_YOUR_TENANT_ID",
        "NamespaceId": "REPLACE_WITH_YOUR_NAMESPACE_ID",
        "Address": "https://dat-b.osisoft.com",
        "ClientId": "REPLACE_WITH_CLIENT_IDENTIFIER",
        "ClientSecret": "REPLACE_WITH_CLIENT_SECRET",
        "DeviceClientId": "REPLACE_WITH_DEVICE_CLIENT_ID",
        "DeviceClientSecret": "REPLACE_WITH_DEVICE_CLIENT_SECRET",
        "ConnectionName": "REPLACE_WITH_DESIRED_CONNECTION_NAME",
        "StreamId": "REPLACE_WITH_DESIRED_STREAM_ID"
	}
```

The authentication values are provided to the ``OSIsoft.Identity.AuthenticationHandler``. 
The AuthenticationHandler is a DelegatingHandler that is attached to an HttpClient pipeline.

Other Configuration
-------------------

The aforementioned appsettings.json file has placeholders for the names of the connection, as well as a client Id to map a device to the topic. You must fill in those values as well.

Set up IngressService
----------------------

The example works through one interface: 

* IOmfIngress for for configuring OMF Connections and sending OMF Messages

The following code block illustrates how to configure the IngressService to use throughout the sample:

```
    AuthenticationHandler authenticationHandler = new AuthenticationHandler(address, clientId, clientSecret);

    OmfIngressService baseOmfIngressService = new OmfIngressService(new Uri(address), null, HttpCompressionMethod.None, authenticationHandler);
    IOmfIngressService omfIngressService = baseOmfIngressService.GetOmfIngressService(tenantId, namespaceId);
```

Note that the instance of the IOmfIngressService is scoped to a tenant and namespace. If you wish to work in a different tenant or namespace, you would need another instance scoped to that tenant and namespace.

OMF Connections
-------------------------
An OMF Connection is made up of three components: one or more Clients, a Topic, and a Subscription. Data is sent to a Topic via a Client, where the data is buffered and made available for the Subscription. The 
Subscription relays data from the Topic to the Sequential Data Store in the namespace that the Subscription resides in. The OmfIngressClient in this example creates a connection using an existing clientId, and 
creating a Topic and Subscription as detailed below.

Clients
---------------

Devices sending OMF messages each need their own unique clientId and clientSecret. The clientId and secret are used to authenticate the requests, and the clientId is used route messages to the proper topic(s). 
ClientIds may be mapped to at most one topic per namespace. For more details on Clients see the [Client Credential Client Documentation](https://ocs-docs.osisoft.com/Documentation/Identity/Identity_ClientCredentialClient.html).

Topics
--------------

A Topic is used to aggregate data received from clients and make it available for consumption 
via a Subscription. A topic must contain at least one client Id. Client Ids may be added to 
or removed from an existing topic. First, we create the Topic locally by instantiating 
a new Topic object:


```
    Topic topic = new Topic()
    {
        Name = "REPLACE_WITH_TOPIC_NAME",
        Description = "This is a sample Topic",
        ClientIds = new List<string>() { mappedClientId }
    };
```

Then use the Ingress client to create the Topic in OCS:

```
    Topic createdTopic = await ingressService.CreateOrUpdateTopicAsync(topic);
```

Subscriptions
---------------------

A Subscription is used to consume data from a Topic and relay it to the Sequential Data Store.
First, we create the Subscription locally by instantiating a new Subscription object:

```
    Subscription subscription = new Subscription()
    {
        TenantId = tenantId,
        NamespaceId = namespaceId,
        Name = "REPLACE_WITH_SUBSCRIPTION_NAME",
        Description = "This is a sample OCS Data Store Subscription",
        Type = SubscriptionType.Sds,
        TopicId = createdTopic.Id,
        TopicTenantId = "REPLACE_WITH_TOPIC_TENANT_ID",
        TopicNamespaceId = "REPLACE_WITH_TOPIC_NAMESPACE_ID"
    };
```

Then use the Ingress client to create the Subscription in OCS:

```
    Subscription createdSubscription = await ingressService.CreateOrUpdateSubscriptionAsync(subscription);
```	

Send OMF Messages
-------------------

OMF messages sent to OCS are translated into objects native to the Sequential Data Store. In this example, we send an OMF Type message which creates an SDS type in the data store, 
an OMF Container message which creates an SDS stream, and then send OMF Data messages, which use the containerId in the message body to route the data to the SDS stream. 
Refer to the data store documentation for how to view the types/streams/data in SDS. For each type of message, we first construct the message body using the OMF library:

```	
    OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));

    OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));

    DataPointType dataPoint = new DataPointType() { Timestamp = DateTime.UtcNow, Value = rand.NextDouble() };
    OmfDataMessage dataMessage = OmfMessageCreator.CreateDataMessage(streamId, dataPoint);
```

Then the devices uses its own ingress client, which uses the device clientId and clientSecret to authenticate the requests. The device clientId is used to route the message
to the Topic that the clientId is mapped to. Note that the message must be serialized before being sent.

```
    var serializedMessage = OmfMessageSerializer.Serialize(omfMessage);
    await deviceIngressService.SendOMFMessageAsync(serializedMessage);
```

Cleanup: Deleting Topics and Subscriptions
-----------------------------------------------------

In order to prevent unused resources from being left behind, this sample performs some cleanup before exiting. 

Deleting Containers and Types can be achieved by constructing the same OMF messages, but instead specifying the Delete action:

```
    OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));
    typeMessage.ActionType = ActionType.Delete;

    OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));
    containerMessage.ActionType = ActionType.Delete;  
```

Then serialize the message and send as shown in the prior section.

Deleting Subscriptions and Topics can be achieved using the Ingress client and passing the corresponding object Ids:

```
    await ingressService.DeleteSubscriptionAsync(createdSubscription.Id);
    await ingressService.DeleteTopicAsync(createdTopic.Id);
```