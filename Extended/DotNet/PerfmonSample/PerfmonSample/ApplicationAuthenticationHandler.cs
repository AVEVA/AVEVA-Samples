using Microsoft.IdentityModel.Clients.ActiveDirectory;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;

namespace PerfmonSample
{
    /// <summary>
    /// The ApplicationAuthenticationHandler is a delegating handler, like the <see cref="OSIsoft.Data.Http.Security.SdsSecurityHandler"/>, 
    /// that retrieves authentication tokens from the Azure Active Directory and ADFS services and adds the token to the outbound request's 
    /// Authorization header.
    /// 
    /// This handler is provided as sample.  One might save the client secret as a SecureString in a formal handler.
    /// </summary>
    public sealed class ApplicationAuthenticationHandler : DelegatingHandler
    {
        #region Declarations

        private readonly string _resource;
        private readonly string _authority;
        private readonly ClientCredential _clientCredential;
        private readonly AuthenticationContext _authenticationContext;

        #endregion

        #region Constructors

        static ApplicationAuthenticationHandler()
        {
            // suppress annoying ADAL logging
            LoggerCallbackHandler.UseDefaultLogging = false;
        }

        /// <summary>
        /// Constructor to create the handler for acquiring security tokens from the Azure Active Directory authority 
        /// and adding those tokens to the header of the request.
        /// </summary>
        /// <param name="resource">Identifier of the target resource that is the recipient of the requested token.</param>
        /// <param name="tenantDomainId">Identifier of the tenant domain.</param>
        /// <param name="aadInstanceFormat">String format that when applied to the <paramref name="tenantDomainId"/> 
        /// specifies the address of the authority to issue token.</param>
        /// <param name="clientId">Identifier of the client requesting the token.</param>
        /// <param name="clientSecret">Secret of the client requesting the token.</param>
        public ApplicationAuthenticationHandler(string resource, string tenantDomainId, string aadInstanceFormat,
            string clientId, string clientSecret)
        {
            // Sanity check...
            if (string.IsNullOrEmpty(tenantDomainId))
                throw new ArgumentNullException("tenantDomainName");
            if (string.IsNullOrEmpty(resource))
                throw new ArgumentNullException("resource");
            if (aadInstanceFormat == null)
                throw new ArgumentNullException("aadInstanceFormat");
            if (string.IsNullOrEmpty(clientId))
                throw new ArgumentNullException("clientId");
            if (string.IsNullOrEmpty(clientSecret))
                throw new ArgumentNullException("clientSecret");

            _resource = resource;
            _authority = string.Format(aadInstanceFormat, tenantDomainId);
            _clientCredential = new ClientCredential(clientId, clientSecret);
            _authenticationContext = new AuthenticationContext(_authority);
        }

        #endregion

        #region Overrides

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request != null)
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await GetAccessTokenAsync());

            return await base.SendAsync(request, cancellationToken);
        }

        #endregion

        #region Private Methods

        private async Task<string> GetAccessTokenAsync()
        {
            AuthenticationResult authenticationResult = null;
            int retry = 0;
            do
            {
                try
                {
                    authenticationResult = await _authenticationContext.AcquireTokenAsync(_resource, _clientCredential);
                }
                catch
                {
                    await Task.Delay(TimeSpan.FromSeconds(1));
                }
            } while (authenticationResult == null && ++retry < 5);

            if (authenticationResult == null)
                throw new InvalidOperationException("Failed to authenticate");

            return authenticationResult.AccessToken;
        }

        #endregion
    }
}
