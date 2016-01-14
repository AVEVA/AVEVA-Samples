

class Constants(object):
    
    #VERY IMPORTANT: edit the following values to reflect the authorization items you were given
    authItems = {'resource' : "PLACEHOLDER_REPLACE_WITH_RESOURCE",
                 'authority' : "PLACEHOLDER_REPLACE_WITH_AUTHORITY", #Ex: "https://login.windows.net/<TENANT-ID>.onmicrosoft.com/oauth2/token,
                 'appId' : "PLACEHOLDER_REPLACE_WITH_USER_ID",
                 'appKey' : "PLACEHOLDER_REPLACE_WITH_USER_SECRET"}
                 
    ###IMPORTANT: For QiServerUrl No "http" is necessary
    ###Ex: "ApplicationUri:3380" instead of "https://ApplicationUri:3380"
    QiServerUrl = "PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL"
