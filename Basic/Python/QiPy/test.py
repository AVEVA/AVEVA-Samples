from qipy import *
import datetime
import time

#print method for returned events
def dumpEvents(foundEvents):
    print "Total Events found: "+ str(len(foundEvents))
    for i in foundEvents:
        print i

client = QiClient(Constants.QiServerUrl, Constants.authItems)

try:
    namespace = QiNamespace()
    namespace.Id = "QiNamespace"

    ######################################################################################################
    # QiNamespace creation
    ######################################################################################################
    print "Qi Namespace Creation"
    client.createNamespace(Constants.TenantId, namespace)

    ######################################################################################################
    # QiType creation
    ######################################################################################################
    print "Qi type creation"

    #create Qi types for double and int, then create properties for all the wavedata properties
    print "Creating Qi type for WaveData instances"
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
    wave.Id = "WaveDataPySample"
    wave.Name = "WaveDataPySample"
    wave.Description = "This is a sample Qi type for storing WaveData type events"
    wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                       cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

    #create the type in Qi service
    print "Creating the WaveData Qi type in Qi service"
    evtType = client.createType(Constants.TenantId, namespace.Id, wave)
    client.listTypes(Constants.TenantId, namespace.Id)

    ######################################################################################################
    # Qi Stream creation
    ######################################################################################################

    #create a stream
    print "Creating a stream in this tenant for the WaveData measurements"

    stream = QiStream()
    stream.Id = "WaveStreamPySample"
    stream.Name = "WaveStreamPySample"
    stream.Description = "A Stream to store the WaveData Qi types events"
    stream.TypeId = "WaveDataPySample"
    stream.BehaviorId = None
    evtStream = client.createStream(Constants.TenantId, namespace.Id, stream)

    client.listStreams(Constants.TenantId, namespace.Id)

    ######################################################################################################
    # CRUD operations for events
    ######################################################################################################

    #create events and insert into the new stream
    print"Artificially generating 100 events and inserting them into the Qi Service"

    #inserting a single event
    timeSpanFormat = "%H:%M:%S"
    spanStr = "0:1:0"
    span = datetime.datetime.strptime(spanStr, timeSpanFormat)
    evt = WaveData.nextWave(span, 2.0, 0)

    client.insertValue(Constants.TenantId, namespace.Id, evtStream, evt)

    #get the last inserted event in a stream
    print "Last inserted event is :"
    lastValue = client.getLastValue(Constants.TenantId, namespace.Id, evtStream)
    print lastValue

    #inserting a list of events
    events = []

    for i in range(2, 200, 2):
        evt = WaveData.nextWave(span, 2.0, i)
        time.sleep(.2)
        events.append(evt)

    client.insertValues(Constants.TenantId, namespace.Id, evtStream, events)

    #retrive events
    print "Retrieving inserted events"

    foundEvents = client.getWindowValues(Constants.TenantId, namespace.Id, evtStream, 0, 198)

    #print all the events
    dumpEvents(foundEvents)

    #update events
    print "Updating events"

    #update the first events
    evt = foundEvents[0]
    evt = WaveData.nextWave(span, 4.0, 0)
    client.updateValue(Constants.TenantId, namespace.Id, evtStream, evt)

    #update the rest of the events
    newEvents = []
    for i in events:
        evt = WaveData.nextWave(span, 4.0, i.Order)
        time.sleep(.2)
        newEvents.append(evt)

    client.updateValues(Constants.TenantId, namespace.Id, evtStream, newEvents)

    #check the results
    print "Retrieving the updated values"

    foundUpdatedEvents = client.getWindowValues(Constants.TenantId, namespace.Id, evtStream, 0, 198)

    #print all the events
    dumpEvents(foundUpdatedEvents)

    ######################################################################################################
    #stream behavior
    ######################################################################################################

    #illustrate how stream behaviors modify retrieval
    #First, pull three items back with GetRangeValues for range values between events.
    #The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
    print "Retrieving three events without a stream behavior"

    foundEvents = client.getRangeValues(Constants.TenantId, namespace.Id, evtStream.Id, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    dumpEvents(foundEvents)

    #create a stream behavior with Discrete and attach it to the existing stream
    behavior = QiStreamBehavior()
    behavior.Id = "evtStreamStepLeading";
    behavior.Mode = QiStreamMode.StepwiseContinuousLeading
    behavior = client.createBehavior(Constants.TenantId, namespace.Id, behavior)

    #update stream to inlude this behavior
    evtStream.BehaviorId = behavior.Id
    client.updateStream(Constants.TenantId, namespace.Id, evtStream)

    #repeat the retrieval
    print "Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval"
    foundEvents = client.getRangeValues(Constants.TenantId, namespace.Id, evtStream.Id, "1", 0, 3, False, QiBoundaryType.ExactOrCalculated)
    dumpEvents(foundEvents)

    #delete events
    print "Deleting events"

    #delete single event
    client.removeValue(Constants.TenantId, namespace.Id, evtStream, 0)

    #delete rest of the events
    client.removeValues(Constants.TenantId, namespace.Id, evtStream,0, 200)
    client.removeValues(Constants.TenantId, namespace.Id, evtStream,1, 199)

    emptyList = client.getWindowValues(Constants.TenantId, namespace.Id, evtStream, 0, 200)

    ######################################################################################################
    # QiType and QiStream deletion
    ######################################################################################################

    #deleting streams and types
    #delete streams first and then types
    #types being referenced cannot be deleted unless referrer is deleted

except Exception as e:
    print e
finally:
    client.deleteStream(Constants.TenantId, namespace.Id, evtStream.Id)
    client.deleteType(Constants.TenantId, namespace.Id, evtType.Id)
    client.deleteBehavior(Constants.TenantId, namespace.Id, behavior.Id)

print "test.py completed successfully!"
