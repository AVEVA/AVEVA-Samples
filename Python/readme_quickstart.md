# QiPy
Quick start:
```
from qipy import *
import datetime

client = QiClient("localhost:12345", "my api key")
types = client.getTypes()

stream = QiStream()
stream.Id = "tangent"
stream.Name = "Tangent"
stream.Description = "More interesting than sinusoid!"
stream.TypeId = "Double"
createdStream = client.createStream(stream)

value = {
    "TimeId" : datetime.datetime.now().isoformat(),
    "Value": 100.001
    }
client.insertValue(createdStream, value)
```
Complete source code for QiPy and test app can be found here: [OSIsoft GitHub](https://github.com/osisoft/Qi-Samples/tree/master/Python/QiPy)

### What's missing from QiPy
The following APIs are not yet implemented in QiPy:

#### Behaviors
* `/qi/behaviors`  GET, POST
* `/qi/behaviors/:behavior_id`  GET, PUT, DELETE 	
 
#### Data
* `/qi/streams/:stream_id/data/createorgetvaluesrequest`   PUT 
* `/qi/streams/:stream_id/data/createremovevaluesrequest`  PUT
* `/qi/streams/:stream_id/data/getdistinctvalue`  GET
* `/qi/streams/:stream_id/data/finddistinctvalue`  GET
* `/qi/streams/:stream_id/data/getfirstvalue`  GET
* `/qi/streams/:stream_id/data/getrangevalues`  GET
* `/qi/streams/:stream_id/data/getintervals`  GET
* `/qi/streams/:stream_id/data/replacevalues`  PUT
* `/qi/streams/:stream_id/data/updatevalues`  PUT
* `/qi/streams/:stream_id/data/patchvalue`  PATCH
* `/qi/streams/:stream_id/data/patchvalues`  PATCH
* `/qi/streams/:stream_id/data/removevalues`  DELETE
* `/qi/streams/:stream_id/data/removewindowvalues`  DELETE 
 
#### Batched data
* `/qi/streams/data/insertvalues`  POST
* `/qi/streams/data/replacevalues`  PUT
* `/qi/streams/data/updatevalues`  PUT

 
 
 
