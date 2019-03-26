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
    private String removeSingleQuery = dataBase + "/RemoveValue?index={index}";
    private String removeMultipleQuery = dataBase + "/RemoveWindowValues?startIndex={startIndex}&endIndex={endIndex}";

    //dataview path
    private String dataviewBase = requestBase + "/Dataviews";
    private String getDataviews = dataviewBase + "?skip={skip}&count={count}";
    private String dataviewPath = dataviewBase + "/{dataview_id}";
    private String getDataviewPreview = dataviewPath + "/preview/interpolated";

    private String datagroupPath = dataviewPath + "/Datagroups";
    private String getDatagroup  = datagroupPath + "/{datagroup_id}";
    private String getDatagroups  = datagroupPath + "?skip={skip}&count={count}";


    public StreamsClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    public String createStreamView(String tenantId, String namespaceId, SdsStreamView streamViewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String streamViewId = streamViewDef.getId();
        
        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId));

            urlConnection = baseClient.getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = mGson.toJson(streamViewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "create streamView request failed");
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

    public String getStreamViewMap(String tenantId, String namespaceId, String streamViewId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId) + "/Map");

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
                throw new SdsError(urlConnection, "get streamView map request failed");
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
    
    public void deleteStreamView(String tenantId, String namespaceId, String streamViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getStreamViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamViewId}", streamViewId));

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
                throw new SdsError(urlConnection, "delete streamView request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
     public String createStream(String tenantId, String namespaceId, SdsStream streamDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
		String streamId = streamDef.getId();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "POST");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();

    }

    public String getStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "GET");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public ArrayList<SdsStream> getStreams(String tenantId, String namespaceId, String query, String skip, String count) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamsPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{query}", query)
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
     
        ArrayList<SdsStream> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<SdsStream>>(){}.getType());
        return results;
        //   return jsonResults.toString();
    }

    public void updateStream(String tenantId, String namespaceId, String streamId, SdsStream streamDef) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void deleteStream(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
                throw new SdsError(urlConnection, "delete stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void updateTags(String tenantId, String namespaceId, String streamId, ArrayList<String> tags) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = baseClient.getConnection(url, "PUT");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update tags request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public ArrayList<String> getTags(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Tags");
            urlConnection = baseClient.getConnection(url, "GET");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
        ArrayList<String> test = new ArrayList<String>();
        
        ArrayList<String> results = mGson.fromJson(jsonResults.toString(), new TypeToken<ArrayList<String>>(){}.getType());
        return results;
    }
    
    public void updateMetadata(String tenantId, String namespaceId, String streamId, Map<String, String> metadata) throws SdsError {

        URL url = null;
        HttpURLConnection urlConnection = null;


        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata");
            urlConnection = baseClient.getConnection(url, "PUT");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update stream request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public String getMetadata(String tenantId, String namespaceId, String streamId, String key) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getStreamPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) + "/Metadata/" + key);
            urlConnection = baseClient.getConnection(url, "GET");
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void insertValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        try {
            url = new URL(baseUrl + insertMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "POST");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "insert single value request failed");

            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getSingleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getLastValue(String tenantId, String namespaceId, String streamId) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(baseUrl + getLastValuePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
                throw new SdsError(urlConnection, "get last value request failed");
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

    public String getFirstValue(String tenantId, String namespaceId, String streamId) throws SdsError {

        URL url;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {

            url = new URL(baseUrl + getFirstValuePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "GET");

        }   catch (Exception e) {
            e.printStackTrace();
        }

        try {

            int httpResult = urlConnection.getResponseCode();
            if (httpResult != HttpURLConnection.HTTP_OK) {
                throw new SdsError(urlConnection, "get first value request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }

            in.close();
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e){
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        return getWindowValues(tenantId,namespaceId,streamId,startIndex,endIndex,"");
    }
    
    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, String filter) throws SdsError {
        return getWindowValues(tenantId,namespaceId,streamId,startIndex,endIndex, filter, "");
    }
    

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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }


    public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType) throws SdsError {
        return getRangeValues(tenantId, namespaceId, streamId, startIndex, "", skip,count, reverse, boundaryType);
    }

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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }


    

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
                throw new SdsError(urlConnection, "get range of interpolated values request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }
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
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }

    public void updateValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "update multiple values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void replaceValues(String tenantId, String namespaceId, String streamId, String json) throws SdsError {
        URL url;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + replaceMultiplePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = baseClient.getConnection(url, "PUT");
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
            if (baseClient.isSuccessResponseCode(httpResult)) {
            } else {
                throw new SdsError(urlConnection, "replace multiple values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removeValue(String tenantId, String namespaceId, String streamId, String index) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeSingleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
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
                throw new SdsError(urlConnection, "remove single value request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removeWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + removeMultipleQuery.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
                    .replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
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
                throw new SdsError(urlConnection, "remove window of values request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

	public void updateStreamType(String tenantId, String namespaceId, String streamId, String streamViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;

        try {
            url = new URL(baseUrl + updateStreamTypePath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
                    .replace("{streamViewId}", streamViewId));
            urlConnection = baseClient.getConnection(url, "PUT");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String json = "";
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
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
        } catch (Exception e) {
            e.printStackTrace();
        }
	}
    



}
