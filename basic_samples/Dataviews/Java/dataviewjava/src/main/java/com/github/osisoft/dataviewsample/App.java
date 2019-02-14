package com.github.osisoft.dataviewsample;


import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import java.time.*;

import  com.github.osisoft.ocs_sample_library_preview.*;
import  com.github.osisoft.ocs_sample_library_preview.sds.*;
import  com.github.osisoft.ocs_sample_library_preview.dataview.*;

public class App {
    // get configuration
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
    static String ocsServerUrl = getConfiguration("ocsServerUrl");	
	
    // id strings
    static String sampleDataviewId = "Dataview_Sample";

    static String samplePressureTypeId = "Time_Pressure_SampleType";
    static String samplePressureStreamId = "Tank_Pressure_SampleStream";
    static String samplePressureStreamName = "Tank Pressure SampleStream";

    static String sampleTemperatureTypeId = "Time_Temperature_SampleType";
    static String sampleTemperatureStreamId = "Tank_Temperature_SampleStream";    
    static String sampleTemperatureStreamName = "Tank Temperature SampleStream";

    static boolean needData = false;

    static SdsClient sdsclient;
    static DataviewClient dataviewclient;
    
    public static void main(String[] args) throws InterruptedException {
    	
        // Create Sds client to communicate with server
    	System.out.println("------------------------------------------------------------------------------------");
        System.out.println(" ######                                                   #    #    #     #    #    ");
        System.out.println(" #     #   ##   #####   ##   #    # # ###### #    #       #   # #   #     #   # #   ");
        System.out.println(" #     #  #  #    #    #  #  #    # # #      #    #       #  #   #  #     #  #   #  ");
        System.out.println(" #     # #    #   #   #    # #    # # #####  #    #       # #     # #     # #     # ");
        System.out.println(" #     # ######   #   ###### #    # # #      # ## # #     # #######  #   #  ####### ");
        System.out.println(" #     # #    #   #   #    #  #  #  # #      ##  ## #     # #     #   # #   #     # ");
        System.out.println(" ######  #    #   #   #    #   ##   # ###### #    #  #####  #     #    #    #     # ");
        System.out.println("------------------------------------------------------------------------------------");
        
        String server = ocsServerUrl + "/";
        ocsClient = new OCSClient();
        System.out.println("Sds endpoint at " + server);
        System.out.println();

        try { 	 

            if(needData)
            {
                createData();
            }
            String sampleStreamId = "SampleStream";

            Dataview dataview = new Dataview();
            dataview.setId(sampleDataviewId);
            DataviewQuery query  = new DataviewQuery();
            query.setId(sampleDataviewId);
            DataviewQueryQuery queryQuery = new DataviewQueryQuery();
            queryQuery.setType("streamname"); 
            queryQuery.setValue(sampleStreamId);
            queryQuery.setOperator("Contains"); 
            query.setQuery(queryQuery);
            DataviewQuery[]  queries  =  new DataviewQuery[1];
            queries[0] = query;
            dataview.setQueries(queries);
            DataviewMapping map = new  DataviewMapping();
            map.setIsDefault("true");
            dataview.setMappings(map); 
            dataview.setIndexDataType("datetime"); 
            DataviewGroupRule groupRule = new DataviewGroupRule();
            groupRule.setId("DefaultGroupRule"); 
            groupRule.setType("StreamTag"); 
            DataviewGroupRule[]  rules  =  new DataviewGroupRule[1];
            rules[0] = groupRule;
//            dataview.setGroupRules(rules);


            System.out.println();
            System.out.println("Cerating dataview");	
            System.out.println(dataviewclient.mGson.toJson(dataview));	
            Dataview dataviewOut = dataviewclient.postDataview(tenantId, namespaceId, dataview);
            
            //Getting the complete set of dataviews to make sure it is there
            System.out.println();
            System.out.println("Getting dataviews");		
            ArrayList<Dataview> dataviews = dataviewclient.getDataviews(tenantId,namespaceId);
            for (Dataview dv: dataviews){
                System.out.println(dataviewclient.mGson.toJson(dv));                
            }            
                
    
            //By default this will get interpolated values every minute over the last hour, which lines up with our data that we sent in.  
            //Beyond the normal API optoins, this function does have the option to return the data in a class if you have created a Type for the data you re retreiving.
        
            System.out.println();            
            System.out.println("Retrieving data from the Dataview");
            Map<String,Object>[] dataviewData = dataviewclient.getDataviewPreview(tenantId, namespaceId, sampleDataviewId);
            System.out.println(dataviewclient.mGson.toJson(dataviewData));
            

            
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            System.out.println("Cleaning up");          
            cleanUp();
        }
    }
    
