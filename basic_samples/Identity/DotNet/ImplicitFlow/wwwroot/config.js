var config = {
    authority: "https://dat-b.osisoft.com/identity",
    redirect_uri: "http://localhost:5003/callback.html",
    response_type: "id_token token",
    scope: "openid ocsapi",
    post_logout_redirect_uri: "http://localhost:5003/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    client_id: "ClientID",
    acr_values: "tenant:" + "TenantID"
};