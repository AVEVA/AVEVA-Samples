from qipy import *
import configparser
import datetime
import time
import math

def printEvents(events):
    print("Total Events found: " + str(len(events)))
    for i in events:
        print(i)

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
sampleNamespaceId = "Samples" #"WaveData_SampleNamespace"
sampleTypeId = "WaveData_SampleType"
sampleStreamId = "WaveData_SampleStream"
sampleBehaviorId = "WaveData_SampleBehavior"

try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    client = QiClient(config.get('Access', 'Tenant'), config.get('Access', 'Address'), config.get('Credentials', 'Resource'), 
                      config.get('Credentials', 'AppId'), config.get('Credentials', 'AppKey'))

    print("----------------------------------")
    print("  ___  _ ____")        
    print(" / _ \(_)  _ \ _   _ ")
    print("| | | | | |_) | | | |")
    print("| |_| | |  __/| |_| |")
    print(" \__\_\_|_|    \__, |")
    print("               |___/ ")	
    print("Version " + str(client.Version))
    print("----------------------------------")
    print("Qi endpoint at {url}".format(url = client.Uri))
    print()

    ######################################################################################################
    # QiNamespace get or creation
    ######################################################################################################
    namespace = QiNamespace()
    namespace.Id = sampleNamespaceId
    namespace = client.createNamespace(namespace)
    
    ######################################################################################################
    # QiType get or creation
    ######################################################################################################
    type = getWaveDataType(sampleTypeId)
    type = client.createType(namespace.Id, type)

    ######################################################################################################
    # Qi Stream creation
    ######################################################################################################
    stream = QiStream()
    stream.Id = sampleStreamId
    stream.Name = "WaveStreamPySample"
    stream.Description = "A Stream to store the WaveData events"
    stream.TypeId = type.Id
    stream.BehaviorId = None
    stream = client.createStream(namespace.Id, stream)

    ######################################################################################################
    # CRUD operations for events
    ######################################################################################################

    start = datetime.datetime.now()
    span = datetime.datetime.strptime("0:1:0", "%H:%M:%S")

    # Insert a single event
    event = nextWave(start, span, 2.0, 0)
    client.insertValue(namespace.Id, stream.Id, event)

    # Insert a list of events
    events = []
    for i in range(2, 20, 2):
        event = nextWave(start + datetime.timedelta(seconds = i * 0.2), span, 2.0, i)
        events.append(event)
    client.insertValues(namespace.Id, stream.Id, events)

    # Get the last inserted event in a stream
    print("Latest event is:")
    print(client.getLastValue(namespace.Id, stream.Id))
    print()

    # Get all the events
    print("All events:")
    events = client.getWindowValues(namespace.Id, stream.Id, 0, 198)
    printEvents(events)
    print()

    # Update the first event
    event = nextWave(start, span, 4.0, 0)
    client.updateValue(namespace.Id, stream.Id, event)

    # Update the rest of the events
    updatedEvents = []
    for i in range(2, 200, 2):
        event = nextWave(start + datetime.timedelta(seconds = i * 0.2), span, 2.0, i)
        updatedEvents.append(event)
    client.updateValues(namespace.Id, stream.Id, updatedEvents)

    ######################################################################################################
    # Stream behavior
    ######################################################################################################

    # Stream behaviors modify retrieval.  We will retrieve three events using the default behavior, Continuous
    events = client.getRangeValues(namespace.Id, stream.Id, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    print("Default (Continuous) stream behavior")
    for e in events:
        print(("{order}: {radians}".format(order = e['Order'], radians = e['Radians'])))

    # Create a Discrete stream behavior 
    discreteBehavior = QiStreamBehavior()
    discreteBehavior.Id = sampleBehaviorId
    discreteBehavior.Mode = QiStreamMode.Discrete
    discreteBehavior = client.createBehavior(namespace.Id, discreteBehavior)

    stream.BehaviorId = discreteBehavior.Id
    client.updateStream(namespace.Id, stream)

    events = client.getRangeValues(namespace.Id, stream.Id, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    print("Discrete stream behavior")
    for e in events:
        print(("{order}: {radians}".format(order = e['Order'], radians = e['Radians'])))

    ######################################################################################################
    # Delete events
    ######################################################################################################

    #delete single event
    client.removeValue(namespace.Id, stream.Id, 0)

    #delete rest of the events
    client.removeWindowValues(namespace.Id, stream.Id, 0, 200)

    event = client.getLastValue(namespace.Id, stream.Id)
    if event != None:
        raise ValueError

    print("completed successfully!")

except Exception as i:
    print(("Encountered Error: {error}".format(error = i)))
    print()

finally:
    ######################################################################################################
    # QiType and QiStream deletion
    ######################################################################################################

    # Clean up the remaining artifacts

    print("Deleting the stream")
    supressError(lambda: client.deleteStream(namespace.Id, sampleStreamId))

    print("Deleting the type")
    supressError(lambda: client.deleteType(namespace.Id, sampleTypeId))

    print("Deleting the behavior")
    supressError(lambda: client.deleteBehavior(namespace.Id, sampleBehaviorId))

print("done")
