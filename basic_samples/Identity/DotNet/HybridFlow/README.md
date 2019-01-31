# Setup

1. Replace the placeholders in the [config](./config.json) file with your TenantID, ClientID and ClientSecret
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

1. Load the solution from the directory above this in Visual Studio
2. Rebuild solution
3. Select HybridFlow project
4. Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode
5. Follow the prompts in the web browser to log in
  - Keep in mind that if you are already logged in with the same Account in the browser, you will not have to log in again
6. Return to the application after having been authenticated in the browser

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

- Follow the prompts in the web browser to log in
- Return to the application after having been authenticated in the browser