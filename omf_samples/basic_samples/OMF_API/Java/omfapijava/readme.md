Building a Java client to send OMF to PI or OCS
==================================================================

The sample code in this topic demonstrates how to send OMF messages
using Java.




Summary of steps to run the Java demo
--------------------------------------
Using Eclipse or any IDE:

1. Clone a local copy of the GitHub repository.

2. Install Maven.

3. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.

4. Replace the configuration strings in ``config.properties``


Using a command line:

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


4. Building and running the project.
   a) cd to your project location.
   b) run ``mvn package exec:java`` on cmd.

To test your porject locally run ``mvn test``

These are also tested using VS Code.

Configure constants for connecting and authentication
-----------------------------------------------------

The SDS Service is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

The values to be replaced are in ``config.properties``:

```
[Configurations]
Namespace = Samples

[Access]
Resource = https://dat-b.osisoft.com
Tenant = REPLACE_WITH_TENANT_ID
ApiVersion = v1-preview

[Credentials]
ProducerToken = REPLACE_WITH_TOKEN_STRING
ClientId = REPLACE_WITH_APPLICATION_IDENTIFIER
ClientSecret = REPLACE_WITH_APPLICATION_SECRET
```



The piserver uses the PI Web API as its OMF accepting endpoint.  It is currently in Beta.  To configure the sample to work against PI update the appsettings.json to have only these parameters and update that parameter values to what is being used. Note: the tenantId is used to autodetect if you are going against OCS or PI, so make sure that is removed if going against PI.

```
[Configurations]
DataServerName = REPLACE_WITH_PI_DATA_ARCHIVE_NAME

[Access]
Resource = REPLACE_WITH_PI_WEB_API_URL
```


See the general readme for information on setting up your endpoint.



----------

[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

---------


For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OMF page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
