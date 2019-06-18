# Setup

Developed against DotNet 2.2.105.

Replace the placeholders in the [apsettings](./apsettings.json) file with your TenantID, NamespaceId, ClientID and ClientSecret.

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection

### Using Visual Studio

- Load the .csproj
- Rebuild solution
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

----------
[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=UOM_DotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

-----------


Tested against DotNet 2.2.105.

For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)