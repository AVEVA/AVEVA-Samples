package samples;

import java.util.ArrayList;
import java.util.List;

import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;

public class Program 
{
	public static void main(String[] args) throws InterruptedException
	{
		final String sampleNamespaceId = "WaveData_SampleNamespace";
		final String sampleTypeId = "WaveData_SampleType";
		final String sampleStreamId = "WaveData_SampleStream";
		final String sampleBehaviorId = "WaveData_SampleBehavior";

		System.out.println("Creating a Qi Client object...");
		String server = Constants._qiServerUrl;
		QiClient qiclient = new QiClient(server);
		
		try
		{
			System.out.println("Creating a QiNamespace...");
            QiNamespace sampleNamespace = new QiNamespace(sampleNamespaceId);
			
			//create QiNamespace
			qiclient.createNamespace(Constants._tenantId, sampleNamespace);
			
			delayForQiConsistency();
			
			// create properties for double Value, DateTime Timstamp, string Units
			System.out.println("Creating a Qi type for WaveData instances");
			QiType sampleType = getWaveDataType(sampleTypeId);
			
			// create the type in the Qi Service
			String evtTypeString = qiclient.createType(Constants._tenantId, sampleNamespaceId, sampleType);
			sampleType = qiclient.mGson.fromJson(evtTypeString, QiType.class);
			
			delayForQiConsistency();

			//create a stream named evtStreamJ
			System.out.println("Creating a stream in this tenant for simple event measurements");
			QiStream sampleStream = new QiStream(sampleStreamId,sampleTypeId);
			String evtStreamString = qiclient.createStream(Constants._tenantId, sampleNamespaceId, sampleStream);
			sampleStream = qiclient.mGson.fromJson(evtStreamString, QiStream.class);
			
			delayForQiConsistency();

			System.out.println("Artificially generating 100 events and inserting them into the Qi Service");

			// How to insert a single event
			WaveData evt = WaveData.next(1, 2.0, 0);
			qiclient.createEvent(Constants._tenantId, sampleNamespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

			List<WaveData> events = new ArrayList<WaveData>();
			// how to insert an a collection of events
			for (int i = 2; i < 200; i+=2)
			{
		        evt = WaveData.next(1, 2.0, i);
				events.add(evt);
			}
			qiclient.createEvents(Constants._tenantId, sampleNamespaceId, sampleStreamId, qiclient.mGson.toJson(events));

			delayForQiConsistency();

			System.out.println("Retrieving the inserted events");
			System.out.println("==============================");
			String jCollection = qiclient.getWindowValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "0", "198");
			Type listType = new TypeToken<ArrayList<WaveData>>() {
			}.getType();			   
			ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);
			
			System.out.println();
			System.out.println("Updating values");
			// take the first value inserted and update 
			evt = foundEvents.get(0);
			evt = WaveData.next(1, 4.0, 0);
			qiclient.updateValue(Constants._tenantId, sampleNamespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

			// update the remaining events (same span, multiplier, order)
			List<WaveData> newEvents = new ArrayList<WaveData>();
			for (WaveData evnt : events)
			{
				WaveData newEvt = WaveData.next(1, 4.0, evnt.getOrder());
				newEvents.add(newEvt);
			}
			qiclient.updateValues(Constants._tenantId, sampleNamespaceId, sampleStreamId,qiclient.mGson.toJson(events));

			delayForQiConsistency();

    		// check the results
    		System.out.println("Retrieving the updated values");
    		System.out.println("=============================");
    		jCollection = qiclient.getWindowValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "0", "198");          
    		foundEvents = qiclient.mGson.fromJson(jCollection, listType);
    		DumpEvents(foundEvents);
	
    		// illustrate how stream behaviors modify retrieval
    		// First, pull three items back with GetRangeValues for range values between events.
    		// The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
    		System.out.println();
    		System.out.println("Retrieving three events without a stream behavior");
    		jCollection = qiclient.getRangeValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
            foundEvents = qiclient.mGson.fromJson(jCollection, listType);
            DumpEvents(foundEvents);
            
    		// now, create a stream behavior with Discrete and attach it to the existing stream
            System.out.println("Creating a QiStreamBehavior");
    		System.out.println("============================");
            QiStreamBehavior behavior = new QiStreamBehavior();
    		behavior.setId(sampleBehaviorId) ;
    		behavior.setMode(QiStreamMode.StepwiseContinuousLeading);
    		String behaviorString = qiclient.createBehavior(Constants._tenantId, sampleNamespaceId, behavior);
    		behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class);
    
