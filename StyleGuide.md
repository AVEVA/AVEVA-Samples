# General Style Guide

## Organization

* For each different technology (for instance OCS, PI Web API) there is a main landing page.
* Each sample is represented on the main landing page for the technology with an appropriate short task name, description including a link to a greater description, links to the individual samples marked by languages, and test status.
* A task level description should include information that is common to all language specific examples below it, including common steps.  This should also include links back to the main page, to all languages and highlight test status of these languages.
* A language specific readme should include information that is unique to this language.  This can include stepping over line examples from the sample with reference back to the general steps.  This readme should also include links back to the main technology page, to the general task readme, and the specific test status.


## Code expectations

* Samples highlight a specific task a person can accomplish.  It can include multiple related tasks.
* The sample should be self contained, setting up and cleaning up after itself as possible.  Anything that is needed in setup of the system needs to be well documented in readme and in code including how to do it.  
* The code follows OSIsoft and industry best practices in design and code style.
* Automated tests are included that check to ensure the sample runs as expected on a clean system, including making sure intermediate results in the sample are as expected.
* Comments are included in the code to help developers understand any interaction that isn't otherwise documented in the code or intellisense help of functions.
* Samples are repeated in various programming languages as appropriate.
* The library samples include functions that are reused across samples. 
* If the task level description includes common steps for the various language samples, each language sample explicitly marks where the steps are in the code.
* Samples (including the sample libraries) do not necessarily go over every possible setting and every endpoint of a service (documentation is there for this).  Samples are to highlight specifc tasks.


