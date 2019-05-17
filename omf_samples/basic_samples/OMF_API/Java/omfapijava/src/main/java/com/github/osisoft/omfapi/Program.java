/** Program.java
 * 
 */

// OMF_API_Java
// Version 1.0.1
// 3-21-19

package com.github.osisoft.omfapi;

//import com.google.gson.reflect.TypeToken;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import java.io.*;
import java.net.*;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;
import java.util.concurrent.ThreadLocalRandom;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import java.time.*;


public class Program 
{
    //holder used for test result
    static Boolean success = true;
    static Exception exc;

    //settings that aren't set by configuration 
    static String compression = "none";
    static String omfVersion = "1.1";
    static boolean forceSend = false;
    
    // used in holding the access token 
    static String cachedAccessToken = null;
    static Date accessTokenExpiration = new Date(Long.MIN_VALUE);
    static long FIVE_SECONDS_IN_MILLISECONDS = 5000;

    
    static boolean sendToOCS = true;

    // Step 1
    static String resource = getConfiguration("resource");;
    static String clientId = getConfiguration("clientId");
    static String clientSecret = getConfiguration("clientSecret");
    static String apiVersion = getConfiguration("apiVersion");
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
    static String dataServerName = getConfiguration("dataServerName");
    static String omfEndPoint = "";
    static String checkBase = "";
  

    //values used across calls of a function
    static int integer_boolean_value = 0;
    static String string_boolean_value = "True";
    static int integer_index1 = 0;
    static int integer_index2_1 = 1;
    static int integer_index2_2 = 1;
	
