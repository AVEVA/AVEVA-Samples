/** Program.java
 * 
 */

package com.github.osisoft.sdsjava;

import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import com.github.osisoft.ocs_sample_library_preview.*;
import  com.github.osisoft.ocs_sample_library_preview.sds.*;

public class Program {
    // get configuration
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
	
    // id strings
    static String sampleTypeId = "WaveData_SampleType";
    static String targetTypeId = "WaveData_SampleTargetType";
    static String integerTargetTypeId = "WaveData_SampleIntegerTargetType";
    static String sampleStreamId = "WaveData_SampleStream";
    static String sampleStreamViewId = "WaveData_SampleStreamView";
    static String sampleManualStreamViewId = "WaveData_SampleManualStreamView";

    static String streamIdSecondary = "SampleStream_Secondary";
    static String streamIdCompound = "SampleStream_Compound";
    static String compoundTypeId = "SampleType_Compound";
    
    static Boolean success = true;
    
    public static void main(String[] args) throws InterruptedException {    	
        toRun();
    }

    public static boolean toRun() {
        // Create Sds client to communicate with server
        System.out.println("---------------------------------------------------");
        System.out.println("  _________    .___          ____.                    ");
        System.out.println(" /   _____/  __| _/______   |    |____ ___  _______   ");
        System.out.println(" \\_____  \\  / __ |/  ___/   |    \\__  \\\\  \\/ /\\__  \\  ");
        System.out.println(" /        \\/ /_/ |\\___ \\/\\__|    |/ __ \\\\   /  / __ \\_");
        System.out.println("/_______  /\\____ /____  >________(____  /\\_/  (____  /");
        System.out.println("        \\/      \\/    \\/              \\/           \\/ ");
        System.out.println("---------------------------------------------------");

        // Step 1
        OCSClient ocsClient = new OCSClient();

        try {            
            // Step 2
            // create a SdsType
            System.out.println("Creating a SdsType");
            SdsType sampleType = getWaveDataType(sampleTypeId);
            String jsonType = ocsClient.Types.createType(tenantId, namespaceId, sampleType);
            sampleType = ocsClient.mGson.fromJson(jsonType, SdsType.class);

            // Step 3
            // create a SdsStream
            System.out.println("Creating a SdsStream");
            SdsStream sampleStream = new SdsStream(sampleStreamId, sampleTypeId);
            String jsonStream = ocsClient.Streams.createStream(tenantId, namespaceId, sampleStream);
            sampleStream = ocsClient.mGson.fromJson(jsonStream, SdsStream.class);

            // Step 4
            // insert data
            System.out.println("Inserting data");

            // insert a single event
            List<WaveData> event = new ArrayList<WaveData>();
            WaveData evt = WaveData.next(1, 2.0, 0);
            event.add(evt);
            ocsClient.Streams.insertValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(event));

            // insert a list of events
            List<WaveData> events = new ArrayList<WaveData>();
            for (int i = 2; i < 20; i += 2) {
                evt = WaveData.next(1, 2.0, i);
                events.add(evt);
                Thread.sleep(10);
            }
            ocsClient.Streams.insertValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(events));

            // Step 5
            // get the last value in stream
            System.out.println("Getting latest event");
            String jsonSingleValue = ocsClient.Streams.getLastValue(tenantId, namespaceId, sampleStreamId);
            WaveData data = ocsClient.mGson.fromJson(jsonSingleValue, WaveData.class);
            System.out.println(data.toString());
            System.out.println();

