# Setup

Developed against DotNet 2.2.300.

1. Replace the placeholders in the [config](./wwwroot/config.js) file with your Tenant Id and Client Id.
2. Ensure that the client contains `http://localhost:5003/callback.html` in the list of RedirectUris

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection
- A web browser
- This application by default will use Port 5003

```
Note: This application is hosted on HTTP.  This is not secure.  You should use a certificate and HTTPS.
```

### Using Visual Studio

- Load the .csproj
- Rebuild project
- Run it
- Pres the *login* button in the browser
- Follow the prompts in the web browser to log in
  - Keep in mind that if you are already logged in with the same account in the browser, you will not have to log in again.

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

- Follow the prompts in the web browser to log in
- Return to the application after having been authenticated in the browser

## Test

[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/OSIsoft_OCS_Samples-CI?branchName=master&jobName=Auth_Implicit_DotNet)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4334&branchName=master)

To test update the appsettings.json to appropriate url for the app, username and password to log in as.  For the test to work, the application must be running previously.  Note the automated tests is only written to work with a personal microsoft account.


To test locally please either set the environmental variable ChromeWebDriver appropriately or update that line of code to use what the location of your Chrome Drive as appropriate in your case (it might be Environment.CurrentDirectory).  


Tested against DotNet 2.2.105.


For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)