var config = {
    authority: "https://dat-b.osisoft.com/identity",
    ApiVersion: "v1",
    client_id: "REPLACE_WITH_CLIENT_ID",
    redirect_uri: "http://localhost:5004/callback.html",
    response_type: "code",
    scope: "openid ocsapi",
    post_logout_redirect_uri: "http://localhost:5004/index.html",
    filterProtocolClaims: true,
    loadUserInfo: true,
    revokeAccessTokenOnSignout: true,
    accessTokenExpiringNotificationTime: 60,
    automaticSilentRenew: true,
    silent_redirect_uri: 'http://localhost:5004/silent-refresh.html',
    acr_values: "tenant:" + "REPLACE_WITH_TENANT_ID"
};