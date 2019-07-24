# version 0.0.3

from ocs_sample_library_preview import (
    SdsTypeCode, SdsType, SdsTypeProperty, SdsStream, OCSClient, Dataview,
    DataviewQuery, DataviewGroupRule, DataviewMapping, DataviewIndexConfig)
import configparser
import datetime
import time
import traceback

###############################################################################
# The following define the identifiers we'll use throughout
###############################################################################

sampleDataviewId = "Dataview_Sample"
sampleDataviewName = "Dataview_Sample_Name"
sampleDataviewDescription = "A Sample Description that describes that this "\
                            "Dataview is just used for our sample."
sampleDataviewDescription_modified = "A longer sample description that "\
                                     "describes that this Dataview is just "\
                                     "used for our sample and this part shows"\
                                     " a put."


samplePressureTypeId = "Time_Pressure_SampleType"
samplePressureStreamId = "Tank_Pressure_SampleStream"
samplePressureStreamName = "Tank Pressure SampleStream"

sampleTemperatureTypeId = "Time_Temperature_SampleType"
sampleTemperatureStreamId = "Tank_Temperature_SampleStream"
sampleTemperatureStreamName = "Tank Temperature SampleStream"


# In this example we will keep the SDS code in its own function.
# The variable needData is used in the main program to decide if we need to do
# this. In the rest of the code it is assumed this is used.
# The SDS code is not highlighted, but should be straightforward to follow.
# It creates enough Types, Streams and Data to see a result.
# For more details on the creating SDS objects see the SDS python example.

# This is kept seperate because chances are your data collection will occur at
# a different time then your creation of Dataviews, but for a complete
# example we assume a blank start.


needData = True
namespaceId = ''
config = configparser.ConfigParser()
config.read('config.ini')
startTime = None


def supressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))


