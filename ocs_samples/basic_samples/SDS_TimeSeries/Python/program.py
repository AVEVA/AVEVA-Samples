# version 0.0.1


from ocs_sample_library_preview import (SdsType, SdsTypeCode, SdsTypeProperty,
                                        OCSClient, SdsStream)
import configparser
import time
import json


sendingToOCS = True
namespaceId = ''
typeValueTimeName = "Value_Time"
typePressureTemperatureTimeName = "Pressure_Temp_Time"

streamPressureName = "Pressure_Tank1"
streamTempName = "Temperature_Tank1"
streamTank0 = "Vessel"
streamTank1 = "Tank1"
streamTank2 = "Tank2"

valueCache = []
valueCache2 = []
exception: Exception = None


def CheckCreation(client, vals):
    return True


def GetType_ValueTime():

    global typeValueTimeName
    typeValueTime = SdsType(
            id=typeValueTimeName,
            description="A Time-Series indexed type with a value",
            sdsTypeCode=SdsTypeCode.Object)

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
    typePressTempTime = SdsType(
            id=typePressureTemperatureTimeName,
            description="A Time-Series indexed type with 2 values",
            sdsTypeCode=SdsTypeCode.Object)

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


def GetData_Tank2():
    global valueCache2
    if valueCache2:
        return valueCache2
    values = []
    values.append({"pressure": 345, "temperature": 89, "time": "2017-01-11T22:20:23.430Z"})

    values.append({"pressure": 356, "temperature": 0, "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 354, "temperature": 88, "time": "2017-01-11T22:22:23.430Z"})

    values.append({"pressure": 374, "temperature": 87, "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.5, "temperature": 88, "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2, "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 87, "time": "2017-01-11T22:28:29.430Z"})

    valueCache2 = values
    return values


def GetPressureData():
    vals = GetData()
    values = []
    for val in vals:
        values.append({"value": val["pressure"], "time": val["time"]})
    return values


def GetTemperatureData():
    vals = GetData()
    values = []
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
        print(("Encountered Error: {error}".format(error=e)))


def main():
    global namespaceId, streamPressureName, streamTempName, exception
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        namespaceId = config.get('Configurations', 'Namespace')

# step 1
        ocsClient: OCSClient = OCSClient(
                config.get('Access', 'ApiVersion'),
                config.get('Access', 'Tenant'),
                config.get('Access', 'Resource'),
                config.get('Credentials', 'ClientId'),
                config.get('Credentials', 'ClientSecret'),
                False)

# step 2
        print('Creating value and time type')
        timeValueType = GetType_ValueTime()
        timeValueType = ocsClient.Types.getOrCreateType(
                namespaceId, timeValueType)

# step 3
        print('Creating a stream for pressure and temperature')
        pressureStream = SdsStream(
                id=streamPressureName,
                typeId=timeValueType.Id,
                description="A stream for pressure data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
        temperatureStream = SdsStream(
                id=streamTempName,
                typeId=timeValueType.Id,
                description="A stream for temperature data of tank1")
        ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

# step 4
        ocsClient.Streams.insertValues(
                namespaceId,
                pressureStream.Id,
                json.dumps((GetPressureData())))
        ocsClient.Streams.insertValues(
                namespaceId,
                temperatureStream.Id,
                json.dumps((GetTemperatureData())))

# step 5
        print('Creating a tank type that has both stream and temperature')
        tankType = GetType_PressTempTime()
        tankType = ocsClient.Types.getOrCreateType(namespaceId, tankType)

# step 6
        print('Creating a tank stream')
        tankStream = SdsStream(
                id=streamTank1,
                typeId=tankType.Id,
                description="A stream for data of tank1s")
        ocsClient.Streams.createOrUpdateStream(namespaceId, tankStream)

# step 7
        ocsClient.Streams.insertValues(namespaceId, streamTank1,
                                       json.dumps(GetData()))

        print()
        print()
        print('Looking at the data in the system.  In this case we have some'
              'null values that are encoded as 0 for the value.')
        data = GetData()
        tank1Sorted = sorted(data, key=lambda x: x['time'], reverse=False)
        print()
        print('Value we sent:')
        print(tank1Sorted[1])
        firstTime = tank1Sorted[0]['time']
        lastTime = tank1Sorted[-1]['time']

# step 8
        results = ocsClient.Streams.getWindowValues(
                namespaceId, streamPressureName, None, firstTime, lastTime)

        print()
        print('Value from pressure stream:')
        print((results)[1])

        print()
        print('Value from tank1 stream:')
        results = ocsClient.Streams.getWindowValues(
                namespaceId, streamTank1, None, firstTime, lastTime)
        print((results)[1])

# step 9
        print()
        print()
        print("turning on verbosity")
        ocsClient.acceptverbosity = True

        print("This means that will get default values back (in our case"
              " 0.0 since we are looking at doubles)")

        print()
        print('Value from pressure stream:')
        results = ocsClient.Streams.getWindowValues(
                namespaceId, streamPressureName, None, firstTime, lastTime)
        print((results)[1])
        print()
        print('Value from tank1 stream:')
        results = ocsClient.Streams.getWindowValues(
                namespaceId, streamTank1, None, firstTime, lastTime)
        print((results)[1])

# step 10

        print()
        print()
        print("Getting data summary")
        # the count of 1 refers to the number of intervals requested
        summaryResults = ocsClient.Streams.getSummaries(
                namespaceId, streamTank1, None, firstTime, lastTime, 1)
        print(summaryResults)

        print()
        print()
        print('Now we want to look at data across multiple tanks.')
        print('For that we can take advantage of bulk stream calls')
        print('Creating new tank streams')
        tankStream = SdsStream(
                id=streamTank2,
                typeId=tankType.Id,
                description="A stream for data of tank2")
        ocsClient.Streams.createOrUpdateStream(namespaceId, tankStream)

        dataTank2 = GetData_Tank2()
        ocsClient.Streams.insertValues(
                namespaceId, streamTank2, json.dumps(GetData_Tank2()))

        tank2Sorted = sorted(dataTank2, key=lambda x: x['time'], reverse=False)
        firstTimeTank2 = tank2Sorted[0]['time']
        lastTimeTank2 = tank2Sorted[-1]['time']

        tankStream = SdsStream(
                id=streamTank0, typeId=tankType.Id, description="")
        ocsClient.Streams.createOrUpdateStream(namespaceId, tankStream)

        ocsClient.Streams.insertValues(
                namespaceId, streamTank0, json.dumps(GetData()))

        time.sleep(10)

# step 11
        print('Getting bulk call results')
        results = ocsClient.Streams.getStreamsWindow(
                namespaceId, [streamTank0, streamTank2], None,
                firstTimeTank2, lastTimeTank2)
        print(results)

    except Exception as ex:
        exception = ex
        print(f"Encountered Error: {ex}")
        print()

    finally:
        # step 12
        print()
        print()
        print()
        print("Cleaning up")
        print("Deleting the stream")
        supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, streamPressureName))
        supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, streamTempName))
        supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, streamTank0))
        supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, streamTank1))
        supressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, streamTank2))

        print("Deleting the types")
        supressError(lambda: ocsClient.Types.deleteType(
                namespaceId, typePressureTemperatureTimeName))
        supressError(lambda: ocsClient.Types.deleteType(
                namespaceId, typeValueTimeName))
    if (exception):
        raise exception


main()
print("done")


def test_main():
    main()
