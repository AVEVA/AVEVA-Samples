var config = {
    authority: "https://dat-b.osisoft.com/identity",
    client_id: "Client ID Placeholder",
    redirect_uri: "http://localhost:5003/callback.html",
    response_type: "id_token token",
    scope: "openid ocsapi",
    post_logout_redirect_uri: "http://localhost:5003/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    acr_values: "tenant:" + "Tenant ID Placeholder"
};