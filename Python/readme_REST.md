#Python samples: Building a client to make REST API calls to Qi service.

This sample demonstrates how Qi REST APIs are invoked.

## Creating a connection

The sample uses *httplib* module to connect a service endpoint. A new connection is opened as follows:

```python
	conn = httplib.HTTPConnection(url-name)
```

* url-name	:	service endpoint (Ex: "localhost:12345")

## Creating a QiType

Qi is capable of storing any data type you care to define.  Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.

A Qi type has the following properties:

```python
        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
        self.__Properties = []
```

The QiType "Id" is the identifier for a particular type. "Name" is string property for user understanding. "Description" is again a string that describes the QiType. "QiTypeCode" is used to identify store what kind of datatypes the QiType stores. The file *QiTypeCode.py* has the list of datatypes that can be stored in the Qi.

A QiType can have multiple properties, which are again QiTypes with the exception that they describe only a single datatype and do not contain multiple properties. Atleast one of the QiType has to be a key, determined by a boolean value, which is used to index the values to be stored. For example, datetimeProperty can be used as key in order store data across a period of time. Qi allows the use of non-time indices, and also permits compound indices.

From QiTypeProperty.py:
```python
    def __init__(self):
            self.__Id = ""
            self.__Name = None
            self.__Description = None
            self.__QiType = None
            self.__IsKey = False
```            	

A Qi type can be created by a POST request as follows:

```python
	conn.request("POST", "/Qi/Types/", QiType, 
						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

* tenantId	:	Tenant ID of the customer (Every REST call must have a header with a tenant ID)
* Returns the QiType object created in a json format
* If a QiType with the same Id exists, url path of the existing QiType is returned

## Creating a Qi Stream

Anything in your process that you wish to measure is a stream in Qi, like a point or tag in the classic Pi Archive.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream.  This is the code to create a stream named `evtStream` for recording events of our sample type.  The value of the `TypeId` property is the value of the QiType `Id` property.