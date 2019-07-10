Building a Python client to make REST API calls to the SDS Service
==================================================================

The sample code in this topic demonstrates how to invoke SDS REST APIs
using Python. By examining the code, you will see how to create an SdsType and SdsStream, 
and how to create, read, update, and delete values in SDS.  You will also see the effect of the accept verbosity header,
summaries value call, and how to do bulk streams calls. 

The sections that follow provide a brief description of the process from
beginning to end.    
	
Developed against Python 3.7.2.

To Run this Sample:
-------------------
1. Clone the GitHub repository
2. Install required modules: ``pip install -r requirements.txt``
3. Open the folder with your favorite IDE
4. Update ``config.ini`` with the credentials provided by OSIsoft
5. Run ``program.py``


To Test the sample:
1. Run ``python test.py``

or

1. Install pytest ``pip install pytest``
2. Run ``pytest program.py``

  

Configure the Sample:
-----------------------

Included in the sample there is a configuration file with placeholders that 
need to be replaced with the proper values. They include information for 
authentication, connecting to the SDS Service, and pointing to a namespace.

The values to be replaced are in ``config.ini``:

```ini
[Configurations]
Namespace = Samples

[Access]
Resource = https://dat-b.osisoft.com
Tenant = REPLACE_WITH_TENANT_ID
ApiVersion = v1

[Credentials]
ClientId = REPLACE_WITH_APPLICATION_IDENTIFIER
ClientSecret = REPLACE_WITH_APPLICATION_SECRET
```



-----------
 [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDS_TSPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

 ----------

 Automated test uses Python 3.6.8 x64

For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)