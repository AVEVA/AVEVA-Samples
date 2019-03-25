Welcome
========

These OMF API based are introductory, language-specific examples of sending data via OMF. They are intended as instructional samples only.

Sample Pattern
--------------

All basic OMF samples are console applications that follow the same sequence of events, allowing you to select the langauge with which you are most comfortable without missing any instructional features. The pattern followed is:

1.  Read Configuration from a file (note some configuration is only settable in the code)
2.  Get auth information for endpoint
3.  Create static types (PI Only)
4.  Create dynamic types
5.  Create dynamic types with non-time stamp indicies and multi-key indicies (OCS only)
6.  Create containers
7.  Send static type data (PI Only)
8.  Send link information (PI Only)
9.  Send data 
10.  Cleanup topics and containers sent

These steps illustrate common OMF messages to send.  Feel free to modify the samples and propose changes.

NOTE: Automated tests are currently OCS only.
NOTE: The examples for PI are not manually tested against the PI Connector Relay.  


---------

|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
------|------------
  <a href="OMF_API/">.NET*</a><br /><a href="Python3/">Python3*</a><br /><a href="Java/">Java*</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

----------

For the main OMF page [ReadMe](../)
For the main landing page [ReadMe](.../)