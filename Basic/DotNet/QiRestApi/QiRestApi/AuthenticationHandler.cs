using Microsoft.IdentityModel.Clients.ActiveDirectory;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;

namespace QiRestApi
{
    /// <summary>
    /// The Active Directory assembly manages all credential caching and refreshing.  We simply call the 
    /// AcquireToken method and attach the token to the request header.
    /// 
    /// This is a very basic handler.  A serious handler should support retry and the like.
    /// </summary>
    public sealed class AuthenticationHandler : DelegatingHandler
    {
        private readonly string _resource;
        private readonly ClientCredential _clientCredential;
        private readonly string _authority;

#if false // Legacy ADAL assembly was very chatty
        static AuthenticationHandler()
        {
            AdalTrace.LegacyTraceSwitch.Level = System.Diagnostics.TraceLevel.Warning;
            AdalTrace.TraceSource.Switch.Level = System.Diagnostics.SourceLevels.Warning;
        }
#endif

        public AuthenticationHandler(string resource, string tenantDomainName, string aadInstanceFormat,
            string clientId, string clientSecret)
        {
            _resource = resource;
            _clientCredential = new ClientCredential(clientId, clientSecret);
            _authority = string.Format(aadInstanceFormat, tenantDomainName);
        }

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request != null)
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await GetAccessTokenAsync());

            return await base.SendAsync(request, cancellationToken);
        }

        private async Task<string> GetAccessTokenAsync()
        {
            var authenticationContext = new AuthenticationContext(_authority);
            var authenticationResult = await authenticationContext.AcquireTokenAsync(_resource, _clientCredential);
            return authenticationResult.AccessToken;
        }

    }
}
