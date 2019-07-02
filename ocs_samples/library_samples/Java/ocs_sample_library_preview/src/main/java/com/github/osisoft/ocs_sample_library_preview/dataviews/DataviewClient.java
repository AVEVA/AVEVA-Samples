/** DataviewClient.java
 * 
 */

package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

import  com.github.osisoft.ocs_sample_library_preview.*;

/**
 * This client helps with all calls against the Dataviews service on OCS
 */
public class DataviewClient {

    private String baseUrl = null;
    private String apiVersion = null;
    private Gson mGson = null;
    private BaseClient baseClient;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}";

    //dataview path
    private String dataviewBase = requestBase + "/Dataviews";
    //private String getDataviews = dataviewBase + "?skip={skip}&count={count}";
    private String dataviewPath = dataviewBase + "/{dataview_id}";
    private String getDataviewPreview = dataviewPath + "/preview/interpolated?startIndex={startIndex}&endIndex={endIndex}&interval={interval}&form={form}&count={count}";
    private String getDataviewInterpolated= dataviewPath + "/data/interpolated?startIndex={startIndex}&endIndex={endIndex}&interval={interval}&form={form}&count={count}";

    private String datagroupPath = dataviewPath + "/Datagroups";
    //private String getDatagroup  = datagroupPath + "/{datagroup_id}";
    private String getDatagroups  = datagroupPath + "?skip={skip}&count={count}";

    /**
     * Constructor 
     * @param base baseclient handles some of the base information needed during calling ocs
     */
    public DataviewClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    /**
     * Creates the Dataview
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @param dataviewDef dataview definition
     * @return the created dataview
     * @throws SdsError any error that occurs
     */
    public Dataview postDataview(String tenantId, String namespaceId, Dataview dataviewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String dataviewId = dataviewDef.getId();
        
        try {
            url = new URL(baseUrl + dataviewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId));
            urlConnection = baseClient.getConnection(url, "POST");

            String body = mGson.toJson(dataviewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "create dataview request failed");
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

     
        Dataview results = mGson.fromJson(response.toString(), new TypeToken<Dataview>(){}.getType());
        return results;
       // return response.toString();
    }    

    /**
     * Updates a dataview
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @param dataviewDef dataview definiton to update to
     * @return updated dataview
     * @throws SdsErrorany error that occurs
     */
    public void putDataview(String tenantId, String namespaceId, Dataview dataviewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        String dataviewId = dataviewDef.getId();
        
        try {
            url = new URL(baseUrl + dataviewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId));
            urlConnection = baseClient.getConnection(url, "PUT");

            String body = mGson.toJson(dataviewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8); 
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED|| httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
            } else {
                throw new SdsError(urlConnection, "update dataview request failed");
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
    }    

    /**
     * deletes the specified dataview
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @param dataviewId dataview to delete
     * @return response (should be empty)
     * @throws SdsError any error that occurs
     */
    public String deleteDataview(String tenantId, String namespaceId, String dataviewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + dataviewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED|| httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
            } else {
                throw new SdsError(urlConnection, "delete dataview request failed");
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
     * gets the specified dataview
     * @param tenantId tenant to go against
     * @param namespaceId namepsace to go against
     * @param dataviewId dataview to get
     * @return the dataview 
     * @throws SdsError any error that occurs
     */
    public Dataview getDataview(String tenantId, String namespaceId, String dataviewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + dataviewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataview request failed");
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

        Dataview results = mGson.fromJson(response.toString(), new TypeToken<Dataview>(){}.getType());
        return results;
       // return response.toString();
    }

    /**
     * retrieves all of the datavies
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @return arraylist of Dataviews
     * @throws SdsError any error that occurs
     */
    public ArrayList<Dataview> getDataviews(String tenantId, String namespaceId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + dataviewBase.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataviews request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream(),StandardCharsets.UTF_8));

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            ArrayList<Dataview> results = mGson.fromJson(response.toString(), new TypeToken<ArrayList<Dataview>>(){}.getType());
            return results;
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
        return null;
    }

    /**
     * gets the datagroups of the specified dataview
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @param dataviewId the dataview to get datagroups from
     * @param skip number of datagroups to skip, used in paging
     * @param count nubmer of datagroups to get
     * @return Datagroups
     * @throws SdsError any error that occurs
     */
    public Datagroups getDatagroups(String tenantId, String namespaceId, String dataviewId, Integer skip, Integer count) throws SdsError {
        String response = getDatagroupsString(tenantId, namespaceId, dataviewId, skip, count) ;

        Datagroups results = mGson.fromJson(response.toString(), new TypeToken<Datagroups>(){}.getType());
        return results;        
    }
    
    /**
     * Returns the datagroups of a dataview as a string rather than casting it into a Datagroups 
     * @param tenantId tenant to go against
     * @param namespaceId namespace to go against
     * @param dataviewId the dataview to get datagroups from
     * @param skip number of datagroups to skip, used in paging
     * @param count nubmer of datagroups to get
     * @return Datagroups as a JSON string
     * @throws SdsError any error that occurs
     */
    public String getDatagroupsString(String tenantId, String namespaceId, String dataviewId, Integer skip, Integer count) throws SdsError {
        
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + getDatagroups.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId).replace("{skip}", skip.toString()).replace("{count}", count.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataview datagroups request failed");
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
     * Get a single datagroupd 
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param dataviewId dataview to get the datagroup from 
     * @param datagroupId specific datagroup from the dataview to get
     * @return datagroup
     * @throws SdsError any error that occurs
     */
    public Datagroup getDatagroup(String tenantId, String namespaceId, String dataviewId, String datagroupId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + getDatagroups.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId).replace("{datagroupId}", datagroupId.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataview datagroup request failed");
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

        Datagroup results = mGson.fromJson(response.toString(), new TypeToken<Datagroup>(){}.getType());
        return results;
       // return response.toString();
    }

    /**
     * Gets a data preview for your dataview
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param dataviewId dataview to get data from
     * @param startIndex start index
     * @param endIndex end index
     * @param interval interval between data points
     * @param form the form to return the data in 
     * @param count number of points to return
     * @param value_class not used
     * @return string of the values you asked for
     * @throws SdsError any error that occurs
     */
    public String getDataviewPreview(String tenantId, String namespaceId, String dataviewId, String startIndex, String endIndex, String interval, String form, Integer count, String value_class) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + getDataviewPreview.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId).replace("{startIndex}", startIndex.toString()).replace("{endIndex}", endIndex.toString()).replace("{interval}", interval.toString()).replace("{form}", form.toString()).replace("{count}", count.toString()).replace("{value_class}", value_class.toString()));
            urlConnection = baseClient.getConnection(url, "GET");
            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataview preview request failed");
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
        

       // Map<String,Object>[]  results = mGson.fromJson(response.toString(), new TypeToken<Map<String,Object>[]>(){}.getType());
      //  return results;
        return response.toString();
    }

    /**
     * get dataview preview using defaults 
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param dataviewId the dataview to get data from 
     * @return the values to return as string
     * @throws SdsError any error that occurs
     */
    public String  getDataviewPreview(String tenantId, String namespaceId, String dataviewId) throws SdsError {
        return getDataviewPreview(tenantId, namespaceId, dataviewId, "","","","",0,"");
    }
    
    /**
     * gets the itnerpolated values of the dataview preview
     * @param tenantId tenant to work against
     * @param namespaceId namespace to work against
     * @param dataviewId the dataview to get data from 
     * @param startIndex the start index
     * @param endIndex the end index
     * @param interval the interval between return points
     * @param form the way the returned data is present
     * @param count the number of returned points
     * @return string of the values asked for
     * @throws SdsError any error that occurs
     */
    public String getDataviewInterpolated(String tenantId, String namespaceId, String dataviewId, String startIndex, String endIndex, String interval, String form, Integer count) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();
        
        try {
            url = new URL(baseUrl + getDataviewInterpolated.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{dataview_id}", dataviewId).replace("{startIndex}", startIndex.toString()).replace("{endIndex}", endIndex.toString()).replace("{interval}", interval.toString()).replace("{form}", form.toString()).replace("{count}", count.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get dataview data interpolated request failed");
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
//        Map<String,Object>[]  results = mGson.fromJson(response.toString(), new TypeToken<Map<String,Object>[]>(){}.getType());
 //       return results;
       // return response.toString();
    }


}
