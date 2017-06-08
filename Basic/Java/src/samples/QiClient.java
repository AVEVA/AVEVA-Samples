package samples;

import java.net.*;
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
	private String requestBase = "api/Tenants/{tenantId}/Namespaces/{namespaceId}";
	private String typesBase = requestBase + "/Types";
	private String streamsBase = requestBase + "/Streams";
	private String behaviorsBase = requestBase + "/Behaviors";
	private String dataManipulateBase = requestBase + "/Streams/{streamId}/Data";
	private String insertSingle = dataManipulateBase + "/InsertValue";
	private String insertMultiple = dataManipulateBase + "/InsertValues";
	private String getTemplate = dataManipulateBase + "/GetWindowValues?";
	private String updateSingle = dataManipulateBase + "/UpdateValue";
	private String updateMultiple = dataManipulateBase + "/UpdateValues";
	private String removeSingleTemplate = dataManipulateBase + "/RemoveValue?index={index}";
	private String removeMultipleTemplate = dataManipulateBase + "/RemoveWindowValues?startIndex={startIndex}&endIndex={endIndex}";

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
	
	public void updateStream(String tenantId, String namespaceId, String streamId, QiStream streamDef)
	{
		
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		

		try
		{
			url = new URL(baseUrl + streamsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) + "/" + streamId );
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
				System.out.println("Update Stream request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Stream update  failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
	
	public String createBehavior(String tenantId, String namespaceId, QiStreamBehavior behavior)
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
			if (HttpResult == HttpURLConnection.HTTP_OK)
			{
				System.out.println("behavior creation request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "behavior creation failed");
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

	public void deleteBehavior(String tenantId, String namespaceId, String behaviorId)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + behaviorsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) + "/" + behaviorId);
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
			   System.out.println("behavior deletion request succeeded");
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

	public String getRangeValues(String tenantId, String namespaceId, String streamId, String startIndex, int skip, int count, boolean reverse, QiBoundaryType boundaryType)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl +streamsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)+ "/" +streamId + "/Data/GetRangeValues?startIndex="+startIndex+"&skip="+skip+"&count="+count+"&reversed="+reverse+"&boundaryType="+boundaryType );
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
				System.out.println("get range values request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "get range values request failed");
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
	
	
	public String createType(String tenantId, String namespaceId, QiType typeDef)
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
				System.out.println("type creation request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Type creation failed");
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


	public String createStream(String tenantId, String namespaceId, QiStream streamDef)
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
				System.out.println("stream creation request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Stream creation failed");
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

	public void createEvent(String tenantId, String namespaceId, String streamId, String evt)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + insertSingle.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
				System.out.println("Event creation request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Event creation failed");

			}
		}
		catch (Exception e)
		{
                        e.printStackTrace();
		}
	}

	public void createEvents(String tenantId, String namespaceId, String streamId, String json) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		int HttpResult = 0; 
		try
		{
			url = new URL(baseUrl + insertMultiple.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
			System.out.println("Events creation request succeeded");
		}

		if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
		{
			throw new QiError(urlConnection, "Events creation failed");
		}
	}

	public String getWindowValues (String tenantId, String namespaceId, String streamId, String startIndex, String endIndex)throws QiError
	{   
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer jsonResults = new StringBuffer();

		try
		{
			url = new URL(baseUrl + getTemplate.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId) +  "startIndex=" + startIndex + "&" + "endIndex=" + endIndex);
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
				System.out.println("GetWindowValues request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "GetWindowValues request failed");
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

	public void updateValue(String tenantId, String namespaceId, String streamId, String json)throws QiError 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + updateSingle.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
				System.out.println("UpdateValue request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "GetWindowValues request failed");
			}

		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}


	public void updateValues(String tenantId, String namespaceId, String streamId, String json) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + updateMultiple.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId));
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
				System.out.println("Update Values request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Update Values request failed");
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
			url = new URL(baseUrl + removeSingleTemplate.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId).replace("{streamId}", streamId).replace("{index}", index));
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
				System.out.println("remove Value request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Remove value request failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	public void removeWindowValues(String tenantId, String namespaceId, String streamId, String startIndex, String endIndex) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + removeMultipleTemplate.replace("{tenantId}", tenantId)
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
				System.out.println("removeWindowValues request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Remove windows value request failed");
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
			url = new URL(baseUrl + streamsBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) + "/" + streamId );
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
				System.out.println("deleteStream request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Delete  Stream failed");
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}


	public void deleteType(String tenantId, String namespaceId, String typeId) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + typesBase.replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId) + "/" + typeId );
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
				System.out.println("deleteType request succeeded");
			}

			if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
			{
				throw new QiError(urlConnection, "Delete type failed");
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
