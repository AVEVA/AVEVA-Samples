package samples;

import java.util.ArrayList;

import java.util.List;

import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;

public class Program {


	public static void main(String[] args) throws InterruptedException
	{
		QiClient qiclient = null;
		QiType evtType = null;
		QiStream evtStream = null;

		try{
			String server = "http://HistorianDevSecurity.cloudapp.net:3380";
			qiclient = new QiClient( server);



			// TODO retract when provisioning is complete
			//System.out.println("Creating a tenant named " + tenantId);
			//qiclient.CreateTenant(tenantId);

			// create properties for double Value, DateTime Timstamp, string Units
			System.out.println("Creating a Qi type for WaveData instances");
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
			type.setName("WaveDataJ");
			type.setId("WaveDataJ");
			type.setDescription("This is a sample stream for storing WaveData type events");
			QiTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty}; 
			type.setProperties(props);


			// create the type in the Qi Service
			String evtTypeString = qiclient.CreateType(type);
			evtType = qiclient.mGson.fromJson(evtTypeString, QiType.class);


			System.out.println("Creating a stream in this tenant for simple event measurements");
			QiStream stream = new QiStream("evtStreamJ",evtType.getId());
			String evtStreamString = qiclient.CreateStream(stream);
			evtStream = qiclient.mGson.fromJson(evtStreamString, QiStream.class);



			System.out.println("Artificially generating 100 events and inserting them into the Qi Service");

			// How to insert a single event

			WaveData evt = WaveData.next(1, 2.0, 0);

			qiclient.CreateEvent(evtStream.getId(), qiclient.mGson.toJson(evt));




			List<WaveData> events = new ArrayList<WaveData>();
			// how to insert an a collection of events
			for (int i = 1; i < 100; i++)
			{
				evt = WaveData.next(1, 2.0, i);
				events.add(evt);
			}
			qiclient.CreateEvents(evtStream.getId(), qiclient.mGson.toJson(events));


			Thread.sleep(2000);


			System.out.println("Retrieving the inserted events");
			System.out.println("==============================");
			String jCollection = qiclient.GetWindowValues(evtStream.getId(), "0", "99");
			Type listType = new TypeToken<ArrayList<WaveData>>() {
			}.getType();
			// List<YourClass> yourClassList = new Gson().fromJson(jsonArray, listType);     

			ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jCollection, listType);
			DumpEvents(foundEvents);


			System.out.println();
			System.out.println("Updating values");
			// take the first value inserted and update 
			evt = foundEvents.get(0);
			evt = WaveData.next(1, 4.0, 0);
			qiclient.updateValue(evtStream.getId(), qiclient.mGson.toJson(evt));



			// update the remaining events (same span, multiplier, order)
			List<WaveData> newEvents = new ArrayList<WaveData>();
			for (WaveData evnt : events)
			{
				WaveData newEvt = WaveData.next(1, 4.0, evnt.getOrder());
				newEvents.add(newEvt);
			}
			qiclient.updateValues(evtStream.getId(),qiclient.mGson.toJson(events));

			Thread.sleep(2000);


			System.out.println();
			System.out.println("Deleting events");
			qiclient.removeValue(evtStream.getId(), "0");


			qiclient.removeWindowValues(evtStream.getId(), "1", "99");
			Thread.sleep(2000);


			System.out.println("Checking for events");
			System.out.println("===================");

			jCollection = qiclient.GetWindowValues(evtStream.getId(), "0", "99");
			Type listType1 = new TypeToken<ArrayList<WaveData>>() {
			}.getType();
			// List<YourClass> yourClassList = new Gson().fromJson(jsonArray, listType);     


			foundEvents = qiclient.mGson.fromJson(jCollection, listType1);
			DumpEvents(foundEvents); 

		}catch(QiError qiEx){

			System.out.println("QiError Msg: " + qiEx.getQiErrorMessage());
			System.out.println("HttpStatusCode: "+ qiEx.getHttpStatusCode());
			System.out.println("HttperrorMessage: "+ qiEx.getHttpErrorMessage());


		}	catch(Exception e){
			e.printStackTrace();

		}
		finally {
			try
			{
				qiclient.deleteStream(evtStream.getId());
				qiclient.deleteType(evtType.getId());
				//  qiclient.deleteTenant(tenantId);
			}
			catch (Exception e)
			{
			}


		}  

	}

	private static void DumpEvents(ArrayList<WaveData> foundEvents) {


		System.out.println("Found" +foundEvents.size() + "events, writing");

		for( WaveData evnt : foundEvents)
		{
			System.out.println(evnt.toString());
		}


	}


}
