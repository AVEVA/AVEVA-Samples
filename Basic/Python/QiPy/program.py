from qipy import *
import configparser
import datetime
import time
import math

def printEvents(events):
    print("Total Events found: " + str(len(events)))
    for e in events:
        e = WaveData.fromJson(e)
        print(e)

#returns a type that represents the wave data
def getWaveDataType(sampleTypeId):
    if sampleTypeId is None or not isinstance(sampleTypeId, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    intType = QiType()
    intType.Id = "intType"
    intType.QiTypeCode = QiTypeCode.Int32

    doubleType = QiType()
    doubleType.Id = "doubleType"
    doubleType.QiTypeCode = QiTypeCode.Double

    # note that the Order is the key (primary index)
    orderProperty = QiTypeProperty()
    orderProperty.Id = "Order"
    orderProperty.QiType = intType
    orderProperty.IsKey = True

    tauProperty = QiTypeProperty()
    tauProperty.Id = "Tau"
    tauProperty.QiType = doubleType

    radiansProperty = QiTypeProperty()
    radiansProperty.Id = "Radians"
    radiansProperty.QiType = doubleType

    sinProperty = QiTypeProperty()
    sinProperty.Id = "Sin"
    sinProperty.QiType = doubleType

    cosProperty = QiTypeProperty()
    cosProperty.Id = "Cos"
    cosProperty.QiType = doubleType

    tanProperty = QiTypeProperty()
    tanProperty.Id = "Tan"
    tanProperty.QiType = doubleType

    sinhProperty = QiTypeProperty()
    sinhProperty.Id = "Sinh"
    sinhProperty.QiType = doubleType

    coshProperty = QiTypeProperty()
    coshProperty.Id = "Cosh"
    coshProperty.QiType = doubleType

    tanhProperty = QiTypeProperty()
    tanhProperty.Id = "Tanh"
    tanhProperty.QiType = doubleType

    #create a QiType for WaveData Class
    wave = QiType()
    wave.Id = sampleTypeId
    wave.Name = "WaveDataPySample"
    wave.Description = "This is a sample Qi type for storing WaveData type events"
    wave.QiTypeCode = QiTypeCode.Object
    wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                       cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

    return wave

# we'll use the following for cleanup, supressing errors
def supressError(qiCall):
    try:
        qiCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error = e)))

