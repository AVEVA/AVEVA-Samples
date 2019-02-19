# OCS Samples
OSIsoft Cloud Services ([OCS](https://www.osisoft.com/Solutions/OSIsoft-Cloud-Services/)) is a highly flexible cloud-based platform that provides scalable, elastic,
centralized environment to aggregate data for reporting, advanced analytics, and third-party applications.  OCS is powered by OSIsoft's Sequential Data Store (SDS). In this GitHub repo, we provide samples which will help you get started with the [OCS API](https://ocs-docs.osisoft.com/) against your [OCS instance](https://cloud.osisoft.com/welcome).

There are three types of samples/apps in the repo:

* <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon">  Getting Started - OCS focused samples for a task, usually implemented as a simple console app.  This also includes base libraries that may be used in other apps.

* <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon">   Ingress apps - Real world examples of applications focused on sending data to OCS.  

* <img src="miscellaneous/images/app-type-e2e.png" alt="e2e icon">   End-End apps - Real world examples of web, desktop, mobile, and other applications using OCS data.  

Some tasks and individual language examples may have some additional labels as follows:

\* denotes that the language example uses the rest API directily instead of a library

* <img src="miscellaneous/images/ctp.png" alt="ctp icon">   This task and code uses services that are currently in preview and may not be available without contacting OCS support.  



The official OCS samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table:



<table>
 <tr>
   <td width="25%">
      <h3><b>Task</b></h3>
  </td>
  <td>
      <h3 width="35%"><b>Description</b></h3>
  </td>
  <td>
      <h3><b>Languages</b></h3>
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>Client Credential Authentication  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
    Covers the client credential flow of authentication against OCS.  Click here For more  <a href="basic_samples/Authentication/">Details</a> on the various credential patterns. 
  </td>
    <td>
     <a href="basic_samples/Authentication/ClientCredentialFlow/DotNet/ClientCredentialFlow">.NET</a>
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>Hybrid Authentication  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
    Covers the hybrid flow of authentication against OCS.  Click here For more  <a href="basic_samples/Identity/">Details</a> on the various credential patterns. 
  </td>
    <td>
     <a href="basic_samples/Authentication/HybridFlow/DotNet/HybridFlow">.NET</a>
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>Implicit Authentication  <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
    Covers the implicit flow of authentication against OCS.  Click here For more  <a href="basic_samples/Identity/">Details</a> on the various credential patterns. 
  </td>
    <td>
     <a href="basic_samples/Authentication/ImplicitFlow/DotNet/ImplicitFlow">.NET and JavaScript</a>
  </td>
 </tr>
 
 <tr>
   <td width="25%">
      <h3>SDS Application <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
    Covers typical operations against the Sds, including creating, updating, and deleting types, streams and events.  This is the recommended starting example, and a good a base for all other Tasks.  <a href="basic_samples/SDS">Details</a>
  </td>
    <td>
     <a href="basic_samples/SDS/DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/DotNet/SdsRestApiCore">.NET*</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/Java/sdsjava">JAVA</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/JavaScript/Angular">Angular</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/JavaScript/NodeJs">nodeJS</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/Python/SDSPy/Python2">Python2</a>&nbsp; &nbsp;
     <a href="basic_samples/SDS/Python/SDSPy/Python3">Python3</a>&nbsp; &nbsp;
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>Ingress Management <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
    Covers management operations for Ingress, including creating and deleting publishers, ingress tokens, topics, and subscriptions.  
  </td>
  <td>
     <a href="basic_samples/IngressClientLibraries/DotNet">.NET</a>&nbsp; &nbsp;
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>UOM <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
  Covers the basic functionality of the UOM system on OCS
  </td>
  <td>
     <a href="advanced_samples/UomsSample/Dotnet/UomsSample">.NET</a>&nbsp; &nbsp;
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>Local OS Performance monitoring <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"></h3>
  </td>
  <td width="35%">
  In this sample we show how to create, add and read data from a stream.  The data is obtained from the OS using Performance monitors.
  </td>
  <td>
     <a href="advanced_samples/PerfmonSample/DotNet/PerfmonSample/">.NET</a>&nbsp; &nbsp;
     <a href="advanced_samples/PerfmonSample/Python3/">Python3</a>&nbsp; &nbsp;
  </td>
 </tr>
 
 <tr>
   <td width="25%">
      <h3>PIToOCS Historical
 <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon"></h3>
  </td>
  <td width="35%">
The project is a complete (very simple) command line application that takes a PIPoint name search mask (e.g. sinu*), a start time and an endtime and writes all the data found for the points and time range into OCS.

  </td>
  <td>
     <a href="advanced_samples/PIToOcsOmfSample/Dotnet/">.NET</a>&nbsp; &nbsp;
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3>PIToOCS Snapshot
 <img src="miscellaneous/images/app-type-ingress.png" alt="ingress icon"></h3>
  </td>
  <td width="35%">
This sample sends snapshot values from PI to OCS via OMF.
  </td>
  <td>
     <a href="advanced_samples/PItoOCSviaAPISample/DotNet">.NET*</a>&nbsp; &nbsp;
  </td>
 </tr>
 <tr>
   <td width="25%">
      <h3> <img src="miscellaneous/images/ctp.png" alt="ctp icon">  Dataviews <img src="miscellaneous/images/app-type-getting-started.png" alt="getting-started icon">
      </h3>
  </td>
  <td width="35%">
These samples highlight basic operations of Dataviews for OCS, including creation, updating, getting data from and deletion of dataviews.  <a href="basic_samples/Dataviews">Details</a>
  </td>
  <td>
     <a href="basic_samples/Dataviews/Python3">Python3</a>&nbsp; &nbsp;
  </td>
 </tr>
 </table>
 
## Credentials 

A credential config.ini or app.config file is used in the examples unless otherwise noted in the example.  
   

     Note: This is not a secure way to store credentials.  This is to be used at your own risk.  
   
   
   You will need to modify these files locally when you run the samples.

## Request for example 

Please raise an issue if you would like to see a new task, a new example inside of a task, or an existing example in a particular langauge.    

## License

[OCS Samples](https://github.com/osisoft/ocs-samples) are licensed under the [Apache 2 license](LICENSE.md).
