package samples;

import java.net.*;
import java.nio.Buffer;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import java.io.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.microsoft.aad.adal4j.AuthenticationContext;
import com.microsoft.aad.adal4j.AuthenticationResult;
import com.microsoft.aad.adal4j.ClientCredential;


public class QiClient {
	Gson mGson =  null;
	private String baseUrl = null;
	@SuppressWarnings("unused")
	private String tenantName = null;
   
	// REST API url strings
	// base of all requests
    private String requestBase = "api/Tenants/{tenantId}/Namespaces/{namespaceId}";

    // type paths
	private String typesBase = requestBase + "/Types";
	private String getTypePath = typesBase + "/{typeId}"; // deleting uses the same URI
	private String getTypesPath = typesBase + "?skip={skip}&count={count}";

    // behavior paths
    private String behaviorsBase = requestBase + "/Behaviors";
    private String getBehaviorPath = behaviorsBase + "/{behaviorId}"; // deleting uses the same URI
    private String getBehaviorsPath = behaviorsBase + "?skip={skip}&count={count}";

	// stream paths
	private String streamsBase = requestBase + "/Streams";
	private String getStreamPath = streamsBase + "/{streamId}"; // updating and deleting uses the same URI
    private String getStreamsPath = streamsBase + "?query={query}&skip={skip}&count={count}";

	// data paths
	private String dataBase = requestBase + "/Streams/{streamId}/Data";
	private String insertSinglePath = dataBase + "/InsertValue";
	private String insertMultiplePath = dataBase + "/InsertValues";
	private String getSingleQuery = dataBase + "/GetValue?index={index}";
	private String getLastValuePath = dataBase + "/GetLastValue?";
	private String getWindowQuery = dataBase + "/GetWindowValues?startIndex={startIndex}&endIndex={endIndex}";
	private String getRangeQuery = dataBase + "/GetRangeValues?startIndex={startIndex}&skip={skip}&count={count}&reversed={reverse}&boundaryType={boundaryType}";
    private String updateSinglePath = dataBase + "/UpdateValue";
    private String updateMultiplePath = dataBase + "/UpdateValues";
    private String replaceSinglePath = dataBase + "/ReplaceValue";
    private String replaceMultiplePath = dataBase + "/ReplaceValues";
	private String removeSingleQuery = dataBase + "/RemoveValue?index={index}";
	private String removeMultipleQuery = dataBase + "/RemoveWindowValues?startIndex={startIndex}&endIndex={endIndex}";

	/*
	Possible Additions:
	- Type reference count
	- behavior reference count
	- patch values
	- unique gets (GetDistinctValue, FindDistinctValue, GetWindowFiltered, GetRangeFiltered, GetIntervals, GetNamespace, GetNamespaceSummary)
	 */

	private static AuthenticationContext _authContext = null;
	private static ExecutorService service = null;
	private static AuthenticationResult result = null;
	
	public static  java.net.HttpURLConnection getConnection(URL url, String method)
	{
		java.net.HttpURLConnection urlConnection = null;
		AuthenticationResult token = AcquireAuthToken();
		
		try
		{
			urlConnection = (java.net.HttpURLConnection) url.openConnection();
			urlConnection.setRequestProperty("Accept", "*/*; q=1");
			urlConnection.setRequestMethod(method);
			urlConnection.setUseCaches(false);
			urlConnection.setConnectTimeout(50000);
			urlConnection.setReadTimeout(50000);
			urlConnection.setRequestProperty("Content-Type", "application/json");
			
			urlConnection.setRequestProperty( "Authorization", token.getAccessTokenType()+ " "+ token.getAccessToken());
			if (method == "POST" || method == "PUT" || method == "DELETE")
			{  	
				urlConnection.setChunkedStreamingMode(0);
				urlConnection.setDoOutput(true);     
			}else if(method == "GET")
			{
				//Do nothing
			}
		}
		catch(SocketTimeoutException e)
		{
			e.getMessage();
		}
		catch (ProtocolException e)
		{
			e.getMessage();
		}
		catch (IllegalStateException e)
		{
			e.getMessage();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}

		return urlConnection;
	}

