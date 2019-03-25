Welcome
========

The Basic SDS Client samples are introductory, language-specific examples of programming against the SDS Service. They are intended as instructional samples only.

Sample Pattern
--------------

All basic SDS samples are console applications that follow the same sequence of events, allowing you to select the langauge with which you are most comfortable without missing any instructional features. The pattern followed is:

1.  Instantiate an SDS client and Obtain an authentication token
2.  Create an SdsType to represent the data being stored
3.  Create an SdsStream to store event data in
4.  Create and insert events into the stream
5.  Retrieve events for a specified range
6.  Retrieve events in table format with headers
7.  Update events
8.  Replace events
9.  Retrieve events and interpolated events 
10. Retrieve filtered events 
11. Demonstrate SdsStream Property Overrides
12. Use SdsStreamViews and SdsStreamViewMaps
13. Use SdsStreamViews to update StreamType
14. Filtering on types 
15. Tags & Metadata
16. Delete events
17. Create an SdsStream with a secondary index, update an existing stream to a secondary index and remove a secondary index
18. Created an SdsType and SdsStream with Compound index
19. Inserting and retreiving compound index data
20. Delete metadata objects

These steps illustrate the fundamental programming steps of SDS.  Feel free to modify the samples and propose changes.

Step numbers are searchable in the code.  For find the relevant part of the code for filtering on types search: Step 14


|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
------|------------
<a href="DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a><br /><a href="/DotNet/SdsRestApiCore">.NET*</a><br /><a href="/Java/sdsjava">JAVA</a><br /><a href="/JavaScript/Angular">Angular</a><br /><a href="/JavaScript/NodeJs">nodeJS</a><br /><a href="/Python/SDSPy/Python2">Python2</a><br /><a href="/Python/SDSPy/Python3">Python3</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDSDotNetAPI)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master) <br /> <br /> <br /> <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/Engineering%20Incubation-CI?branchName=master&jobName=SDSPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)



Note: Currently the Angular, nodeJS, Pyhton2, and Python 3 examples are missing some steps, and searchability on step numbers.  This is coming soon!

For the main OCS page [ReadMe](../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OCS-Samples)