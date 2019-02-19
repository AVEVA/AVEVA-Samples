# program.py
#
# Copyright (C) 2019 OSIsoft, LLC. All rights reserved.
#
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
#
# OSIsoft, LLC
# 1600 Alvarado St, San Leandro, CA 94577

from ocs_sample_library_preview import *
import configparser
import datetime
import time
import math
import inspect
import collections
import traceback



######################################################################################################
# The following define the identifiers we'll use throughout
######################################################################################################

sampleDataviewId = "Dataview_Sample"
sampleDataviewName = "Dataview_Sample_Name"
sampleDataviewDescription = "A Sample Description that describes that this Dataview is just used for our sample."
sampleDataviewDescription_modified = "A longer sample description that describes that this Dataview is just used for our sample and this part shows a post."


samplePressureTypeId = "Time_Pressure_SampleType"
samplePressureStreamId = "Tank_Pressure_SampleStream"
samplePressureStreamName = "Tank Pressure SampleStream"

sampleTemperatureTypeId = "Time_Temperature_SampleType"
sampleTemperatureStreamId = "Tank_Temperature_SampleStream"
sampleTemperatureStreamName = "Tank Temperature SampleStream"



#In this example we will keep the SDS code in its own function. 
#The variable needData is used in the main program to decide if we need to do this. 
#In the rest of the code it is assumed this is used.
#The SDS code is not highlighted, but should be straightforward to follow.  
#It creates enough Types, Streams and Data to see a result.  For more details on the creating SDS objects see the SDS python example.
#This is kept seperate because chances are your data collection will occur at a different time then your creation of Dataviews, but for a complete example we assume a blank start.  

needData = True
namespaceId = ''
firstData = {}
config = configparser.ConfigParser()
config.read('config.ini')

def supressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error = e)))

def createData(ocsClient):
    
    import random
    
    doubleType = SdsType()
    doubleType.Id = "doubleType"
    doubleType.SdsTypeCode = SdsTypeCode.Double
    
    dateTimeType = SdsType()
    dateTimeType.Id = "dateTimeType"
    dateTimeType.SdsTypeCode = SdsTypeCode.DateTime
    
    pressureDoubleProperty = SdsTypeProperty()
    pressureDoubleProperty.Id = "pressure"
    pressureDoubleProperty.SdsType = doubleType
    
    temperatureDoubleProperty = SdsTypeProperty()
    temperatureDoubleProperty.Id = "temperature"
    temperatureDoubleProperty.SdsType = doubleType
    
    timeDateTimeProperty = SdsTypeProperty()
    timeDateTimeProperty.Id = "time"
    timeDateTimeProperty.SdsType = dateTimeType
    timeDateTimeProperty.IsKey = True

    pressure_SDSType = SdsType()
    pressure_SDSType.Id = samplePressureTypeId
    pressure_SDSType.Description = "This is a sample Sds type for storing Pressure type events for Dataviews"
    pressure_SDSType.SdsTypeCode = SdsTypeCode.Object
    pressure_SDSType.Properties = [pressureDoubleProperty, timeDateTimeProperty]

    temperature_SDSType = SdsType()
    temperature_SDSType.Id = sampleTemperatureTypeId
    temperature_SDSType.Description = "This is a sample Sds type for storing Temperature type events for Dataviews"
    temperature_SDSType.SdsTypeCode = SdsTypeCode.Object
    temperature_SDSType.Properties = [temperatureDoubleProperty, timeDateTimeProperty]

    print('Creating SDS Type')
    print(pressure_SDSType.toJson())
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType)
    ocsClient.Types.getOrCreateType(namespaceId, temperature_SDSType)

    pressureStream = SdsStream()
    pressureStream.Id = samplePressureStreamId
    pressureStream.Name = samplePressureStreamName
    pressureStream.Description = "A Stream to store the sample Pressure events"
    pressureStream.TypeId = samplePressureTypeId
    
    temperatureStream = SdsStream()
    temperatureStream.Id = sampleTemperatureStreamId
    temperatureStream.Name = sampleTemperatureStreamName
    temperatureStream.Description = "A Stream to store the sample Pressure events"
    temperatureStream.TypeId = sampleTemperatureTypeId

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
    ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

    start = datetime.datetime.now() - datetime.timedelta(hours = 1)

    pressureValues = []
    temperatureValues = []
    print('Sending Values')
    for i in range(1,60,1):
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
        pVal =  ('{"time" : "'+ (start + datetime.timedelta(minutes = i* 1)).strftime("%Y-%m-%dT%H:%M:%SZ")+'", "pressure":' + str(random.uniform(0, 100)) + '}')
        tVAl = ('{"time" : "'+ (start + datetime.timedelta(minutes = i * 1)).strftime("%Y-%m-%dT%H:%M:%SZ")+'", "temperature":' + str(random.uniform(50, 70)) + '}')
        if i ==1:
            firstData =('{"time" : "'+ (start + datetime.timedelta(minutes = i* 1)).strftime("%Y-%m-%dT%H:%M:%SZ")+'", "pressure":' + pv +', "temperature":' + tv + '}')

        pressureValues.append(pVal)
        temperatureValues.append(tVAl)

    print('Sending Pressure Values')
    ocsClient.Streams.insertValues(namespaceId, samplePressureStreamId, str(pressureValues).replace("'",""))
    print('Sending Temperature Values')
    ocsClient.Streams.insertValues(namespaceId, sampleTemperatureStreamId, str(temperatureValues).replace("'",""))


