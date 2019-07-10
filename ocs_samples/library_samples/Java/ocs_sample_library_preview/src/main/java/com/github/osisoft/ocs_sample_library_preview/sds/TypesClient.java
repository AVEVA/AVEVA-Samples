/** SdsClient.java
 * 
 */

package com.github.osisoft.ocs_sample_library_preview.sds;

import com.google.gson.Gson;
import com.github.osisoft.ocs_sample_library_preview.BaseClient;
import com.github.osisoft.ocs_sample_library_preview.SdsError;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

/**
 * TypesClient
 */
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
    private String getTypesPath = typesBase + "?skip={skip}&count={count}&query={query}";

    /**
     * base constructor
     * @param base this base client helps make the OCS calls
     */
    public TypesClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    /**
     * creates the type
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param typeDef the type to create
     * @return the created type
     * @throws SdsError  any error that occurs
     */
    public String createType(String tenantId, String namespaceId, SdsType typeDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String typeId = typeDef.getId();
        
        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "POST");

            String body = mGson.toJson(typeDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8); 
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "create type request failed ");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }
    
    /**
     * get the type 
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param typeId the type to get
     * @return the string of the type
     * @throws SdsError  any error that occurs
     */
    public String getType(String tenantId, String namespaceId, String typeId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get single type request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * gets the types 
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param skip number of types to skip, useful in paging
     * @param count number of types to return
     * @return string of the types
     * @throws SdsError any error that occurs
     */
    public String getTypes(String tenantId, String namespaceId, int skip, int count) throws SdsError {
        return getTypes(tenantId,namespaceId,skip,count, "");
    }

    /**
     * gets the types 
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param skip number of types to skip, useful in paging
     * @param count number of types to return
     * @param query query to reduce the number of types returned
     * @return string of the types
     * @throws SdsError any error that occurs
     */
    public String getTypes(String tenantId, String namespaceId, int skip, int count, String query) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            //string 
            url = new URL(baseUrl + getTypesPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{query}", query).replace("{skip}", String.valueOf(skip)).replace("{count}", String.valueOf(count)));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple types request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));
            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * Deletes the type
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param typeId the type to delete
     * @throws SdsError  any error that occurs
     */
    public void deleteType(String tenantId, String namespaceId, String typeId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + typePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "delete type request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
