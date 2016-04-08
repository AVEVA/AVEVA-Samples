from qipy import *
import datetime
import time

#print method for returned events
def dumpEvents(foundEvents):
    print "Total Events found: "+ str(len(foundEvents))
    for i in foundEvents:
        print i

#prints a formatted error using the errorDescription and the error itself
def printError(errorDescription, error):
    if errorDescription is None or not isinstance(errorDescription, str):
        raise TypeError("errorDescription is not an instantiated string")

    if error is None or not isinstance(error, BaseException):
        raise TypeError("error is not an instantiated BaseException")

    print "\n\n======= " + errorDescription + " ======="
    print error
    print "======= End of " + errorDescription + " ======="

#trys to make a call and catches a qi error or regular exception
def handleQiCall(qiCall):
    if qiCall is None or not callable(qiCall):
        raise TypeError("Must be a callable function")

    try:
        qiCall()
    except QiError as qe:
        printError("Error in Qi Service", qe)
    except BaseException as e:
        printError("Unknown Error", e)

#delays the program for an amount of time to allow the multiple servers on Qi to become consistent with recent calls
def delayForQiConsistency():
    millisecondsToWait = 5000;
    seconds = millisecondsToWait / 1000.0

    print "Waiting for " + str(seconds) + " seconds in order to allow the multiple servers on Qi to become consistent with recent calls...\n"
    time.sleep(seconds)

