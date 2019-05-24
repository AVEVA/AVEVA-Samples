The sample code in this folder demonstrates how to utilize the PI Web API in R. The sample code is dependent on:
- [Downloading R](https://cran.r-project.org/mirrors.html)
- [Installing httr](https://cran.r-project.org/web/packages/httr/index.html) to work with HTTP and jsonlite for parsing and generating JSON

In order to run this sample, you must configure PI Web API with the proper security to:
- Create an AF database
- Create AF catagories
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

To run the sample script:  
- Open RStudio  
- Open sampleCode.R  
- Click the __Source__ menu option to execute the sample code  

Automated tests are also available to test the above mentioned functionality. You must have already [installed testthat](https://testthat.r-lib.org/) in order to run the tests. Note that the tests must be updated with the appropriate:
- Username  
- Password  
- PI Web API host  
- AF Server  
- PI Data Archive  

To run the unit tests:
- Open RStudio  
- Open run_tests.r  
- Change the test_dir path to the folder in which you placed the R scripts  
    - test_results <- test_dir("c:\\R", env = test_env(), reporter="summary")  
    - Click the __Source__ menu option to execute the sample code  

For the main PI Web API page [ReadMe](../)  
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)