from ocs_sample_library_preview import *
import configparser
import time
import json

  
  
sendingToOCS = True
namespaceId = ''
typeValueTimeName = "Value_Time"
typePressureTemperatureTimeName = "Pressure_Temp_Time"

streamPressureName = "Pressure_Tank1"
streamTempName = "Temperature_Tank1"
streamTank1 = "Tank1"
streamTank2 = "Tank2"

valueCache = []
exception: Exception = None

def CheckCreation(client, vals):
    return True

def GetType_ValueTime():
    global typeValueTimeName
    typeValueTime = SdsType(id = typeValueTimeName, description = "A Time-Series indexed type with a value", sdsTypeCode = SdsTypeCode.Object)
    
    doubleType = SdsType()
    doubleType.Id = "doubleType"
    doubleType.SdsTypeCode = SdsTypeCode.Double

    timeType = SdsType()
    timeType.Id = "string"
    timeType.SdsTypeCode = SdsTypeCode.DateTime

    
    value = SdsTypeProperty()
    value.Id = "value"
    value.SdsType = doubleType

    time = SdsTypeProperty()
    time.Id = "time"
    time.SdsType = timeType
    time.IsKey = True
    
    typeValueTime.Properties = []
    typeValueTime.Properties.append(value)
    typeValueTime.Properties.append(time)

    return typeValueTime
    
def GetType_PressTempTime():
    global typePressureTemperatureTimeName
    typePressTempTime = SdsType(id = typePressureTemperatureTimeName, description = "A Time-Series indexed type with 2 values", sdsTypeCode = SdsTypeCode.Object)
    
    doubleType = SdsType()
    doubleType.Id = "doubleType"
    doubleType.SdsTypeCode = SdsTypeCode.Double

    timeType = SdsType()
    timeType.Id = "string"
    timeType.SdsTypeCode = SdsTypeCode.DateTime

    
    temperature = SdsTypeProperty()
    temperature.Id = "temperature"
    temperature.SdsType = doubleType
    
    pressure = SdsTypeProperty()
    pressure.Id = "pressure"
    pressure.SdsType = doubleType

    time = SdsTypeProperty()
    time.Id = "time"
    time.SdsType = timeType
    time.IsKey = True
    
    typePressTempTime.Properties = [temperature, pressure, time]

    return typePressTempTime

