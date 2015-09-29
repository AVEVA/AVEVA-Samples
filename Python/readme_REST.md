#Python Samples: Building a Client to make REST API Calls to the Qi Service.

This sample demonstrates how Qi REST APIs are invoked using python.

## Creating a connection

The sample uses *httplib* module to connect a service endpoint. A new connection is opened as follows:

```python
	conn = httplib.HTTPConnection(url-name)
```

* url-name is the service endpoint (Ex: "localhost:12345").

## Creating a Qi type

Qi is capable of storing any data type you care to define.  Each data stream is associated with a Qi type, so that only events conforming to that type can be inserted into the stream.  The first step in Qi programming, then, is to define the types for your tenant.

A Qi type has the following properties:

```python
        self.__Id = ""
        self.__Name = None
        self.__Description = None
        self.__QiTypeCode = self.__qiTypeCodeMap[QiTypeCode.Object]
        self.__Properties = []
```

The Qi type "Id" is the identifier for a particular type. "Name" is string property for user understanding. "Description" is again a string that describes the Qi type. "QiTypeCode" is used to identify what kind of datatypes the Qi type stores. The file *QiTypeCode.py* has a list of datatypes that can be stored in the Qi.

A Qi types can have multiple properties, which are again Qi types with the exception that they describe only a single datatype and do not contain multiple properties. Atleast one of the Qi type has to be a key, determined by a boolean value, which is used to index the values to be stored. For example, time can be used as key in order store time based data. Qi allows the use of non-time indices, and also permits compound indices.

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
	conn.request("POST", "/qi/types/", QiType, 
						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

* tenant_id	:	Tenant ID of the customer (Every REST call must have a header with a tenant ID)
* Returns the QiType object in a json format
* If a Qi type with the same Id exists, url path of the existing Qi type is returned
* QiType object is passed in json format


## Creating a Qi Stream

Anything in your process that you wish to measure is a stream in Qi, like a point or tag in a chart.  All you have to do is create a local QiStream instance, give it an id, assign it a type, and submit it to the Qi Service.  You may optionally assign a stream behavior to the stream. The value of the `TypeId` property is the value of the Qi type `Id` property.

```python
    def __init__(self):
        self.__Id = 0
        self.__Name = None
        self.__Description = None
        self.__TypeId = None
```

QiStream can be created by a POST request as follows:

```python
conn.request("POST", "/qi/streams/", QiStream, 
						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

* QiStream object is passed in json format

## Create and Insert Events into the Stream

A single event is a data point in the Stream. An event object cannot be emtpy and should have atleast the key value of the Qi type for the event. Events are passed in json format.

An event can be created using following POST request:

```python
conn.request("POST", "/qi/streams/" + qi_Stream.Id + , "/data/insertvalue", 
						payload,
						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

* qi_Stream.Id is the stream ID
* payload is the event object in json format

Inserting multiple values is similar, but the payload has list of events and the url for POST call varies

```python
conn.request("POST", "/qi/streams/" + qi_Stream.Id + , "/data/insertvalues", 
						payload,
						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

## Retrieve Events

There are many methods that allow for the retrieval of events from a stream.  This sample demonstrates the most basic method of retrieving all the events on a particular time range. In general, the index values must be of the same type as the index assigned in the Qi type.  Compound indices' values are concatenated with a pipe ('|') separator.

```python
 conn.request("GET", "/qi/streams/" + qi_stream.Id + "/data/GetWindowValues?" + params,
 						headers = {"QiTenant":"tenant_id",
						"Content-type":"application/json",
						"Accept": "text/plain"})
```

* params has the starting and ending key value of the window
		Ex: For a time index, params will be "endIndex=<*end_time*>&startIndex=<*start_time*>"

## Update Events

Updating events is hanlded by PUT REST call as follows:

```python
 conn.request("PUT", "/qi/streams/" + qi_stream.Id + "/data/replaceValue", 
                     payload,
                     headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```

* payload has the new value for the event correseponding to the key value that is to be updated

Updating multiple events is similar but the payload has an array of event objects and url for POST call varies

```python
 conn.request("PUT", "/qi/streams/" + qi_stream.Id + "/data/replaceValues", 
                     payload,
                     headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```

## Deleting Events

An event at a particular data point can be deleted by passing the *key* value for that data point to following DELETE REST call:

```python
 conn.request("DELETE", "/qi/streams/" + qi_stream.Id + "/data/removevalue?" + params, 
                     headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```

Delete can also be done over a window of key value as follows:

```python
 conn.request("DELETE", "/qi/streams/" + qi_stream.Id + "/data/removevalues?" + params, 
                     headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```

* params has the starting and ending key value of the window
			Ex: For a time index, params:endIndex=<*end_time*>&startIndex=<*start_time*>

## Bonus: Deleting Types and Streams

Deleting Streams and types can be achieved by a DELETE REST call and passing the corresponding ID

```python
 conn.request("DELETE", "/qi/streams/" + stream_id, 
 					headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```

```python
conn.request('DELETE', '/qi/types/' + type_id,
					headers = {"QiTenant":"tenant_id",
					"Content-type":"application/json",
					"Accept": "text/plain"})
```