    private static void createData() {
        
        try {

            SdsType doubleType = new SdsType();
            doubleType.setId("doubleType");
            doubleType.setSdsTypeCode(SdsTypeCode.Double);

            SdsType dateTimeType = new SdsType();
            dateTimeType.setId("dateTimeType");
            dateTimeType.setSdsTypeCode(SdsTypeCode.DateTimeOffset);


            SdsTypeProperty pressureDoubleProperty = new SdsTypeProperty();
            pressureDoubleProperty.setId("pressure");
            pressureDoubleProperty.setSdsType(doubleType);

            SdsTypeProperty temperatureDoubleProperty = new SdsTypeProperty();
            temperatureDoubleProperty.setId("temperature");
            temperatureDoubleProperty.setSdsType(doubleType);
            
            SdsTypeProperty timeDateTimeProperty = new SdsTypeProperty();
            timeDateTimeProperty.setId("time");
            timeDateTimeProperty.setSdsType(dateTimeType);
            timeDateTimeProperty.setIsKey(true);

            // Create a SdsType for our WaveData class; the metadata properties are the ones we just created
            
            SdsType pressure_SDSType = new SdsType();
            pressure_SDSType.setId(samplePressureTypeId);
            SdsTypeProperty[] props = {pressureDoubleProperty, timeDateTimeProperty};
            pressure_SDSType.setProperties(props);
            pressure_SDSType.setSdsTypeCode(SdsTypeCode.Object);

            SdsType temperature_SDSType = new SdsType();
            temperature_SDSType.setId(sampleTemperatureTypeId);
            SdsTypeProperty[] props2 = {temperatureDoubleProperty, timeDateTimeProperty};
            temperature_SDSType.setProperties(props2);
            temperature_SDSType.setSdsTypeCode(SdsTypeCode.Object);

            

            System.out.println("Creating SDS Type");
            System.out.println(sdsclient.mGson.toJson(pressure_SDSType));


            sdsclient.createType(tenantId, namespaceId, pressure_SDSType);
            sdsclient.createType(tenantId, namespaceId, temperature_SDSType);

            SdsStream pressureStream = new SdsStream(samplePressureStreamId, samplePressureTypeId);
            pressureStream.setName(samplePressureStreamName);

            SdsStream temperatureStream = new SdsStream(sampleTemperatureStreamId, sampleTemperatureTypeId);
            temperatureStream.setName(sampleTemperatureStreamName);
            
            System.out.println("Creating SDS Streams");
            String jsonStream = sdsclient.createStream(tenantId, namespaceId, pressureStream);
            jsonStream = sdsclient.createStream(tenantId, namespaceId, temperatureStream);

            Instant start = Instant.now().minus(Duration.ofHours(1));

            ArrayList<String> pressureValues = new ArrayList<String>();
            ArrayList<String> temperatureValues = new ArrayList<String>();

            System.out.println("Creating values");
            for (int i = 1; i < 60; i += 1) 
            {
                String pVal =  ("{\"time\" : \""+ start.plus(Duration.ofMinutes(i* 1)) +"\", \"pressure\":" + Math.random() * 100 + "}");
                String tVal =  ("{\"time\" : \""+ start.plus(Duration.ofMinutes(i* 1)) +"\", \"temperature\":" + (Math.random() * 20 + 50) + "}");
                pressureValues.add(pVal);
                temperatureValues.add(tVal);
            }

            String pVals = "[" + String.join(",", pressureValues) + "]";
            String tVals = "[" + String.join(",", temperatureValues) + "]";

            System.out.println("Sending pressure values");
            sdsclient.updateValues(tenantId, namespaceId, samplePressureStreamId, pVals);
            System.out.println("Sending temperature values");
            sdsclient.updateValues(tenantId, namespaceId, sampleTemperatureStreamId, tVals);

        }
        catch (Exception e) {
            printError("Error craeting Sds Objects", e);
        }
    }

    /**
     * Prints out a formated error string
     *
     * @param exceptionDescription - the description of what the error is
     * @param exception            - the exception thrown
     */
    private static void printError(String exceptionDescription, Exception exception) {
        System.out.println("\n\n======= " + exceptionDescription + " =======");
        System.out.println(exception.toString());
        System.out.println("======= End of " + exceptionDescription + " =======");
    }

    
    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        InputStream inputStream;

        try {
            inputStream = new FileInputStream(System.getProperty("user.dir") + "\\basic_samples\\Dataviews\\JAVA\\config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return property;
    }
	
    public static void cleanUp() 
	{
        try
        {
            if(true)
            {
                System.out.println("Deleting the streams");
                sdsclient.deleteStream(tenantId, namespaceId, samplePressureStreamId);
                sdsclient.deleteStream(tenantId, namespaceId, sampleTemperatureStreamId);
                System.out.println("Deleting the types");
                sdsclient.deleteType(tenantId, namespaceId, samplePressureTypeId);
                sdsclient.deleteType(tenantId, namespaceId, sampleTemperatureTypeId);

            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    };
    
    public static Boolean getBool()
    {
        return false;
    }
}
