var config = {
    authority: "https://dat-b.osisoft.com/identity",
    ApiVersion: "v1",
    client_id: "REPLACE_WITH_CLIENT_ID",
    redirect_uri: "http://localhost:5003/callback.html",
    response_type: "id_token token",
    scope:"openid ocsapi",
    post_logout_redirect_uri : "http://localhost:5003/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    acr_values: "tenant:" + "REPLACE_WITH_TENANT_ID"
};