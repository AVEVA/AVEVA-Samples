﻿using System;
using System.IO;
using Microsoft.Extensions.Configuration;

namespace ClientCredentialFlow
{
    static class Program
    {
        private static IConfiguration _configuration;

        static void Main(string[] args)
        {
            InitConfig();
                
            ClientFlow.OcsUrl = GetConfigValue("OCSUrl");

            var tenantId = GetConfigValue("TenantId");
            var clientId = GetConfigValue("ClientCredentialFlow:ClientId");
            var clientSecret = GetConfigValue("ClientCredentialFlow:ClientSecret");
            ClientFlow.CreateAuthenticatedHttpClient(clientId, clientSecret);

            // Make an HTTP request to OCS using the authenticated client - since this is the first request, the AuthenticationHandler will
            // authenticate and acquire an Access Token and cache it.
            var response = ClientFlow.AuthenticatedHttpClient.GetAsync($"api/Tenants/{tenantId}").Result;
            response.EnsureSuccessStatusCode();
            Console.WriteLine(response.Content.ReadAsStringAsync());
            Console.WriteLine($"HTTP GET api/Tenants/{tenantId} successful");

            // Make another request to OCS - this call should use the cached Access Token.
            response = ClientFlow.AuthenticatedHttpClient.GetAsync($"api/Tenants/{tenantId}/Users").Result;
            response.EnsureSuccessStatusCode();
            Console.WriteLine($"HTTP GET api/Tenants/{tenantId}/Users successful");
        }

        private static void InitConfig()
        {
            try {
                _configuration = new ConfigurationBuilder()
                .AddJsonFile("config.json", optional:false, reloadOnChange:false)
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
            try {
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
            catch(Exception)
            {
                Console.WriteLine($"Configuration issue");
                Environment.Exit(1);
            }

            return "";
        }
    }
}
