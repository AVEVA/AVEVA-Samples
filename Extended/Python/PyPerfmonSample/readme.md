### Introduction
The purpose of this sample is to demonstrate proper Sequential Data Store (SDS) Type and Stream design using real-world measurements.

This sample is an example of real-time monitoring of performance counters and is agnostic of OS. In the final example, for 30 seconds (at intervals of 5 seconds), we send the metric generated from the performance counter to SDS where it is stored. Finally we make queries directly to Sds to retrieve the data we stored.

###Dependencies
Using pip installer, download the following modules
* adal
* psutil

### SDS Stream and Type
An SdsType named 'event_type' is defined in the sample. This defines the type of the data values being pushed into SDS.

```python
event_type = SdsType()
event_type.Id = type_id
event_type.Name = type_id
event_type.Description = "This is a sample Sds type for storing {}Data events".format(type_id)
event_type.SdsTypeCode = SdsTypeCode.Object
event_type.Properties = []

int_type = SdsType()
int_type.Id = 'intType'
int_type.SdsTypeCode = SdsTypeCode.Int64

date_time_type = SdsType()
date_time_type.Id = 'dateTimeType'
date_time_type.SdsTypeCode = SdsTypeCode.DateTime

string_type = SdsType()
string_type.Id = 'stringType'
string_type.SdsTypeCode = SdsTypeCode.String

# time_prop is the primary key
time_prop = SdsTypeProperty()
time_prop.Id = 'Time'
time_prop.SdsType = date_time_type
time_prop.IsKey = True
event_type.Properties.append(time_prop)
)
```

In this sample, a SDS Type is created for every performance counter category.  If multiple instances of the same category exist, a separate stream should be created for each subsequent instance.


```python
stream = SdsStream(stream_id=stream_id, name=name,
                           description="A Stream to store '{}' events".format(type_name),
                           type_id=event_type.Id)
```
### Reading events from SDS
We read the recent events pushed to Sds for a specific performance counter using filter expressions. As discussed above a stream receives events from multiple performance counters under a performance category. 

```python
events = self.client.get_window_values(self.namespaceId,
                                       stream_id,
                                       SdsTypeData,
                                       str(time_key_start),
                                       end=str(time_key_end)	
```