def GetData():
    global valueCache
    if valueCache:
        return valueCache
    values = []    
    values.append({"pressure": 346, "temperature": 91, "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 0, "temperature": 0, "time": "2017-01-11T22:22:23.430Z"})
    values.append({"pressure": 386, "temperature": 93, "time": "2017-01-11T22:24:23.430Z"})
    values.append({"pressure": 385, "temperature": 92, "time": "2017-01-11T22:25:23.430Z"})
    values.append({"pressure": 385, "temperature": 0, "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92, "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2, "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 0, "time": "2017-01-11T22:28:29.430Z"})
    valueCache = values
    return values

    

def GetDataTank2():
    global valueCache
    if valueCache:
        return valueCache
    values = []    
    values.append({"pressure": 345, "temperature": 89, "time": "2017-01-11T22:20:23.430Z"})

    values.append({"pressure": 356, "temperature": 0, "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 354, "temperature": 88, "time": "2017-01-11T22:22:23.430Z"})


    values.append({"pressure": 374, "temperature": 87, "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.5, "temperature": 88, "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2, "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 87, "time": "2017-01-11T22:28:29.430Z"})
    valueCache = values
    return values

def GetPressureData():
    vals = GetData()
    values =[]
    for val in vals:
        values.append({"value": val["pressure"], "time": val["time"]})
    return values

def GetTemperatureData():
    vals = GetData()
    values =[]
    for val in vals:
        values.append({"value": val["temperature"], "time": val["time"]})
    return values

def supressError(sdsCall):
    global exception
    try:
        sdsCall()
    except Exception as e:
        if not (exception):
            exception = e
        print(("Encountered Error: {error}".format(error = e)))

def main():
    global namespaceId,streamPressureName,streamTempName, exception
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        namespaceId = config.get('Configurations', 'Namespace')

        ocsClient: OCSClient = OCSClient(config.get('Access', 'ApiVersion'),config.get('Access', 'Tenant'), config.get('Access', 'Resource'), 
                        config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'), False)

        print('Creating value and time type')
        timeValueType = GetType_ValueTime()
        timeValueType = ocsClient.Types.getOrCreateType(namespaceId, timeValueType)

        print('Creating a pressure stream and temperature')
        pressureStream = SdsStream(id = streamPressureName, typeId = timeValueType.Id,  description = "A stream for pressure data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
        temperatureStream = SdsStream(id = streamTempName, typeId = timeValueType.Id, description = "A stream for temperature data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

     #   ocsClient.Streams.insertValues(namespaceId,pressureStream.Id, json.dumps((GetPressureData())) )
     #   ocsClient.Streams.insertValues(namespaceId,temperatureStream.Id, json.dumps((GetTemperatureData())) )


        

        print('Creating a tank type that has both stream and temperature')
        tankType = GetType_PressTempTime()
        tankType = ocsClient.Types.getOrCreateType(namespaceId, tankType)

        print('Creating a tank stream')
        tankStream = SdsStream(id = streamTank1, typeId = tankType.Id, description = "A stream for pressure data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, tankStream
        )
     #   ocsClient.Streams.insertValues(namespaceId,streamTank1, json.dumps(GetData()) )



        print()
        print()
        print('Looking at the data in the system.  In this case we have some null values that are encoded as 0 for the value.')
        data = GetData()
        tank1Sorted = sorted(data, key=lambda x: x['time'], reverse=False)
        print()
        print('Value we sent:')
        print(tank1Sorted[1])
        firstTime = tank1Sorted[0]['time']
        lastTime = tank1Sorted[-1]['time']


        results = ocsClient.Streams.getWindowValues(namespaceId, streamPressureName, None, firstTime, lastTime)
        
        print()
        print('Value from pressure stream:')
        print((results)[1])

        print()
        print('Value from tank1 stream:')
        results = ocsClient.Streams.getWindowValues(namespaceId, streamTank1, None, firstTime, lastTime)
        print((results)[1])

    

        print()
        print()
        print("turning on verbosity")
        ocsClient.acceptverbosity = True

        print("This means that will get default values back (in our case 0.0 since we are looking at doubles)")



        print()
        print('Value from pressure stream:')
        results = ocsClient.Streams.getWindowValues(namespaceId, streamPressureName, None, firstTime, lastTime)
        print((results)[1])
        print()
        print('Value from tank1 stream:')
        results = ocsClient.Streams.getWindowValues(namespaceId, streamTank1, None, firstTime, lastTime)
        print((results)[1])




        print()
        print()
        
        print('Now we want to look at data across multiple tanks.  For that we can take advantage of bulk stream calls')
        print('Creating a second tank stream')
        tankStream = SdsStream(id = streamTank2, typeId = tankType.Id, description = "A stream for pressure data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, tankStream)

        dataTank2 = GetDataTank2()
    #    ocsClient.Streams.insertValues(namespaceId,streamTank2, json.dumps(GetDataTank2()) )
        tank2Sorted = sorted(dataTank2, key=lambda x: x['time'], reverse=False)
        firstTimeTank2 = tank2Sorted[0]['time']
        lastTimeTank2 = tank2Sorted[-1]['time']

        
        print('Getting bulk call results')
        results = ocsClient.Streams.getStreamsWindow(namespaceId, [streamTank1, streamTank2], None, firstTimeTank2, lastTimeTank2)
        print(results)







        #the count of 1 rfers to the number of intervals requested
        print()
        print("Getting data summary")
        summaryResults = ocsClient.Streams.getSummaries(namespaceId, streamTank1, None, firstTime, lastTime,1)
        print(summaryResults)
        








    except Exception as i:   
        exception = i     
        print(("Encountered Error: {error}".format(error = i)))
        print()

    finally:
        return
        print()
        print()
        print()
        print("Cleaning up")
        print("Deleting the stream")
        supressError(lambda: ocsClient.Streams.deleteStream(namespaceId, streamPressureName))
        supressError(lambda: ocsClient.Streams.deleteStream(namespaceId, streamTempName))
        supressError(lambda: ocsClient.Streams.deleteStream(namespaceId, streamTank1))


        print("Deleting the types")
        supressError(lambda: ocsClient.Types.deleteType(namespaceId, typePressureTemperatureTimeName))
        supressError(lambda: ocsClient.Types.deleteType(namespaceId, typeValueTimeName))
    if (exception):
        raise exception



main()
print("done")

def test_main():
    main()