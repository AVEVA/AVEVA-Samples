# OCS Samples
OSIsoft Cloud Services ([OCS](https://www.osisoft.com/Solutions/OSIsoft-Cloud-Services/)) is a highly flexible cloud-based platform that provides scalable, elastic,
centralized environment to aggregate data for reporting, advanced analytics, and third-party applications.  OCS is powered by OSIsoft's Sequential Data Store (SDS). In this GitHub repo, we provide samples which will help you get started with the [OCS API](https://ocs-docs.osisoft.com/) against your [OCS instance](https://cloud.osisoft.com/welcome).

There are three types of samples/apps in the repo:

* <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon">  Getting Started - OCS focused samples for a task, usually implemented as a simple console app.  This also includes base libraries that may be used in other apps.

* <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon">   Ingress apps - Real world examples of applications focused on sending data to OCS.  

* <img src="miscellaneous/images/app-type-e2e.png" alt="e2e icon">   End-End apps - Real world examples of web, desktop, mobile, and other applications using OCS data.  

Some tasks and individual language examples may have some additional labels as follows:

* \* denotes that the language example uses the rest API directily instead of a library

* <img src="miscellaneous/images/ctp.png" alt="ctp icon">   This task and code uses services that are currently in preview.  If you are interested in this functionality, please contact OCS support.  



The official OCS samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table:

Task|Description|Languages&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
----|-----------|---------
**Client Credential Authentication**  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the client credential flow of authentication against OCS.  Click here For more  <a href="basic_samples/Authentication/">Details</a> on the various credential patterns. | <a href="basic_samples/Authentication/ClientCredentialFlow/DotNet/ClientCredentialFlow">.NET</a>
**Hybrid Authentication**  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the hybrid flow of authentication against OCS.  Click here For more  <a href="basic_samples/Identity/">Details</a> on the various credential patterns. | <a href="basic_samples/Authentication/HybridFlow/DotNet/HybridFlow">.NET</a>
**Implicit Authentication**  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the implicit flow of authentication against OCS.  Click here For more  <a href="basic_samples/Identity/">Details</a> on the various credential patterns. | <a href="basic_samples/Authentication/ImplicitFlow/DotNet/ImplicitFlow">.NET and JavaScript</a>
**SDS Application** <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers typical operations against the Sds, including creating, updating, and deleting types, streams and events.  This is the recommended starting example, and a good a base for all other Tasks.  <a href="basic_samples/SDS">Details</a> | <a href="basic_samples/SDS/DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a><br /><a href="basic_samples/SDS/DotNet/SdsRestApiCore">.NET*</a><br /><a href="basic_samples/SDS/Java">JAVA</a> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /><a href="basic_samples/SDS/JavaScript/Angular">Angular</a><br /><a href="basic_samples/SDS/JavaScript/NodeJs">nodeJS</a><br /><a href="basic_samples/SDS/Python/SDSPy/Python2">Python2</a><br /><a href="basic_samples/SDS/Python/SDSPy/Python3">Python3</a> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)
**Ingress Management** <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers management operations for Ingress, including creating and deleting publishers, ingress tokens, topics, and subscriptions. | <a href="basic_samples/IngressClientLibraries/DotNet">.NET</a>&nbsp; &nbsp;
**UOM** <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the basic functionality of the UOM system on OCS | <a href="advanced_samples/UomsSample/Dotnet/UomsSample">.NET</a>&nbsp; &nbsp;
**Local OS Performance monitoring** <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> |  In this sample we show how to create, add and read data from a stream.  The data is obtained from the OS using Performance monitors. | <a href="advanced_samples/PerfmonSample/DotNet/PerfmonSample/">.NET</a><br /><a href="advanced_samples/PerfmonSample/Python3/">Python3</a>&nbsp; &nbsp;
**PIToOCS Historical** <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon"> | The project is a complete (very simple) command line application that takes a PIPoint name search mask (e.g. sinu*), a start time and an endtime and writes all the data found for the points and time range into OCS. | <a href="advanced_samples/PIToOcsOmfSample/Dotnet/">.NET</a>&nbsp; &nbsp;
**PIToOCS Snapshot** <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon"> | This samples sends snapshot values from PI to OCS via OMF. | <a href="advanced_samples/PItoOCSviaAPISample/DotNet">.NET*</a>&nbsp; &nbsp;


## Credentials 

A credential config.ini or app.config file is used in the examples unless otherwise noted in the example.  
   

     Note: This is not a secure way to store credentials.  This is to be used at your own risk.  
   
   
   You will need to modify these files locally when you run the samples.

## Request for example 

Please raise an issue if you would like to see a new task, a new example inside of a task, or an existing example in a particular langauge.    

## Contributions

If you wish to contribute please take a look at the [contribution guide](CONTRIBUTING.md).

## License

[OCS Samples](https://github.com/osisoft/ocs-samples) are licensed under the [Apache 2 license](LICENSE.md).
