package samples;

import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class Program {
    // get configuration
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
    static String qiServerUrl = getConfiguration("qiServerUrl");	
	
    // id strings
    static String sampleTypeId = "WaveData_SampleType";
    static String targetTypeId = "WaveData_SampleTargetType";
    static String integerTargetTypeId = "WaveData_SampleIntegerTargetType";
    static String sampleStreamId = "WaveData_SampleStream";
    static String sampleBehaviorId = "WaveData_SampleBehavior";  
    static String sampleViewId = "WaveData_SampleView";
    static String sampleManualViewId = "WaveData_SampleManualView";
    
    
    public static void main(String[] args) throws InterruptedException {
    	
        // Create Qi client to communicate with server
    	System.out.println("---------------------------------------------------");
        System.out.println("________  .__     ____.                   ");
        System.out.println("\\_____  \\ |__|   |    |____ ___  _______   ");
        System.out.println(" /  / \\  \\|  |   |    \\__  \\\\  \\/ /\\__  \\  ");
        System.out.println("/   \\_/.  \\  /\\__|    |/ __ \\\\   /  / __ \\_");
        System.out.println("\\_____\\ \\_/__\\________(____  /\\_/  (____  /");
        System.out.println("       \\__>                \\/           \\/ ");
        System.out.println("---------------------------------------------------");
        
        String server = qiServerUrl + "/";
        QiClient qiclient = new QiClient(server);
        System.out.println("Qi endpoint at " + server);
        System.out.println();

        try { 	          	
            // create a QiType
        	System.out.println("Creating a QiType");
            QiType sampleType = getWaveDataType(sampleTypeId);
            String jsonType = qiclient.createType(tenantId, namespaceId, sampleType);
            sampleType = qiclient.mGson.fromJson(jsonType, QiType.class);
            
            //create a QiStream
            System.out.println("Creating a QiStream");
            QiStream sampleStream = new QiStream(sampleStreamId, sampleTypeId);
            String jsonStream = qiclient.createStream(tenantId, namespaceId, sampleStream);
            sampleStream = qiclient.mGson.fromJson(jsonStream, QiStream.class);	
            
            // insert data
            System.out.println("Inserting data");
            
            // insert a single event
            WaveData evt = WaveData.next(1, 2.0, 0);
            qiclient.insertValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // insert a list of events
            List<WaveData> events = new ArrayList<WaveData>();
            for (int i = 2; i < 20; i += 2) {
                evt = WaveData.next(1, 2.0, i);
                events.add(evt);
                Thread.sleep(10);
            	}
            qiclient.insertValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(events));
            
            // get the last value in stream
            System.out.println("Getting latest event");
            String jsonSingleValue = qiclient.getLastValue(tenantId, namespaceId, sampleStreamId);
            WaveData data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class);
            System.out.println(data.toString());
            System.out.println();
            
            // get all values
            System.out.println("Getting all events");            
            String jsonMultipleValues = qiclient.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "20");
            Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData> type
            ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
            // update the first value
            System.out.println("Updating events");
            evt = WaveData.next(1, 1.0, 0);
            qiclient.updateValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // update existing values and add 10 new values using update
            List<WaveData> newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 40; i += 2) // note: update will replace a value if it already exists, and create one if it does not
            {
                WaveData newEvt = WaveData.next(1, 1.0, i);
                newEvents.add(newEvt);
                Thread.sleep(10); // sleep for a bit because WaveData.radians is based on clock
            }
            qiclient.updateValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

            // retrieve values
            System.out.println("Getting updated events");
            jsonMultipleValues = qiclient.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "40");
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
            // replace the first value
            System.out.println("Replacing events");
            evt = WaveData.next(1, 0.5, 0);
            qiclient.replaceValue(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // replace the remaining values
            newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 20; i += 2) {
                WaveData newEvt = WaveData.next(1, 0.5, i);
                newEvents.add(newEvt);
                Thread.sleep(10);
            }
            qiclient.replaceValues(tenantId, namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

            // retrieve values again to see replaced values
            System.out.println("Getting replaced events");
            jsonMultipleValues = qiclient.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "40");
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
   		 	// QiStreamBehaviors 
            System.out.println("QiStreamBehaviors determine whether Qi interpolates or extrapolates data at the requested index location");
            System.out.println();
   		 	listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); 
   		 	jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
   		 	foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
         
   		 	System.out.println("Default (Continuous) stream behavior, requesting data starting at index location '1', Qi will interpolate this value:");
   		 	for (WaveData evnt : foundEvents) {
   		 		System.out.println("Order: " + evnt.getOrder() + ", Radians: " + evnt.getRadians());
   		 	}
   		 	System.out.println();
         
   		 	// create a stream behavior with Discrete and attach it to the existing stream
   		 	QiStreamBehavior behavior = new QiStreamBehavior();
   		 	behavior.setId(sampleBehaviorId);
   		 	behavior.setMode(QiStreamMode.Discrete);
   		 	String behaviorString = qiclient.createBehavior(tenantId, namespaceId, behavior);
   		 	behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class);
   		 	sampleStream.setBehaviorId(sampleBehaviorId);
   		 	qiclient.updateStream(tenantId, namespaceId, sampleStreamId, sampleStream);

   		 	// repeat the retrieval
   		 	jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
   		 	foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
   		 	System.out.println("Discrete stream behavior, Qi does not interpolate and returns the data starting at the next index location containing data:");
   		 	for (WaveData evnt : foundEvents) {
   		 		System.out.println("Order: " + evnt.getOrder() + ", Radians: " + evnt.getRadians());
   		 	}
   		 	System.out.println();
         
   		 	// QiViews 
   		 	System.out.println("QiViews"); 
   		 	System.out.println("Here is some of our data as it is stored on the server:");
   		 	for (WaveData evnt : foundEvents) {
   		 		System.out.println("Sin: " + evnt.getSin() + ", Cos: " + evnt.getCos() + ", Tan" + evnt.getTan());            
   		 	}
   		 	System.out.println();
         
   		 	// create target QiTypes         
   		 	QiType targetType = getWaveDataTargetType(targetTypeId);
   		 	String jsonTargetType = qiclient.createType(tenantId, namespaceId, targetType);
   		 	targetType = qiclient.mGson.fromJson(jsonTargetType, QiType.class);         
   		 	QiType targetIntegerType = getWaveDataTargetIntegerType(integerTargetTypeId);
   		 	String jsonTargetIntegerType = qiclient.createType(tenantId, namespaceId, targetIntegerType);
   		 	targetIntegerType = qiclient.mGson.fromJson(jsonTargetIntegerType, QiType.class);
         
   		 	// create a QiView
   		 	QiView autoView = new QiView();
   		 	autoView.setId(sampleViewId);
   		 	autoView.setName("SampleAutoView");
   		 	autoView.setDescription("This is a view mapping SampleType to SampleTargetType");
   		 	autoView.setSourceTypeId(sampleTypeId);
   		 	autoView.setTargetTypeId(targetTypeId);
   		 	String jsonAutoView = qiclient.createView(tenantId, namespaceId, autoView);
   		 	autoView = qiclient.mGson.fromJson(jsonAutoView, QiView.class);
                  
   		 	// create QiViewProperties
   		 	QiViewProperty vp1 = new QiViewProperty();
   		 	vp1.setSourceId("Order");
   		 	vp1.setTargetId("OrderTarget");
         
   		 	QiViewProperty vp2 = new QiViewProperty();
   		 	vp2.setSourceId("Sin");
   		 	vp2.setTargetId("SinInt");
         
   		 	QiViewProperty vp3 = new QiViewProperty();
   		 	vp3.setSourceId("Cos");
   		 	vp3.setTargetId("CosInt");
         
   		 	QiViewProperty vp4 = new QiViewProperty();
   		 	vp4.setSourceId("Tan");
   		 	vp4.setTargetId("TanInt");
         
   		 	QiViewProperty[] props = {vp1,vp2,vp3,vp4};
         
   		 	// create a QiView with explicit QiViewProperties         
   		 	QiView manualView = new QiView();
   		 	manualView.setId(sampleManualViewId);
   		 	manualView.setName("SampleManualView");
   		 	manualView.setDescription("This is a view mapping SampleType to SampleTargetType");
   		 	manualView.setSourceTypeId(sampleTypeId);
   		 	manualView.setTargetTypeId(integerTargetTypeId);
   		 	manualView.setProperties(props);
   		 	String jsonManualView = qiclient.createView(tenantId, namespaceId, manualView);
   		 	manualView = qiclient.mGson.fromJson(jsonManualView, QiView.class);
         
   		 	// range values with automatically mapped QiView
   		 	System.out.println("Specifying a view with a QiType of the same shape returns values that are automatically mapped to the target QiType's properties:");
   		 	Type targetListType = new TypeToken<ArrayList<WaveDataTarget>>() {}.getType(); 
   		 	jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated, sampleViewId);
   		 	ArrayList<WaveDataTarget> foundTargetEvents = qiclient.mGson.fromJson(jsonMultipleValues, targetListType);
   		 	for (WaveDataTarget evnt : foundTargetEvents) {
   		 		System.out.println("SinTarget: " + evnt.getSinTarget() + ", CosTarget: " + evnt.getCosTarget() + ", TanTarget: " + evnt.getTanTarget());            
   		 	}
   		 	System.out.println();

   		 	// range values with manually mapped QiView
   		 	System.out.println("QiViews can also convert certain types of data, here we return integers where the original values were doubles:");
   		 	Type integerListType = new TypeToken<ArrayList<WaveDataInteger>>() {}.getType(); 
   		 	jsonMultipleValues = qiclient.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated, sampleManualViewId);
   		 	ArrayList<WaveDataInteger> foundIntegerEvents = qiclient.mGson.fromJson(jsonMultipleValues, integerListType);
   		 	for (WaveDataInteger evnt : foundIntegerEvents) {
   		 		System.out.println("SinInt: " + evnt.getSinInt() + ", CosInt: " + evnt.getCosInt() + ", TanInt: " + evnt.getTanInt());            
   		 	}
   		 	System.out.println();
         
   		 	// QiViewMaps
   		 	System.out.println("We can query Qi to return the QiViewMap for our QiView, here is the one generated automatically:");
   		 	Type qiViewType = new TypeToken<QiViewMap>() {}.getType(); 
   		 	String jsonViewMap = qiclient.getViewMap(tenantId, namespaceId, sampleViewId);
   		 	QiViewMap viewMap = qiclient.mGson.fromJson(jsonViewMap, qiViewType);
   		 	dumpQiViewMap(viewMap);
   		 	System.out.println();
         
   		 	System.out.println("Here is our explicit mapping, note QiViewMap will return all properties of the Source Type, even those without a corresponding Target property::");
   		 	qiViewType = new TypeToken<QiViewMap>() {}.getType(); 
   		 	jsonViewMap = qiclient.getViewMap(tenantId, namespaceId, sampleManualViewId);
   		 	viewMap = qiclient.mGson.fromJson(jsonViewMap, qiViewType);
   		 	dumpQiViewMap(viewMap);
   		 	System.out.println();
         
         
   		 	// delete data
   		 	
   		 	// remove the first value
   		 	System.out.println("Deleting values from the QiStream");
   		 	qiclient.removeValue(tenantId, namespaceId, sampleStreamId, "0");

   		 	// remove remaining values
   		 	qiclient.removeWindowValues(tenantId, namespaceId, sampleStreamId, "2", "40");

   		 	// retrieve values to check deletion
   		 	jsonMultipleValues = qiclient.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "200");
   		 	foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
   		 	if(foundEvents.isEmpty())
   		 		System.out.println("All values deleted successfully!"); 	

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                System.out.println("Cleaning up");          
                cleanUp(qiclient);
                System.out.println("done");
            } catch (Exception e) {
                printError("Error deleting the Qi Objects", e);
            }
        }
    }

    /**
     * Returns the WaveData QiType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveData QiType
     */
    private static QiType getWaveDataType(String sampleTypeId) {
        QiType intType = new QiType();
        intType.setId("intType");
        intType.setQiTypeCode(QiTypeCode.Int32);

        QiType doubleType = new QiType();
        doubleType.setId("doubleType");
        doubleType.setQiTypeCode(QiTypeCode.Double);

        QiTypeProperty orderProperty = new QiTypeProperty();
        orderProperty.setId("Order");
        orderProperty.setQiType(intType);
        orderProperty.setIsKey(true);

        QiTypeProperty tauProperty = new QiTypeProperty();
        tauProperty.setId("Tau");
        tauProperty.setQiType(doubleType);

        QiTypeProperty radiansProperty = new QiTypeProperty();
        radiansProperty.setId("Radians");
        radiansProperty.setQiType(doubleType);

        QiTypeProperty sinProperty = new QiTypeProperty();
        sinProperty.setId("Sin");
        sinProperty.setQiType(doubleType);

        QiTypeProperty cosProperty = new QiTypeProperty();
        cosProperty.setId("Cos");
        cosProperty.setQiType(doubleType);

        QiTypeProperty tanProperty = new QiTypeProperty();
        tanProperty.setId("Tan");
        tanProperty.setQiType(doubleType);

        QiTypeProperty sinhProperty = new QiTypeProperty();
        sinhProperty.setId("Sinh");
        sinhProperty.setQiType(doubleType);

        QiTypeProperty coshProperty = new QiTypeProperty();
        coshProperty.setId("cosh");
        coshProperty.setQiType(doubleType);

        QiTypeProperty tanhProperty = new QiTypeProperty();
        tanhProperty.setId("Tanh");
        tanhProperty.setQiType(doubleType);

        // Create a QiType for our WaveData class; the metadata properties are the ones we just created
        QiType type = new QiType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty};
        type.setProperties(props);
        type.setQiTypeCode(QiTypeCode.Object);

        return type;
    }
    
    /**
     * Returns the WaveDataTarget QiType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveDataTarget QiType
     */
    private static QiType getWaveDataTargetType(String sampleTypeId) {
        QiType intType = new QiType();
        intType.setId("intType");
        intType.setQiTypeCode(QiTypeCode.Int32);

        QiType doubleType = new QiType();
        doubleType.setId("doubleType");
        doubleType.setQiTypeCode(QiTypeCode.Double);

        QiTypeProperty orderTargetProperty = new QiTypeProperty();
        orderTargetProperty.setId("OrderTarget");
        orderTargetProperty.setQiType(intType);
        orderTargetProperty.setIsKey(true);

        QiTypeProperty tauTargetProperty = new QiTypeProperty();
        tauTargetProperty.setId("TauTarget");
        tauTargetProperty.setQiType(doubleType);

        QiTypeProperty radiansTargetProperty = new QiTypeProperty();
        radiansTargetProperty.setId("RadiansTarget");
        radiansTargetProperty.setQiType(doubleType);

        QiTypeProperty sinTargetProperty = new QiTypeProperty();
        sinTargetProperty.setId("SinTarget");
        sinTargetProperty.setQiType(doubleType);

        QiTypeProperty cosTargetProperty = new QiTypeProperty();
        cosTargetProperty.setId("CosTarget");
        cosTargetProperty.setQiType(doubleType);

        QiTypeProperty tanTargetProperty = new QiTypeProperty();
        tanTargetProperty.setId("TanTarget");
        tanTargetProperty.setQiType(doubleType);

        QiTypeProperty sinhTargetProperty = new QiTypeProperty();
        sinhTargetProperty.setId("SinhTarget");
        sinhTargetProperty.setQiType(doubleType);

        QiTypeProperty coshTargetProperty = new QiTypeProperty();
        coshTargetProperty.setId("CoshTarget");
        coshTargetProperty.setQiType(doubleType);

        QiTypeProperty tanhTargetProperty = new QiTypeProperty();
        tanhTargetProperty.setId("TanhTarget");
        tanhTargetProperty.setQiType(doubleType);

        // Create a QiType for our WaveData class; the metadata properties are the ones we just created
        QiType type = new QiType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        QiTypeProperty[] props = {orderTargetProperty, tauTargetProperty, radiansTargetProperty, sinTargetProperty, cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty};
        type.setProperties(props);
        type.setQiTypeCode(QiTypeCode.Object);

        return type;
    	
    }

    /**
     * Returns the WaveDataInteger QiType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveDataInteger QiType
     */    
    private static QiType getWaveDataTargetIntegerType(String sampleTypeId) {
        QiType intType = new QiType();
        intType.setId("intType");
        intType.setQiTypeCode(QiTypeCode.Int32);

        QiTypeProperty orderTargetProperty = new QiTypeProperty();
        orderTargetProperty.setId("OrderTarget");
        orderTargetProperty.setQiType(intType);
        orderTargetProperty.setIsKey(true);

        QiTypeProperty sinIntProperty = new QiTypeProperty();
        sinIntProperty.setId("SinInt");
        sinIntProperty.setQiType(intType);

        QiTypeProperty cosIntProperty = new QiTypeProperty();
        cosIntProperty.setId("CosInt");
        cosIntProperty.setQiType(intType);

        QiTypeProperty tanIntProperty = new QiTypeProperty();
        tanIntProperty.setId("TanInt");
        tanIntProperty.setQiType(intType);
        
        // Create a QiType for our WaveData class; the metadata properties are the ones we just created
        QiType type = new QiType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        QiTypeProperty[] props = {orderTargetProperty, sinIntProperty, cosIntProperty, tanIntProperty};
        type.setProperties(props);
        type.setQiTypeCode(QiTypeCode.Object);

        return type;
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

    private static void dumpEvents(ArrayList<WaveData> foundEvents) {
        for (WaveData evnt : foundEvents) {
            System.out.println(evnt.toString());
        }
    }
    
    private static void dumpQiViewMap(QiViewMap qiViewMap) { 
        for (QiViewProperty prop : qiViewMap.getProperties()) {
            if(prop.getTargetId() != null)
           	 System.out.println(prop.getSourceId() + " => " + prop.getTargetId());
            else
           	 System.out.println(prop.getSourceId() + " => Not mapped");
        }
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
	
    public static void cleanUp(QiClient qiclient) throws QiError 
	{
		System.out.println("Deleting the stream");
        qiclient.deleteStream(tenantId, namespaceId, sampleStreamId);
        System.out.println("Deleting the types");
        qiclient.deleteType(tenantId, namespaceId, sampleTypeId);
        qiclient.deleteType(tenantId, namespaceId, targetTypeId);
        qiclient.deleteType(tenantId, namespaceId, integerTargetTypeId);
        System.out.println("Deleting the behavior");
        qiclient.deleteBehavior(tenantId, namespaceId, sampleBehaviorId);
        System.out.println("Deleting the views");
        qiclient.deleteView(tenantId, namespaceId, sampleViewId);
        qiclient.deleteView(tenantId, namespaceId, sampleManualViewId);        
	};
}