def main():

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

        ocsClient = OCSClient(config.get('Access', 'ApiVersion'), config.get('Access', 'Tenant'), config.get('Access', 'Resource'), 
                        config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')
        
        print(namespaceId)
        print (ocsClient.uri)


        if needData:
            createData(ocsClient)    

        sampleStreamId = "SampleStream"

        ######################################################################################################
        # Dataviews
        ######################################################################################################	

        #We need to create the dataview.  Dataview are complex objects so we write out each step in the long comment below.
        #For our dataview we are going to combine the two streams that were created, using a search to find the streams, using common part of their name. 
        #We are using the default mappings.  This means our columns won't be renamed.  Another typical use of columns is to change what stream propertis get mapped to which column.  
        #Mappings allow you to rename a column in the results to something different.  So if we want to we could rename Pressure to press.
        #We then define the IndexDataType.  Currently only datetime is supported.
        #Next we need to define the grouping rules.  Grouping decides how each row in the result is filled in. 
        #In this case we are grouping by tag, which effectively squashes are results together so that way Pressure and Temperature and Time all get results in a row.
        #If we grouped by StreamName, each row would be filled is as fully as it can by each Stream name.  Giving us results with Pressure and Time seperate from Pressure and Temperature

        queryObj  = DataviewQuery(sampleDataviewId, 'streamname',sampleStreamId, 'Contains' )
        groupRuleObj = DataviewGroupRule( "DefaultGroupRule","StreamTag")
        mappingObj = DataviewMapping(isDefault= True)

        dataview  = Dataview(id = sampleDataviewId, queries= [queryObj], indexDataType = "datetime", groupRules=[groupRuleObj], mappings= mappingObj, name = sampleDataviewName, description= sampleDataviewDescription)
        
        print
        print("Creating dataview")		
        dataviews = ocsClient.Dataviews.postDataview(namespaceId, dataview)

        print
        print("Getting dataview")		
        dv = ocsClient.Dataviews.getDataview(namespaceId, sampleDataviewId)

        #assert is added to make sure we get back what we are expecting
        assert dv.toJson() == '{"Id": "Dataview_Sample", "Queries": [{"Id": "Dataview_Sample", "Query": {"Type": "StreamName", "Value": "SampleStream", "Operator": "Contains"}}], "Name": "Dataview_Sample", "Description": null, "Mappings": {"IsDefault": true}, "IndexDataType": "datetime", "GroupRules": [{"Id": "StreamTag", "Type": null, "TokenRules": null}]}', 'Dataview is different'
        dv.Description = sampleDataviewDescription_modified

        print
        print("Updating dataview")		
        dv = ocsClient.Dataviews.postDataview(namespaceId, dv)
            
        assert dv.toJson() == '{"Id": "Dataview_Sample", "Queries": [{"Id": "Dataview_Sample", "Query": {"Type": "StreamName", "Value": "SampleStream", "Operator": "Contains"}}], "Name": "Dataview_Sample", "Description": null, "Mappings": {"IsDefault": true}, "IndexDataType": "datetime", "GroupRules": [{"Id": "StreamTag", "Type": null, "TokenRules": null}]}', 'Dataview is different'
    

        #Getting the complete set of dataviews to make sure it is there
        print
        print("Getting dataviews")		
        dataviews = ocsClient.Dataviews.getDataviews(namespaceId)
        for dataview1 in dataviews:
            if hasattr(dataview1, "Id") :
                print(dataview1.toJson())	            

        	
        #Getting the datagroups of the defined dataview.  The datgroup lets you see what is returned by the Dataview Query.
        print
        print("Getting Datagroups")		
        datagroups = ocsClient.Dataviews.getDatagroups(namespaceId, sampleDataviewId)
        for datagroup in datagroups:
            print(datagroup.toJson())	 
            

        #By default the preview get interpolated values every minute over the last hour, which lines up with our data that we sent in.  
        #Beyond the normal API optoins, this function does have the option to return the data in a class if you have created a Type for the data you are retreiving.

        print
        print("Retrieving data preview from the Dataview")		
        dataviewData = ocsClient.Dataviews.getDataviewPreview(namespaceId,sampleDataviewId)
        print(str(dataviewData))
        if needData:
            assert dataviewData[0] == firstData, "Data not what was expected"       

        '''

        #Now we can get the data creating a session.  The session allows us to get pages of data ensuring that the underlying data won't change as we collect the pages.
        #There are apis to manage the sessions, but that is beyond the scope of this basic example.
        #To highlight the use of the sessions this we will access the data, add a stream that would be added to result. 
        #It won't show up because of the session, but we will see it in the preview that doesn't use the session.

        print
        print("Retrieving data preview from the Dataview")		
        dataviewData = ocsClient.Dataviews.getDataInterpolated(namespaceId,sampleDataviewId)
        print(str(dataviewData))
        if needData:
            assert dataviewData[0] == firstData, "Data not what was expected"      
        '''


    except Exception as ex:
        print(("Encountered Error: {error}".format(error = ex)))
        print
        traceback.print_exc()
        print

    finally:
        ######################################################################################################
        # Dataview deletion
        ######################################################################################################

        
        print
        print
        print("Deleting dataview")	 
        
        supressError(lambda: ocsClient.Dataviews.deleteDataview(namespaceId, sampleDataviewId))

        
        #check, including assert is added to make sure we deleted it
        dv = None
        try:
            dv = ocsClient.Dataviews.getDataview(namespaceId, sampleDataviewId)        
        except Exception as ex:
            dv= None
        finally:
            assert dv is None , 'Delete failed'
        
        if needData:  
            print("Deleting added Streams")
            supressError(lambda: ocsClient.Streams.deleteStream(namespaceId, samplePressureStreamId))
            supressError(lambda: ocsClient.Streams.deleteStream(namespaceId, sampleTemperatureStreamId))

            print("Deleting added Types")
            supressError(lambda: ocsClient.Types.deleteType(namespaceId, samplePressureTypeId))
            supressError(lambda: ocsClient.Types.deleteType(namespaceId, sampleTemperatureTypeId))


main()
print("done")

## Straightforward test to make sure program is working using asserts in program.  Can run it yourself with pytest program.py
def test_main():
    main()