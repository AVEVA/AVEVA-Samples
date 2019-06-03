using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using static System.Int32;

namespace HybridFlow
{
    static class Program
    {
        private static IConfiguration _configuration;

        /// <summary>
        /// Authorization header name.
        /// </summary>
        private const string AuthorizationHeaderName = "Authorization";

        static void Main(string[] args)
        {
            InitConfig();

            HybridFlow.OcsUrl = GetConfigValue("OCSUrl");
            HybridFlow.RedirectHost = GetConfigValue("HybridFlow:RedirectHost");
            HybridFlow.RedirectPort = Parse(GetConfigValue("HybridFlow:RedirectPort"));
            HybridFlow.RedirectPath = GetConfigValue("HybridFlow:RedirectPath");

            var tenantId = GetConfigValue("TenantId");
            var clientId = GetConfigValue("HybridFlow:ClientId");
            var clientSecret = GetConfigValue("HybridFlow:ClientSecret");
            var scope = GetConfigValue("HybridFlow:Scope");

            // Get access token and refresh token.
            var (accessToken, refreshToken, expiration) =
                HybridFlow.GetHybridFlowAccessToken(clientId, clientSecret, scope, tenantId);
            Console.WriteLine("Access Token: " + accessToken);
            var refreshStatus = !string.IsNullOrEmpty(refreshToken) ? refreshToken : "No refresh token requested";
            Console.WriteLine("Refresh Token: " + refreshStatus);
            Console.WriteLine("Expires: " + expiration);

            //  Make a request to GetTenant endpoint
            Console.WriteLine(GetRequest($"{GetConfigValue("OCSUrl")}/api/Tenants/{tenantId}", accessToken).Result
                ? "Request succeeded"
                : "request failed");


            // Check if offline_access scope has been requested. This scope can be requested for hybrid clients
            // that have been created with AllowRefreshToken option set to true, which is also the default option.
            if (scope.Contains("offline_access"))
            {
                // Get a new access token from a refresh token. If the previous access token has not expired it can still be used.
                // This will also reissue a new refresh token. Old refresh token will no longer be valid after use.
                (accessToken, refreshToken, expiration) =
                    HybridFlow.GetAccessTokenFromRefreshToken(refreshToken, clientId, clientSecret);
                Console.WriteLine("Access Token: " + accessToken);
                Console.WriteLine("Refresh Token: " + refreshToken);
                Console.WriteLine("Expires: " + expiration);
            }
            else
            {
                Console.WriteLine("No refresh token requested.");
            }


            //  Make a request to GetTenant endpoint
            Console.WriteLine(GetRequest($"{GetConfigValue("OCSUrl")}/api/Tenants/{tenantId}", accessToken).Result
                ? "Request succeeded"
                : "request failed");
        }

        private static async Task<bool> GetRequest(string endpoint, string accessToken)
        {
            Console.WriteLine("Make request: ");
            var request = new HttpRequestMessage()
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri(endpoint),
            };

            // Attach  the access token to the Authorization header in the HTTP request.
            request.Headers.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            try
            {
                using (var client = new HttpClient())
                {
                    var response = await client.SendAsync(request);
                    response.EnsureSuccessStatusCode();

                    // Uncomment this line to get the results of the calls
                    //var responseBodyJson = JsonConvert.SerializeObject(response.Content.ReadAsStringAsync().Result, Formatting.Indented);
                    //Console.WriteLine(responseBodyJson);

                    return true;
                }
            }
            catch (HttpRequestException)
            {
                return false;
            }
        }

        private static void InitConfig()
        {
            try
            {
                _configuration = new ConfigurationBuilder()
                    .AddJsonFile("config.json", optional: false, reloadOnChange: false)
                    .Build();
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("Config file missing");
                Environment.Exit(1);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error while initiating configuration: " + ex.ToString());
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

                if (value != null) return value;
                Console.WriteLine($"Missing the value for \"{key}\" in config file");
                Environment.Exit(1);

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
