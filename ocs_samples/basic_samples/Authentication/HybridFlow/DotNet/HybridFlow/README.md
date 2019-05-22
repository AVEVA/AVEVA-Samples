# Setup

1. Replace the placeholders in the [appsettings](./appsettings.json) file with your TenantID, ClientID and ClientSecret
2. Ensure that this client was created to allow Refresh Tokens
  - If this client does not allow refresh tokens, no refresh token will be issued upon authentication
3. Ensure that the client contains $"{RedirectHost}:{RedirectPort}/{RedirectPath}" in the list of RedirectUris
  - Default value from config is: `http://127.0.0.1:54567/signin-oidc`
  - You can change the values to match your preferences

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection
- A web browser

### Using Visual Studio

1. Load the .csproj
2. Rebuild solution
3. Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode
4. Follow the prompts in the web browser to log in
  - Keep in mind that if you are already logged in with the same Account in the browser, you will not have to log in again
5. Return to the application after having been authenticated in the browser

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

- Follow the prompts in the web browser to log in
- Return to the application after having been authenticated in the browser


## Test

[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=Auth_Hybrid_DotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

To  test autonomously using the test project, update your appsettings.json with you password and userName to login in as.   Note the automated tests is only written to work with a personal microsoft account.




For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)