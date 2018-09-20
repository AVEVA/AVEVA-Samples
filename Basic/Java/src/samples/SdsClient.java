/* SdsClient.java

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
*/

package samples;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.microsoft.aad.adal4j.AuthenticationContext;
import com.microsoft.aad.adal4j.AuthenticationResult;
import com.microsoft.aad.adal4j.ClientCredential;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;


public class SdsClient {
    private static AuthenticationContext authContext = null;
    private static ExecutorService service = null;
    private static AuthenticationResult result = null;
    Gson mGson = null;
    private String baseUrl = null;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/Tenants/{tenantId}/Namespaces/{namespaceId}";
    // type paths
    private String typesBase = requestBase + "/Types";
    private String typePath = typesBase + "/{typeId}";
    private String getTypesPath = typesBase + "?skip={skip}&count={count}";
    // behavior paths
    private String behaviorsBase = requestBase + "/Behaviors";
    private String getBehaviorPath = behaviorsBase + "/{behaviorId}";
    private String getBehaviorsPath = behaviorsBase + "?skip={skip}&count={count}";
    // stream paths
    private String streamsBase = requestBase + "/Streams";
    private String getStreamPath = streamsBase + "/{streamId}";
    private String getStreamsPath = streamsBase + "?query={query}&skip={skip}&count={count}";
    // view paths
    private String viewBase = requestBase + "/Views";
    private String getViewPath = viewBase + "/{viewId}";
        
    
    // data paths
    private String dataBase = requestBase + "/Streams/{streamId}/Data";
    private String insertSinglePath = dataBase + "/InsertValue";
    private String insertMultiplePath = dataBase + "/InsertValues";
    private String getSingleQuery = dataBase + "/GetValue?index={index}";
    private String getLastValuePath = dataBase + "/GetLastValue?";
    private String getWindowQuery = dataBase + "/GetWindowValues?startIndex={startIndex}&endIndex={endIndex}";
    private String getRangeQuery = dataBase + "/GetRangeValues?startIndex={startIndex}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}";
    private String getRangeViewQuery = dataBase + "/GetRangeValues?startIndex={startIndex}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}&viewId={viewId}";
    private String updateSinglePath = dataBase + "/UpdateValue";
    private String updateMultiplePath = dataBase + "/UpdateValues";
    private String replaceSinglePath = dataBase + "/ReplaceValue";
    private String replaceMultiplePath = dataBase + "/ReplaceValues";
    private String removeSingleQuery = dataBase + "/RemoveValue?index={index}";
    private String removeMultipleQuery = dataBase + "/RemoveWindowValues?startIndex={startIndex}&endIndex={endIndex}";

    public SdsClient(String baseUrl) {
        this.baseUrl = baseUrl;
        this.mGson = new Gson();
    }

