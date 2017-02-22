

class Constants(object):
    #VERY IMPORTANT: edit the following values to reflect the authorization items you were given
    authItems = {'resource' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
                 'authority' : "PLACEHOLDER_REPLACE_WITH_RESOURCE", #Ex: "https://login.windows.net/<TENANT-NAME>.onmicrosoft.com/oauth2/token,
                 'appId' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
                 'appKey' : "PLACEHOLDER_REPLACE_WITH_RESOURCE"}
                 
    TenantId = "PLACEHOLDER_REPLACE_WITH_RESOURCE" #A guid for the Id of the tenant --- NOT the appId
    ###IMPORTANT: For QiServerUrl No "http" is necessary
    ###Ex: "ApplicationUri:443" instead of "https://ApplicationUri:443"
    QiServerUrl = "PLACEHOLDER_REPLACE_WITH_RESOURCE"
