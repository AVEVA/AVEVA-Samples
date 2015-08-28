from qipy import *
import datetime
import time

# client = QiClient("historianmain.cloudapp.net:3380", "my api key")
client = QiClient("chad-dev:12345", "my api key")

print "Qi type operations"

#get all Qi types
def listTypes():
    types = client.getTypes()
    print "{len} Qi types found:".format(len = len(types))
    print ", ".join(t.Name for t in types)


listTypes()

#create a double type
#  QiType(double)
#  L QiTypeProperty(DateTime)
#  L QiTypeProperty(double)
doubleType = QiType()
doubleType.Id = "doubleType"
doubleType.QiTypeCode = QiTypeCode.Double
doubleProperty = QiTypeProperty()
doubleProperty.Id = "Value"
doubleProperty.QiType = doubleType

dateTimeType = QiType()
dateTimeType.Id = "dateTimeType"
dateTimeType.QiTypeCode = QiTypeCode.DateTime
dateTimeProperty = QiTypeProperty()
dateTimeProperty.Id = "TimeId"
dateTimeProperty.QiType = dateTimeType
dateTimeProperty.IsKey = True

type = QiType()
type.Name = "Double"
type.Id = "Double"
type.Description = "more than a single"
type.Properties = [doubleProperty, dateTimeProperty]
createdType = client.createType(type)
print "created double type"

listTypes()

#create an Int64 type
try:
    type = client.getType("Int64")
except QiError as e:
    print e.value

#create byte type
#  QiType(byte)
#  L QiTypeProperty(DateTime)
#  L QiTypeProperty(Byte)
byteType = QiType()
byteType.Id = "byteType"
byteType.QiTypeCode = QiTypeCode.Byte
byteProperty = QiTypeProperty()
byteProperty.Id = "Value"
byteProperty.QiType = byteType

dateTimeType = QiType()
dateTimeType.Id = "dateTimeType"
dateTimeType.QiTypeCode = QiTypeCode.DateTime
dateTimeProperty = QiTypeProperty()
dateTimeProperty.Id = "TimeId"
dateTimeProperty.QiType = dateTimeType
dateTimeProperty.IsKey = True

type = QiType()
type.Name = "byte"
type.Id = "byte"
type.Description = "more than a nibble"
type.Properties = [byteProperty, dateTimeProperty]
createdType = client.createType(type)
print "created byte type"

listTypes()

#delete byte type
client.deleteType("byte")
print "deleted byte type"

listTypes()


#stream operations:
print "Qi stream operations"

#list all Qi streams
def listStreams():
    streams = client.getStreams()
    print "{len} Qi streams found:".format(len = len(streams))
    print ", ".join("{0} ({1})".format(t.Name, t.TypeId)  for t in streams)

listStreams()

#create a stream
stream = QiStream()
stream.Id = "tangent"
stream.Name = "Tangent"
stream.Description = "More interesting than sinusoid!"
stream.TypeId = "Double"
createdStream = client.createStream(stream)
print "created tangent"

listStreams()

#edit stream
createdStream.Name = "Cosine"
client.editStream(createdStream)
print "renamed tangent to cosine"

listStreams()


#write some data 
now = datetime.datetime.utcfromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%SZ")
value = {
    "TimeId" : now,
    "Value": 100.001
    }
client.insertValue(createdStream, value)
print "inserted value: " + str(value)

#read the data 
print client.getLastValue(createdStream)

#edit the data
value["Value"] = 200.002
client.replaceValue(createdStream, value)
print "replace value: " + str(value)

#read the data 
print client.getLastValue(createdStream)

#delete the data
client.removeValue(createdStream, value["TimeId"])
print "removed value at: " + value["TimeId"]

#read the data 
print client.getLastValue(createdStream)

#delete stream
client.deleteStream(stream.Id)
print "deleted tangent"

listStreams()


print "If you made it this far, everything works!"