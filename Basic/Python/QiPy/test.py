from qipy import *
import datetime
import random

client = QiClient("localhost:12345", "my api key")

print "Qi type operations"

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
wave.Id = "WaveData"
wave.Name = "WaveData"
wave.Description = "This is a sample Qi type for storing WaveData type events"
wave.Properties = [orderProperty, tauProperty, radiansProperty, sinProperty, 
                   cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty]

#create the type in Qi service
print "Creating the WaveData Qi type in Qi service"
evtType = client.createType(wave)
client.listTypes()

#create a stream
print "Creating a stream in this tenant for the WaveData measurements"

stream = QiStream()
stream.Id = "WaveStream"
stream.Name = "WaveStream"
stream.Description = "A Stream to store the WaveData Qi types events"
stream.TypeId = "WaveData"
evtStream = client.createStream(stream)

client.listStreams()


#CRUD operations

#create events and insert into the new stream
print"Artificially generating 100 events and inserting them into the Qi Service"

#inserting a single event
timeSpanFormat = "%H:%M:%S"
spanStr = "0:0:1"
span = datetime.datetime.strptime(spanStr, timeSpanFormat)
evt = WaveData.nextWave(span, 2.0, 0)

client.insertValue(evtStream, evt)

#get the last inserted event in a stream
print "Last inserted event is :"
print client.getLastValue(evtStream)

#inserting a list of events
events = []
for i in range(2, 200, 2):
    evt = WaveData.nextWave(span, 2.0, i)
    time.sleep(.2)
    events.append(evt)

client.insertValues(evtStream, events)

#retrive events
print "Retrieving inserted events"

foundEvents = client.getWindowValues(evtStream, 0, 99)

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

#delete events
print "deleting events"

#delete single event
client.removeValue(evtStream, 0)

#delete rest of the events
client.removeValues(evtStream,0,99)

emptyList = client.getWindowValues(evtStream, 0, 99)

#deleting streams and types
#delete streams first and then types
#types being referenced cannot be deleted unless referrer is deleted
client.deleteStream("WaveStream")
client.deleteType("WaveData")

print "test.py completed successfully!"
