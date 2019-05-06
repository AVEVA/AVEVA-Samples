// <copyright file="SdsSecurityHandler.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IdentityModel.Client;

namespace SdsRestApiCore
{
    public sealed class SdsSecurityHandler : DelegatingHandler
    {
        private readonly string _resource;
        private readonly string _clientId;
        private readonly string _clientSecret;
        private string _accessToken;
        private DateTime _accessTokenExpiry = DateTime.MinValue;

        public SdsSecurityHandler(string resource, string clientId, string clientSecret)
        {
            _resource = resource;
            _clientId = clientId;
            _clientSecret = clientSecret;

            InnerHandler = new HttpClientHandler()
            {
                AllowAutoRedirect = false
            };
        }

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request != null)
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await GetAccessTokenAsync(cancellationToken));

            return await base.SendAsync(request, cancellationToken);
        }

        private async Task<string> GetAccessTokenAsync(CancellationToken cancellationToken)
        {
            if (_accessToken != null && DateTime.UtcNow < _accessTokenExpiry)
            {
                return _accessToken;
            }

            using (HttpClient client = new HttpClient())
            {
                var discoveryRequest = new DiscoveryDocumentRequest {
                    Address = _resource + "/identity",
                    Policy = new DiscoveryPolicy
                    {
                        Authority = "https://identity.osisoft.com",
                        ValidateEndpoints = false,
                        ValidateIssuerName = false
                    }
                };

                var discoveryResponse = await client.GetDiscoveryDocumentAsync(discoveryRequest, cancellationToken);

                if (discoveryResponse.IsError)
                    throw new InvalidOperationException(discoveryResponse.Error);

                var clientCredentialsTokenRequest = new ClientCredentialsTokenRequest
                {
                    Address = discoveryResponse.TokenEndpoint,
                    ClientId = _clientId,
                    ClientSecret = _clientSecret,
                    Scope = "ocsapi" 
                };

                DateTime now = DateTime.UtcNow;

                var tokenResponse = await client.RequestClientCredentialsTokenAsync(clientCredentialsTokenRequest, cancellationToken);

                if (discoveryResponse.IsError)
                    throw new InvalidOperationException(tokenResponse.Error);

                if (string.IsNullOrEmpty(tokenResponse.AccessToken))
                    throw new InvalidOperationException("Failed to acquire Access Token");

                _accessToken = tokenResponse.AccessToken;

                // Add a buffer of 30 seconds to the expiration delta.
                _accessTokenExpiry = now.AddSeconds(tokenResponse.ExpiresIn - 30);

                return _accessToken;
            }
        }
    }
}
