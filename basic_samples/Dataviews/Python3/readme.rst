Building a Python client to make calls to the Dataview Service
==================================================================

The sample code in this demonstrates how to invoke Dataview REST APIs via the sample Python client library. 
By examining the code, you will see how to establish a connection 
to SDS, obtain an authorization token, create an  SdsType and  SdsStream with data (if needed), 
create a Dataview, update it, retreive it, and retrieve data from it a couple of different ways.  
At the end everything that was created is deleted. 


	
To Run this Sample:
-------------------
1. Clone the GitHub repository
2. Install required modules: ``pip install -r requirements.txt``
3. Open the folder with your favorite IDE
4. Update ``config.ini`` with the credentials provided by OSIsoft
5. Run ``program.py``

