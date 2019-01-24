### Introduction
In this sample we show how to create, add and read data from a stream. We will deal with non unique time stamps and compound indexes.

This sample is an example of real time monitoring of performance counters in a windows system. Every few milliseconds we send the metric generated from the performance counter to SDS where it is stored. Finally we make queries directly to SDS to retrieve the data we stored.

### SdsStream and Type

In this sample a stream is created for each Performance Counter Category. All the counters under a performance counter category share the same stream. Overall multiple streams are created to handle multiple performance counter category.

```csharp
     SDSStream stream = new SdsStream()
     {
        Id = categoryName,
        TypeId = type.Id,
        Description = categoryHelp,
      };
      SDSStream createdStream = metadataService.GetOrCreateStreamAsync(stream)
                                              .GetAwaiter().GetResult();
```


### Reading performance counter data and Writing to SDS

We read data out of multiple performance counters under the same performance counter category and batch them before pushing into SDS. The use of timers generates an event every few milliseconds which reads data from all the performance counters under a category, batches them up and writes to SDS. A separate timer object is used for each performance counter category.

### Reading events from SDS
We read the recent events pushed to SDS for a specific performance counter. As discussed above a stream receives events from multiple performance counters under a performance category. 
