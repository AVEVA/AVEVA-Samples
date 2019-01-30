# Setup

Replace the placeholders in the [config](./config.json) file with your TenantID, ClientID and ClientSecret.

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection
- A web browser

### Using Visual Studio

- Load the solution from the directory above this in Visual Studio
- Select HybridFlow project
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode
- Follow the prompts in the web browser to log in
  - Keep in mind that if you are already logged in with the same Account in the browser, you will not have to log in again.
- Return to the application after having been authenticated in the browser

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```
- Follow the prompts in the web browser to log in
- Return to the application after having been authenticated in the browser

