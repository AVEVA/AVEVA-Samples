Using the OCS Dataview Service in JAVA
==================================================================

The sample code in this demonstrates how to invoke Dataview REST APIs via the sample JAVA client [library]( https://github.com/osisoft/OSI-Samples/tree/master/library_samples/Java/ocs_sample_library_preview ). 
By examining the code, you will see how to establish a connection 
to SDS, obtain an authorization token, create an  SdsType and  SdsStream with data (if needed), 
create a Dataview, update it, retreive it, and retrieve data from it a couple of different ways.  
At the end everything that was created is deleted. 




Summary of steps to run the Java demo
--------------------------------------
Using Eclipse or any IDE:

1. Clone a local copy of the GitHub repository.

2. Install Maven.

3. *Install the ocs_sample_library_preview to your local Maven repo using run mvn install pom.xml from \\library_samples\\Java\\ocs_sample_library_preview\\

4. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.

5. Replace the configuration strings in ``config.properties``


Using a command line:

1. Clone a local copy of the GitHub repository.

2. Download apache-maven-x.x.x.zip from http://maven.apache.org and extract it.

3. Setting environment variables.
   a) For Java JDK
      Variable name - JAVA_HOME
      Variable value - location to the Java JDK in User variables.

      and, also add JDK\bin path to the Path variable in System variables.

   b) For Maven
      Variable name - MAVEN_HOME
      Variable value - location to the extracted folder for the
                       maven ~\apache-maven-x.x.x in User variables.

      and, also add ~\apache-maven-x.x.x\bin path to the Path variable in System variables.

4. *Install the  ocs_sample_library_preview to your local Maven repo using run mvn install pom.xml from \library_samples\Java\ocs_sample_library_preview\

5. Building and running the project.
   a) cd to your project location.
   b) run "mvn package exec:java" on cmd.

*Currently this project is not hosted on the central Maven repo and must be compiled and installed locally.

-------------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=DataviewJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

---------

Tested against Maven 3.6.1 and Java 1.8.0_212.

For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OCS page [ReadMe](../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)