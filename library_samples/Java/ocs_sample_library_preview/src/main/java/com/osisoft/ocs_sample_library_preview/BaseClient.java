/** BaseClient.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package com.osisoft.ocs_sample_library_preview;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;


public class BaseClient {
    private String cachedAccessToken = null;
    private Date accessTokenExpiration = new Date(Long.MIN_VALUE);
    private long FIVE_SECONDS_IN_MILLISECONDS = 5000;
    public Gson mGson = null;
    public String baseUrl = null;
    public String apiVersion = null;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}";

    //config parameters
    private String gclientId = "";
    private String gclientSecret = "";
    private String gresource = "";

    public BaseClient() {
        // It should not set static fields from construtor like that..
        gclientId = getConfiguration("clientId");
        gclientSecret = getConfiguration("clientSecret");
        gresource = getConfiguration("resource");
        gresource = gresource.endsWith("/") ? gresource :  gresource + "/";

        this.baseUrl = gresource;
        this.apiVersion = getConfiguration("apiVersion");
        this.mGson = new Gson();
    }
    
    public BaseClient(String apiVersion, String clientId, String clientSecret, String resource) {
        // It should not set static fields from construtor like that..
        gclientId = clientId;
        gclientSecret = clientSecret;
        gresource = resource;
        gresource = gresource.endsWith("/") ? gresource :  gresource + "/";

        this.baseUrl = gresource;
        this.apiVersion = apiVersion;
        this.mGson = new Gson();
    }
   
    public HttpURLConnection getConnection(URL url, String method) {
        HttpURLConnection urlConnection = null;
        String token = AcquireAuthToken();

        try {
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(method);
            urlConnection.setRequestProperty("Accept", "*/*; q=1");
            urlConnection.setRequestProperty("Content-Type", "application/json");
            urlConnection.setRequestProperty("Authorization", "Bearer " + token);
            urlConnection.setUseCaches(false);
            urlConnection.setConnectTimeout(50000);
            urlConnection.setReadTimeout(50000);
            if ("POST".equals(method) || "PUT".equals(method) ||"DELETE".equals(method)) {
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

    protected String AcquireAuthToken() {

        if (cachedAccessToken != null){
            long tokenExpirationTime = accessTokenExpiration.getTime(); // returns time in milliseconds.
            long currentTime = System.currentTimeMillis();
            long timeDifference = tokenExpirationTime - currentTime;

            if(timeDifference > FIVE_SECONDS_IN_MILLISECONDS)
                return cachedAccessToken;
        }

        // get new token 
        try {
            URL discoveryUrl = new URL(gresource + "identity/.well-known/openid-configuration");
            URLConnection request = discoveryUrl.openConnection();
            request.connect();
            JsonParser jp = new JsonParser(); 
            JsonObject rootObj = jp.parse(new InputStreamReader((InputStream) request.getContent())).getAsJsonObject(); 
            String tokenUrl = rootObj.get("token_endpoint").getAsString(); 

            URL token = new URL(tokenUrl);
            HttpURLConnection tokenRequest = (HttpURLConnection) token.openConnection();
            tokenRequest.setRequestMethod("POST");
            tokenRequest.setRequestProperty("Accept", "application/json");
            tokenRequest.setDoOutput(true);
            tokenRequest.setDoInput(true);
            tokenRequest.setUseCaches(false);

            String postString = "client_id=" + URLEncoder.encode(gclientId, "UTF-8") 
                + "&client_secret=" + URLEncoder.encode(gclientSecret, "UTF-8") 
                + "&grant_type=client_credentials";
            byte[] postData = postString.getBytes("UTF-8");
            tokenRequest.setRequestProperty( "Content-Length", Integer.toString( postData.length));
            tokenRequest.getOutputStream().write(postData);

            InputStream in = new BufferedInputStream(tokenRequest.getInputStream());
            String result = org.apache.commons.io.IOUtils.toString(in, "UTF-8");
            in.close();

            jp = new JsonParser(); 
            JsonObject response = jp.parse(result).getAsJsonObject(); 
            cachedAccessToken = response.get("access_token").getAsString();
            Integer timeOut = response.get("expires_in").getAsInt();
            accessTokenExpiration = new Date(System.currentTimeMillis() + timeOut * 1000);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            // Do nothing
        } 

        return cachedAccessToken;
    }

    private String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        InputStream inputStream;

         if(propertyId.equals("clientId") && !gclientId.isEmpty()){
            return gclientId;
        }

        if(propertyId.equals("clientSecret") && !gclientSecret.isEmpty()){
            return gclientSecret;
        }

        if(propertyId.equals("resource") && ! gresource.isEmpty()){
            return gresource;
        }

        try {
            inputStream = new FileInputStream("config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return property.trim();
    }

    public boolean isSuccessResponseCode(int responseCode) {
        return responseCode >= 200 && responseCode < 300;
    }


}