            // get all values
            System.out.println("Getting all events");
            String jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "20");
            Type listType = new TypeToken<ArrayList<WaveData>>() {
            }.getType(); // necessary for gson to decode list of WaveData, represents ArrayList<WaveData>
                         // type
            ArrayList<WaveData> foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
            // Step 6
            // get all values
            System.out.println("Getting all events in table format with headers");
            String jsonMultipleValuesTable = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "20", "", "tableh");            
            System.out.println(jsonMultipleValuesTable);
            System.out.println();

            // Step 7
            // update the first value
            System.out.println("Updating events");
            List<WaveData> newEvent = new ArrayList<WaveData>();
            evt = WaveData.next(1, 4.0, 0);
            newEvent.add(evt);
            ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvent));

            // update existing values and add 10 new values using update
            List<WaveData> newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 40; i += 2) // note: update will replace a value if it already exists, and create one if
                                            // it does not
            {
                WaveData newEvt = WaveData.next(1, 4.0, i);
                newEvents.add(newEvt);
                Thread.sleep(10); // sleep for a bit because WaveData.radians is based on clock
            }
            ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvents));

            // retrieve values
            System.out.println("Getting updated events");
            jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "40");
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();

            // Step 8
            // replace the first value
            System.out.println("Replacing events");
            newEvent = new ArrayList<WaveData>();
            evt = WaveData.next(1, 5.0, 0);
            newEvent.add(evt);
            ocsClient.Streams.replaceValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvent));

            // replace the remaining values
            newEvents = new ArrayList<WaveData>();
            for (int i = 2; i < 40; i += 2) {
                WaveData newEvt = WaveData.next(1, 5.0, i);
                newEvents.add(newEvt);
                Thread.sleep(10);
            }
            ocsClient.Streams.replaceValues(tenantId, namespaceId, sampleStreamId, ocsClient.mGson.toJson(newEvents));

            // Step 9
            // retrieve values again to see replaced values
            System.out.println("Getting replaced events");
            jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "40");
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
            //String tenantId, String namespaceId, String streamId, String startIndex, String endIndex, int skip, int count, boolean reverse, SdsBoundaryType boundaryType) throws SdsError {
       
            String retrievedInterpolated = ocsClient.Streams.getRangeValuesInterpolated(tenantId, namespaceId, sampleStreamId, "5", "32",4);
      
            System.out.println("SDS will interpolate a value for each index asked for (5,14,23,32):");
            System.out.println(retrievedInterpolated);

            // Step 10
            // retrieve filtered values see replaced values
            System.out.println("Getting filtered events");
            jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "180", "Radians%20lt%2050");
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println("Total events found: " + foundEvents.size());
            dumpEvents(foundEvents);
            System.out.println();
            
            //Step 11
            //We will retrieve a sample of our data
            System.out.println("SDS can return a sample of your data population to show trends.");
            System.out.println("Getting Sampled Values:");
            jsonMultipleValues = ocsClient.Streams.getSampledValues(tenantId, namespaceId, sampleStreamId, "0", "40", 4, "Sin");
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            dumpEvents(foundEvents);
            System.out.println();

            // Step 12
            // Property Overrides
            System.out.println("Property Overrides");
            System.out.println(
                    "Sds can interpolate or extrapolate data at an index location where data does not explicitly exist:");
            System.out.println();
            listType = new TypeToken<ArrayList<WaveData>>() {
            }.getType();
            jsonMultipleValues = ocsClient.Streams.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3,
                    false, SdsBoundaryType.ExactOrCalculated);
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);

            System.out.println(
                    "Default (Continuous) requesting data starting at index location '1', where we have not entered data, SDS will interpolate a value for each property:");
            for (WaveData evnt : foundEvents) {
                System.out.println(
                        "Order: " + evnt.getOrder() + ", Radians: " + evnt.getRadians() + ", Cos: " + evnt.getCos());
            }
            System.out.println();

            // Create a Discrete stream PropertyOverride indicating that we do not want Sds
            // to calculate a value for Radians and update our stream
            SdsStreamPropertyOverride propertyOverride = new SdsStreamPropertyOverride();
            propertyOverride.setSdsTypePropertyId("Radians");
            propertyOverride.setInterpolationMode(SdsInterpolationMode.Discrete);
            List<SdsStreamPropertyOverride> propertyOverrides = new ArrayList<SdsStreamPropertyOverride>();
            propertyOverrides.add(propertyOverride);

            // update the stream
            sampleStream.setPropertyOverrides(propertyOverrides);
            ocsClient.Streams.updateStream(tenantId, namespaceId, sampleStreamId, sampleStream);

            // repeat the retrieval
            jsonMultipleValues = ocsClient.Streams.getRangeValues(tenantId, namespaceId, sampleStreamId, "1", 0, 3,
                    false, SdsBoundaryType.ExactOrCalculated);
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            System.out.println(
                    "We can override this behavior on a property by property basis, here we override the Radians property instructing SDS not to interpolate.");
            System.out.println("SDS will now return the default value for the data type:");
            for (WaveData evnt : foundEvents) {
                System.out.println(
                        "Order: " + evnt.getOrder() + ", Radians: " + evnt.getRadians() + ", Cos: " + evnt.getCos());
            }
            System.out.println();

            // Step 13
            // SdsStreamViews
            System.out.println("SdsStreamViews");
            System.out.println("Here is some of our data as it is stored on the server:");
            for (WaveData evnt : foundEvents) {
                System.out.println("Sin: " + evnt.getSin() + ", Cos: " + evnt.getCos() + ", Tan" + evnt.getTan());
            }
            System.out.println();

            // create target SdsTypes
            SdsType targetType = getWaveDataTargetType(targetTypeId);
            String jsonTargetType = ocsClient.Types.createType(tenantId, namespaceId, targetType);
            targetType = ocsClient.mGson.fromJson(jsonTargetType, SdsType.class);
            SdsType targetIntegerType = getWaveDataTargetIntegerType(integerTargetTypeId);
            ocsClient.Types.createType(tenantId, namespaceId, targetIntegerType);

            // create a SdsStreamView
            SdsStreamView autoStreamView = new SdsStreamView();
            autoStreamView.setId(sampleStreamViewId);
            autoStreamView.setName("SampleAutoStreamView");
            autoStreamView.setDescription("This is a StreamView mapping SampleType to SampleTargetType");
            autoStreamView.setSourceTypeId(sampleTypeId);
            autoStreamView.setTargetTypeId(targetTypeId);
            ocsClient.Streams.createStreamView(tenantId, namespaceId, autoStreamView);

            // create SdsStreamViewProperties
            SdsStreamViewProperty vp1 = new SdsStreamViewProperty();
            vp1.setSourceId("Order");
            vp1.setTargetId("OrderTarget");

            SdsStreamViewProperty vp2 = new SdsStreamViewProperty();
            vp2.setSourceId("Sin");
            vp2.setTargetId("SinInt");

            SdsStreamViewProperty vp3 = new SdsStreamViewProperty();
            vp3.setSourceId("Cos");
            vp3.setTargetId("CosInt");

            SdsStreamViewProperty vp4 = new SdsStreamViewProperty();
            vp4.setSourceId("Tan");
            vp4.setTargetId("TanInt");

            SdsStreamViewProperty[] props = { vp1, vp2, vp3, vp4 };

            // create a SdsStreamView with explicit SdsStreamViewProperties
            SdsStreamView manualStreamView = new SdsStreamView();
            manualStreamView.setId(sampleManualStreamViewId);
            manualStreamView.setName("SampleManualStreamView");
            manualStreamView.setDescription("This is a StreamView mapping SampleType to SampleTargetType");
            manualStreamView.setSourceTypeId(sampleTypeId);
            manualStreamView.setTargetTypeId(integerTargetTypeId);
            manualStreamView.setProperties(props);
            ocsClient.Streams.createStreamView(tenantId, namespaceId, manualStreamView);
          

            // range values with automatically mapped SdsStreamView
            System.out.println(
                    "Specifying a StreamView with a SdsType of the same shape returns values that are automatically mapped to the target SdsType's properties:");
            Type targetListType = new TypeToken<ArrayList<WaveDataTarget>>() {
            }.getType();
            jsonMultipleValues = ocsClient.Streams.getRangeValuesStreamView(tenantId, namespaceId, sampleStreamId, "1", 0, 3,
                    false, SdsBoundaryType.ExactOrCalculated, sampleStreamViewId);
            ArrayList<WaveDataTarget> foundTargetEvents = ocsClient.mGson.fromJson(jsonMultipleValues, targetListType);
            for (WaveDataTarget evnt : foundTargetEvents) {
                System.out.println("SinTarget: " + evnt.getSinTarget() + ", CosTarget: " + evnt.getCosTarget()
                        + ", TanTarget: " + evnt.getTanTarget());
            }
            System.out.println();

            // range values with manually mapped SdsStreamView
            System.out.println(
                    "SdsStreamViews can also convert certain types of data, here we return integers where the original values were doubles:");
            Type integerListType = new TypeToken<ArrayList<WaveDataInteger>>() {
            }.getType();
            jsonMultipleValues = ocsClient.Streams.getRangeValuesStreamView(tenantId, namespaceId, sampleStreamId, "1", 0, 3,
                    false, SdsBoundaryType.ExactOrCalculated, sampleManualStreamViewId);
            ArrayList<WaveDataInteger> foundIntegerEvents = ocsClient.mGson.fromJson(jsonMultipleValues,
                    integerListType);
            for (WaveDataInteger evnt : foundIntegerEvents) {
                System.out.println("SinInt: " + evnt.getSinInt() + ", CosInt: " + evnt.getCosInt() + ", TanInt: "
                        + evnt.getTanInt());
            }
            System.out.println();

            // SdsStreamViewMaps
            System.out.println(
                    "We can query SDS to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:");
            Type sdsStreamViewType = new TypeToken<SdsStreamViewMap>() {
            }.getType();
            String jsonStreamViewMap = ocsClient.Streams.getStreamViewMap(tenantId, namespaceId, sampleStreamViewId);
            SdsStreamViewMap streamViewMap = ocsClient.mGson.fromJson(jsonStreamViewMap, sdsStreamViewType);
            dumpSdsStreamViewMap(streamViewMap);
            System.out.println();

            System.out.println(
                    "Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
            sdsStreamViewType = new TypeToken<SdsStreamViewMap>() {
            }.getType();
            jsonStreamViewMap = ocsClient.Streams.getStreamViewMap(tenantId, namespaceId, sampleManualStreamViewId);
            streamViewMap = ocsClient.mGson.fromJson(jsonStreamViewMap, sdsStreamViewType);
            dumpSdsStreamViewMap(streamViewMap);
            System.out.println();
            
            // Step 14
            System.out.println("We will now update the stream type based on the streamview");
            
            String firstVal = ocsClient.Streams.getFirstValue(tenantId, namespaceId, sampleStreamId);
            ocsClient.Streams.updateStreamType(tenantId, namespaceId, sampleStreamId, sampleStreamViewId);
            
            String newStreamString = ocsClient.Streams.getStream(tenantId, namespaceId, sampleStreamId);
            SdsStream newStream = ocsClient.mGson.fromJson(newStreamString, SdsStream.class);

            String firstValUpdated = ocsClient.Streams.getFirstValue(tenantId, namespaceId, sampleStreamId);

            System.out.println("The new type id" + newStream.getTypeId() + " compared to the original one " + sampleStream.getTypeId());
            System.out.println("The new type value " + firstValUpdated + " compared to the original one " + firstVal);
            System.out.println();
            
            // Step 15 

            String types = ocsClient.Types.getTypes(tenantId, namespaceId, 0, 100);
            String typesFiltered = ocsClient.Types.getTypes(tenantId, namespaceId, 0, 100, "Id:*Target*");
            
            System.out.println("All Types: " + types);
            System.out.println("Filtered Types: " + typesFiltered);
            System.out.println();
            
            // Step 16
            // tags and metadata
            System.out.println("Let's add some Tags and Metadata to our stream:");
            System.out.println();

            ArrayList<String> tags = new ArrayList<String>();
            tags.add("waves");
            tags.add("periodic");
            tags.add("2018");
            tags.add("validated");

            Map<String, String> metadata = new HashMap<String, String>();
            metadata.put("Region", "North America");
            metadata.put("Country", "Canada");
            metadata.put("Province", "Quebec");

            ocsClient.Streams.updateTags(tenantId, namespaceId, sampleStreamId, tags);
            ocsClient.Streams.updateMetadata(tenantId, namespaceId, sampleStreamId, metadata);

            System.out.println("Tags now associated with " + sampleStreamId);
            tags = ocsClient.Streams.getTags(tenantId, namespaceId, sampleStreamId);

            for (String tag : tags) {
                System.out.println(tag);
            }
            System.out.println();

            String region = ocsClient.Streams.getMetadata(tenantId, namespaceId, sampleStreamId, "Region");
            String country = ocsClient.Streams.getMetadata(tenantId, namespaceId, sampleStreamId, "Country");
            String province = ocsClient.Streams.getMetadata(tenantId, namespaceId, sampleStreamId, "Province");

            System.out.println("Metadata now associated with " + sampleStreamId);
            System.out.println("Metadata key Region: " + region);
            System.out.println("Metadata key Country: " + country);
            System.out.println("Metadata key Province: " + province);

            System.out.println();

            // Step 17
            // delete data

            // remove the first value
            System.out.println("Deleting values from the SdsStream");
            ocsClient.Streams.removeValue(tenantId, namespaceId, sampleStreamId, "0");

            // remove remaining values
            ocsClient.Streams.removeWindowValues(tenantId, namespaceId, sampleStreamId, "2", "40");

            // retrieve values to check deletion
            jsonMultipleValues = ocsClient.Streams.getWindowValues(tenantId, namespaceId, sampleStreamId, "0", "200");
            foundEvents = ocsClient.mGson.fromJson(jsonMultipleValues, listType);
            if (foundEvents.isEmpty())
                System.out.println("All values deleted successfully!");
            
            // Step 18
            System.out.println("Adding a stream with a secondary index.");
            SdsStreamIndex index  = new SdsStreamIndex();
            index.setSdsTypePropertyId("Radians");

            SdsStream secondary = new SdsStream(streamIdSecondary, sampleTypeId);
            secondary.setIndexes(Arrays.asList(index));

            String secondaryS = ocsClient.Streams.createStream(tenantId, namespaceId, secondary);
            secondary = ocsClient.mGson.fromJson(secondaryS, SdsStream.class);

            int count =0;
            if(sampleStream.getIndexes() != null) 
            {
                count =  sampleStream.getIndexes().size();
            }
            System.out.println("Secondary indexes on streams original:" + count + ". New one:  " + secondary.getIndexes().size());
            System.out.println();

            
            // Modifying an existing stream with a secondary index.
            System.out.println("Modifying a stream to have a secondary index.");

            String streamS = ocsClient.Streams.getStream(tenantId, namespaceId, sampleStream.getId());
            sampleStream = ocsClient.mGson.fromJson(streamS, SdsStream.class);
            
            index  = new SdsStreamIndex();
            index.setSdsTypePropertyId("RadiansTarget");
            sampleStream.setIndexes(Arrays.asList(index));


            ocsClient.Streams.updateStream(tenantId, namespaceId, sampleStream.getId(), sampleStream);
            
            streamS = ocsClient.Streams.getStream(tenantId, namespaceId, sampleStream.getId());
            sampleStream = ocsClient.mGson.fromJson(streamS, SdsStream.class);
            
            // Modifying an existing stream to remove the secondary index
            System.out.println("Removing a secondary index from a stream.");

            secondary.getIndexes().clear();

            ocsClient.Streams.updateStream(tenantId, namespaceId, secondary.getId(), secondary);
            
            streamS = ocsClient.Streams.getStream(tenantId, namespaceId, secondary.getId());
            secondary = ocsClient.mGson.fromJson(streamS, SdsStream.class);

            int numberOfIndicies=  0;
            List<SdsStreamIndex> indicies = secondary.getIndexes();
            if( indicies != null  ){
                numberOfIndicies = indicies.size();
            }

            System.out.println("Secondary indexes on streams original:" + sampleStream.getIndexes().size() + ". New one:  " + numberOfIndicies);

            // Step 19
            // Adding Compound Index Type
            System.out.println("Creating an SdsType with a compound index");
            SdsType typeCompound = getWaveCompoundDataType(compoundTypeId);
            
            jsonType = ocsClient.Types.createType(tenantId, namespaceId, typeCompound);
            typeCompound = ocsClient.mGson.fromJson(jsonType, SdsType.class);

            // create an SdsStream
            System.out.println("Creating an SdsStream off of type with compound index");
            SdsStream streamCompound = new SdsStream (streamIdCompound,  typeCompound.getId(),  "This is a sample SdsStream for storing WaveData type measurements");
     
            ocsClient.Streams.createStream(tenantId, namespaceId, streamCompound);

            
            // Step 20

            System.out.println("Inserting data");
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(1, 10)}));
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(2, 2)}));
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(3, 1)}));
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(10, 3)}));
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(10, 8)}));
            ocsClient.Streams.insertValues(tenantId, namespaceId, streamIdCompound, ocsClient.mGson.toJson(new WaveDataCompound[]{WaveDataCompound.next(10, 10)}));

            String latestCompound = ocsClient.Streams.getLastValue(tenantId, namespaceId, streamIdCompound);
            String firstCompound = ocsClient.Streams.getFirstValue(tenantId, namespaceId, streamIdCompound);

            String windowVal = ocsClient.Streams.getWindowValues(tenantId, namespaceId, streamIdCompound, "2|1", "10|8");


            System.out.println( "First data: "+ firstCompound + " Latest data: " + latestCompound);
            System.out.println();
            System.out.println("Window Data:");
            System.out.println(windowVal);

        } catch (SdsError e) {
            handleException(e);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            try {
                // Step 21
				System.out.println();
                System.out.println("Cleaning up");
                cleanUp(ocsClient);
                System.out.println("done");
            } catch (SdsError e) {
                printError("Error deleting the Sds Objects", e);
                handleException(e);
            }
        }
        return success;
    }

    /**
     * Returns the WaveData SdsType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveData SdsType
     */
    private static SdsType getWaveDataType(String sampleTypeId) {
        SdsType intType = new SdsType();
        intType.setId("intType");
        intType.setSdsTypeCode(SdsTypeCode.Int32);

        SdsType doubleType = new SdsType();
        doubleType.setId("doubleType");
        doubleType.setSdsTypeCode(SdsTypeCode.Double);

        SdsTypeProperty orderProperty = new SdsTypeProperty();
        orderProperty.setId("Order");
        orderProperty.setSdsType(intType);
        orderProperty.setIsKey(true);

        SdsTypeProperty tauProperty = new SdsTypeProperty();
        tauProperty.setId("Tau");
        tauProperty.setSdsType(doubleType);

        SdsTypeProperty radiansProperty = new SdsTypeProperty();
        radiansProperty.setId("Radians");
        radiansProperty.setSdsType(doubleType);

        SdsTypeProperty sinProperty = new SdsTypeProperty();
        sinProperty.setId("Sin");
        sinProperty.setSdsType(doubleType);

        SdsTypeProperty cosProperty = new SdsTypeProperty();
        cosProperty.setId("Cos");
        cosProperty.setSdsType(doubleType);

        SdsTypeProperty tanProperty = new SdsTypeProperty();
        tanProperty.setId("Tan");
        tanProperty.setSdsType(doubleType);

        SdsTypeProperty sinhProperty = new SdsTypeProperty();
        sinhProperty.setId("Sinh");
        sinhProperty.setSdsType(doubleType);

        SdsTypeProperty coshProperty = new SdsTypeProperty();
        coshProperty.setId("cosh");
        coshProperty.setSdsType(doubleType);

        SdsTypeProperty tanhProperty = new SdsTypeProperty();
        tanhProperty.setId("Tanh");
        tanhProperty.setSdsType(doubleType);

        // Create a SdsType for our WaveData class; the metadata properties are the ones we just created
        SdsType type = new SdsType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        SdsTypeProperty[] props = {orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty};
        type.setProperties(props);
        type.setSdsTypeCode(SdsTypeCode.Object);

        return type;
    }
    

    /**
     * Returns the WaveData SdsType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveData SdsType
     */
    private static SdsType getWaveCompoundDataType(String sampleTypeId) {
        SdsType intType = new SdsType();
        intType.setId("intType");
        intType.setSdsTypeCode(SdsTypeCode.Int32);

        SdsType doubleType = new SdsType();
        doubleType.setId("doubleType");
        doubleType.setSdsTypeCode(SdsTypeCode.Double);

        SdsTypeProperty orderProperty = new SdsTypeProperty();
        orderProperty.setId("Order");
        orderProperty.setSdsType(intType);
        orderProperty.setIsKey(true);    
        orderProperty.setOrder(1);        

        SdsTypeProperty multiplierProperty = new SdsTypeProperty();
        multiplierProperty.setId("Multiplier");
        multiplierProperty.setSdsType(intType);
        multiplierProperty.setIsKey(true);
        multiplierProperty.setOrder(2);        

        SdsTypeProperty tauProperty = new SdsTypeProperty();
        tauProperty.setId("Tau");
        tauProperty.setSdsType(doubleType);

        SdsTypeProperty radiansProperty = new SdsTypeProperty();
        radiansProperty.setId("Radians");
        radiansProperty.setSdsType(doubleType);

        SdsTypeProperty sinProperty = new SdsTypeProperty();
        sinProperty.setId("Sin");
        sinProperty.setSdsType(doubleType);

        SdsTypeProperty cosProperty = new SdsTypeProperty();
        cosProperty.setId("Cos");
        cosProperty.setSdsType(doubleType);

        SdsTypeProperty tanProperty = new SdsTypeProperty();
        tanProperty.setId("Tan");
        tanProperty.setSdsType(doubleType);

        SdsTypeProperty sinhProperty = new SdsTypeProperty();
        sinhProperty.setId("Sinh");
        sinhProperty.setSdsType(doubleType);

        SdsTypeProperty coshProperty = new SdsTypeProperty();
        coshProperty.setId("cosh");
        coshProperty.setSdsType(doubleType);

        SdsTypeProperty tanhProperty = new SdsTypeProperty();
        tanhProperty.setId("Tanh");
        tanhProperty.setSdsType(doubleType);

        // Create a SdsType for our WaveData class; the metadata properties are the ones we just created
        SdsType type = new SdsType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeCompound");
        SdsTypeProperty[] props = {orderProperty, multiplierProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty};
        type.setProperties(props);
        type.setSdsTypeCode(SdsTypeCode.Object);

        return type;
    }
    
    /**
     * Returns the WaveDataTarget SdsType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveDataTarget SdsType
     */
    private static SdsType getWaveDataTargetType(String sampleTypeId) {
        SdsType intType = new SdsType();
        intType.setId("intType");
        intType.setSdsTypeCode(SdsTypeCode.Int32);

        SdsType doubleType = new SdsType();
        doubleType.setId("doubleType");
        doubleType.setSdsTypeCode(SdsTypeCode.Double);

        SdsTypeProperty orderTargetProperty = new SdsTypeProperty();
        orderTargetProperty.setId("OrderTarget");
        orderTargetProperty.setSdsType(intType);
        orderTargetProperty.setIsKey(true);

        SdsTypeProperty tauTargetProperty = new SdsTypeProperty();
        tauTargetProperty.setId("TauTarget");
        tauTargetProperty.setSdsType(doubleType);

        SdsTypeProperty radiansTargetProperty = new SdsTypeProperty();
        radiansTargetProperty.setId("RadiansTarget");
        radiansTargetProperty.setSdsType(doubleType);

        SdsTypeProperty sinTargetProperty = new SdsTypeProperty();
        sinTargetProperty.setId("SinTarget");
        sinTargetProperty.setSdsType(doubleType);

        SdsTypeProperty cosTargetProperty = new SdsTypeProperty();
        cosTargetProperty.setId("CosTarget");
        cosTargetProperty.setSdsType(doubleType);

        SdsTypeProperty tanTargetProperty = new SdsTypeProperty();
        tanTargetProperty.setId("TanTarget");
        tanTargetProperty.setSdsType(doubleType);

        SdsTypeProperty sinhTargetProperty = new SdsTypeProperty();
        sinhTargetProperty.setId("SinhTarget");
        sinhTargetProperty.setSdsType(doubleType);

        SdsTypeProperty coshTargetProperty = new SdsTypeProperty();
        coshTargetProperty.setId("CoshTarget");
        coshTargetProperty.setSdsType(doubleType);

        SdsTypeProperty tanhTargetProperty = new SdsTypeProperty();
        tanhTargetProperty.setId("TanhTarget");
        tanhTargetProperty.setSdsType(doubleType);

        // Create a SdsType for our WaveData class; the metadata properties are the ones we just created
        SdsType type = new SdsType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        SdsTypeProperty[] props = {orderTargetProperty, tauTargetProperty, radiansTargetProperty, sinTargetProperty, cosTargetProperty, tanTargetProperty, sinhTargetProperty, coshTargetProperty, tanhTargetProperty};
        type.setProperties(props);
        type.setSdsTypeCode(SdsTypeCode.Object);

        return type;
    	
    }

    /**
     * Returns the WaveDataInteger SdsType for the sample
     *
     * @param sampleTypeId - the id for the type
     * @return WaveDataInteger SdsType
     */    
    private static SdsType getWaveDataTargetIntegerType(String sampleTypeId) {
        SdsType intType = new SdsType();
        intType.setId("intType");
        intType.setSdsTypeCode(SdsTypeCode.Int32);

        SdsTypeProperty orderTargetProperty = new SdsTypeProperty();
        orderTargetProperty.setId("OrderTarget");
        orderTargetProperty.setSdsType(intType);
        orderTargetProperty.setIsKey(true);

        SdsTypeProperty sinIntProperty = new SdsTypeProperty();
        sinIntProperty.setId("SinInt");
        sinIntProperty.setSdsType(intType);

        SdsTypeProperty cosIntProperty = new SdsTypeProperty();
        cosIntProperty.setId("CosInt");
        cosIntProperty.setSdsType(intType);

        SdsTypeProperty tanIntProperty = new SdsTypeProperty();
        tanIntProperty.setId("TanInt");
        tanIntProperty.setSdsType(intType);
        
        // Create a SdsType for our WaveData class; the metadata properties are the ones we just created
        SdsType type = new SdsType();
        type.setId(sampleTypeId);
        type.setName("WaveDataTypeJ");
        SdsTypeProperty[] props = {orderTargetProperty, sinIntProperty, cosIntProperty, tanIntProperty};
        type.setProperties(props);
        type.setSdsTypeCode(SdsTypeCode.Object);

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
    
    private static void dumpSdsStreamViewMap(SdsStreamViewMap sdsStreamViewMap) { 
        for (SdsStreamViewProperty prop : sdsStreamViewMap.getProperties()) {
            if(prop.getTargetId() != null){
				System.out.println(prop.getSourceId() + " => " + prop.getTargetId());
			}
            else {
				System.out.println(prop.getSourceId() + " => Not mapped");
			}
        }
    }
    
    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        System.out.println(new File(".").getAbsolutePath());

        try(InputStream inputStream = new FileInputStream("config.properties")) {
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return property;
    }
    public static void handleException(SdsError e) 
	{
        success = false;
        e.printStackTrace();
    }

	
    public static void cleanUp(OCSClient ocsClient) throws SdsError 
	{
        System.out.println("Deleting the stream");
        try{ocsClient.Streams.deleteStream(tenantId, namespaceId, sampleStreamId);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Streams.deleteStream(tenantId, namespaceId, streamIdSecondary);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Streams.deleteStream(tenantId, namespaceId, streamIdCompound);}
        catch(SdsError e){handleException(e);}

        System.out.println("Deleting the streamViews");
        try{ocsClient.Streams.deleteStreamView(tenantId, namespaceId, sampleStreamViewId);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Streams.deleteStreamView(tenantId, namespaceId, sampleManualStreamViewId);}
        catch(SdsError e){handleException(e);}

        System.out.println("Deleting the types");
        try{ocsClient.Types.deleteType(tenantId, namespaceId, sampleTypeId);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Types.deleteType(tenantId, namespaceId, targetTypeId);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Types.deleteType(tenantId, namespaceId, integerTargetTypeId);}
        catch(SdsError e){handleException(e);}
        try{ocsClient.Types.deleteType(tenantId, namespaceId, compoundTypeId);}
        catch(SdsError e){handleException(e);}
	}
}
