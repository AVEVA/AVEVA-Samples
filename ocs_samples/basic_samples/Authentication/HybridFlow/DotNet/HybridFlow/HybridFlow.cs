using System;
using System.Net.Http;
using System.Threading.Tasks;
using IdentityModel.Client;
using IdentityModel.OidcClient;

namespace HybridFlow
{
    public static class HybridFlow
    {
        private static OidcClient _oidcClient;
        private static string _ocsIdentityUrl;
        private static string _redirectHost;
        private static int _redirectPort;
        private static string _redirectPath;
        private const string Authority = "https://identity.osisoft.com";

        public static string OcsUrl
        {
            set => _ocsIdentityUrl = value + IdentityResourceSuffix;
        }

        public static string RedirectHost
        {
            set => _redirectHost = value;
        }

        public static int RedirectPort
        {
            set => _redirectPort = value;
        }

        public static string RedirectPath
        {
            set => _redirectPath = value;
        }

        /// <summary>
        /// Identity resource suffix.
        /// </summary>
        private const string IdentityResourceSuffix = "/identity";

        public static (string, string, DateTime) GetHybridFlowAccessToken(string clientId, string clientSecret,
            string scope, string tenantId)
        {
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("|  Sign in with OIDC    |");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("");

            LoginResult loginResult = null;
            do
            {
                if (loginResult != null)
                {
                    Console.WriteLine(loginResult.Error);
                    return ("", "", DateTime.Now);
                }

                Console.WriteLine("Prompting for login via a browser...");
                loginResult = SignIn(clientId, clientSecret, scope, tenantId).Result;
            } while (loginResult.IsError);


            return (loginResult.AccessToken, loginResult.RefreshToken, loginResult.AccessTokenExpiration.ToLocalTime());
        }

        private static async Task<ProviderInformation> GetProviderInformation()
        {
            // Discover endpoints from metadata.
            using (HttpClient client = new HttpClient())
            {
                // Create a discovery request
                var discoveryDocumentRequest = new DiscoveryDocumentRequest
                {
                    Address = _ocsIdentityUrl,
                    Policy = new DiscoveryPolicy
                    {
                        ValidateIssuerName = false
                    }
                };

                var discoveryResponse =
                    await client.GetDiscoveryDocumentAsync(discoveryDocumentRequest);

                return discoveryResponse.IsError
                    ? throw new Exception($"Error while getting the discovery document: {discoveryResponse.Error}")
                    : new ProviderInformation()
                    {
                        IssuerName = discoveryResponse.Issuer,
                        KeySet = discoveryResponse.KeySet,
                        AuthorizeEndpoint = discoveryResponse.AuthorizeEndpoint,
                        TokenEndpoint = discoveryResponse.TokenEndpoint,
                        EndSessionEndpoint = discoveryResponse.EndSessionEndpoint,
                        UserInfoEndpoint = discoveryResponse.UserInfoEndpoint,
                        TokenEndPointAuthenticationMethods =
                            discoveryResponse.TokenEndpointAuthenticationMethodsSupported
                    };
            }
        }

        private static async Task<LoginResult> SignIn(string clientId, string clientSecret, string scope,
            string tenantId)
        {
            // create a redirect URI using an available port on the loopback address.
            // requires the OP to allow random ports on 127.0.0.1 - otherwise set a static port
            var browser = new SystemBrowser(_redirectPort);
            var redirectUri = string.Format($"{_redirectHost}:{browser.Port}/{_redirectPath}");
            try
            {
                // Create the OICD client Options
                var options = new OidcClientOptions
                {
                    Authority = _ocsIdentityUrl,
                    ClientId = clientId,
                    ClientSecret = clientSecret,
                    RedirectUri = redirectUri,
                    Scope = scope,
                    FilterClaims = false,
                    Flow = OidcClientOptions.AuthenticationFlow.Hybrid,
                    Browser = browser,
                    Policy = new Policy
                    {
                        Discovery = new DiscoveryPolicy
                        {
                            ValidateIssuerName = false
                        }
                    },
                };

                _oidcClient = new OidcClient(options);
                var loginRequest = new LoginRequest
                {
                    FrontChannelExtraParameters = new {acr_values = $"tenant:{tenantId}"}
                };

                // Login with the client. This call will open a new tab in your default browser
                return await _oidcClient.LoginAsync(loginRequest);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error while logging in: {ex}");
                throw ex;
            }
        }

        public static (string, string, DateTime) GetAccessTokenFromRefreshToken(string refreshToken, string clientId,
            string clientSecret)
        {
            Console.WriteLine("");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("|  Getting Access token from Refresh token    |");
            Console.WriteLine("+-----------------------+");
            Console.WriteLine("");

            return RefreshTokenAsync(refreshToken, clientId, clientSecret).Result;
        }

        private static async Task<(string, string, DateTime)> RefreshTokenAsync(string refreshToken, string clientId,
            string clientSecret)
        {
            if (refreshToken == "")
            {
                Console.WriteLine("No refresh token provided");
            }

            Console.WriteLine("Using refresh token: {0}", refreshToken);

            // Get provider information manually
            var provider = await GetProviderInformation();

            // Make a refresh token request. This will issue new access and refresh tokens.
            var tokenClient = new HttpClient();
            var response = await tokenClient.RequestRefreshTokenAsync(new RefreshTokenRequest
            {
                Address = provider.TokenEndpoint,

                ClientId = clientId,
                ClientSecret = clientSecret,
                RefreshToken = refreshToken
            });

            if (response.IsError)
            {
                Console.WriteLine("Error while getting the refresh token: " + response.Error);
                return ("", "", DateTime.Now);
            }

            return (response.AccessToken, response.RefreshToken,
                DateTime.Now.AddSeconds(response.ExpiresIn).ToLocalTime());
        }

        public static async void Logout()
        {
            await _oidcClient.LogoutAsync();
        }
    }
}
