# Welcome to the testing guide!

For OSI Samples testing we are concerned with testing the samples to ensure that each sample works completely and as expected with no errors. We check final and intermittant results in the samples to ensure the results are as expected. The goal for the tests is to ensure a level of confidence of operation in each sample. We test to make sure that the sample is working and running as expected on a clean system, so that a user of a sample knows they have a good starting base to learn from.

The way the tests are run can be found by looking at the Continuous Integration pipeline as defined by the file [azure-pipelines](azure-pipelines.yml). Note that some jobs are run on OSIsoft hosted test agents; this is intended to simplify security for the automated tests since the test agent is inside our domain. However, with proper security for a computer and PI Web API, it is possible to make it safe to open a server to the internet. To see what is deployed on the OSIsoft hosted test agents see the [on prem testing](miscellaneous/ON_PREM_TESTING.md) document.

Test against OCS (including OMF tests to OCS) are on every PR and every update to the master branch.

Tests can also be run manually. Steps for running a test manually locally is noted in the specific sample readme, but also can be found by inspecting the .yml files.

Unless otherwise noted in the sample readme, all tests have these basic assumptions:

- All noted expections and requirements in the sample readme are followed
- The azure-pipelines jobs specifying a `vmImage` use Microsoft hosted agents to run the tests
- The azure-pipelines jobs specifying a `name` and `demands` use OSIsoft-hosted agents to run the tests
