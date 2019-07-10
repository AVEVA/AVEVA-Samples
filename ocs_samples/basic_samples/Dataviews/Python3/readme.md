Using the OCS Dataview Service in Python
==================================================================

The sample code in this demonstrates how to invoke Dataview REST APIs via the sample Python client [library]( https://github.com/osisoft/OSI-Samples/tree/master/library_samples/Python3/ocs_sample_library_preview ). 
By examining the code, you will see how to establish a connection 
to SDS, obtain an authorization token, create an  SdsType and  SdsStream with data (if needed), 
create a Dataview, update it, retreive it, and retrieve data from it a couple of different ways.  
At the end everything that was created is deleted. 

This example uses the ocs_sample_library_preview library which is also included in this github repo.  It is downloadable via pip.

	
Developed against Python 3.7.2.

To Run this Sample:
-------------------
1. Clone the GitHub repository
2. Install required modules: ``pip install -r requirements.txt``
3. Open the folder with your favorite IDE
4. Update ``config.ini`` with the credentials provided by OSIsoft
5. Run ``program.py``



To test the sample after running it:
1. Run ``python test.py``

or

1. Install pytest ``pip install pytest``
2. Run ``pytest program.py``


-------------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=DataviewPy)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

-----------



 Automated test uses Python 3.6.8 x64


For the general steps or switch languages see the Task  [ReadMe](../)<br />
For the main OCS page [ReadMe](../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)