/** SdsClient.java
 * 
 */

package com.github.osisoft.ocs_sample_library_preview.sds;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.github.osisoft.ocs_sample_library_preview.BaseClient;
import com.github.osisoft.ocs_sample_library_preview.SdsError;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Map;


/**
 * StreamsClient
 */
public class StreamsClient {
    private String baseUrl = null;
    private String apiVersion = null;
    private Gson mGson = null;
    private BaseClient baseClient;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}";
    // stream paths
    private String streamsBase = requestBase + "/Streams";
    private String getStreamPath = streamsBase + "/{streamId}";
    private String getStreamsPath = streamsBase + "?query={query}&skip={skip}&count={count}";
    private String updateStreamTypePath = streamsBase + "/{streamId}/Type?streamViewId={streamViewId}";
    // StreamView paths
    private String streamViewBase = requestBase + "/StreamViews";
    private String getStreamViewPath = streamViewBase + "/{streamViewId}";
        
    
    // data paths
    private String dataBase = requestBase + "/Streams/{streamId}/Data";
    private String insertMultiplePath = dataBase;
    private String getSingleQuery = dataBase + "?index={index}";
    private String getLastValuePath = dataBase + "/Last?";
    private String getFirstValuePath = dataBase + "/First?";
    private String getWindowQuery = dataBase + "?startIndex={startIndex}&endIndex={endIndex}&form={form}&filter={filter}";
    private String getRangeQuery = dataBase + "/Transform?startIndex={startIndex}&endindex={endindex}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}";
    private String getRangeInterpolatedQuery = dataBase + "/Transform/Interpolated?startIndex={startIndex}&endindex={endindex}&count={count}";
    private String getRangeStreamViewQuery = dataBase + "/Transform?startIndex={startIndex}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}&streamViewId={streamViewId}";
    private String updateMultiplePath = dataBase;
    private String replaceMultiplePath = dataBase + "?allowCreate=false";
    private String removeSingleQuery = dataBase + "?index={index}";
    private String removeMultipleQuery = dataBase + "?startIndex={startIndex}&endIndex={endIndex}";
    private String getSampledValuesQuery = dataBase + "/Sampled?startIndex={startIndex}&endIndex={endIndex}&intervals={intervals}&sampleBy={sampleBy}";



    /**
     * Base Constructor
     * @param base baseclient that helps with OCS calls
     */
    public StreamsClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    /**
     * creates a stream view
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param {SdsStreamView} streamViewDef SdsStreamView to create
     * @return created SdsStreamView as a string
     * @throws SdsError  any error that occurs
     */
    public String createStreamView(String tenantId, String namespaceId, SdsStreamView streamViewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String streamViewId = streamViewDef.getId();
        
        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId));

            urlConnection = baseClient.getConnection(url, "POST");

            String body = mGson.toJson(streamViewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "create streamView request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    /**
     * gets a streamviewmap
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamViewId the streamview to retreivemap
     * @return the streamviewmap as a string
     * @throws SdsError any error that occurs
     */
    public String getStreamViewMap(String tenantId, String namespaceId, String streamViewId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId) + "/Map");

            urlConnection = baseClient.getConnection(url, "GET");
            
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get streamView map request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }
    
    /**
     * delete stream view
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamViewId the streamview to delete
     * @throws SdsError any error that occurs
     */
    public void deleteStreamView(String tenantId, String namespaceId, String streamViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId));

            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "delete streamView request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * creates the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamDef the stream to create
     * @return the created stream as a string
     * @throws SdsError any error that occurs
     */
     public String createStream(String tenantId, String namespaceId, SdsStream streamDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
		String streamId = streamDef.getId();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "POST");

            String body = mGson.toJson(streamDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            }

            if (httpResult != HttpURLConnection.HTTP_OK && httpResult != HttpURLConnection.HTTP_CREATED) {
                throw new SdsError(urlConnection, "create stream request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response.toString();

    }

    /**
     * gets the specified stream
     * @param tenantId tenant to wrok against
     * @param namespaceId namespace to work against
     * @param streamId stream to get
     * @return the stream as a string
     * @throws SdsError
     */
    public String getStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get single stream request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * gets a streams
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param query query used to help filter the results
     * @param skip number of streams to skip, used for paging
     * @param count number of streams to return
     * @return Arraylist<SdsStream> 
     * @throws SdsError any error that occurs
     */
    public ArrayList<SdsStream> getStreams(String tenantId, String namespaceId, String query, String skip, String count) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamsPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{query}", query)
                    .replace("{skip}", skip).replace("{count}", count));
            urlConnection = baseClient.getConnection(url, "GET");
            
            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple streams request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }
     
        ArrayList<SdsStream> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<SdsStream>>(){}.getType());
        return results;
        //   return jsonResults.toString();
    }

    /**
     * updates the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the id of the stream to update
     * @param streamDef the new stream definition
     * @throws SdsError any error that occurs
     */
    public void updateStream(String tenantId, String namespaceId, String streamId, SdsStream streamDef) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");

            String body = mGson.toJson(streamDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * delete the specified stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to delete
     * @throws SdsError any error that occurs
     */
    public void deleteStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "delete stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * update the tags associated with a stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to update tags on
     * @param tags ArrayList<String> of tags
     * @throws SdsError any error that occurs
     */
    public void updateTags(String tenantId, String namespaceId, String streamId, ArrayList<String> tags) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = baseClient.getConnection(url, "PUT");

            String body = mGson.toJson(tags);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update tags request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * gets the tags assocaited with the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get tags of
     * @return ArrayList<String> of tags
     * @throws SdsError any error that occurs
     */
    public ArrayList<String> getTags(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get multiple streams request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        ArrayList<String> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<String>>(){}.getType());
        return results;
    }
    
    /***
     * updates the meta data of a stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the stream to update the meta data of
     * @param metadata Map<String, String> 
     * @throws SdsError  any error that occurs
     */
    public void updateMetadata(String tenantId, String namespaceId, String streamId, Map<String, String> metadata) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata");
            urlConnection = baseClient.getConnection(url, "PUT");

            String body = mGson.toJson(metadata);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * gets metadata value from key associated with the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get metadata from
     * @param key the specific key to get the value from 
     * @return the specific string value from the metadata Map<String, String> 
     * @throws SdsError  any error that occurs
     */
    public String getMetadata(String tenantId, String namespaceId, String streamId, String key) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata/" + key);
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResponse = urlConnection.getResponseCode();
            if (httpResponse == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get metadata request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * inserts values into the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to insert values into
     * @param json json string of the array of values to insert
     * @throws SdsError  any error that occurs
     */
    public void insertValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        try {
            url = new URL(baseUrl + insertMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "POST");

            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "insert single value request failed");

            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * gets value at specified index
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get value of
     * @param index index to get value at
     * @return string of the value
     * @throws SdsError  any error that occurs
     */
    public String getValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getSingleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get single value request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /***
     * gets the last value of a stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the stream to get the last of 
     * @return string of the last value
     * @throws SdsError  any error that occurs
     */
    public String getLastValue(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getLastValuePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK) {
            } else {
                throw new SdsError(urlConnection, "get last value request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * gets the first value in the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get the first value of
     * @return string value of the fire value in the stream
     * @throws SdsError any error that occurs
     */
    public String getFirstValue(String tenantId, String namespaceId, String streamId) throws SdsError {

        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {

            url = new URL(baseUrl + getFirstValuePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult != HttpURLConnection.HTTP_OK) {
                throw new SdsError(urlConnection, "get first value request failed");
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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * gets window value of stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get window value from 
     * @param startIndex starting index
     * @param endIndex ending index
     * @return string of values
     * @throws SdsError  any error that occurs
     */
    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        return getWindowValues(tenantId,namespaceId,streamId,startIndex,endIndex,"");
    }
    
    /**
     * gets window value of stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get window value from 
     * @param startIndex starting index
     * @param endIndex ending index
     * @param filter filter to reduce the number of values returned
     * @return string of values
     * @throws SdsError any error that occurs
     */
    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, String filter) throws SdsError {
        return getWindowValues(tenantId,namespaceId,streamId,startIndex,endIndex, filter, "");
    }    

    /**
     * gets window value of stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get window value from 
     * @param startIndex starting index
     * @param endIndex ending index
     * @param filter filter to reduce the number of values returned
     * @param form use this to specify the format of the returned payload 
     * @return string of values
     * @throws SdsError any error that occurs
     */
    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, String filter, String form) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            String intermediate  = getWindowQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endIndex}", endIndex).replace("{form}", form).replace("{filter}", filter);
            if(form.equals("")){
                intermediate = intermediate.replace("&form=", "");
            }
            url = new URL(baseUrl + intermediate);
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get window of values request request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));


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
        } catch (IOException e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    /**
     * gets sampled values from the stream
     * @param tenantId tenant to work under
     * @param namespaceId namespace within tenant
     * @param streamId name of stream to get data from
     * @param startIndex starting index
     * @param endIndex ending index
     * @param intervals number of intervals to run sample
     * @param sampleBy property to sample by
     * @return
     * @throws SdsError errors that may occur
     */
    public String getSampledValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, int intervals, String sampleBy) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        try{
            url = new URL(baseUrl + getSampledValuesQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
            .replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endIndex}", endIndex)
            .replace("{intervals}", "" + intervals).replace("{sampleBy}", sampleBy));
            urlConnection = baseClient.getConnection(url, "GET");
        
            int httpResult = urlConnection.getResponseCode();
            if(httpResult != HttpURLConnection.HTTP_OK){
                throw new SdsError(urlConnection, "get sampled values request failed");
            }
            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while((inputLine = in.readLine()) != null){
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
        } catch (IOException e) {
            e.printStackTrace();
        }
        return response.toString();
    }

    /**
     * gets the specified range of values from the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get range of values from 
     * @param startIndex the starting index
     * @param skip number of values to skip (good for paging)
     * @param count number of values to return 
     * @param reverse whether to go forward or backward in regards to the index when getting more values 
     * @param boundaryType  SdsBoundaryType
     * @return string of the array of values 
     * @throws SdsError any error that occurs
     */
    public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType) throws SdsError {
        return getRangeValues(tenantId, namespaceId, streamId, startIndex, "", skip,count, reverse, boundaryType);
    }

    /**
     * gets the specified range of values from the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to get range of values from 
     * @param startIndex the starting index
     * @param endIndex the ending index
     * @param skip number of values to skip (good for paging)
     * @param count number of values to return 
     * @param reverse whether to go forward or backward in regards to the index when getting more values 
     * @param boundaryType  SdsBoundaryType
     * @return string of the array of values 
     * @throws SdsError any error that occurs
     */
    public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            String intermediate = getRangeQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
            .replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endindex}", endIndex)
            .replace("{skip}", "" + skip).replace("{count}", "" + count)
            .replace("{reverse}", "" + reverse).replace("{boundaryType}", "" + boundaryType);
            if(endIndex.equals("")){
                intermediate = intermediate.replace("&endindex=", "");
            }
            url = new URL(baseUrl + intermediate );
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get range of values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response.toString();
    }
        
    /**
     * gets interpolated values in the range specified
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the stream to get values from 
     * @param startIndex the starting index
     * @param endIndex the ending index
     * @param count the number of values to return
     * @return string of the array of values
     * @throws SdsError any error that occurs
     */
    public String getRangeValuesInterpolated(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, int count) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            String intermediate = getRangeInterpolatedQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
            .replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endindex}", endIndex).replace("{count}", "" + count);
            url = new URL(baseUrl + intermediate );
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get range of interpolated values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    /**
     * gets a range of values from a streamview
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the stream to get values from 
     * @param startIndex the starting index
     * @param skip the number of values to skip (good for paging)
     * @param count the number of values to return
     * @param reverse whether to go forward or backward in regards to the index when getting more values 
     * @param boundaryType SdsBoundaryType
     * @param streamViewId the streamview definition to desribe how to view the data 
     * @return string of the array of values
     * @throws SdsError any error that occurs
     */
    public String getRangeValuesStreamView(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType, String streamViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            url = new URL(baseUrl + getRangeStreamViewQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{streamId}", streamId).replace("{startIndex}", startIndex)
                    .replace("{skip}", "" + skip).replace("{count}", "" + count)
                    .replace("{reverse}", "" + reverse).replace("{boundaryType}", "" + boundaryType)
                    .replace("{streamViewId}", "" + streamViewId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get range of values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    /**
     * updates the stream with the values specified
     * @param tenantId tenant to work against
     * @param namespaceId namepsace to work against
     * @param streamId the stream to update the values of
     * @param json the values to update on the stream
     * @throws SdsError any error that occurs
     */
    public void updateValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");

            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update multiple values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * replace the values on the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId the stream to replace values in
     * @param json the values to replace
     * @throws SdsError any error that occurs
     */
    public void replaceValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + replaceMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");

            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "replace multiple values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * removes a value from the stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to remove value from 
     * @param index index to remove
     * @throws SdsError any error that occurs
     */
    public void removeValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeSingleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "remove single value request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * remove a window of values from a stream
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to remove values from
     * @param startIndex starting index to remove
     * @param endIndex ending index to remove
     * @throws SdsError any error that occurs 
     */
    public void removeWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeMultipleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
                    .replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "remove window of values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * update the stream type to a new type using a streamview
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param streamId stream to update 
     * @param streamViewId streamview to change the type of the stream to
     * @throws SdsError any error that occurs
     */
	public void updateStreamType(String tenantId, String namespaceId, String streamId, String streamViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateStreamTypePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
                    .replace("{streamViewId}", streamViewId));
            urlConnection = baseClient.getConnection(url, "PUT");

            String json = "";
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(json);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "replace multiple values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;        
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
}
