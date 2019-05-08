Building a .NET sample to send OMF to PI or OCS
==================================================================


Building a sample with the rest calls directly
----------------------------------------------

The sample does not makes use of the OSIsoft Cloud Services Client Libraries.   When working in .NET, 
it is generally recommended that you use the OCS Client Libraries metapackage, OSIsoft.OCSClients. The metapackage is a NuGet package available 
from https://api.nuget.org/v3/index.json. The libraries offer a framework of classes that make client development easier.

The sample also does not use any libraries for connecting to PI.  Generally a library will be easier to use.

This sample also doesn't use any help to build the JSON strings for the OMF messages. This works for simple examples, and for set demos, but if building something more it may be easier to not form the JSON messages by hand.  

[OMF documentation](https://omf-docs.readthedocs.io/en/latest/)
[SDS documentation](https://ocs-docs.osisoft.com/Documentation/SequentialDataStore/Data_Store_and_SDS.html)


Getting Starting
----------------------------

In this example we assume that you have the dotnet core CLI.

To run this example from the commandline run

```
dotnet restore
dotnet run
```

to test this program change directories to the test and run

```
dotnet restore
dotnet test
```


Configure constants for connecting and authentication
-----------------------------------------------------

The SDS Service is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

```json
{
"NamespaceId": "REPLACE_WITH_NAMESPACE_ID",
"TenantId": "REPLACE_WITH_TENANT_ID",
"Resource": "https://dat-b.osisoft.com",
"ClientId": "REPLACE_WITH_CLIENT_IDENTIFIER",
"ClientKey": "REPLACE_WITH_CLIENT_SECRET"
}
```


The piserver uses the PI Web API as its OMF accepting endpoint.  To configure the sample to work against PI update the appsettings.json to have only these parameters and update that parameter values to what is being used. Note: the tenantId is used to autodetect if you are going against OCS or PI, so make sure that is removed if going against PI.

```json
{
  "Resource": "REPLACE_WITH_PI_WEB_API_URL",
  "dataservername": "REPLACE_WITH_PI_DATA_ARCHIVE_NAME"
}
```

See the general readme for information on setting up your endpoint.

-----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

-----------


For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OMF page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
