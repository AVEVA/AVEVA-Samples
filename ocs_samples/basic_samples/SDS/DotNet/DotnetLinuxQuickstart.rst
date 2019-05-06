Quick Start .NET Core on Linux
==============================

SDS Client Libraries are Portable
--------------------------------

The .NET SDS Client Libraries example was built using .NET Core.  This allows the application
to be built and run against a number of different platforms including Windows, macOS and Linux.  
For those who are relatively new to working with Linux or .NET Core this quick start provides a 
straight forward example of how to configure your environment and quickly get the sample code
built and running. 

Microsoft Documentation
-----------------------

This example is configured to run on an Ubuntu 16.04 operating system, readers of this example 
should refer to the following Microsoft documentation to configure their environment: 

https://docs.microsoft.com/en-us/dotnet/core/linux-prerequisites?tabs=netcore2x 

Specifically, in the command sequence below the first command prints the distribution information, i.e. your OS.
Use the output of this command to choose the appropriate environment, e.g. Ubuntu, Fedora, etc.
in the Microsoft documentation.  This will in turn change the value of your fifth command.  

Version Considerations
----------------------

.NET Core is currently split into two major versions, 1x and 2x.  This example targets .NET Core 2.x.  If you wish to 
use the .NET Core 1.x version you will need to make changes to sudo apt-get install dotnet-sdk-2.1.3 command in the sequence
as well as the SdsClientLibrariesCore.csproj file within the project directory.   

Command Sequence 
-----------------

The following command sequence demonstrates the minimum configuration and execution steps needed to run the 
SdsClientLibrariesCore project on a new installation of Ubuntu 16.04, users should make appropriate changes for
other platforms.  Additionally, as with all of the sample code, the TenantId, NamespaceId and Access Key settings 
will need to be specified, this step is shown here by opening the appsettings.json file with the Nano file editor. 

::

	lsb_release -a 
	sudo apt-get install curl
	curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
	sudo apt-get update
	sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-xenial-prod xenial main" > /etc/apt/sources.list.d/dotnetdev.list'
	sudo apt-get update
	sudo apt-get install dotnet-sdk-2.1.3
	sudo apt-get install git
	sudo git clone https://github.com/osisoft/OSI-Samples
	cd OSI-Samples/basic_samples/SDS/DotNet/SdsClientLibraries/SdsClientLibraries
	sudo nano appsettings.json
	sudo dotnet publish
	sudo dotnet run bin/Debug/netcoreapp2.0/publish/SdsClientLibrariesCore.dll 


Further reading
---------------

The following links are provided for those that would like further information regarding .NET Core, the Linux command line 
or the Nano text editor:

https://docs.microsoft.com/en-us/dotnet/core/

https://help.ubuntu.com/community/UsingTheTerminal

https://www.nano-editor.org/dist/v2.9/nano.html
