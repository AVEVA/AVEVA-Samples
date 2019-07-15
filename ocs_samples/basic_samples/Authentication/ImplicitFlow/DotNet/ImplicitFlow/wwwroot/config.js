var config = {
    authority: "https://dat-b.osisoft.com/identity",
    ApiVersion: "v1",
    client_id: "REPLACE_WITH_CLIENT_ID",
    redirect_uri: "http://localhost:5003/callback.html",
    response_type: "id_token token",
    scope: "openid ocsapi",
    post_logout_redirect_uri: "http://localhost:5003/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    accessTokenExpiringNotificationTime: 3600,
    automaticSilentRenew: true,
    silent_redirect_uri: 'http://localhost:5003/silent-refresh.html',
    acr_values: "tenant:" + "REPLACE_WITH_TENANT_ID"
};