def createData(ocsClient):
    import random
    global namespaceId, startTime

    doubleType = SdsType(id="doubleType", sdsTypeCode=SdsTypeCode.Double)
    dateTimeType = SdsType(id="dateTimeType", sdsTypeCode=SdsTypeCode.DateTime)

    pressureDoubleProperty = SdsTypeProperty(id="pressure", sdsType=doubleType)
    temperatureDoubleProperty = SdsTypeProperty(id="temperature",
                                                sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(id="time", sdsType=dateTimeType,
                                           isKey=True)

    pressure_SDSType = SdsType(
        id=samplePressureTypeId,
        description="This is a sample Sds type for storing Pressure type "
                    "events for Dataviews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, timeDateTimeProperty])
    temperature_SDSType = SdsType(
        id=sampleTemperatureTypeId,
        description="This is a sample Sds type for storing Temperature type "
                    "events for Dataviews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[temperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Type')
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType)
    ocsClient.Types.getOrCreateType(namespaceId, temperature_SDSType)

    pressureStream = SdsStream(
        id=samplePressureStreamId,
        name=samplePressureStreamName,
        description="A Stream to store the sample Pressure events",
        typeId=samplePressureTypeId)

    temperatureStream = SdsStream(
        id=sampleTemperatureStreamId,
        name=sampleTemperatureStreamName,
        description="A Stream to store the sample Temperature events",
        typeId=sampleTemperatureTypeId)

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
    ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)

    pressureValues = []
    temperatureValues = []
    
    def valueWithTime(timestamp, sensor, value):
        return f'{{"time": "{timestamp}", "{sensor}": {str(value)} }}'
    
    print('Generating Values')
    for i in range(1, 30, 1):
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
        timestamp = (start + datetime.timedelta(minutes=i * 2)).isoformat(timespec='seconds')
        pVal = valueWithTime(timestamp, "pressure", random.uniform(0, 100)) 
        tVAl = valueWithTime(timestamp, "temperature", random.uniform(50, 70))
        
        pressureValues.append(pVal)
        temperatureValues.append(tVAl)

    print('Sending Pressure Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        samplePressureStreamId,
        str(pressureValues).replace("'", ""))
    print('Sending Temperature Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleTemperatureStreamId,
        str(temperatureValues).replace("'", ""))
    startTime = start


def main(test=False):
    global namespaceId
    success = True
    exception = {}

    try:
        print("--------------------------------------------------------------------")
        print(" ######                                             ######  #     # ")
        print(" #     #   ##   #####   ##   #    # # ###### #    # #     #  #   #  ")
        print(" #     #  #  #    #    #  #  #    # # #      #    # #     #   # #   ")
        print(" #     # #    #   #   #    # #    # # #####  #    # ######     #    ")
        print(" #     # ######   #   ###### #    # # #      # ## # #          #    ")
        print(" #     # #    #   #   #    #  #  #  # #      ##  ## #          #    ")
        print(" ######  #    #   #   #    #   ##   # ###### #    # #          #    ")
        print("--------------------------------------------------------------------")

        # Step 1
        ocsClient = OCSClient(config.get('Access', 'ApiVersion'),
                              config.get('Access', 'Tenant'),
                              config.get('Access', 'Resource'),
                              config.get('Credentials', 'ClientId'),
                              config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')

        print(namespaceId)
        print(ocsClient.uri)

        # Step 2
        if needData:
            createData(ocsClient)

        sampleStreamId = "SampleStream"

        #######################################################################
        # Dataviews
        #######################################################################

        # We need to create the dataview.
        # For our dataview we are going to combine the two streams that were
        # created, using a search to find the streams,
        # using common part of their name.

        # We are using the default mappings.
        # This means our columns will keep their original names.
        # Another typical use of columns is to change what stream properties
        # get mapped to which column.

        # Mappings allow you to rename a column in the results to something
        # different.  So if we want to we could rename Pressure to press.

        # We then define the IndexDataType.  Currently only
        # datetime is supported.

        # Next we need to define IndexConfig.  It holds the default
        #  startIndex and endIndex to define a time period, mode (interpolated),
        #  and interpolation interval. 

        # Our results when looking at it like a table looks like:
        # 
        # time,pressure,temperature
        # 2019-06-27T12:23:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:24:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:25:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:26:00Z,40.5653155047711,59.4181700259214
        # 2019-06-27T12:27:00Z,54.5602717243303,55.4288084527031
        # ...

        # Step 3
        queryObj = DataviewQuery(sampleDataviewId, f"name:*{sampleStreamId}*")
        mappingObj = DataviewMapping(isDefault=True)
        if startTime:
            indexConfigObj = DataviewIndexConfig(startIndex=startTime.isoformat(timespec='minutes'),
                                                 endIndex=(startTime + datetime.timedelta(minutes=40)).isoformat(timespec='minutes'),
                                                 mode="Interpolated",
                                                 interval="00:01:00")
        else:
            indexConfigObj = None
        dataview = Dataview(id=sampleDataviewId, queries=queryObj,
                            indexDataType="datetime",
                            mappings=mappingObj, name=sampleDataviewName,
                            indexConfig=indexConfigObj,
                            description=sampleDataviewDescription)
        print
        print("Creating dataview")
        print(dataview.toJson())
        dataviews = ocsClient.Dataviews.postDataview(namespaceId, dataview)

        # Step 4
        print
        print("Getting dataview")
        dv = ocsClient.Dataviews.getDataview(namespaceId, sampleDataviewId)
        # assert is added to make sure we get back what we are expecting
        expectedJSON = '{"Id": "Dataview_Sample", "Queries": [{"Id": "Dataview_Sample", "Query": "name:*SampleStream*"}], "Name": "Dataview_Sample_Name", "Description": "A Sample Description that describes that this Dataview is just used for our sample.", "Mappings": {"IsDefault": true, "Columns": [{"Name": "time", "IsKey": true, "DataType": "DateTime", "MappingRule": {"PropertyPaths": ["time"]}}, {"Name": "pressure", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["pressure"]}}, {"Name": "temperature", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["temperature"]}}]}, "IndexConfig": ' + indexConfigObj.toJson(withSeconds=True) + ', "IndexDataType": "DateTime", "GroupRules": []}'
        assert dv.toJson().lower() == expectedJSON.lower(), 'Dataview is different: ' + dv.toJson()

        dv.Description = sampleDataviewDescription_modified
        dv.Mappings.IsDefault = False  # for now we have to change this to post

        # Step 5
        print
        print("Updating dataview")
        # No dataview returned, success is 204
        ocsClient.Dataviews.putDataview(namespaceId, dv)

        # Step 6
        # Getting the complete set of dataviews to make sure it is there
        print
        print("Getting dataviews")
        dataviews = ocsClient.Dataviews.getDataviews(namespaceId)
        for dataview1 in dataviews:
            if hasattr(dataview1, "Id"):
                print(dataview1.toJson())

        # Getting the datagroups of the defined dataview.
        # The datgroup lets you see what is returned by the Dataview Query.
        print
        print("Getting Datagroups")

        # Step 7
        # This works for the automated test.  You can use this or the below.
        datagroups = ocsClient.Dataviews.getDatagroups(
            namespaceId, sampleDataviewId, 0, 100, True)
        print('datagroups')
        print(datagroups)

        # By default the preview get interpolated values every minute over the
        # last hour, which lines up with our data that we sent in.

        # Beyond the normal API options, this function does have the option
        # to return the data in a class if you have created a Type for the
        # data you are retrieving.

        # Step 8
        print
        print("Retrieving data preview from the Dataview")
        dataviewDataPreview1 = ocsClient.Dataviews.getDataInterpolated(
            namespaceId, sampleDataviewId)
        print(str(dataviewDataPreview1[0]))

        # Step 9
        print()
        print("Getting data as a table, seperated by commas, with headers")
        # Get the first 20 rows, keep token for next 20 rows
        dataviewDataTable1, token = ocsClient.Dataviews.getDataInterpolated(
            namespaceId, sampleDataviewId, form="csvh", count=20)

        # Display received 20 lines showing: 
        #   * First lines with extrapolation (first value replicated of each stream)
        #   * Interpolated values at 1 minute interval, stream recorded at 2 minutes interval
        print(dataviewDataTable1)
        # Get the last 20 rows using token, then display (without row header) 
        dataviewDataTable2, token = ocsClient.Dataviews.getDataInterpolated(
            namespaceId, sampleDataviewId, form="csv", count=20, continuationToken=token)   
        print(dataviewDataTable2, "\n\n")
        assert token is None, "Continuation token is not None"
        
        # Now override startIndex/endIndex/interval of previous Data View
        # Ask for last 5 minutes of data, aligned on the seconds, interpolated at 30 seconds
        startIndex = (startTime + datetime.timedelta(minutes=55)).isoformat(timespec='seconds')
        endIndex = (startTime + datetime.timedelta(minutes=60)).isoformat(timespec='seconds')
        dataviewDataTable3, token2 = ocsClient.Dataviews.getDataInterpolated(
            namespaceId, sampleDataviewId, form="csvh", count=10, continuationToken=None,
            startIndex=startIndex, endIndex=endIndex, interval="00:00:30")
        print(dataviewDataTable3)
        assert token2 is None, "Continuation token is not None"

    except Exception as ex:
        print((f"Encountered Error: {ex}"))
        print
        traceback.print_exc()
        print
        success = False
        exception = ex

    finally:
        #######################################################################
        # Dataview deletion
        #######################################################################
        
        print
        print
        print("Deleting dataview")

        # Step 10
        supressError(lambda: ocsClient.Dataviews.deleteDataview(
            namespaceId, sampleDataviewId))

        # check, including assert is added to make sure we deleted it
        dv = None
        try:
            dv = ocsClient.Dataviews.getDataview(namespaceId, sampleDataviewId)
        except Exception as ex:
            # Exception is expected here since dataview has been deleted
            dv = None
        finally:
            assert dv is None, 'Delete failed'
            print("Verification OK: dataview effectively deleted")
            
        if needData:
            print("Deleting added Streams")
            supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, samplePressureStreamId))
            supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleTemperatureStreamId))

            print("Deleting added Types")
            supressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureTypeId))
            supressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTemperatureTypeId))
        if test and not success:
            raise exception


main()
print("done")


# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py
def test_main():
    main(True)
