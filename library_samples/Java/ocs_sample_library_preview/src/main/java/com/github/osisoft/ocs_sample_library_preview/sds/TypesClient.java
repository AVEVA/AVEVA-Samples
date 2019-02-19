/** SdsClient.java
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

package  com.github.osisoft.ocs_sample_library_preview.sds;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;
import  com.github.osisoft.ocs_sample_library_preview.BaseClient;
import  com.github.osisoft.ocs_sample_library_preview.SdsError;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;


public class TypesClient {
    private String baseUrl = null;
    private String apiVersion = null;
    private Gson mGson = null;
    private BaseClient baseClient;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}";
    // type paths
    private String typesBase = requestBase + "/Types";
    private String typePath = typesBase + "/{typeId}";
    private String getTypesPath = typesBase + "?skip={skip}&count={count}";


    public TypesClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    public String createType(String tenantId, String namespaceId, SdsType typeDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String typeId = typeDef.getId();
        
        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "POST");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "create type request failed ");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }
    
    public String getType(String tenantId, String namespaceId, String typeId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "GET");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getTypes(String tenantId, String namespaceId, String skip, String count) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getTypesPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{skip}", skip).replace("{count}", count));
            urlConnection = baseClient.getConnection(url, "GET");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void deleteType(String tenantId, String namespaceId, String typeId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "DELETE");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "delete type request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    



}