#returns a type that represents the wave data
def getWaveDataType(sampleTypeId):
    if sampleTypeId is None or not isinstance(sampleTypeId, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    print "Qi type creation"

    doubleType = QiType()
    doubleType.Id = "doubleType"
    doubleType.QiTypeCode = QiTypeCode.Double

    intType = QiType()
    intType.Id = "intType"
    intType.QiTypeCode = QiTypeCode.Int32

    orderProperty =  QiTypeProperty()
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
    wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                       cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

    return wave

client = QiClient(Constants.QiServerUrl, Constants.authItems)
sampleNamespaceId = "WaveData_SampleNamespace"
sampleTypeId = "WaveData_SampleType"
sampleStreamId = "WaveData_SampleStream"
sampleBehaviorId = "WaveData_SampleBehavior"


try:
    sampleNamespace = QiNamespace()
    sampleNamespace.Id = sampleNamespaceId

    ######################################################################################################
    # QiNamespace creation
    ######################################################################################################
    print "Qi Namespace Creation"
    client.createNamespace(Constants.TenantId, sampleNamespace)
    
    delayForQiConsistency()
    
    ######################################################################################################
    # QiType creation
    ######################################################################################################
    #create Qi types for double and int, then create properties for all the wavedata properties
    print "Creating Qi type for WaveData instances"
    sampleType = getWaveDataType(sampleTypeId)

    #create the type in Qi service
    print "Creating the WaveData Qi type in Qi service"
    sampleType = client.createType(Constants.TenantId, sampleNamespaceId, sampleType)
    client.listTypes(Constants.TenantId, sampleNamespaceId)

    delayForQiConsistency()

    ######################################################################################################
    # Qi Stream creation
    ######################################################################################################

    #create a stream
    print "Creating a stream in this tenant for the WaveData measurements"

    sampleStream = QiStream()
    sampleStream.Id = sampleStreamId
    sampleStream.Name = "WaveStreamPySample"
    sampleStream.Description = "A Stream to store the WaveData Qi types events"
    sampleStream.TypeId = sampleTypeId
    sampleStream.BehaviorId = None
    sampleStream = client.createStream(Constants.TenantId, sampleNamespaceId, sampleStream)

    delayForQiConsistency()

    client.listStreams(Constants.TenantId, sampleNamespaceId)

    ######################################################################################################
    # CRUD operations for events
    ######################################################################################################

    #create events and insert into the new stream
    print"Artificially generating 100 events and inserting them into the Qi Service"

    #inserting a single event
    timeSpanFormat = "%H:%M:%S"
    spanStr = "0:1:0"
    span = datetime.datetime.strptime(spanStr, timeSpanFormat)
    waveDataEvent = WaveData.nextWave(span, 2.0, 0)

    print "Inserting the first event"
    client.insertValue(Constants.TenantId, sampleNamespaceId, sampleStream, waveDataEvent)

    delayForQiConsistency()

    #inserting a list of events
    waveDataEvents = []

    for i in range(2, 200, 2):
        waveDataEvent = WaveData.nextWave(span, 2.0, i)
        time.sleep(.2)
        waveDataEvents.append(waveDataEvent)

    print "Inserting the rest of the events"

    client.insertValues(Constants.TenantId, sampleNamespaceId, sampleStream, waveDataEvents)

    delayForQiConsistency()

    #get the last inserted event in a stream
    print "Last inserted event is :"
    lastValue = client.getLastValue(Constants.TenantId, sampleNamespaceId, sampleStream)
    print lastValue

    #retrive events
    print "Retrieving inserted events"

    foundEvents = client.getWindowValues(Constants.TenantId, sampleNamespaceId, sampleStream, 0, 198)

    #print all the events
    dumpEvents(foundEvents)

    #update events
    print "Updating events"

    #update the first events
    waveDataEvent = foundEvents[0]
    waveDataEvent = WaveData.nextWave(span, 4.0, 0)
    client.updateValue(Constants.TenantId, sampleNamespaceId, sampleStream, waveDataEvent)

    #update the rest of the events
    newEvents = []
    for i in waveDataEvents:
        waveDataEvent = WaveData.nextWave(span, 4.0, i.Order)
        time.sleep(.2)
        newEvents.append(waveDataEvent)

    client.updateValues(Constants.TenantId, sampleNamespaceId, sampleStream, newEvents)

    delayForQiConsistency()

    #check the results
    print "Retrieving the updated values"

    foundUpdatedEvents = client.getWindowValues(Constants.TenantId, sampleNamespaceId, sampleStream, 0, 198)

    #print all the events
    dumpEvents(foundUpdatedEvents)

    ######################################################################################################
    #stream behavior
    ######################################################################################################

    #illustrate how stream behaviors modify retrieval
    #First, pull three items back with GetRangeValues for range values between events.
    #The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
    print "Retrieving three events without a stream behavior"

    foundEvents = client.getRangeValues(Constants.TenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    dumpEvents(foundEvents)

    #create a stream behavior with Discrete and attach it to the existing stream
    print "Creating a stream behavior..."
    sampleBehavior = QiStreamBehavior()
    sampleBehavior.Id = sampleBehaviorId;
    sampleBehavior.Mode = QiStreamMode.StepwiseContinuousLeading
    sampleBehavior = client.createBehavior(Constants.TenantId, sampleNamespaceId, sampleBehavior)

    delayForQiConsistency()

    #update stream to inlude this behavior
    sampleStream.BehaviorId = sampleBehaviorId
    client.updateStream(Constants.TenantId, sampleNamespaceId, sampleStream)

    delayForQiConsistency()

    #repeat the retrieval
    print "Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval"
    foundEvents = client.getRangeValues(Constants.TenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    dumpEvents(foundEvents)

    #delete events
    print "Deleting events"

    #delete single event
    client.removeValue(Constants.TenantId, sampleNamespaceId, sampleStream, 0)

    #delete rest of the events
    client.removeValues(Constants.TenantId, sampleNamespaceId, sampleStream, 0, 200)
    client.removeValues(Constants.TenantId, sampleNamespaceId, sampleStream, 1, 199)

    delayForQiConsistency()

    emptyList = client.getWindowValues(Constants.TenantId, sampleNamespaceId, sampleStream, 0, 200)

except QiError as qe:
    printError("Error in Qi Service", qe)
except Exception as e:
    printError("Unknown Error", e)
finally:
    ######################################################################################################
    # QiType and QiStream deletion
    ######################################################################################################

    #deleting streams and types
    #delete streams first and then types
    #types being referenced cannot be deleted unless referrer is deleted

    print "Deleting the stream"
    handleQiCall(lambda: client.deleteStream(Constants.TenantId, sampleNamespaceId, sampleStreamId))

    print "Deleting the type"
    handleQiCall(lambda: client.deleteType(Constants.TenantId, sampleNamespaceId, sampleTypeId))

    print "Deleting the behavior"
    handleQiCall(lambda: client.deleteBehavior(Constants.TenantId, sampleNamespaceId, sampleBehaviorId))

print "test.py completed successfully!"
