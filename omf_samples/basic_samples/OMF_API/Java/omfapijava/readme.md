Building a Java client to send OMF to PI or OCS
==================================================================

The sample code in this topic demonstrates how to send OMF messages
using Java.




Summary of steps to run the Java demo
--------------------------------------
Using Eclipse or any IDE:

1. Clone a local copy of the GitHub repository.

2. Install Maven.

3. If you are using Eclipse, select ``File`` > ``Import`` >
   ``Maven``> ``Existing maven project`` and then select the local
   copy.

4. Replace the configuration strings in ``config.properties``


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


4. Building and running the project.
   a) cd to your project location.
   b) run "mvn package exec:java" on cmd.

----------

[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=OMF_APIJava)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

---------


For the general steps or switch languages see the Task  [ReadMe](../../)<br />
For the main OMF page [ReadMe](../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OCS-Samples)