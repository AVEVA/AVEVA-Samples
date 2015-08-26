# QiPy
Quick start:
```
import qipy as qi

qi.info()
channel = qi.channel("qi.osisoft.com:3380", "my api key")
channel.getTypes()
```

### What's missing from QiPy
The following APIs are not yet implemented in QiPy:

**Types** 
* `/qi/types` * GET, POST 
* `/qi/types/:type_id` * GET, PUT ,DELETE
 
**Behaviors** 
* `/qi/behaviors` * GET, POST
* `/qi/behaviors/:behavior_id` * GET, PUT, DELETE 	
 
**Streams**
* `/qi/streams` * GET, POST 
* `/qi/streams/:stream_id` * GET, PUT, DELETE
* `/qi/streams/:stream_id` * GET
 
**Data**
* `/qi/streams/:stream_id/data/getvalue` * GET
* `/qi/streams/:stream_id/data/getvalues` * GET
* `/qi/streams/:stream_id/data/createorgetvaluesrequest`  * PUT 
* `/qi/streams/:stream_id/data/createremovevaluesrequest` * PUT
* `/qi/streams/:stream_id/data/getdistinctvalue` * GET
* `/qi/streams/:stream_id/data/finddistinctvalue` * GET
* `/qi/streams/:stream_id/data/getfirstvalue` * GET
* `/qi/streams/:stream_id/data/getlastvalue` * GET
* `/qi/streams/:stream_id/data/getwindowvalues` * GET
* `/qi/streams/:stream_id/data/getrangevalues` * GET
* `/qi/streams/:stream_id/data/getintervals` * GET
* `/qi/streams/:stream_id/data/insertvalue` * POST
* `/qi/streams/:stream_id/data/insertvalues` * POST
* `/qi/streams/:stream_id/data/replacevalue` * PUT
* `/qi/streams/:stream_id/data/replacevalues` * PUT
* `/qi/streams/:stream_id/data/updatevalue` * PUT
* `/qi/streams/:stream_id/data/updatevalues` * PUT
* `/qi/streams/:stream_id/data/patchvalue` * PATCH
* `/qi/streams/:stream_id/data/patchvalues` * PATCH
* `/qi/streams/:stream_id/data/removevalue` * DELETE
* `/qi/streams/:stream_id/data/removevalues` * DELETE
* `/qi/streams/:stream_id/data/removewindowvalues` * DELETE 
 
**Batched data**
* `/qi/streams/data/insertvalues` * POST
* `/qi/streams/data/replacevalues` * PUT
* `/qi/streams/data/updatevalues` * PUT

**Subscriptions**
* `/qi/streams/:stream_id/subscriptions` * GET, POST
* `/qi/streams/:stream_id/subscriptions:subscription_id` * GET, DELETE 
 
 
 
 

