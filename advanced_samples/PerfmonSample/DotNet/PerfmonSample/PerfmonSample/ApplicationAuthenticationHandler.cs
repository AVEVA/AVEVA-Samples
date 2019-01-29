// <copyright file="ApplicationAuthenticationHandler.cs" company="OSIsoft, LLC">
//
// Copyright (C) 2018-2019 OSIsoft, LLC. All rights reserved.
//
// THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
// OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
// THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
//
// RESTRICTED RIGHTS LEGEND
// Use, duplication, or disclosure by the Government is subject to restrictions
// as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
// Computer Software clause at DFARS 252.227.7013
//
// OSIsoft, LLC
// 1600 Alvarado St, San Leandro, CA 94577
// </copyright>

using IdentityModel.Client;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;

namespace PerfmonSample
{
    /// <summary>
    /// The ApplicationAuthenticationHandler is a delegating handler, like the <see cref="OSIsoft.Identity.AuthenticationHandler"/>, 
    /// that retrieves authentication tokens the token service and adds the token to the outbound request's header.
    /// 
    /// This handler is provided as sample.
    /// </summary>
    public sealed class ApplicationAuthenticationHandler: DelegatingHandler
    {
        private readonly string _resource;
        private readonly string _clientId;
        private readonly string _clientSecret;
        private string _accessToken;
        private DateTime _accessTokenExpiry = DateTime.MinValue;

        public ApplicationAuthenticationHandler(string resource, string clientId, string clientSecret)
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
                var discoveryRequest = new DiscoveryDocumentRequest
                {
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