    public static void main( String[] args )
    {
        try
        {
            toRun(false);
        }
        catch (Exception e) {
        }
    }     
    
        
    private static void disableSslVerification() {
        try
        {
            // Create a trust manager that does not validate certificate chains
            TrustManager[] trustAllCerts = new TrustManager[] {new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
                public void checkClientTrusted(X509Certificate[] certs, String authType) {
                }
                public void checkServerTrusted(X509Certificate[] certs, String authType) {
                }
            }
            };

            // Install the all-trusting trust manager
            SSLContext sc = SSLContext.getInstance("SSL");
            sc.init(null, trustAllCerts, new java.security.SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

            // Create all-trusting host name verifier
            HostnameVerifier allHostsValid = new HostnameVerifier() {
                public boolean verify(String hostname, SSLSession session) {
                    return true;
                }
            };

            // Install the all-trusting host verifier
            HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (KeyManagementException e) {
            e.printStackTrace();
        }
    }
    
    
    public static boolean toRun(Boolean test) throws Exception {
        disableSslVerification();

        // Create Sds client to communicate with server
        System.out.println("------------------------------------------------------------------");
        System.out.println(" .d88888b.  888b     d888 8888888888        8888888b. Y88b   d88P ");
        System.out.println("d88P\" \"Y88b 8888b   d8888 888               888   Y88b Y88b d88P  ");
        System.out.println("888     888 88888b.d88888 888               888    888  Y88o88P   ");
        System.out.println("888     888 888Y88888P888 8888888           888   d88P   Y888P    ");
        System.out.println("888     888 888 Y888P 888 888               8888888P\"     888     ");
        System.out.println("888     888 888  Y8P  888 888               888           888     ");
        System.out.println("Y88b. .d88P 888   \"   888 888               888           888     ");
        System.out.println(" \"Y88888P\"  888       888 888      88888888 888           888     ");
        System.out.println("------------------------------------------------------------------");

        try {

            if(!forceSend){
                sendToOCS = (tenantId != null && !tenantId.isEmpty());
            }
            
            if (sendToOCS){
                checkBase = resource + "/api/" + apiVersion + "/tenants/" + tenantId + "/namespaces/" + namespaceId;
                omfEndPoint = checkBase + "/omf";
            }
            else{
                checkBase = resource;
                omfEndPoint = checkBase + "/omf";
            }

            // Step 2 
            AcquireAuthToken();
            
            System.out.println("Sending Types and Containers");
            // Steps 3-8 contained in here
            oneTimeSendMessages("create");

            System.out.println("Sending Data ");
            // Step 9
            int count = 0;
            String val2 = "";

            while (count == 0 || (!test && count < 2)){
                String val = create_data_values_for_first_dynamic_type("Container1");
                val2 = val;

                sendOMF(val,"data", "create");
                sendOMF(create_data_values_for_first_dynamic_type("Container2"),"data", "create");
                sendOMF(create_data_values_for_second_dynamic_type("Container3"),"data", "create");
                sendOMF(create_data_values_for_third_dynamic_type("Container4"),"data", "create");

                if(sendToOCS){
                    sendOMF(create_data_values_for_NonTimeStampIndexAndMultiIndex_type("Container5", "Container6"),"data", "create");
                }

                Thread.sleep(1000);
                count = count +1;
            }

            checkSends(val2);

        }
        catch (Exception e) {
            success = false;
            e.printStackTrace();
            exc = e;
        } finally {
            System.out.println("Deletings");

            try{
                // Step 10
                oneTimeSendMessages("Delete");
            }
            catch(Exception e) {
                if(!success && sendToOCS){
                    success = false;
                    exc = e;                    
                }
                e.printStackTrace();
            }

            System.out.println("Done");
        }
        if(!success){
            success = false;
            throw exc;               
        }
        return success;
    }
    
    private static void checkSends(String lastVal) throws Exception {
        System.out.println("Checks");
        Gson gson = new Gson();
        if(sendToOCS){
            String json1;
            // just getting back the type or stream means that it worked
            json1 = getValue(checkBase + "/Types" + "/FirstDynamicType");
            //System.out.println(json1);
            json1 = getValue(checkBase + "/Streams" + "/Container1");
            //System.out.println(json1);
            json1 = getValue(checkBase + "/Streams" + "/Container1"+ "/Data/last");
            //System.out.println(json1);

            Map<String, Object> mappy = gson.fromJson(json1, Map.class);
            String temp = " \"IntegerProperty\": " + mappy.get("IntegerProperty").toString().replace(".0", "");
            
            if(!lastVal.contains(temp))
                throw new Exception("Expected value not found from sending it via OMF");

        }
        else{

            String json1;
            json1 = getValue(checkBase + "/dataservers?name=" + dataServerName);
            Map<String, Object> mappy = gson.fromJson(json1, Map.class);
            Map<String, Object> mappy2 = ( Map<String, Object>)mappy.get("Links");
        
            String pointsURL = mappy2.get("Points").toString();

            json1 = getValue(pointsURL+ "?nameFilter=container1*");
            Map<String, Object> mappy3 = gson.fromJson(json1, Map.class);
            Map<String, Object> mappy4 = ((ArrayList<Map<String, Object>>)mappy3.get("Items")).get(0);
            Map<String, Object> mappy5 = ((Map<String, Object>)mappy4.get("Links"));
            String EndValueUrl = mappy5.get("EndValue").toString();
            
            String json3 = getValue(EndValueUrl);
            Map<String, Object> mappy6 = gson.fromJson(json3, Map.class);
            String temp = mappy6.get("Value").toString().replace(".0", "");;
            if(!lastVal.contains(temp))
                throw new Exception("Expected value not found from sending it via OMF");
        }
    
    
    }

    private static String create_data_values_for_first_dynamic_type(String containerid) {
        return "[" +
        "        {" +
        "            \"containerid\": \"" + containerid +"\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"timestamp\": \"" + Instant.now().toString()   +"\"," +
        "                    \"IntegerProperty\": " + ThreadLocalRandom.current().nextInt(0, 100) +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
    }

    
    private static String create_data_values_for_second_dynamic_type(String containerid) {
            
        if(string_boolean_value == "True"){
            string_boolean_value = "False";
        }
        else{
            string_boolean_value = "True";
        }
        return "[" +
        "        {" +
        "            \"containerid\": \""+containerid+"\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"timestamp\": \""+Instant.now().toString() +"\"," +
        "                    \"NumberProperty1\": "+ThreadLocalRandom.current().nextInt(0, 100)+"," +
        "                    \"NumberProperty2\": "+ThreadLocalRandom.current().nextInt(0, 100)+"," +
        "                    \"StringEnum\": \""+string_boolean_value +"\"" +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
    }

    
    private static String create_data_values_for_third_dynamic_type(String containerid) {
            
        if(integer_boolean_value == 0){
            integer_boolean_value = 1;
        }
        else{
            integer_boolean_value = 0;
        }
        return "[" +
        "        {" +
        "            \"containerid\": \""+containerid+"\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"timestamp\": \""+Instant.now().toString() +"\"," +
        "                    \"IntegerEnum\": "+integer_boolean_value+"," +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
    }
    
    private static String create_data_values_for_NonTimeStampIndexAndMultiIndex_type(String NonTimeStampIndexID, String MultiIndexId) {
            
        integer_index1 = integer_index1 + 2;
        if(integer_index2_2 % 3 == 0){
            integer_index2_2 = 1;
            integer_index2_1 = integer_index2_1 +1;
        }
        else{
            integer_index2_2 = integer_index2_2 + 1;
        }
        return "[" +
        "        {" +
        "            \"containerid\": \""+NonTimeStampIndexID+"\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"Value\": "+ThreadLocalRandom.current().nextInt(0, 88)+"," +
        "                    \"Int_Key\": "+integer_index1+"" +
        "                }," +
        "                {" +
        "                    \"Value\": "+ThreadLocalRandom.current().nextInt(0, 88)+"," +
        "                    \"Int_Key\": "+integer_index1 + 1+"" +
        "                }" +
        "            ]" +
        "        }," +
        "        {" +
        "            \"containerid\": \""+MultiIndexId+"\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"Value1\": "+ThreadLocalRandom.current().nextInt(-125, 0)+"," +
        "                    \"Value2\": "+ThreadLocalRandom.current().nextInt(0, 42)+"," +
        "                    \"IntKey\": "+integer_index2_1+"," +
        "                    \"IntKey2\": "+integer_index2_2+"" +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
    }

    private static void oneTimeSendMessages(String action) throws Exception {
        if(sendToOCS)
        {
            return;
        }


        //Step 3
        sendOMF(getFirstandSecondStaticTypeString(),"type",action);
        //Step 4
        sendOMF(getDynamicTypeString(),"type",action);        
        //Step 5
        if(sendToOCS){
            sendOMF(getDynamicTypeMultiIndexString(),"type",action);
        }

        //Step 6
        sendOMF(getContainers(),"container",action);
        if(sendToOCS){
            sendOMF(getMultiIndexContainers(),"type",action);
        }
            
        //Step 7
        sendOMF(getStatic1(),"data",action);
        //Step 8
        //sendOMF(getLink1(),"data",action);
      //  sendOMF(getLink2(),"data",action);
        
    }

    private static String getLink2() {
        return "[" +
        "        {" +
        "            \"typeid\": \"__Link\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"FirstStaticType\"," +
        "                            \"index\": \"Asset1\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"containerid\": \"Container1\"" +
        "                    }" +
        "                }," +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"SecondStaticType\"," +
        "                            \"index\": \"Asset2\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"containerid\": \"Container2\"" +
        "                    }" +
        "                }," +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"SecondStaticType\"," +
        "                            \"index\": \"Asset2\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"containerid\": \"Container3\"" +
        "                    }" +
        "                }," +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"SecondStaticType\"," +
        "                            \"index\": \"Asset2\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"containerid\": \"Container4\"" +
        "                    }" +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";        
    }

    private static String getLink1() {
        return "[" +
        "        {" +
        "            \"typeid\": \"__Link\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"FirstStaticType\"," +
        "                            \"index\": \"_ROOT\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"typeid\": \"FirstStaticType\"," +
        "                            \"index\": \"Asset1\"" +
        "                    }" +
        "                }," +
        "                {" +
        "                    \"source\": {" +
        "                            \"typeid\": \"FirstStaticType\"," +
        "                            \"index\": \"Asset1\"" +
        "                    }," +
        "                    \"target\": {" +
        "                            \"typeid\": \"SecondStaticType\"," +
        "                            \"index\": \"Asset2\"" +
        "                    }" +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
    }

    private static String getStatic1() {
        return "[" +
        "        {" +
        "            \"typeid\": \"FirstStaticType\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"index\": \"Asset1\"," +
        "                    \"name\": \"Parent element\"," +
        "                    \"StringProperty\": \"Parent element attribute value\"" +
        "                }" +
        "            ]" +
        "        }," +
        "        {" +
        "            \"typeid\": \"SecondStaticType\"," +
        "            \"values\": [" +
        "                {" +
        "                    \"index\": \"Asset2\"," +
        "                    \"name\": \"Child element\"," +
        "                    \"StringProperty\": \"Child element attribute value\"" +
        "                }" +
        "            ]" +
        "        }" +
        "    ]";
        
    }

    private static String getMultiIndexContainers() {
        return "[" +
        "            {" +
        "                \"id\": \"Container5\"," +
        "                \"typeid\": \"NonTimeStampIndex\"" +
        "            }," +
        "            {" +
        "                \"id\": \"Container6\"," +
        "                \"typeid\": \"MultiIndex\"" +
        "            }" +
        "        ]";
    }

    private static String getContainers() {
        return "[" +
        "        {" +
        "            \"id\": \"Container1\"," +
        "            \"typeid\": \"FirstDynamicType\"" +
        "        }," +
        "        {" +
        "            \"id\": \"Container2\"," +
        "            \"typeid\": \"FirstDynamicType\"" +
        "        }," +
        "        {" +
        "            \"id\": \"Container3\"," +
        "            \"typeid\": \"SecondDynamicType\"" +
        "        }," +
        "        {" +
        "            \"id\": \"Container4\"," +
        "            \"typeid\": \"ThirdDynamicType\"" +
        "        }" +
        "    ]";
    }

    private static String getDynamicTypeMultiIndexString() {
        return "[" +
        "            {" +
        "                \"id\": \"NonTimeStampIndex\"," +
        "                \"name\": \"NonTimeStampIndex\"," +
        "                \"classification\": \"dynamic\"," +
        "                \"type\": \"object\"," +
        "                \"description\": \"Integer Fun\"," +
        "                \"properties\": {" +
        "                    \"Value\": {" +
        "                        \"type\": \"number\"," +
        "                        \"name\": \"Value\"," +
        "                        \"description\": \"This could be any value\"" +
        "                    }," +
        "                    \"Int_Key\": {" +
        "                        \"type\": \"integer\"," +
        "                        \"name\": \"Integer Key\"," +
        "                        \"isindex\": true," +
        "                        \"description\": \"A non-time stamp key\"" +
        "                    }" +
        "                }" +
        "            },        " +
        "            {" +
        "                \"id\": \"MultiIndex\"," +
        "                \"name\": \"Multi_index\"," +
        "                \"classification\": \"dynamic\"," +
        "                \"type\": \"object\"," +
        "                \"description\": \"This one has multiple indicies\"," +
        "                \"properties\": {" +
        "                    \"Value\": {" +
        "                        \"type\": \"number\"," +
        "                        \"name\": \"Value1\"," +
        "                        \"description\": \"This could be any value\"" +
        "                    },                " +
        "                    \"Value2\": {" +
        "                        \"type\": \"number\"," +
        "                        \"name\": \"Value2\"," +
        "                        \"description\": \"This could be any value too\"" +
        "                    }," +
        "                    \"IntKey\": {" +
        "                        \"type\": \"integer key part 1\"," +
        "                        \"name\": \"integer key part 1\"," +
        "                        \"isindex\": true," +
        "                        \"description\": \"This could represent any integer value\"" +
        "                    }," +
        "                    \"IntKey2\": {" +
        "                        \"type\": \"integer key part 2\"," +
        "                        \"name\": \"integer key part 2\"," +
        "                        \"isindex\": true," +
        "                        \"description\": \"This could represent any integer value as well\"" +
        "                    }" +
        "                }" +
        "            }" +
        "        ]";
    }

    private static String getDynamicTypeString() {
        return "[" +
        "        {" +
        "            \"id\": \"FirstDynamicType\"," +
        "            \"name\": \"First dynamic type\"," +
        "            \"classification\": \"dynamic\"," +
        "            \"type\": \"object\"," +
        "            \"description\": \"not in use\"," +
        "            \"properties\": {" +
        "                \"timestamp\": {" +
        "                    \"format\": \"date-time\"," +
        "                    \"type\": \"string\"," +
        "                    \"isindex\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"IntegerProperty\": {" +
        "                    \"type\": \"integer\"," +
        "                    \"description\": \"PI point data referenced integer attribute\"" +
        "                }" +
        "            }" +
        "        }," +
        "        {" +
        "            \"id\": \"SecondDynamicType\"," +
        "            \"name\": \"Second dynamic type\"," +
        "            \"classification\": \"dynamic\"," +
        "            \"type\": \"object\"," +
        "            \"description\": \"not in use\"," +
        "            \"properties\": {" +
        "                \"timestamp\": {" +
        "                    \"format\": \"date-time\"," +
        "                    \"type\": \"string\"," +
        "                    \"isindex\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"NumberProperty1\": {" +
        "                    \"type\": \"number\"," +
        "                    \"description\": \"PI point data referenced number attribute 1\"," +
        "                    \"format\": \"float64\"" +
        "                }," +
        "                \"NumberProperty2\": {" +
        "                    \"type\": \"number\"," +
        "                    \"description\": \"PI point data referenced number attribute 2\"," +
        "                    \"format\": \"float64\"" +
        "                }," +
        "                \"StringEnum\": {" +
        "                    \"type\": \"string\"," +
        "                    \"enum\": [\"False\", \"True\"]," +
        "                    \"description\": \"String enumeration to replace boolean type\"" +
        "                }" +
        "            }" +
        "        }," +
        "        {" +
        "            \"id\": \"ThirdDynamicType\"," +
        "            \"name\": \"Third dynamic type\"," +
        "            \"classification\": \"dynamic\"," +
        "            \"type\": \"object\"," +
        "            \"description\": \"not in use\"," +
        "            \"properties\": {" +
        "                \"timestamp\": {" +
        "                    \"format\": \"date-time\"," +
        "                    \"type\": \"string\"," +
        "                    \"isindex\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"IntegerEnum\": {" +
        "                    \"type\": \"integer\"," +
        "                    \"format\": \"int16\"," +
        "                    \"enum\": [0, 1]," +
        "                    \"description\": \"Integer enumeration to replace boolean type\"" +
        "                }" +
        "            }" +
        "        }" +
        "    ]";
    }

    private static String getFirstandSecondStaticTypeString() {
        return "[" +
        "        {" +
        "            \"id\": \"FirstStaticType\"," +
        "            \"name\": \"First static type\"," +
        "            \"classification\": \"static\"," +
        "            \"type\": \"object\"," +
        "            \"description\": \"First static asset type\"," +
        "            \"properties\": {" +
        "                \"index\": {" +
        "                    \"type\": \"string\"," +
        "                    \"isindex\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"name\": {" +
        "                    \"type\": \"string\"," +
        "                    \"isname\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"StringProperty\": {" +
        "                    \"type\": \"string\"," +
        "                    \"description\": \"First static asset type's configuration attribute\"" +
        "                }" +
        "            }" +
        "        }," +
        "        {" +
        "            \"id\": \"SecondStaticType\"," +
        "            \"name\": \"Second static type\"," +
        "            \"classification\": \"static\"," +
        "            \"type\": \"object\"," +
        "            \"description\": \"Second static asset type\"," +
        "            \"properties\": {" +
        "                \"index\": {" +
        "                    \"type\": \"string\"," +
        "                    \"isindex\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"name\": {" +
        "                    \"type\": \"string\"," +
        "                    \"isname\": true," +
        "                    \"description\": \"not in use\"" +
        "                }," +
        "                \"StringProperty\": {" +
        "                    \"type\": \"string\"," +
        "                    \"description\": \"Second static asset type's configuration attribute\"" +
        "                }" +
        "            }" +
        "        }" +
        "    ]";
        
    }



    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        InputStream inputStream;

        try {
            System.out.println(new File(".").getAbsolutePath());
            inputStream = new FileInputStream("config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return property;
    }

    public static String getValue(String urlIn) throws Exception{
        URL url = null;
        HttpURLConnection urlConnection = null;
        String inputLine;
        StringBuffer jsonResults = new StringBuffer();

        try {
            url = new URL(urlIn );
            urlConnection = getConnection(url, "GET", "" , "");
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.getMessage();
        } catch (Exception e) {
            e.printStackTrace();
        }
        int httpResult = urlConnection.getResponseCode();

        try {

            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new Exception("get single value request failed");
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(urlConnection.getInputStream()));

            while ((inputLine = in.readLine()) != null) {
                jsonResults.append(inputLine);
            }
            in.close();
        }  catch (Exception e) {
            StringBuffer httpErrorMessage = new StringBuffer();

            try {        
                String inputLineError;
                if (urlConnection.getErrorStream() != null) {
                    BufferedReader in = new BufferedReader(
                            new InputStreamReader(urlConnection.getErrorStream()));
    
                    while ((inputLineError = in.readLine()) != null) {
                        httpErrorMessage.append(inputLineError);
                    }
                    in.close();
                }
    
            } catch (IOException exc) {
                exc.printStackTrace();
            }

            throw new Exception("Get value failed." + url.toString() + "  "  + httpResult + "  " + httpErrorMessage.toString());
        }

        return jsonResults.toString();
	}

    public static void sendOMF(String messageToSend, String message_type, String action ) throws Exception {
        URL url = null;
        HttpURLConnection urlConnection = null;
        try {
            url = new URL(omfEndPoint);
            urlConnection = getConnection(url, "POST",message_type, action);
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
            writer.write(messageToSend);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (isSuccessResponseCode(httpResult) || httpResult ==409) {
            } else {

                StringBuffer httpErrorMessage = new StringBuffer();

                try {        
                    String inputLine;
                    if (urlConnection.getErrorStream() != null) {
                        BufferedReader in = new BufferedReader(
                                new InputStreamReader(urlConnection.getErrorStream()));
        
                        while ((inputLine = in.readLine()) != null) {
                            httpErrorMessage.append(inputLine);
                        }
                        in.close();
                    }
        
                } catch (IOException e) {
                    e.printStackTrace();
                }

                throw new Exception("Post OMF failed."  + httpResult + "  " + httpErrorMessage.toString());
            }
        } catch (Exception e) {
            success = false;
            e.printStackTrace();
            throw e;
        }
	}

    protected static String AcquireAuthToken() {

        if(!sendToOCS){
            return null;
        }

        if (cachedAccessToken != null){
            long tokenExpirationTime = accessTokenExpiration.getTime(); // returns time in milliseconds.
            long currentTime = System.currentTimeMillis();
            long timeDifference = tokenExpirationTime - currentTime;

            if(timeDifference > FIVE_SECONDS_IN_MILLISECONDS)
                return cachedAccessToken;
        }

        // get new token 
        try {
            URL discoveryUrl = new URL(resource + "/identity/.well-known/openid-configuration");
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

            String postString = "client_id=" + URLEncoder.encode(clientId, "UTF-8") 
                + "&client_secret=" + URLEncoder.encode(clientSecret, "UTF-8") 
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
    

    public static boolean isSuccessResponseCode(int responseCode) {
        return responseCode >= 200 && responseCode < 300;
    }
    
   
    public static HttpURLConnection getConnection(URL url, String method, String message_type, String action) {
        HttpURLConnection urlConnection = null;

        try {
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(method);
            if(sendToOCS){
                urlConnection.setRequestProperty("Accept", "*/*; q=1");
                urlConnection.setRequestProperty("Content-Type", "application/json");
                String token = AcquireAuthToken();
                urlConnection.setRequestProperty("Authorization", "Bearer " + token);
                urlConnection.setRequestProperty("producertoken", token);
            }
            urlConnection.setRequestProperty("messagetype", message_type);
            urlConnection.setRequestProperty("action", action);
            urlConnection.setRequestProperty("omfversion", omfVersion);
            urlConnection.setRequestProperty("messageformat", "json");
//            urlConnection.setRequestProperty("compression", compression);
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
}
