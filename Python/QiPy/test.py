from qipy import *
import datetime
import random

client = QiClient("localhost:12345", "my api key")

print "Qi type operations"

#get all Qi types
def listTypes():
    types = client.getTypes()
    print "{len} Qi types found:".format(len = len(types))
    print ",\n ".join(t.Name for t in types)


listTypes()

#create a double type
#  QiType(double)
#  ├─ QiTypeProperty(DateTime)
#  └─ QiTypeProperty(double)
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

int64Type = QiType()
int64Type.Id = "int64Type"
int64Type.QiTypeCode = QiTypeCode.Int64
int64Property = QiTypeProperty()
int64Property.Id = "Value"
int64Property.QiType = int64Type
dateTimeType = QiType()
dateTimeType.Id = "dateTimeType"
dateTimeType.QiTypeCode = QiTypeCode.DateTime
dateTimeProperty = QiTypeProperty()
dateTimeProperty.Id = "TimeId"
dateTimeProperty.QiType = dateTimeType
dateTimeProperty.IsKey = True

type = QiType()
type.Name = "int64"
type.Id = "int64"
type.Description = "as long as a long"
type.Properties = [int64Property, dateTimeProperty]
createdType = client.createType(type)
print "created int64 type"

listTypes()


#create byte type
#  QiType(byte)
#  ├─ QiTypeProperty(DateTime)
#  └─ QiTypeProperty(Byte)
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
value = {
    "TimeId" : datetime.datetime.now().isoformat(),
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

# write a bunch of data
values = [{"Value": random.random() * 1000, 
           "TimeId": (datetime.datetime.now() - datetime.timedelta(minutes=x)).isoformat()} 
          for x in range(1000)]

client.insertValues(createdStream, values)
print "inserted {count} values".format(count = len(values))
print "Last value is {value}".format(value = client.getLastValue(createdStream))

#get the last few minutes of values
print "Recent values are {values}".format(values = 
        client.getWindowValues(createdStream, 
        (datetime.datetime.now() - datetime.timedelta(minutes = 100)).isoformat(), 
        datetime.datetime.now().isoformat()))

#delete stream
client.deleteStream(stream.Id)
print "deleted tangent"

listStreams()




print "If you made it this far, everything works!"