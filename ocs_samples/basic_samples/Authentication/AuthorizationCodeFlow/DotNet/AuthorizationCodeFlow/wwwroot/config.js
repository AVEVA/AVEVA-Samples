var config = {
    authority: "https://dat-b.osisoft.com/identity",
    ApiVersion: "v1",
    client_id: "Client ID Placeholder",
    redirect_uri: "http://localhost:5004/callback.html",
    response_type: "code",
    scope: "openid ocsapi",
    post_logout_redirect_uri: "http://localhost:5004/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    acr_values: "tenant:" + "Tenant ID Placeholder"
};