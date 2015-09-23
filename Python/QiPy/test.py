from qipy import *
import datetime

#print method for returned events
def dumpEvents(foundEvents):
    print "Total Events found: "+ str(len(foundEvents))
    for i in foundEvents:
        print i

authItems = {'resource' : "https://qihomeprod.onmicrosoft.com/historian",
             'authority' : "https://login.windows.net/qitenant1prod.onmicrosoft.com/oauth2/token",
             'appId' : "64f52acc-4a02-40ad-a059-7dcd1d38be68",
             'appKey' : "GjqVItbTHEgW1f8u3zaPUAqP8wDjDHrZpMUq8Mb8ZNo="}

QiServerUrl = "qi-data.osisoft.com:3380"

client = QiClient(QiServerUrl, authItems)

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
wave.Id = "WaveDataPy"
wave.Name = "WaveDataPy"
wave.Description = "This is a sample Qi type for storing WaveData type events"
wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                   cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

#create the type in Qi service
print "Creating the WaveData Qi type in Qi service"
evtType = client.createType(wave)
client.listTypes()

######################################################################################################
# Qi Stream creation
######################################################################################################

#create a stream
print "Creating a stream in this tenant for the WaveData measurements"

stream = QiStream()
stream.Id = "WaveStreamPy"
stream.Name = "WaveStreamPy"
stream.Description = "A Stream to store the WaveData Qi types events"
stream.TypeId = "WaveDataPy"
evtStream = client.createStream(stream)

client.listStreams()

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

client.insertValue(evtStream, evt)

#get the last inserted event in a stream
print "Last inserted event is :"
print client.getLastValue(evtStream)

#inserting a list of events
events = []
for i in range(1,200,2):
    evt = WaveData.nextWave(span, 2.0, i)
    events.append(evt)

client.insertValues(evtStream, events)

#retrive events
print "Retrieving inserted events"

foundEvents = client.getWindowValues(evtStream, 0, 99)

#print all the events
dumpEvents(foundEvents)

#update events
print "Updating events"

#update the first events
evt = foundEvents[0]
evt = WaveData.nextWave(span, 4.0, 0)
client.updateValue(evtStream, evt)

#update the rest of the events
newEvents = []
for i in events:
    evt = WaveData.nextWave(span, 4.0, i.Order)
    newEvents.append(evt)

client.updateValues(evtStream, newEvents)

#check the results
print "Retrieving the updated values"

foundUpdatedEvents = client.getWindowValues(evtStream, 0, 99)

#print all the events
dumpEvents(foundUpdatedEvents)

######################################################################################################
#stream behaviour
######################################################################################################

#illustrate how stream behaviors modify retrieval
#First, pull three items back with GetRangeValues for range values between events.
#The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
print "Retrieving three events without a stream behaviour"

foundEvents = client.getRangeValues("WaveStreamPy", "1", 0, 3, False, QiBoundaryType.ExactOrCalculated.value)
dumpEvents(foundEvents)

#create a stream behavior with Discrete and attach it to the existing stream
behaviour = QiStreamBehaviour()
behaviour.Id = "evtStreamStepLeading";
behaviour.Mode = QiStreamMode.StepwiseContinuousLeading.value;
behaviour = client.createBehaviour(behaviour)

#update stream to inlude this behaviour
evtStream.BehaviourId = behaviour.Id
client.updateStream(evtStream)

#repeat the retrieval
print "Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval"
foundEvents = client.getRangeValues("WaveStreamPy", "1", 0, 3, False, QiBoundaryType.ExactOrCalculated.value)
dumpEvents(foundEvents)

#delete events
print "deleting events"

#delete single event
client.removeValue(evtStream, 1)

#delete rest of the events
client.removeValues(evtStream,0, 200)

emptyList = client.getWindowValues(evtStream, 0, 200)

######################################################################################################
# QiType and QiStream deletion
######################################################################################################

#deleting streams and types
#delete streams first and then types
#types being referenced cannot be deleted unless referrer is deleted
client.deleteStream("WaveStreamPy")
client.deleteType("WaveDataPy")

print "test.py completed successfully!"