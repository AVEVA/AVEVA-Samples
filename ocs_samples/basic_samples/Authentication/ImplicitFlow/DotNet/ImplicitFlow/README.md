# Setup

1. Replace the placeholders in the [config](./wwwroot/config.js) file with your TenantID and ClientID.
2. Ensure that the client contains `http://localhost:5003/callback.html` in the list of RedirectUris

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection
- A web browser

### Using Visual Studio

- Load the solution from the directory above this in Visual Studio
- Rebuild solution
- Select ImplicitFlow project
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



For the general steps or switch languages see the Task  [ReadMe](../../../)<br />
For the main OCS page [ReadMe](../../../../../)<br />
For the main landing page on master [ReadMe](https://github.com/osisoft/OCS-Samples)