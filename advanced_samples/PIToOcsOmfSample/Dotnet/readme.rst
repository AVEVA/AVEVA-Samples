
PI to OCS Samples 
============

Writing to OSIsoft Cloud Services (OCS) using OSIsoft Message Format (OMF)
--------------------------------------------------------------------------

OSIsoft Cloud Services is able to ingest OSIsoft Message Format messages. OCS includes services that 
unpack OMF message content and write the contained information to the SDS (the OCS data store).

OSIsoft Cloud Services documentation can be found at https://cloud.osisoft.com/documentation
OSIsoft Message Format documentation can be found at http://omf-docs.osisoft.com/en/v1.0/ 

This sample is not intended to be used as a robust tool for migrating data from PI Data Archive to
OSIsoft Cloud Services. Its limitations are:
* Only the most recently written event will be migrated to OCS for PI Data Archive events with 
duplicate timestamps.
* Bad values from PI Data Archive are not migrated to OCS. This is the only consideration made for 
PI Data Archive system digital states.
* Limited error handling


Building a Client with the SDS Client Libraries
----------------------------------------------

This sample makes use of the OSIsoft SDS Client Libraries. When working in 
.NET, it is recommended that you use these libraries. The libraries are available as NuGet packages 
from https://api.nuget.org/v3/index.json . The packages used are:

* OSIsoft.Models
* OSIsoft.Http.Client  
* OSIsoft.Http.Security 

The libraries offer a framework of classes that make client development easier.


Configure constants for connecting and authentication
-----------------------------------------------------

OSIsoft Cloud Services is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an app.config configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

::
    <appSettings>	  
        <add key="address" value="https://dat-a.osisoft.com" />
        <add key="accountId" value="REPLACE_WITH_ACCOUNT_ID" />
        <add key="resource" value="https://qihomeprod.onmicrosoft.com/ocsapi" />
        <add key="clientId" value="REPLACE_WITH_CLIENT_IDENTIFIER" />
        <add key="clientSecret" value="REPLACE_WITH_CLIENT_SECRET" />
	    ...
    </appSettings>
	
The authentication values are provided to the ``OSIsoft.Http.Security.SdsSecurityHandler``. 
The SdsSecurityHandler is a DelegatingHandler that is attached to an HttpClient pipeline.


Other Configuration
-------------------
   <appSettings>	  
     ...
	 <add key="publisherName" value="REPLACE_WITH_PUBLISHER_NAME" />
     <add key="topicName" value="REPLACE_WITH_TOPIC_NAME" />
     <add key="subscriptionName" value="REPLACE_WITH_SUBSCRIPTION_NAME" />
     <add key="namespaceId" value="REPLACE_WITH_NAMESPACE_ID" />
     <add key="PIDataArchive" value="REPLACE_WITH_PI_SERVER_NAME" />
   </appSettings>

Manage Data Ingress Resources for OCS
-----------------

Publishers, topics, and subscriptions facilitate ingress to OCS. More information is 
available in the OSIsoft Cloud Services documentation. OCS exposes management APIs for 
these ingress resources and there is a nuget library.

This sample sends HTTP REST requests to this management API to create the ingress 
resources that accept PI point data.


Create SdsTypes
---------------

To use SDS, you define SdsTypes that describe the kinds of data you want to store in 
SdsStreams. SdsTypes are the model that define SdsStreams.

PI point data can generally be represented as as a SdsType with a DateTime index and some
other value property. The PI to OCS via OMF sample defines five different possible values 
property kinds in five different SdsTypes. The value properties are integer, float, string,
time and blobs.

OSIsoft Clouds Services' ingress capabilities allow for the definition of SdsTypes in OCS 
through OMF type messages. The sample creates these OMF type messages and send them to 
OCS.

Create SdsStreams
------------------

In OSIsoft Cloud Services, an ordered series of events is stored in a SdsStream. In this
sample, a PI point maps directly to a SdsStream. All the data written to a single SdsStream 
is read from a single PI point.

As with the SdsTypes, SdsStreams can be created in OCS via OMF messages. This sample sends 
OMF container messages to OCS to create a SdsStream for each PI point. These SdsStreams are 
indexed on time.

	
Read PI point data
----------------------------------------

PI point data is read from a configured PI server using the OSIsoft AFSDK client. 


Write PI point data to OSIsoft Cloud Services
----------------------------------------

A single PI point event translates to a single event in a SdsStream. OSIsoft Message Format 
can be used to send data to OSIsoft Cloud Services. This sample creates and sends OMF data 
messages to OCS.
 
* If there are events with duplicate timestamps for a given PI point, this sample uses the 
most recently written
event for the OMF data message. 
* PI point events with system digital state values are filtered out before OMF data messages 
are created.
* OMF data messages are sent in chunks so that the size does not exceed the OMF maximum 
message size.