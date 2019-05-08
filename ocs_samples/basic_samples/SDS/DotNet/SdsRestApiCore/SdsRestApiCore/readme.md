.NET Samples using API Calls
============

Building a Client with the rest calls directly
----------------------------------------------

The sample does not makes use of the OSIsoft Cloud Services Client Libraries.   When working in .NET, 
it is generally recommended that you use the OCS Client Libraries metapackage, OSIsoft.OCSClients. The metapackage is a NuGet package available 
from https://api.nuget.org/v3/index.json. The libraries offer a framework of classes that make client development easier.

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

----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNetAPI)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

----------------

For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