    public static java.net.HttpURLConnection getConnection(URL url, String method) {
        java.net.HttpURLConnection urlConnection = null;
        AuthenticationResult token = AcquireAuthToken();

        try {
            urlConnection = (java.net.HttpURLConnection) url.openConnection();
            urlConnection.setRequestProperty("Accept", "*/*; q=1");
            urlConnection.setRequestMethod(method);
            urlConnection.setUseCaches(false);
            urlConnection.setConnectTimeout(50000);
            urlConnection.setReadTimeout(50000);
            urlConnection.setRequestProperty("Content-Type", "application/json");

            urlConnection.setRequestProperty("Authorization", token.getAccessTokenType() + " " + token.getAccessToken());
            if (method == "POST" || method == "PUT" || method == "DELETE") {
                urlConnection.setDoOutput(true);
            } else if (method == "GET") {
                //Do nothing
            }
        } catch (SocketTimeoutException e) {
            e.getMessage();
        } catch (ProtocolException e) {
            e.getMessage();
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return urlConnection;
    }

    static protected AuthenticationResult AcquireAuthToken() {
        // get configuration
        String clientId = getConfiguration("clientId");
        String clientSecret = getConfiguration("clientSecret");
        String authority = getConfiguration("authority");
        String resource = getConfiguration("resource");

        service = Executors.newFixedThreadPool(1);
        try {
            if (authContext == null) {
                authContext = new AuthenticationContext(authority, true, service);
            }

            // tokens expire after a certain period of time
            // You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
            // ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed

            ClientCredential userCred = new ClientCredential(clientId, clientSecret);
            Future<AuthenticationResult> authResult = authContext.acquireToken(resource, userCred, null);
            result = authResult.get();
        } catch (Exception e) {
            // Do nothing
        } finally {
            service.shutdown();
        }
        return result;
    }

    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        InputStream inputStream;

        try {
            inputStream = new FileInputStream("config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return property;
    }

    private static void printSdsErrorMessage(SdsError sdsError) {
        System.out.println("SdsError Msg: " + sdsError.getSdsErrorMessage());
        System.out.println("HttpStatusCode: " + sdsError.getHttpStatusCode());
        System.out.println("errorMessage: " + sdsError.getMessage());
    }

    public String createType(String tenantId, String namespaceId, SdsType typeDef) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String typeId = typeDef.getId();
        
        try {
            url = new URL(baseUrl + typePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = mGson.toJson(typeDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "create type request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }
    
    public String createView(String tenantId, String namespaceId, SdsView viewDef) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String viewId = viewDef.getId();
        
        try {
            url = new URL(baseUrl + getViewPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{viewId}", viewId));
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = mGson.toJson(viewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "create view request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    public String getViewMap(String tenantId, String namespaceId, String viewId) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getViewPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{viewId}", viewId) + "/Map");
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get view map request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }
    
    public String getType(String tenantId, String namespaceId, String typeId) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + typePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get single type request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getTypes(String tenantId, String namespaceId, String skip, String count) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getTypesPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{skip}", skip).replace("{count}", count));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple types request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void deleteType(String tenantId, String namespaceId, String typeId) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + typePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "delete type request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void deleteView(String tenantId, String namespaceId, String viewId) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getViewPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{viewId}", viewId));
            urlConnection = getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "delete view request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
     public String createStream(String tenantId, String namespaceId, SdsStream streamDef) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
		String streamId = streamDef.getId();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = mGson.toJson(streamDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            }

            if (httpResult != HttpURLConnection.HTTP_OK && httpResult != HttpURLConnection.HTTP_CREATED) {
                throw new SdsError(urlConnection, "create stream request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();

    }

    public String getStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get single stream request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public ArrayList<SdsStream> getStreams(String tenantId, String namespaceId, String query, String skip, String count) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamsPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{query}", query)
                    .replace("{skip}", skip).replace("{count}", count));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple streams request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
     
        ArrayList<SdsStream> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<SdsStream>>(){}.getType());
        return results;
        //   return jsonResults.toString();
    }

    public void updateStream(String tenantId, String namespaceId, String streamId, SdsStream streamDef) throws SdsError {

        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }


        try {
            String body = mGson.toJson(streamDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void deleteStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "delete stream request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void updateTags(String tenantId, String namespaceId, String streamId, ArrayList<String> tags) throws SdsError {

        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }


        try {
            String body = mGson.toJson(tags);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "update tags request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public ArrayList<String> getTags(String tenantId, String namespaceId, String streamId) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple streams request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
        ArrayList<String> test = new ArrayList<String>();
        
        ArrayList<String> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<String>>(){}.getType());
        return results;
    }
    
    public void updateMetadata(String tenantId, String namespaceId, String streamId, Map<String, String> metadata) throws SdsError {

        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata");
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }


        try {
            String body = mGson.toJson(metadata);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public String getMetadata(String tenantId, String namespaceId, String streamId, String key) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata/" + key);
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get metadata request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void insertValue(String tenantId, String namespaceId, String streamId, String evt) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + insertSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(evt);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "insert single value request failed");

            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void insertValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        try {
            url = new URL(baseUrl + insertMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "insert single value request failed");

            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getSingleQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get single value request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getLastValue(String tenantId, String namespaceId, String streamId) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getLastValuePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get last value request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getWindowQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get window of values request request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));


            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            url = new URL(baseUrl + getRangeQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{streamId}", streamId).replace("{startIndex}", startIndex)
                    .replace("{skip}", "" + skip).replace("{count}", "" + count)
                    .replace("{reverse}", "" + reverse).replace("{boundaryType}", "" + boundaryType));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get range of values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType, String viewId) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            url = new URL(baseUrl + getRangeViewQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{streamId}", streamId).replace("{startIndex}", startIndex)
                    .replace("{skip}", "" + skip).replace("{count}", "" + count)
                    .replace("{reverse}", "" + reverse).replace("{boundaryType}", "" + boundaryType)
                    .replace("{viewId}", "" + viewId));
            urlConnection = getConnection(url, "GET");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get range of values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    
    public void updateValue(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "update single value request failed");
            }

        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void updateValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "update multiple values request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void replaceValue(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + replaceSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "replace single value request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void replaceValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + replaceMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "replace multiple values request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removeValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeSingleQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
            urlConnection = getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "remove single value request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removeWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeMultipleQuery.replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
                    .replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
            urlConnection = getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "remove window of values request failed");
            }
        } catch (SdsError sdsError) {
            printSdsErrorMessage(sdsError);
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
