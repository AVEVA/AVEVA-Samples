# Setup

Replace the placeholders in the [config](./config.json) file with your Tenant Id, Client Id and Client Secret.

## Running the sample

### Requirements

- .net core 2.2.1 or later
- Reliable internet connection

### Using Visual Studio

- Load the solution from the directory above this in Visual Studio
- Rebuild solution
- Select ClientCredentialFlow project
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```