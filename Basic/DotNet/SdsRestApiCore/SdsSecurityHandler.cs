using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Clients.ActiveDirectory;

namespace SdsRestApiCore
{
    public sealed class SdsSecurityHandler : DelegatingHandler
    {
        private readonly string _resource;
        private readonly ClientCredential _clientCredential;
        private readonly string _authority;

        public SdsSecurityHandler(string resource, string tenantId, string aadInstanceFormat, string appId, string appKey)
        {
            _resource = resource;
            _clientCredential = new ClientCredential(appId, appKey);
            _authority = string.Format(aadInstanceFormat, tenantId);

            InnerHandler = new HttpClientHandler()
            {
                AllowAutoRedirect = false
            };
        }

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request != null)
            {
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await GetAccessTokenAsync());
            }

            return await base.SendAsync(request, cancellationToken);
        }

        private async Task<string> GetAccessTokenAsync()
        {
            AuthenticationContext authenticationContext = new AuthenticationContext(_authority);
            AuthenticationResult result = await authenticationContext.AcquireTokenAsync(_resource, _clientCredential);
            return result.AccessToken;
        }
    }
}
