using System;
using System.Net.Http;
using OSIsoft.Identity;

namespace ClientCredentialFlow
{
    public static class ClientFlow
    {
        private static string _ocsUrl;

        public static string OcsUrl
        {
            set => _ocsUrl = value;
        }

        public static HttpClient AuthenticatedHttpClient { get; private set; }

        public static void CreateAuthenticatedHttpClient(string clientId, string clientSecret)
        {
            Console.WriteLine("+-------------------------------------+");
            Console.WriteLine("|  Sign in with Client Credentials    |");
            Console.WriteLine("+-------------------------------------+");
            Console.WriteLine("");

            AuthenticatedHttpClient = new HttpClient(InitiateAuthenticationHandler(clientId, clientSecret))
            {
                BaseAddress = new Uri(_ocsUrl)
            };
        }

        private static AuthenticationHandler InitiateAuthenticationHandler(string clientId, string clientSecret)
        {
            // Create an instance of the AuthenticationHandler.
            return new AuthenticationHandler(new Uri(_ocsUrl), clientId, clientSecret)
            {
                InnerHandler = new HttpClientHandler()
                {
                    AllowAutoRedirect = false,
                }
            };
        }
    }
}
