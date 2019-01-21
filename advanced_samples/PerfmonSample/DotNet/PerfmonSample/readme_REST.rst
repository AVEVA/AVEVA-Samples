Performance Counter Sample
============

Building SDS Types an Stream for Performance Counters
--------------------------------------

This sample demonstrates proper stream design in the Sequential Data Store, SDS, using Performance Counter Categories as an example.  

The sample creates SDS Types with a DateTime index and long integer properties for each Counter in the Category Instance.  The counters in a Category Instance represent a unique object being monitored in a computer system.  Every property is sampled at the same time; they share the same index.  Thus it makes sense to group the counters and their sample time into a single SDS Type.  There is a one-to-one relationship between Performance Counter Categories and SDS Types.

Category Instances, monitored objects, are distinct, so they are represented as distinct SDS Streams.  There is a one-to-one relationship between Instances and Streams.

Clients and Authorization Handlers
---------------------

This sample relies on both the SDS Client Libraries and the System.Net.Http.HttpClient.  A sample Authorization Handler is included as an example.  The OSIsoft.Data.Http.Security.SdsSecurityHandler, included with the Client Libraries, could have been used in its place.

Configure constants for connecting and authentication
---------------------

Azure Active Directory secures the SDS.  Clients must provide an Authorization Header including a token obtained from the Azure Active Directory authority.  Tokens are acquired by and attached to request headers using the OSIsoft.Data.Http.Security.SdsSecurityHandler and PerfmonSample.ApplicationAuthenticationHandler.  

The sample includes an App.config configuration file to hold configuration strings, including the authentication strings. You must replace the placeholders with the authentication-related values you received from OSIsoft.

{
        "NamespaceId": "REPLACE_WITH_NAMESPACE_ID",
        "TenantId": "REPLACE_WITH_TENANT_ID",
        "Address": "https://dat-a.osisoft.com",
        "Resource": "https://qihomeprod.onmicrosoft.com/ocsapi",
        "ClientId": "REPLACE_WITH_CLIENT_IDENTIFIER",
        "ClientSecret": "REPLACE_WITH_CLIENT_SECRET"
}

Overall Flow
---------------

The sample is documented internally.

It begins by creating the clients needed to communicate with SDS.  Security handlers are added to the clients.

Next, it iterates through a collection of Performance Counter Category names, specified in the Categories collection.  For each Category it
* Creates an SDS Type
* Iterates through Instances of the Category creating
     ** An SDS Stream
     ** A function that will be used to read the Instance Counters, create an event and update the Stream

Once the Types, Streams and update functions are created, we update the streams a number of times.

Then we read data from the streams.  The data is displayed in raw JSON.

Finally all Streams and Types are deleted.
