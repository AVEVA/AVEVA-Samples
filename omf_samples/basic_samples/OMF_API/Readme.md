Welcome
========

These OMF API based samples are introductory, language-specific examples of sending data via OMF. They are intended as instructional samples only.  These samples do use any libraries to make their OMF calls.  

Sample Pattern
--------------

All OMF API samples are console applications that follow the same sequence of events, allowing you to select the langauge with which you are most comfortable without missing any instructional features. The pattern followed is:

1.  Read Configuration from a file (note some configuration is only settable in the code)
2.  Get auth information for endpoint
3.  Create static types (PI Only)
4.  Create dynamic types
5.  Create dynamic types with non-time stamp indicies and multi-key indicies (OCS only)
6.  Create containers
7.  Send static type data (PI Only)
8.  Send link information (PI Only)
9.  Send data 
10. Cleanup topics and containers sent

These steps illustrate common OMF messages to send.  Most OMF sending applications will follow the common paradigm of creating a Type, creating a Container, and then sending Data.  

The samples are based on OMF v1.1. 

The samples are written in a way that the same sample can send to both PI and OCS.  This is controlled by either the crendential file passed in or by an override variable in the program.


NOTE: Automated tests are currently OCS only.

NOTE: The examples for PI are tested against the PI Web API OMF accepting endpoint.  



Configuring OCS or the PI system to accept OMF messages
-----------------------------------------------------

Sending to OCS:
Configure OMF Ingress.  This can be done programmatically, but here are the steps to do it via the OCS portal:

Note: UI is still a work-in-progress, so once that is finalized we will update this with the steps.


Sending to PI:
1) Install PI Web API 2019 (not released currently)
2) Configure OMF endpoint during installation


OMF limitations on OCS and PI
-----------------------------------------------------
This list is not exhuastive, but rather a few key details to know.  

1) PI only accepts DateTime timestamp
2) OCS only accepts Dynamic OMFType classification 
3) OCS does not accept Link type



---------

|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
------|------------
  <a href="OMF_API/">.NET*</a><br /><a href="Python3/">Python3*</a><br /><a href="Java/">Java*</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

----------

For the main OMF page [ReadMe](../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
