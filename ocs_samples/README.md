# OCS Samples
OSIsoft Cloud Services ([OCS](https://www.osisoft.com/Solutions/OSIsoft-Cloud-Services/)) is a highly flexible cloud-based platform that provides scalable, elastic,
centralized environment to aggregate data for reporting, advanced analytics, and third-party applications.  OCS is powered by OSIsoft's Sequential Data Store (SDS). In this GitHub repo, we provide samples which will help you get started with the [OCS API](https://ocs-docs.osisoft.com/) against your [OCS instance](https://cloud.osisoft.com/welcome).

There are three types of samples/apps in the repo:

* <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon">  Getting Started - OCS focused samples for a task, usually implemented as a simple console app.  This also includes base libraries that may be used in other apps.

* <img src="../miscellaneous/images/app-type-ingress.png" alt="ingress icon">   Ingress apps - Real world examples of applications focused on sending data to OCS.  

* <img src="../miscellaneous/images/app-type-e2e.png" alt="e2e icon">   End-End apps - Real world examples of web, desktop, mobile, and other applications using OCS data.  

Some tasks and individual language examples may have some additional labels as follows:

* \* denotes that the language example uses the rest API directily instead of a library

* <img src="../miscellaneous/images/ctp.png" alt="ctp icon">   This task and code uses services that are currently in preview.  If you are interested in this functionality, please contact OCS support.  



The official OCS samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table:


Task|Description|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
----|-----------|---------|-----------
**<a href="basic_samples/Authentication/">Authentication</a>**  <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | **Client Credential** <a href="basic_samples/Authentication/">Details</a> <br /> **Hybrid Authentication** <a href="basic_samples/Authentication/">Details</a> <br /> **Implicit Authentication** <a href="basic_samples/Authentication/">Details</a>  | <a href="basic_samples/Authentication/ClientCredentialFlow/DotNet/ClientCredentialFlow">.NET</a> <br /><a href="basic_samples/Authentication/HybridFlow/DotNet/HybridFlow">.NET</a><br /><a href="basic_samples/Authentication/ImplicitFlow/DotNet/ImplicitFlow">.NET and JavaScript</a>
**<a href="basic_samples/SDS">Types, Streams, and retreiving Data</a>** <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers typical operations against the Sds, including creating, updating, and deleting types, streams and events.  This is the recommended starting example, and a good a base for all other Tasks.  <a href="basic_samples/SDS">Details</a> | <a href="basic_samples/SDS/DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a><br /><a href="basic_samples/SDS/DotNet/SdsRestApiCore">.NET*</a><br /><a href="basic_samples/SDS/Java/sdsjava">JAVA</a><br /><a href="basic_samples/SDS/JavaScript/Angular">Angular</a><br /><a href="basic_samples/SDS/JavaScript/NodeJs">nodeJS</a><br /><a href="basic_samples/SDS/Python/SDSPy/Python2">Python2</a><br /><a href="basic_samples/SDS/Python/SDSPy/Python3">Python3</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNetAPI)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> <br /> <br /> <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)
**<a href="basic_samples/IngressClientLibraries/DotNet">Ingress Management</a>** <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers management operations for Ingress, including creating and deleting publishers, ingress tokens, topics, and subscriptions. | <a href="basic_samples/IngressClientLibraries/DotNet">.NET</a>&nbsp; &nbsp;
**<a href="advanced_samples/UomsSample/Dotnet/UomsSample">UOM</a>** <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the basic functionality of the UOM system on OCS | <a href="advanced_samples/UomsSample/Dotnet/UomsSample">.NET</a>&nbsp; &nbsp;
**<a href="library_samples//">Sample Libraries</a>** <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | These sample libraries are used as the base for the other samples.  They are designed to be straightforward implementations of the REST APIs.  They are for use in the samples.  <a href="library_samples/">Details</a>|  <a href="library_samples/Java/ocs_sample_library_preview/">Java</a><br /><a href="library_samples/Python3/">Python3</a>
<img src="../miscellaneous/images/ctp.png" alt="ctp icon">  **<a href="basic_samples/Dataviews/">Dataviews</a>** <img src="../miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | These samples highlight basic operations of Dataviews for OCS, including creation, updating, getting data from and deletion of dataviews.  <a href="basic_samples/Dataviews">Details</a> |  <a href="basic_samples/Dataviews/Java/dataviewjava">Java</a><br /><a href="basic_samples/Dataviews/Python3">Python3</a>|[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=DataviewJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=DataviewPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

For sending OMF to OCS please see the OMF area: <a href="../omf_samples/">omf_samples</a> <br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OCS-Samples)

## Credentials 

A credential config.ini or app.config file is used in the examples unless otherwise noted in the example.  
   

     Note: This is not a secure way to store credentials.  This is to be used at your own risk.  
   
   
   You will need to modify these files locally when you run the samples.

## Request for example 

Please raise an issue if you would like to see a new task, a new example inside of a task, or an existing example in a particular langauge.    

## Contributions

If you wish to contribute please take a look at the [contribution guide](../CONTRIBUTING.md).

## License

[OCS Samples](https://github.com/osisoft/ocs-samples) are licensed under the [Apache 2 license](../LICENSE.md).
