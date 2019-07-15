Welcome
========

The SDS client time series samples are introductory, language-specific examples of programming against the SDS Service. They are intended as instructional samples only.


There are some differences between these samples and the Waveform samples.  The differences include the Type being used and some of the calls being highlighted.  Please check out the Sample Pattern of both samples and the code to determine which sample is most appropriate for you.

Note: The calls highlighted here which are not in the other sample are not specific to Time-Series data.

Sample Pattern
--------------

All SDS Time Series samples are console applications that follow the same sequence of events, allowing you to select the langauge with which you are most comfortable without missing any instructional features. The pattern followed is:

1.  Instantiate an SDS client and Obtain an authentication token
2.  Create an SdsType to represent a time value pair
3.  Create SdsStreams to store event data in
4.  Insert data of Simple Type
5.  Create an SdsType to represent a complex type that has 2 values and a timestamp
6.  Create SdsStream to store event data in
7.  Insert data of Complex Type
8.  View window data
9.  View window data after turning on AcceptVerbosity
10. View summary data
11. Do bulk call on stream retreival
12. Delete objects

These steps illustrate the fundamental programming steps of SDS.  Feel free to modify the samples and propose changes.

Step numbers are searchable in the code.  For example to find the relevant part of the code for accepting verbosity: ```step 9```


|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
------|------------
<a href="Python">Python3</a> |  [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDS_TSPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)
<a href="DotNet/Try">DotNet</a> |  [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=SDS_TSDotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)



For the main OCS page [ReadMe](../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
