
PI to OCS Samples 
============

Writing to OSIsoft Cloud Services (OCS) using OSIsoft Message Format (OMF)
--------------------------------------------------------------------------

OSIsoft Cloud Services is able to ingest OSIsoft Message Format messages. OCS includes services that 
unpack OMF message content and write the contained information to the Qi (the OCS data store).

OSIsoft Cloud Services documentation can be found at https://cloud.osisoft.com/documentation
OSIsoft Message Format documentation can be found at http://omf-docs.osisoft.com/en/v1.0/ 

This sample is not intended to be used as a robust tool for migrating data from PI Data Archive to
OSIsoft Cloud Services. Its limitations are:
* Only the most recently written event will be migrated to OCS for PI Data Archive events with 
duplicate timestamps.
* Bad values from PI Data Archive are not migrated to OCS. This is the only consideration made for 
PI Data Archive system digital states.
* Limited error handling


Building a Client with the Qi Client Libraries
----------------------------------------------

The sample described in this section makes use of the OSIsoft Qi Client Libraries. When working in 
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
    &lt;appSettings&gt;	  
        &lt;add key="address" value="https://qi-data.osisoft.com" /&gt;
        &lt;add key="accountId" value="REPLACE_WITH_ACCOUNT_ID" /&gt;
        &lt;add key="resource" value="https://qihomeprod.onmicrosoft.com/ocsapi" /&gt;
        &lt;add key="clientId" value="REPLACE_WITH_CLIENT_IDENTIFIER" /&gt;
        &lt;add key="clientSecret" value="REPLACE_WITH_CLIENT_SECRET" /&gt;
	    ...
    &lt;/appSettings&gt;
	
The authentication values are provided to the ``OSIsoft.Http.Security.QiSecurityHandler``. 
The QiSecurityHandler is a DelegatingHandler that is attached to an HttpClient pipeline.


Other Configuration
-------------------
   &lt;appSettings&gt;	  
     ...
	 &lt;add key="publisherName" value="REPLACE_WITH_PUBLISHER_NAME" /&gt;
     &lt;add key="topicName" value="REPLACE_WITH_TOPIC_NAME" /&gt;
     &lt;add key="subscriptionName" value="REPLACE_WITH_SUBSCRIPTION_NAME" /&gt;
     &lt;add key="namespaceId" value="REPLACE_WITH_NAMESPACE_ID" /&gt;
     &lt;add key="PIDataArchive" value="REPLACE_WITH_PI_SERVER_NAME" /&gt;
   &lt;/appSettings&gt;

Manage Data Ingress Resources for OCS
-----------------

Publishers, topics, and subscriptions facilitate ingress to OCS. More information is 
available in the OSIsoft Cloud Services documentation. OCS exposes management APIs for 
these ingress resources.

This sample sends HTTP REST requests to this management API to create the ingress 
resources that accept PI point data.


Create QiTypes
---------------

To use Qi, you define QiTypes that describe the kinds of data you want to store in 
QiStreams. QiTypes are the model that define QiStreams.

PI point data can generally be represented as as a QiType with a DateTime index and some
other value property. The PI to OCS via OMF sample defines five different possible values 
property kinds in five different QiTypes. The value properties are integer, float, string,
time and blobs.

OSIsoft Clouds Services' ingress capabilities allow for the definition of QiTypes in OCS 
through OMF type messages. The sample creates these OMF type messages and send them to 
OCS.

Create QiStreams
------------------

In OSIsoft Cloud Services, an ordered series of events is stored in a QiStream. In this
sample, a PI point maps directly to a QiStream. All the data written to a single QiStream 
is read from a single PI point.

As with the QiTypes, QiStreams can be created in OCS via OMF messages. This sample sends 
OMF container messages to OCS to create a QiStream for each PI point. These QiStreams are 
indexed on time.

	
Read PI point data
----------------------------------------

PI point data is read from a configured PI server using the OSIsoft AFSDK client. 


Write PI point data to OSIsoft Cloud Services
----------------------------------------

A single PI point event translates to a single event in a QiStream. OSIsoft Message Format 
can be used to send data to OSIsoft Cloud Services. This sample creates and sends OMF data 
messages to OCS.
 
* If there are events with duplicate timestamps for a given PI point, this sample uses the 
most recently written
event for the OMF data message. 
* PI point events with system digital state values are filtered out before OMF data messages 
are created.
* OMF data messages are sent in chunks so that the size does not exceed the OMF maximum 
message size.