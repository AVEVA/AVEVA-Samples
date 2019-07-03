# Client Credential Flow Sample and Test

This client uses the OAuth2/OIDC Client Credential Flow to obtain an access token. See the root folder [README](../../../README.md) for more information about this flow.

## Requirements

- .Net Core 2.2.1 or later

Replace the placeholders in the [apsettings](./apsettings.json) file with your Tenant Id, Client Id and Client Secret, and the current Api Version. There is no need to replace the Namespace Id for this sample.

Developed against DotNet 2.2.105.

## Running the sample

### Prerequisites

- Register a Client Credential client in OCS.
- Replace the placeholders in the [appsettings](./appsettings.json)  file with your Tenant Id, Client Id, and Client Secret obtained from registration.

### Using Visual Studio

- Load the .csproj
- Rebuild project
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode

### Using Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

## Running the automated test

### Using Visual Studio 
 
- Load the .csproj from the ClientCredentialFlowTest directory above this in Visual Studio
- Rebuild project
- Open Test Explorer and make sure there is one test called Test1 showing
- Run the test

### Using Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of the ClientCredentialFlowTest project:

```shell
dotnet test
```

&nbsp;

[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=Auth_CC_DotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

Tested against DotNet 2.2.105.

For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)