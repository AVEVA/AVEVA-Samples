package samples;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;

import com.google.gson.reflect.TypeToken;
import com.sun.org.apache.xpath.internal.patterns.ContextMatchStepPattern;

import java.lang.reflect.Type;

public class Program 
{
	public static void main(String[] args) throws InterruptedException
	{
		final String sampleTypeId = "WaveData_SampleType";
		final String sampleStreamId = "WaveData_SampleStream";
		final String sampleBehaviorId = "WaveData_SampleBehavior";

		// Create Qi client to communicate with server
		System.out.println("Creating a Qi Client object...");
		String server = Constants._qiServerUrl + "/";
		QiClient qiclient = new QiClient(server);

		try
		{
			// following is only for testing purposes
//			System.out.println(qiclient.createTenant());
//			System.out.println(qiclient.createNamespace());

			// create properties for double Value, DateTime Timstamp, string Units
			System.out.println("Creating a Qi type for WaveData instances");
			System.out.println("=========================================");
			QiType sampleType = getWaveDataType(sampleTypeId);
			
			// create the type in the Qi Service
			String evtTypeString = qiclient.createType(Constants._tenantId, Constants._namespaceId, sampleType);
			sampleType = qiclient.mGson.fromJson(evtTypeString, QiType.class); // sampleType built from returned JSON object
			
			delayForQiConsistency();

			// get the QiType just created
			System.out.println("Getting the WaveData type");
			System.out.println("=========================");
			String returnedType = qiclient.getType(Constants._tenantId, Constants._namespaceId, sampleTypeId);
			System.out.println(qiclient.mGson.fromJson(returnedType, QiType.class));
			System.out.println(returnedType);

			// get all types for the given namespace
			System.out.println();
			System.out.println("Getting all types");
			System.out.println("=================");
			System.out.println(qiclient.getTypes(Constants._tenantId, Constants._namespaceId, "0", "100"));

			//create a stream named WaveData_SampleStream
			System.out.println();
			System.out.println("Creating a stream in this tenant for simple event measurements");
			System.out.println("==============================================================");
			QiStream sampleStream = new QiStream(sampleStreamId, sampleType.getId());
			String evtStreamString = qiclient.createStream(Constants._tenantId, Constants._namespaceId, sampleStream);
			sampleStream = qiclient.mGson.fromJson(evtStreamString, QiStream.class); // sampleStream built from returned JSON object
			
			delayForQiConsistency();

			// get the stream that was just created
			System.out.println("Getting the QiStream that was just created");
			System.out.println("==========================================");
			String returnedStream = qiclient.getStream(Constants._tenantId, Constants._namespaceId, sampleStreamId);
			System.out.println(qiclient.mGson.fromJson(returnedStream, QiStream.class));
			System.out.println(returnedStream);

			// get all streams associated with the given namespace
			System.out.println();
			System.out.println("Getting all streams");
			System.out.println("===================");
			System.out.println(qiclient.getStreams(Constants._tenantId, Constants._namespaceId, "","0", "100"));

			System.out.println();
			System.out.println("Artificially generating 100 events and inserting them into the Qi Service");
			System.out.println("=========================================================================");

			// How to insert a single event
			System.out.println("*** creating first event ***");
			WaveData evt = WaveData.next(1, 2.0, 0);
			qiclient.insertValue(Constants._tenantId, Constants._namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

			// How to get a single event
			System.out.println("*** getting first event ***");
			String jSingle = qiclient.getSingleValue(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0");
			Type singleType = new TypeToken<WaveData>(){}.getType();
			WaveData data = qiclient.mGson.fromJson(jSingle, singleType);
			System.out.println(data.toString());


			List<WaveData> events = new ArrayList<WaveData>();
			// how to insert an a collection of events
			System.out.println("*** creating remaining events ***");
			for (int i = 2; i < 20; i+=2)
			{
		        evt = WaveData.next(1, 2.0, i);
				events.add(evt);
			}
			qiclient.insertValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, qiclient.mGson.toJson(events));

			delayForQiConsistency();

			// get the last value inserted into the stream
			System.out.println("Getting the last event to be inserted");
			System.out.println("=====================================");
			String returnedValue = qiclient.getLastValue(Constants._tenantId, Constants._namespaceId, sampleStreamId);
			System.out.println(qiclient.mGson.fromJson(returnedValue, WaveData.class));
			System.out.println(returnedValue);

			System.out.println();
			System.out.println("Retrieving the inserted events");
			System.out.println("==============================");
			String jCollection = qiclient.getWindowValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0", "198");
			Type listType = new TypeToken<ArrayList<WaveData>>() {
			}.getType();			   
			ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);
			
			System.out.println();
			System.out.println("Updating values");
			System.out.println("===============");
			// take the first value inserted and update 
			//evt = foundEvents.get(0);
			evt = WaveData.next(1, 4.0, 0);
			qiclient.updateValue(Constants._tenantId, Constants._namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

			// update the remaining events and then some (same span, multiplier, order)
			List<WaveData> newEvents = new ArrayList<WaveData>();
			for (int i = 2; i < 200; i+=2) // note: update will replace a value if it already exists, and create one if it does not
			{
				WaveData newEvt = WaveData.next(1, 4.0, i);
				newEvents.add(newEvt);
			}
			qiclient.updateValues(Constants._tenantId, Constants._namespaceId, sampleStreamId,qiclient.mGson.toJson(newEvents));

			delayForQiConsistency();

    		// check the results
    		System.out.println("Retrieving the updated values");
    		System.out.println("=============================");
    		jCollection = qiclient.getWindowValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0", "198");
    		foundEvents = qiclient.mGson.fromJson(jCollection, listType);
    		DumpEvents(foundEvents);

    		System.out.println();
			System.out.println("Replacing values"); // note: replacing a value will fail if the value does not exist
			System.out.println("================");
			// replace the first value
    		evt = WaveData.next(1, 10.0, 0);
    		qiclient.replaceValue(Constants._tenantId, Constants._namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

    		// replace the remaining values
			newEvents = new ArrayList<WaveData>();
			for (int i = 2; i < 200; i+=2)
			{
				WaveData newEvt = WaveData.next(1, 10.0, i);
				newEvents.add(newEvt);
			}
			qiclient.replaceValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

			// check the results again
			System.out.println();
			System.out.println("Retrieving the replaced values");
			System.out.println("==============================");
			jCollection = qiclient.getWindowValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0", "198");
			foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);

    		// illustrate how stream behaviors modify retrieval
    		// First, pull three items back with GetRangeValues for range values between events.
    		// The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
    		System.out.println();
    		System.out.println("Retrieving three events without a stream behavior");
			System.out.println("=================================================");
    		jCollection = qiclient.getRangeValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
            foundEvents = qiclient.mGson.fromJson(jCollection, listType);
            DumpEvents(foundEvents);
            
    		// now, create a stream behavior with Discrete and attach it to the existing stream
			System.out.println();
            System.out.println("Creating a QiStreamBehavior");
    		System.out.println("============================");
            QiStreamBehavior behavior = new QiStreamBehavior();
    		behavior.setId(sampleBehaviorId) ;
    		behavior.setMode(QiStreamMode.StepwiseContinuousLeading);
    		String behaviorString = qiclient.createBehavior(Constants._tenantId, Constants._namespaceId, behavior);
    		System.out.println(qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class));


    		// get the QiBehavior that was just created
			System.out.println();
			System.out.println("Getting WaveData_SampleBehavior");
			System.out.println("===============================");
			String returnedBehavior = qiclient.getBehavior(Constants._tenantId, Constants._namespaceId, sampleBehaviorId);
			System.out.println(qiclient.mGson.fromJson(returnedBehavior, QiStreamBehavior.class));
			System.out.println(returnedBehavior);

			// get all QiBehaviors associated with the given namespace
			System.out.println();
			System.out.println("Getting all QiBehaviors");
			System.out.println("=======================");
			System.out.println(qiclient.getBehaviors(Constants._tenantId, Constants._namespaceId, "0", "100"));

    		// update the stream to include this behavior
    		//evtStream.setBehaviorId("evtStreamStepLeading") ;
			System.out.println();
			System.out.println("Updating stream behavior");
			System.out.println("========================");
    		sampleStream.setBehaviorId(sampleBehaviorId);
    		qiclient.updateStream(Constants._tenantId, Constants._namespaceId, sampleStreamId, sampleStream);

    		// repeat the retrieval
    		System.out.println();
    		System.out.println("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
			System.out.println("==============================================================================================");
    		jCollection = qiclient.getRangeValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
    		foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);
						
			System.out.println();
			System.out.println("Deleting events");
			System.out.println("===============");

			System.out.println("*** deleting first event ***");
			qiclient.removeValue(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0");
			
			// remove the first value -- index is the timestamp of the event
			System.out.println("*** deleting remaining events ***");
			qiclient.removeWindowValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "1", "198");
			
			delayForQiConsistency();
			
			System.out.println("Checking for events");
			System.out.println("===================");

			jCollection = qiclient.getWindowValues(Constants._tenantId, Constants._namespaceId, sampleStreamId, "0", "198");
			Type listType1 = new TypeToken<ArrayList<WaveData>>() {
			}.getType();
		     
			foundEvents = qiclient.mGson.fromJson(jCollection, listType1);
			DumpEvents(foundEvents);

			System.out.println();
			System.out.println("*******************************");
			System.out.println("Completed sample with no errors");
			System.out.println("*******************************");
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
				System.out.println("\nCleaning up");
				System.out.println("============");
				qiclient.deleteStream(Constants._tenantId, Constants._namespaceId, sampleStreamId);
				qiclient.deleteBehavior(Constants._tenantId, Constants._namespaceId, sampleBehaviorId);
				qiclient.deleteType(Constants._tenantId, Constants._namespaceId, sampleTypeId);
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
		System.out.println("Found " + foundEvents.size() + " events, writing");
		for( WaveData evnt : foundEvents)
		{
			System.out.println(evnt.toString());
		}
	}
}
