from qipy import *

# client = QiClient("historianmain.cloudapp.net:3380", "my api key")
client = QiClient("chad-dev:12345", "my api key")

#get types
types = client.getTypes()
print "{len} Qi types found.".format(len = len(types))
print ", ".join(t.Name for t in types)

#get Int64 type
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

#delete byte type
client.deleteType("byte")




print "If you made it this far, everything works!"