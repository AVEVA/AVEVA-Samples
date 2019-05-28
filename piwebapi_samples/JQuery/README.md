The sample code in this folder demonstrates how to utilize the PI Web API in jQuery. You must have already [downloaded jQuery](https://jquery.com/download/) in order to run this sample application.


Getting Started
------------

To run the sample code:
- The sample code was developed to run in the Chrome browser
- Clone the GitHub repository
- Open Visual Studio Code  
- Open the folder in which you placed the code
- Open the file: launch.json
- Search for the text "url":, change this to the path to index.html. For example: "url": "file:///C:/PI Web API/JQuery/index.html",
- Click "Start Debugging" on the Debug menu


Getting Started with Tests
------------

To run the sample tests:
- You must have already [installed Karma](https://karma-runner.github.io/latest/index.html) in order to run automated tests.
- Open the file: samplePIWebAPI.js
- Search for the text "var configDefaults"
- Change the text for PIWebAPIUrl, add your PI Web API Url.  For example:  'PIWebAPIUrl': 'https://mydomain.com/piwebapi',
- Change the text for AssetServer, add your Asset Server Name.  For example:  'AssetServer': 'AssetServerName',
- Change the text for PIServer, add your PI Server Name.  For example:  'PIServer': 'PIServerName'
- Change the text for Name, add your PI Web API user name.  For example:  'Name': 'MyUserName',
- Change the text for Password, add your PI Web API user password.  For example:  'Password': 'MyUserPassword'
- Change the text for AuthType, add your PI Web API authentication method (Basic or Kerberos).  For example:  'AuthType': 'Basic',
- Open the file: launch.json
- Search for the text "url":, change this to the path to SpecRunner.html. For example: "url": "file:///C:/PI Web API/JQuery/JasmineUnitTests/SpecRunner.html",
- Click "Start Debugging" on the Debug menu

System Configuration
----------------------------

In order to run this sample, you must configure PI Web API with the proper security to:
- Create an AF database
- Create AF categories
- Create AF templates
- Create AF elements with attributes
- Create PI Points associated with element attributes
- Write and read element attributes
- Delete all the above AF/PI Data Archive objects  

In addition, PI Web API must be configured to allow CORS as follows:  

|Attribute|Value 
------|------------
CorsExposedHeaders|Allow,Content-Encoding,Content-Length,Date,Location  
CorsHeaders|*  
CorsMethods|*  
CorsOrigins|*  
CorsSupportsCredentials|True  
DisableWrites|False  

Functionality
------------

This sample shows basic functionality of the PI Web API, not every feature. The sample is meant to show a basic sample application that uses the PI Web API to read and write data to a PI Data Archive and AF. Tests are also included to verify that the code is functioning as expected.

The functionality included with this sample includes(recommended order of execution):
- Create an AF database
- Create a category
- Create an element template
- Create an element and associate the element's attributes with PI tags where appropriate
- Write a single value to the attribute
- Write a 100 values to an attribute
- Perform a Batch (6 steps in 1 call) operation which includes:  
  - Get the sample tag  
  - Read the sample tag's snapshot value  
  - Read the sample tag's last 10 recorded values  
  - Write a value to the sample tag  
  - Write 3 values to the sample tag  
  - Read the last 10 recorded values from the sample tag only returning the value and timestamp
- Return all the values over the last 2 days
- Return timestamp and values over the last 2 days  
- Delete the element
- Delete the element template
- Delete the sample database

[![Build Status](https://osisoft.visualstudio.com/NOC/_apis/build/status/PI%20Web%20API%20(JQuery)?branchName=dev)](https://osisoft.visualstudio.com/NOC/_build/latest?definitionId=4624&branchName=dev)   

For the main PI Web API page [ReadMe](../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)