    		// update the stream to include this behavior
    		//evtStream.setBehaviorId("evtStreamStepLeading") ;
    		sampleStream.setBehaviorId(sampleBehaviorId);
    		qiclient.updateStream(Constants._tenantId, sampleNamespace.getId(),sampleStreamId, sampleStream);

    		// repeat the retrieval
    		System.out.println();
    		System.out.println("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
    		jCollection = qiclient.getRangeValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
    		foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);
						
			System.out.println();
			System.out.println("Deleting events");
			qiclient.removeValue(Constants._tenantId, sampleNamespaceId, sampleStreamId, "0");
			
			// remove the first value -- index is the timestamp of the event
			qiclient.removeWindowValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "1", "198");
			
			delayForQiConsistency();
			
			System.out.println("Checking for events");
			System.out.println("===================");

			jCollection = qiclient.getWindowValues(Constants._tenantId, sampleNamespaceId, sampleStreamId, "0", "198");
			Type listType1 = new TypeToken<ArrayList<WaveData>>() {
			}.getType();
		     
			foundEvents = qiclient.mGson.fromJson(jCollection, listType1);
			DumpEvents(foundEvents); 
		}
		catch(QiError qiEx)
		{
			System.out.println("QiError Msg: " + qiEx.getQiErrorMessage());
			System.out.println("HttpStatusCode: "+ qiEx.getHttpStatusCode());
			System.out.println("errorMessage: "+ qiEx.getMessage());
		}	
		catch(Exception e)
		{
			e.printStackTrace();

		}
		finally 
		{
			try
			{
				qiclient.deleteStream(Constants._tenantId, sampleNamespaceId, sampleStreamId);
				qiclient.deleteBehavior(Constants._tenantId, sampleNamespaceId, sampleBehaviorId);
				qiclient.deleteType(Constants._tenantId, sampleNamespaceId, sampleTypeId);
			}
			catch (Exception e)
			{				
				printError("Error deleting the Qi Objects", e);
			}
		}  
	}
	
	/**
	 * Returns the WaveData QiType for the sample
	 * @param sampleTypeId - the id for the type
	 * @return WaveData QiType
	 */
	private static QiType getWaveDataType(String sampleTypeId)
	{
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

		// Create a QiType for our WaveData class; the metadata proeprties are the ones we just created
		QiType type = new QiType();
		type.setId(sampleTypeId);
		type.setName("WaveDataTypeJ");
		QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
		type.setProperties(props);
		type.setQiTypeCode(QiTypeCode.Empty);
		
		return type;
	}
	
	/**
	 * Prints out a formated error string
	 * @param exceptionDescription - the description of what the error is
	 * @param exception - the exception thrown
	 */
	private static void printError(String exceptionDescription, Exception exception)
	{
		System.out.println("\n\n======= " + exceptionDescription + " =======");
		System.out.println(exception.toString());
		System.out.println("======= End of " + exceptionDescription + " =======");
	}
	
	/**
	 * Delays the program for an amount of time to allow the multiple servers on Qi to become consistent with recent calls
	 * @throws InterruptedException
	 */
	private static void delayForQiConsistency() throws InterruptedException
	{
		int millisecondsToWait = 5000;
		double seconds = millisecondsToWait / 1000.0;
		
		System.out.println("Waiting for " + seconds + " seconds in order to allow the multiple servers on Qi to become consistent with recent calls...\n");
		Thread.sleep(millisecondsToWait);
	}

	private static void DumpEvents(ArrayList<WaveData> foundEvents)
	{
		System.out.println("Found " +foundEvents.size() + " events, writing");
		for( WaveData evnt : foundEvents)
		{
			System.out.println(evnt.toString());
		}
	}
}
