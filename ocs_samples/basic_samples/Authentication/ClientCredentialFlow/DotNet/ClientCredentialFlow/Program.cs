using System;
using System.IO;
using Microsoft.Extensions.Configuration;

namespace ClientCredentialFlow
{
    public static class Program
    {
        private static IConfiguration _configuration;

        public static void Main(string[] args)
        {
            InitConfig();

            ClientFlow.OcsUrl = GetConfigValue("Resource");

            var tenantId = GetConfigValue("TenantId");
            var clientId = GetConfigValue("ClientId");
            var clientSecret = GetConfigValue("ClientKey");
            var version = GetConfigValue("ApiVersion");
            ClientFlow.CreateAuthenticatedHttpClient(clientId, clientSecret);

            // Make an HTTP request to OCS using the authenticated client - since this is the first request, the AuthenticationHandler will
            // authenticate and acquire an Access Token and cache it.
            try
            {
                var response = ClientFlow.AuthenticatedHttpClient.GetAsync($"api/{version}/Tenants/{tenantId}/Users").Result;
                response.EnsureSuccessStatusCode();
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
                Console.WriteLine($"HTTP GET api/{version}/Tenants/{tenantId}/Users successful");
            }
            catch (AggregateException ex)
            {
                foreach (var inEx in ex.Flatten().InnerExceptions)
                {
                    Console.WriteLine($"Authentication failed with the following error: {inEx.Message}");
                }
                throw (ex);
            }

            // Make another request to OCS - this call should use the cached Access Token.
            try
            {
                var response = ClientFlow.AuthenticatedHttpClient.GetAsync($"api/{version}/Tenants/{tenantId}/Users").Result;
                response.EnsureSuccessStatusCode();
                Console.WriteLine($"HTTP GET api/{version}/Tenants/{tenantId}/Users successful");
            }
            catch (AggregateException ex)
            {
                foreach(var inEx in ex.Flatten().InnerExceptions)
                {
                    Console.WriteLine($"Authentication failed with the following error: {inEx.Message}");
                }
                throw (ex);
            }
        }

        private static void InitConfig()
        {
            try
            {
                _configuration = new ConfigurationBuilder()
                    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
                    .Build();
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine("Config file missing: " + ex);
                Environment.Exit(1);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error while initiating configuration: " + ex);
                Environment.Exit(1);
            }
        }

        private static string GetConfigValue(string key)
        {
            try
            {
                if (_configuration == null)
                {
                    Console.WriteLine("Config Null");
                    InitConfig();
                }

                var value = _configuration.GetValue<string>(key);

                if (value == null)
                {
                    Console.WriteLine($"Missing the value for \"{key}\" in config file");
                    Environment.Exit(1);
                }

                return value;
            }
            catch (Exception)
            {
                Console.WriteLine($"Configuration issue");
                Environment.Exit(1);
            }

            return "";
        }
    }
}
