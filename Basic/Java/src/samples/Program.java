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

    public static void main(String[] args) throws InterruptedException {
        final String sampleTypeId = "WaveData_SampleType";
        final String sampleStreamId = "WaveData_SampleStream";
        final String sampleBehaviorId = "WaveData_SampleBehavior";

        // get configuration
        String _tenantId = getConfiguration("_tenantId");
        String _namespaceId = getConfiguration("_namespaceId");
        String _qiServerUrl = getConfiguration("_qiServerUrl");

        // Create Qi client to communicate with server
        System.out.println("Creating a Qi Client object...");
        String server = _qiServerUrl + "/";
        QiClient qiclient = new QiClient(server);

        try {
            // create QiType locally
            QiType sampleType = getWaveDataType(sampleTypeId);

            // create the type in the Qi Service
            String jsonType = qiclient.createType(_tenantId, _namespaceId, sampleType);
            sampleType = qiclient.mGson.fromJson(jsonType, QiType.class);

            //create a stream named WaveData_SampleStream
            QiStream sampleStream = new QiStream(sampleStreamId, sampleType.getId());
            String jsonStream = qiclient.createStream(_tenantId, _namespaceId, sampleStream);
            sampleStream = qiclient.mGson.fromJson(jsonStream, QiStream.class);

            // insert a single event
            WaveData evt = WaveData.next(1, 2.0, 0);
            qiclient.insertValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // get a single event
            String jsonSingleValue = qiclient.getSingleValue(_tenantId, _namespaceId, sampleStreamId, "0");
            WaveData data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class);
            System.out.println(data.toString());

            // insert an a collection of events
            List<WaveData> events = new ArrayList<WaveData>();
            for (int i = 2; i < 20; i += 2) {
                evt = WaveData.next(1, 2.0, i);
                events.add(evt);
                Thread.sleep(10);
            }
            qiclient.insertValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(events));

            // get last value inserted in stream
            jsonSingleValue = qiclient.getLastValue(_tenantId, _namespaceId, sampleStreamId);
            data = qiclient.mGson.fromJson(jsonSingleValue, WaveData.class);
            System.out.println(data.toString());

            // retrieve values
            String jsonMultipleValues = qiclient.getWindowValues(_tenantId, _namespaceId, sampleStreamId, "0", "18");
            Type listType = new TypeToken<ArrayList<WaveData>>() {}.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData> type
            ArrayList<WaveData> foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            // update the first value
            evt = WaveData.next(1, 1.0, 0);
            qiclient.updateValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // update existing values and add 90 new values using update
            List<WaveData> newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 200; i += 2) // note: update will replace a value if it already exists, and create one if it does not
            {
                WaveData newEvt = WaveData.next(1, 1.0, i);
                newEvents.add(newEvt);
                Thread.sleep(10); // sleep for a bit because WaveData.radians is based on clock
            }
            qiclient.updateValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

            // retrieve values
            jsonMultipleValues = qiclient.getWindowValues(_tenantId, _namespaceId, sampleStreamId, "0", "198");
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            // replace the first value
            evt = WaveData.next(1, 0.5, 0);
            qiclient.replaceValue(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(evt));

            // replace the remaining values
            newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 200; i += 2) {
                WaveData newEvt = WaveData.next(1, 0.5, i);
                newEvents.add(newEvt);
                Thread.sleep(10);
            }
            qiclient.replaceValues(_tenantId, _namespaceId, sampleStreamId, qiclient.mGson.toJson(newEvents));

            // retrieve values again to see replaced values
            jsonMultipleValues = qiclient.getWindowValues(_tenantId, _namespaceId, sampleStreamId, "0", "198");
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            // stream behavior changes how non-existent data is retrieved
            jsonMultipleValues = qiclient.getRangeValues(_tenantId, _namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            // create a stream behavior with Discrete and attach it to the existing stream
            QiStreamBehavior behavior = new QiStreamBehavior();
            behavior.setId(sampleBehaviorId);
            behavior.setMode(QiStreamMode.Discrete);
            String behaviorString = qiclient.createBehavior(_tenantId, _namespaceId, behavior);
            behavior = qiclient.mGson.fromJson(behaviorString, QiStreamBehavior.class);
            System.out.println(behavior.getId());
            sampleStream.setBehaviorId(sampleBehaviorId);
            qiclient.updateStream(_tenantId, _namespaceId, sampleStreamId, sampleStream);

            // repeat the retrieval
            jsonMultipleValues = qiclient.getRangeValues(_tenantId, _namespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            // remove the first value
            qiclient.removeValue(_tenantId, _namespaceId, sampleStreamId, "0");

            // remove remaining values
            qiclient.removeWindowValues(_tenantId, _namespaceId, sampleStreamId, "1", "198");

            // retrieve values to check deletion
            jsonMultipleValues = qiclient.getWindowValues(_tenantId, _namespaceId, sampleStreamId, "0", "198");
            foundEvents = qiclient.mGson.fromJson(jsonMultipleValues, listType);
            DumpEvents(foundEvents);

            System.out.println();
            System.out.println("===============================");
            System.out.println("Completed sample with no errors");
            System.out.println("===============================");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                System.out.println("\nCleaning up");
                System.out.println("============");
                qiclient.deleteStream(_tenantId, _namespaceId, sampleStreamId);
                qiclient.deleteBehavior(_tenantId, _namespaceId, sampleBehaviorId);
                qiclient.deleteType(_tenantId, _namespaceId, sampleTypeId);
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
     *
     * @param exceptionDescription - the description of what the error is
     * @param exception            - the exception thrown
     */
    private static void printError(String exceptionDescription, Exception exception) {
        System.out.println("\n\n======= " + exceptionDescription + " =======");
        System.out.println(exception.toString());
        System.out.println("======= End of " + exceptionDescription + " =======");
    }

    private static void DumpEvents(ArrayList<WaveData> foundEvents) {
        System.out.println("Found " + foundEvents.size() + " events, writing");
        for (WaveData evnt : foundEvents) {
            System.out.println(evnt.toString());
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
}