# Generate a new WaveData event
def nextWave(now, interval, multiplier, order):
    totalSecondsDay = (now - now.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
    intervalSeconds = (interval - interval.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
    radians = ((totalSecondsDay % intervalSeconds ) / intervalSeconds) * 2 * math.pi
        
    newWave = WaveData()
    newWave.Order = order
    newWave.Radians = radians
    newWave.Tau = radians / (2 * math.pi)
    newWave.Sin = multiplier * math.sin(radians)
    newWave.Cos = multiplier * math.cos(radians)
    newWave.Tan = multiplier * math.tan(radians)
    newWave.Sinh = multiplier * math.sinh(radians)
    newWave.Cosh = multiplier * math.cosh(radians)
    newWave.Tanh = multiplier * math.tanh(radians)
        
    return newWave

######################################################################################################
# The following define the identifiers we'll use throughout
######################################################################################################
sampleTypeId = "WaveData_SampleType"
sampleStreamId = "WaveData_SampleStream"
sampleBehaviorId = "WaveData_SampleBehavior"

try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    namespace_id = config.get('Configurations', 'Namespace') # namespace is an existing namespace for a given tenant
    client = QiClient(config.get('Access', 'Tenant'), config.get('Access', 'Address'), config.get('Credentials', 'Resource'),
                      config.get('Credentials', 'Authority'), config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

    print("----------------------------------")
    print("  ___  _ ____")        
    print(" / _ \(_)  _ \ _   _ ")
    print("| | | | | |_) | | | |")
    print("| |_| | |  __/| |_| |")
    print(" \__\_\_|_|    \__, |")
    print("               |___/ ")	
    print("Version " + str(client.Version))
    print("----------------------------------")
    print("Qi endpoint at {url}".format(url=client.Uri))
    print()

    ######################################################################################################
    # QiType creation and gets
    ######################################################################################################
    type = getWaveDataType(sampleTypeId)
    type = client.createType(namespace_id, type)
    print(client.getType(namespace_id,type.Id))
    print(str(client.getTypes(namespace_id)))

    ######################################################################################################
    # Qi Stream creation and gets
    ######################################################################################################
    stream = QiStream()
    stream.Id = sampleStreamId
    stream.Name = "WaveStreamPySample"
    stream.Description = "A Stream to store the WaveData events"
    stream.TypeId = type.Id
    stream.BehaviorId = None
    stream = client.createStream(namespace_id, stream)
    print(client.getStream(namespace_id, sampleStreamId).toJsonString())
    print(str(client.getStreams(namespace_id, "")))

    ######################################################################################################
    # CRUD operations for events
    ######################################################################################################
    start = datetime.datetime.now()
    span = datetime.datetime.strptime("0:1:0", "%H:%M:%S")

    # Insert a single event
    event = nextWave(start, span, 2.0, 0)
    client.insertValue(namespace_id, stream.Id, event)

    # Insert a list of events
    events = []
    for i in range(2, 20, 2):
        event = nextWave(start + datetime.timedelta(seconds=(i * 0.2)), span, 2.0, i)
        events.append(event)
    client.insertValues(namespace_id, stream.Id, events)

    # Get the last inserted event in a stream
    event = client.getLastValue(namespace_id, stream.Id, WaveData)
    print("Latest value:")
    print(event)

    # Get value with index = 4
    event = client.getValue(namespace_id, stream.Id, WaveData, 4)
    print("Value with index = 4:")
    print(event)

    # Get all the events
    events = client.getWindowValues(namespace_id, stream.Id, WaveData, 0, 198)
    print("All events:")
    for e in events:
        print(e.toJsonString())

    # Update the first event
    event = nextWave(start, span, 4.0, 0)
    client.updateValue(namespace_id, stream.Id, event)

    # Update the rest of the events
    updatedEvents = []
    for i in range(2, 200, 2):
        event = nextWave(start + datetime.timedelta(seconds=i * 0.2), span, 2.0, i)
        updatedEvents.append(event)
    client.updateValues(namespace_id, stream.Id, updatedEvents)

    # Replace the first event
    event = nextWave(start, span, 10.0, 0)
    client.replaceValue(namespace_id, stream.Id, event)

    # Replace the rest of the events
    replacedEvents = []
    for i in range(2, 200, 2):
        event = nextWave(start + datetime.timedelta(seconds=i * 0.2), span, 10.0, i)
        replacedEvents.append(event)
    client.replaceValues(namespace_id, stream.Id, replacedEvents)

    ######################################################################################################
    # Stream behavior
    ######################################################################################################
    # Stream behaviors modify retrieval.  Retrieves three events using the default behavior, Continuous
    print("Retrieving values with no behavior specified")
    events = client.getRangeValues(namespace_id, stream.Id, WaveData, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    for e in events:
        print(e.toJsonString())

    # Create a Discrete stream behavior 
    discreteBehavior = QiStreamBehavior()
    discreteBehavior.Id = sampleBehaviorId
    discreteBehavior.Mode = QiStreamMode.Discrete
    discreteBehavior = client.createBehavior(namespace_id, discreteBehavior)

    # Get a behavior by ID
    print(client.getBehavior(namespace_id, discreteBehavior.Id))

    # Get multiple behaviors
    print(str(client.getBehaviors(namespace_id, 0, 100)))

    # Update the stream with behavior
    stream.BehaviorId = discreteBehavior.Id
    client.updateStream(namespace_id, stream)

    # Retrieve events with modified stream
    events = client.getRangeValues(namespace_id, stream.Id, WaveData, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    print("Discrete stream behavior")
    for e in events:
        print(e.toJsonString())

    ######################################################################################################
    # Delete events
    ######################################################################################################
    print("Deleting values")
    # Delete single event
    client.removeValue(namespace_id, stream.Id, 0)

    # Delete rest of the events
    client.removeWindowValues(namespace_id, stream.Id, 0, 200)

    # Attempt to retrieve the last value, fail if found
    event = client.getLastValue(namespace_id, stream.Id, WaveData)
    if event != None:
        raise ValueError

    print("Completed successfully!")

except Exception as i:
    print(("Encountered Error: {error}".format(error=i)))
    print()

finally:
    ######################################################################################################
    # QiType and QiStream deletion
    ######################################################################################################

    # Clean up the remaining artifacts
    supressError(lambda: client.deleteStream(namespace_id, sampleStreamId))
    supressError(lambda: client.deleteType(namespace_id, sampleTypeId))
    supressError(lambda: client.deleteBehavior(namespace_id, sampleBehaviorId))

print("Done")