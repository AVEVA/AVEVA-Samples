# OMF Samples
The OSIsoft Message Format ([OMF](https://pisquare.osisoft.com/community/developers-club/omf)) defines a set of message headers and bodies that can be used to generate messages for ingestion into a compliant back-end system.  The PI System and OCS both have a compliant OMF receiving endpoint.   

OMF can be used to develop data acquisition applications on platforms and in languages for which there are no supported OSIsoft libraries.  Official documentation can be found [here](https://omf-docs.readthedocs.io/en/latest/).


Some tasks and individual language examples have labels as follows:

* \* denotes that the language example uses the rest API directily instead of a library

* <img src="../miscellaneous/images/ctp.png" alt="ctp icon">   This task and code uses services that are currently in preview.  If you are interested in this functionality, please contact OSISoft.  



The official OMF samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table:

Task|Description|Languages|&nbsp;&nbsp;&nbsp;OCS&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| PI Test Status
----|-----------|---------|-----------
<img src="../miscellaneous/images/ctp.png" alt="ctp icon">  **<a href="basic_samples/OMF_API/">Basic API</a>** | These samples demonstrate sending some typical OMF messages.  The applications are configurable to both PI and OCS.  <a href="basic_samples/OMF_API">Details</a>   |  <a href="basic_samples/OMF_API/CSharp/OMF_API/">.NET*</a><br /><a href="basic_samples/OMF_API/Python3/">Python3*</a><br /><a href="basic_samples/OMF_API/Java/omfapijava">Java*</a>  | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)|[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_%20on-prem?branchName=master&jobName=OMF_APIDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4782&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_%20on-prem?branchName=master&jobName=OMF_APIPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4782&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_%20on-prem?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4782&branchName=master)




Configuring OCS or the PI system to accept OMF messages
-----------------------------------------------------

Sending to OCS:
Configure OMF Connection.  This can be done programmatically, but here are the general steps to do it via the OCS portal:

1) Create an OMF application client credential.
2) Setup the OMF Connection to use the client credential and point to a namespace.
3) Use the OMF Connection information in your application.


Sending to PI:
PI Web API OMF accepting endpoint is not currently released.  Currently you can use the PI Connector Relay which these samples have not been tested against.


OMF limitations on OCS and PI
-----------------------------------------------------
This list is not exhuastive, but rather a few key details to know.  

1) PI only accepts DateTime timestamp as the property index 
2) PI can only have 1 index
2) OCS only accepts Dynamic OMFType classification 
3) OCS does not accept Link type data


## Credentials 

A credential config.ini or app.config file is used in the examples unless otherwise noted in the example.  
   

     Note: This is not a secure way to store credentials.  This is to be used at your own risk.  
   
   
   You will need to modify these files locally when you run the samples.

## Request for example 

Please raise an issue if you would like to see a new task, a new example inside of a task, or an existing example in a particular langauge.    

## Contributions

If you wish to contribute please take a look at the [contribution guide](../CONTRIBUTING.md).

## License

[OSI Samples](https://github.com/osisoft/OSI-Samples) are licensed under the [Apache 2 license](../LICENSE.md).



For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
