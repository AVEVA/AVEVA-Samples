module.exports = {

    //VERY IMPORTANT: edit the following values to reflect the authorization items you were given
    authItems: {
        'resource': "https://pihomemain.onmicrosoft.com/historian",
        'authority': "https://login.windows.net/<PLACEHOLDER_REPLACE_WITH_TENANT_NAME>.onmicrosoft.com/oauth2/token",
        'clientId': "PLACEHOLDER_REPLACE_WITH_CLIENT_ID",
        'clientSecret': "PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET"
    },
    qiServerUrl: "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL",
    tenantId: "PLACEHOLDER_REPLACE_WITH_TENANT_ID",  // a guid for the Id of the tenant --- NOT the clientId
    namespaceId: "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID"
}