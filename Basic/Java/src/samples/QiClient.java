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
	@SuppressWarnings("unused")
	private String tenantsBase = "/Qi/Tenants";
	private String typesBase = "/Qi/Types";
	private String streamsBase = "/Qi/Streams";
	private String behaviorsBase = "/Qi/Behaviors";
	private String insertSingle = "/Data/InsertValue";
	private String insertMultiple = "/Data/InsertValues";
	private String getTemplate = "/Data/GetWindowValues?";
	private String updateSingle = "/Data/UpdateValue";
	private String updateMultiple = "/Data/UpdateValues";
	@SuppressWarnings("unused")
	private String removeSingleTemplate = "/{0}/Data/RemoveValue?index={1}";
	@SuppressWarnings("unused")
	private String removeMultipleTemplate = "/{0}/Data/RemoveWindowValues?startIndex={1}&endIndex={2}";
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
			urlConnection.setRequestMethod(method);
			urlConnection.setUseCaches(false);
			urlConnection.setConnectTimeout(10000);
			urlConnection.setReadTimeout(10000);
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
	
	public void UpdateStream(String streamId, QiStream streamDef){
		
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		

		try
		{
			url = new URL(baseUrl + streamsBase + "/" +streamId );
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
				System.out.println("Update Stream request succeded");
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
	
	public String CreateBehavior(QiStreamBehavior behavior){
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl + behaviorsBase );
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
				System.out.println("behavior creation request succeded");
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

	public void DeleteBehavior(String behaviorId)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + behaviorsBase + "/" + behaviorId);
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
			   System.out.println("behavior creation request succeded");
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

	public String getRangeValues(String streamId, String startIndex, int skip, int count, boolean reverse, QiBoundaryType boundaryType)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl +streamsBase+ "/" +streamId + "/Data/GetRangeValues?startIndex="+startIndex+"&skip="+skip+"&count="+count+"&reversed="+reverse+"&boundaryType="+boundaryType );
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
				System.out.println("get range values request succeded");
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
	
	
	public String CreateType(QiType typeDef)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();

		try
		{
			url = new URL(baseUrl + typesBase );
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
				System.out.println("type creation request succeded");
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


	public String CreateStream(QiStream streamDef)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer response = new StringBuffer();
		
		try
		{
			url = new URL(baseUrl + streamsBase );
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
				System.out.println("stream creation request succeded");
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



	public void CreateEvent(String streamId, String evt)
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + insertSingle);
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
				System.out.println("Event creation request succeded");
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



	public void CreateEvents(String streamId, String json) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		int HttpResult = 0; 
		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + insertMultiple);
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
			System.out.println("Events creation request succeded");
		}

		if (HttpResult != HttpURLConnection.HTTP_OK && HttpResult != HttpURLConnection.HTTP_CREATED)
		{
			throw new QiError(urlConnection, "Events creation failed");
		}
	}



	public String GetWindowValues (String streamId, String startIndex, String endIndex)throws QiError
	{   
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		String inputLine;
		StringBuffer jsonResults = new StringBuffer();

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + getTemplate +  "startIndex=" + startIndex + "&" + "endIndex=" + endIndex);
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
				System.out.println("GetWindowValues request succeded");
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



	public void updateValue(String streamId, String json)throws QiError 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + updateSingle);
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
				System.out.println("UpdateValue request succeded");
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


	public void updateValues(String streamId, String json) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + updateMultiple);
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
				System.out.println("Update Values request succeded");
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



	public void removeValue(String streamId, String index) throws QiError
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		
		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + "/" + "/Data/RemoveValue?index=" + index);
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
				System.out.println("remove Value request succeded");
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

	public void removeWindowValues(String streamId, String startIndex, String endIndex) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId + "/Data/RemoveWindowValues?startIndex=" + startIndex + "&" + "endIndex=" + endIndex );
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
				System.out.println("removeWindowValues request succeded");
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

	public void deleteStream(String streamId) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;
		
		try
		{
			url = new URL(baseUrl + streamsBase + "/" + streamId );
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
				System.out.println("deleteStream request succeded");
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


	public void deleteType(String typeId) 
	{
		java.net.URL url = null;
		java.net.HttpURLConnection urlConnection = null;

		try
		{
			url = new URL(baseUrl + typesBase + "/" + typeId );
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
				System.out.println("deleteType request succeded");
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
