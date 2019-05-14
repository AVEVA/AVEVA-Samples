Building a Python client to send OMF to PI or OCS
==================================================================

The sample code in this topic demonstrates how to send OMF messages
using Python. 

The samples were built and tested against Python 3.  If you are using 
a different version you might encounter errors or unexepected behavior.    
	
To Run this Sample:
-------------------
1. Clone the GitHub repository
2. Install required modules: ``pip install -r requirements.txt``
3. Open the folder with your favorite IDE
4. Update ``config.ini`` with tour credentials
5. Check and update the program to ensure you are sending to OCS or PI.  
6. Run ``program.py``  from commandline run ``python program.py``


To Run the provided test:
1. Install pytest ``pip install pytest``
2. Run ``pytest program.py``


Configure constants for connecting and authentication
-----------------------------------------------------

The SDS Service is secured by obtaining tokens from Azure Active Directory. Such clients 
provide a client application identifier and an associated secret (or key) that are 
authenticated against the directory. The sample includes an appsettings.json configuration 
file to hold configuration strings, including the authentication strings. You must 
replace the placeholders with the authentication-related values you received from OSIsoft. 

The values to be replaced are in ``config.ini``:

```ini
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

```ini
[Configurations]
DataServerName = REPLACE_WITH_PI_DATA_ARCHIVE_NAME

[Access]
Resource = REPLACE_WITH_PI_WEB_API_URL
```

See the general readme for information on setting up your endpoint.

-----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

-----------


For the general steps or switch languages see the Task  [ReadMe](../)<br />
For the main OMF page [ReadMe](../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