	public QiClient(String baseUrl)
	{	
		mGson = new GsonBuilder().registerTypeAdapter(GregorianCalendar.class, new UTCDateTypeAdapter()).setDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'").create();
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		this.baseUrl =  baseUrl;
		
		try
		{
			url = new URL(this.baseUrl);		
			urlConnection = getConnection(url, "POST");
			urlConnection.setDoOutput(true);
			urlConnection.setRequestMethod("POST");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}
		catch (ProtocolException e)
		{
			e.getMessage();
		}         
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public String createTenant() {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL("http://localhost:5000/api/Tenants");
            urlConnection = getConnection(url, "POST");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            String body = "{'Id':'"+ Constants._tenantId + "'}";
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200 || httpResponse == 201) {
                System.out.println("createTenant request successful");
            }
            else {
                throw new QiError(urlConnection, "createTenant request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return jsonResults.toString();
    }

    public String createNamespace()
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL("http://localhost:5000/api/Tenants/" + Constants._tenantId + "/Namespaces");
            urlConnection = getConnection(url, "POST");
        } catch(MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch(IllegalStateException e) {
            e.getMessage();
        } catch(Exception e) {
            e.printStackTrace();
        }

        try {
            String payload = "{'Id':'" + Constants._namespaceId + "'}";
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(payload);
            writer.close();

            if(urlConnection.getResponseCode() == 200 || urlConnection.getResponseCode() == 201) {
                System.out.println("createNamespace request succeeded");
            } else {
                throw new QiError(urlConnection, "createNamespace request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();

        } catch(Exception e) {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String createType(String tenantId, String namespaceId, QiType typeDef) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try
        {
            url = new URL(baseUrl + typesBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) );
            urlConnection = getConnection(url,"POST");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            String body = mGson.toJson(typeDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("create type request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "create type request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null)
            {
                response.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return response.toString();
    }

    public String getType(String tenantId, String namespaceId, String typeId) throws QiError
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getTypePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResult = urlConnection.getResponseCode();
            if(httpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("get single type request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get single type request failed");
            }

            BufferedReader in = new BufferedReader( new InputStreamReader(urlConnection.getInputStream()));

            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getTypes(String tenantId, String namespaceId, String skip, String count)
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getTypesPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                                                        .replace("{skip}", skip).replace("{count}", count));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResult = urlConnection.getResponseCode();
            if(httpResult == 200) {
                System.out.println("get multiple types request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get multiple types request failed");
            }

            BufferedReader in = new BufferedReader( new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void deleteType(String tenantId, String namespaceId, String typeId)
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + getTypePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{typeId}", typeId));
            urlConnection = getConnection(url,"DELETE");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("delete type request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "delete type request failed");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public String createBehavior(String tenantId, String namespaceId, QiStreamBehavior behavior) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try
        {
            url = new URL(baseUrl + behaviorsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) );
            urlConnection = getConnection(url,"POST");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            String body = mGson.toJson(behavior);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK || HttpResult == HttpURLConnection.HTTP_CREATED)
            {
                System.out.println("create behavior request succeeded");
            }
            else {
                throw new QiError(urlConnection, "create behavior request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null)
            {
                response.append(inputLine);
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return response.toString();
    }

    public String getBehavior(String tenantId, String namespaceId, String behaviorId) throws QiError
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getBehaviorPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{behaviorId}", behaviorId));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("get single behavior request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get single behavior request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getBehaviors(String tenantId, String namespaceId, String skip, String count)
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getBehaviorsPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                                                            .replace("{skip}", skip).replace("{count}", count));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("get multiple behaviors request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get multiple behaviors request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void deleteBehavior(String tenantId, String namespaceId, String behaviorId) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + getBehaviorPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{behaviorId}", behaviorId));
            urlConnection = getConnection(url,"DELETE");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int HttpResult = urlConnection.getResponseCode();

            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("delete behavior request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "delete behavior request failed");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public String createStream(String tenantId, String namespaceId, QiStream streamDef) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer response = new StringBuffer();

        try
        {
            url = new URL(baseUrl + streamsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) );
            urlConnection = getConnection(url,"POST");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            String body = mGson.toJson(streamDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(body);
            writer.close();

            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("create stream request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "create stream request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null)
            {
                response.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return response.toString();

    }

    public String getStream(String tenantId, String namespaceId, String streamId) throws QiError
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("get single stream request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get single stream request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getStreams(String tenantId, String namespaceId, String query, String skip, String count)
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getStreamsPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{query}", query)
                    .replace("{skip}", skip).replace("{count}", count));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("get multiple streams request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get multiple streams request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public void updateStream(String tenantId, String namespaceId, String streamId, QiStream streamDef) throws QiError
	{
		
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		

		try
		{
			url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
			urlConnection = getConnection(url,"PUT");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}        
		catch (Exception e)
		{
			e.printStackTrace();
		}

		
		try
		{
			String body = mGson.toJson(streamDef);           
			OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
			OutputStreamWriter writer = new OutputStreamWriter(out);
			writer.write(body);
			writer.close();

			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("update stream request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "update stream request failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

    public void deleteStream(String tenantId, String namespaceId, String streamId)
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + getStreamPath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url,"DELETE");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("delete stream request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "delete stream request failed");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void insertValue(String tenantId, String namespaceId, String streamId, String evt) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + insertSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url,"POST");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(evt);
            writer.close();

            int HttpResult = urlConnection.getResponseCode();
            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("insert single value request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "insert single value request failed");

            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void insertValues(String tenantId, String namespaceId, String streamId, String json) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        int HttpResult = 0;
        try
        {
            url = new URL(baseUrl + insertMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url,"POST");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            HttpResult = urlConnection.getResponseCode();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        if (HttpResult == HttpURLConnection.HTTP_OK)
        {
            System.out.println("insert multiple values request succeeded");
        }

        if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
        {
            throw new QiError(urlConnection, "insert multiple values request failed");
        }
    }

    public String getSingleValue(String tenantId, String namespaceId, String streamId, String index) throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getSingleQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
            urlConnection = getConnection(url,"GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int HttpResult = urlConnection.getResponseCode();

            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("get single value request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "get single value request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));


            while ((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getLastValue(String tenantId, String namespaceId, String streamId) throws QiError
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getLastValuePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("get last value request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "get last value request failed");
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

    public String getWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex)throws QiError
    {
        java.net.URL url = null;
        java.net.HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try
        {
            url = new URL(baseUrl + getWindowQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
            urlConnection = getConnection(url,"GET");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            int HttpResult = urlConnection.getResponseCode();

            if (HttpResult == HttpURLConnection.HTTP_OK)
            {
                System.out.println("get window of values request succeeded");
            }

            if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
            {
                throw new QiError(urlConnection, "get window of values request request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));


            while ((inputLine = in.readLine()) != null)
            {
                jsonResults.append(inputLine);
            }
            in.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        return jsonResults.toString();
    }

	public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, QiBoundaryType boundaryType)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl + getRangeQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                                                        .replace("{streamId}", streamId).replace("{startIndex}", startIndex)
                                                        .replace("{skip}", "" + skip).replace("{count}", "" + count)
                                                        .replace("{reverse}", "" + reverse).replace("{boundaryType}", "" + boundaryType));
			urlConnection = getConnection(url,"GET");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e)
		{
			e.getMessage();
		}        
		catch (Exception e) 
		{
			e.printStackTrace();
		}

		try
		{
		   int HttpResult = urlConnection.getResponseCode();

		   if (HttpResult == HttpURLConnection.HTTP_OK)
           {
				System.out.println("get range of values request succeeded");
           }

           if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
           {
               throw new QiError(urlConnection, "get range of values request failed");
           }

            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null)
            {
                response.append(inputLine);
            }
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}

		return response.toString();
	}

	public void updateValue(String tenantId, String namespaceId, String streamId, String json)throws QiError 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + updateSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
			urlConnection = getConnection(url,"PUT");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}         
		catch (Exception e) 
		{
			e.printStackTrace();
		}

		try
		{
			OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
			OutputStreamWriter writer = new OutputStreamWriter(out);
			writer.write(json);
			writer.close();

			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("update single value request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "update single value request failed");
			}

		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public void updateValues(String tenantId, String namespaceId, String streamId, String json) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + updateMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
			urlConnection = getConnection(url,"PUT");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}         
		catch (Exception e)
		{
			e.printStackTrace();
		}
		
		try
		{
			OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
			OutputStreamWriter writer = new OutputStreamWriter(out);
			writer.write(json);
			writer.close();

			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("update multiple values request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "update multiple values request failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

    public void replaceValue(String tenantId, String namespaceId, String streamId, String json) throws QiError
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + replaceSinglePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("replace single value request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "replace single value request failed");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void replaceValues(String tenantId, String namespaceId, String streamId, String json)
    {
        java.net.URL url;
        java.net.HttpURLConnection urlConnection = null;

        try
        {
            url = new URL(baseUrl + replaceMultiplePath.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
            urlConnection = getConnection(url, "PUT");
        }
        catch (MalformedURLException mal)
        {
            System.out.println("MalformedURLException");
        }
        catch (IllegalStateException e)
        {
            e.getMessage();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        try
        {
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out);
            writer.write(json);
            writer.close();

            int httpResponse = urlConnection.getResponseCode();
            if(httpResponse == 200)
            {
                System.out.println("replace multiple values request succeeded");
            }
            else
            {
                throw new QiError(urlConnection, "replace multiple values request failed");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

	public void removeValue(String tenantId, String namespaceId, String streamId, String index) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		
		try
		{
			url = new URL(baseUrl + removeSingleQuery.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
			urlConnection = getConnection(url,"DELETE");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}         
		catch (Exception e)
		{
			e.printStackTrace();
		}

		try
		{
			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("remove single value request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "remove single value request failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public void removeWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + removeMultipleQuery.replace("{tenantId}", tenantId)
											.replace("{namespaceId}", namespaceId).replace("{streamId}", streamId)
											.replace("{startIndex}", startIndex).replace("{endIndex}", endIndex));
			urlConnection = getConnection(url,"DELETE");
		}
		catch (MalformedURLException mal)
		{
			System.out.println("MalformedURLException");
		}
		catch (IllegalStateException e) 
		{
			e.getMessage();
		}         
		catch (Exception e) 
		{
			e.printStackTrace();
		}

		try
		{
			int HttpResult = urlConnection.getResponseCode();
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("remove window of values request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "remove window of values request failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	static protected AuthenticationResult AcquireAuthToken()
	{

		service = Executors.newFixedThreadPool(1);
		try
		{
			if (_authContext == null)
			{
				_authContext = new AuthenticationContext(Constants._authority, true , service);
			}

			// tokens expire after a certain period of time
			// You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
			// ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed

			ClientCredential userCred = new ClientCredential(Constants._appId, Constants._appKey);
			Future<AuthenticationResult> authResult = _authContext.acquireToken(Constants._resource, userCred, null);

			//AcquireToken(_resource, userCred);
			result = authResult.get();
		}
		catch (Exception e)
		{
                       // Do nothing
		}
		finally 
		{
			service.shutdown();
		}
		return result;  
	}
}
