Building a Java client to make REST API calls to OCS
===============================================================

The sample code described in this topic demonstrates how to use Java to store 
and retrieve data from SDS using only the SDS REST API. 

This project is built using Apache Maven. To run the code in this example, you 
must first download and install the Apache Maven software. See 
`Apache Maven Project <https://maven.apache.org/download.cgi>`__ 
for more information. All of the necessary dependencies are specified within 
the pom.xml file.

Summary of steps to run 
--------------------------------------
Using Eclipse or any IDE
1. Clone a local copy of the GitHub repository.
2. Install Maven.
3. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.

Using a command line
1. Clone a local copy of the GitHub repository.
2. Download apache-maven-x.x.x.zip from http://maven.apache.org and extract it.
3. Setting environment variables.
   a) For Java JDK
      Variable name - JAVA_HOME
      Variable value - location to the Java JDK in User variables.

      and, also add JDK\bin path to the Path variable in System variables.

   b) For Maven
      Variable name - MAVEN_HOME
      Variable value - location to the extracted folder for the
                       maven ~\apache-maven-x.x.x in User variables.

      and, also add ~\apache-maven-x.x.x\bin path to the Path variable in System variables.

*Currently this project is not hosted on the central Maven repo and must be compiled and installed locally to be used in any of the other examples.
To do this run mvn install library_samples\Java\ocs_sample_library_preview\pom.xml

Instantiate an OCS Client
-----------------------

Each REST API call consists of an HTTP request along with a specific URL and
HTTP method. The URL contains the server name plus the extension
that is specific to the call. Like all REST APIs, the SDS REST API maps
HTTP methods to CRUD operations as shown in the following table:

+---------------+------------------+--------------------+
| HTTP Method   | CRUD Operation   | Content Found In   |
+===============+==================+====================+
| POST          | Create           | Message body       |
+---------------+------------------+--------------------+
| GET           | Retrieve         | URL parameters     |
+---------------+------------------+--------------------+
| PUT           | Update           | Message body       |
+---------------+------------------+--------------------+
| DELETE        | Delete           | URL parameters     |
+---------------+------------------+--------------------+

The constructor for the OCSClient class takes the base URL (that is, the
protocol, server address and port number) and the api version. It also creates a new Gson
serializer/deserializer to convert between Java Objects and JSON.  This is all done in subclass used as a base.

```java
public BaseClient() {
    gclientId = getConfiguration("clientId");
    gclientSecret = getConfiguration("clientSecret");
    gresource = getConfiguration("resource");
    gresource = gresource.endsWith("/") ? gresource :  gresource + "/";

    this.baseUrl = gresource;
    this.apiVersion = getConfiguration("apiVersion");
    this.mGson = new Gson();
}
```

Configure the Sample:
-----------------------

Included in the samples are a configuration file with placeholders 
that need to be replaced with the proper values. They include information 
for authentication, connecting to the SDS Service, and pointing to a namespace.

The SDS Service is secured using Azure Active Directory. The sample application 
is an example of a *confidential client*. Confidential clients provide an 
application ID and secret that are authenticated against the directory. These 
are referred to as client IDs and client secrets, which are associated with 
a given tenant. They are created through the tenant's administration portal. 
The steps necessary to create a new client ID and secret are described below.

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
value so authentication occurs against the correct tenant. The URL for the SDS 
Service connection must also be changed to reflect the destination address of 
the requests. 

Finally, a valid namespace ID for the tenant must be given as well. To create 
a namespace, click on the ``Manage`` tab then navigate to the ``Namespaces`` 
page. At the top the add button will create a new namespace after the required 
forms are completed. This namespace is now associated with the logged-in tenant 
and may be used in the sample.

The values to be replaced are in ``config.properties``:

```
resource = https://dat-b.osisoft.com
clientId = PLACEHOLDER_REPLACE_WITH_CLIENT_ID
clientSecret = PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET
tenantId = PLACEHOLDER_REPLACE_WITH_TENANT_ID
namespaceId = PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID
apiVersion = v1
```

Obtain an Authentication Token
------------------------------

Near the end of the ``BaseClient.Java`` file is a method called
``AcquireAuthToken``. The first step in obtaining an authorization token
is to connect to the Open ID discovery endpoint and get a URI for obtaining the token.
Thereafter, the token based on ``clientId`` and ``clientSecret`` is retrieved.

The token is cached, but as tokens have a fixed lifetime, typically one hour, but can be refreshed
by the authenticating authority for a longer period. If the refresh
period has expired, the credentials must be presented to the authority
again. To streamline development, the ``AcquireToken`` method hides
these details from client programmers. As long as you call
``AcquireToken`` before each HTTP call, you will have a valid token. 


