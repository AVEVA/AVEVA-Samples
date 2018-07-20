### Introduction
In this sample we show how to create, add and read data from a stream. We will deal with non unique time stamps and compound indexes.

This sample is an example of real time monitoring of performance counters in a windows system. Every few milliseconds we send the metric generated from the performance counter to Qi where it is stored. Finally we make queries directly to Qi to retrieve the data we stored.

### QiStream and Type

In this sample a stream is created for each Performance Counter Category. All the counters under a performance counter category share the same stream. Overall multiple streams are created to handle multiple performance counter category.

```csharp
     QiStream stream = new QiStream()
     {
        Id = categoryName,
        TypeId = type.Id,
        Description = categoryHelp,
      };
      QiStream createdStream = metadataService.GetOrCreateStreamAsync(stream)
                                              .GetAwaiter().GetResult();
```

A QiType named PerformanceEvent is defined in the sample. This defines the type of the data values being pushed into Qi.

```csharp
      QiTypeBuilder builder = new QiTypeBuilder();
      QiType type = builder.Create<PerformanceEvent>();
      type.Id = _typeId;
      type = metadataService.GetOrCreateTypeAsync(type)
                            .GetAwaiter().GetResult();
```

### Reading performance counter data and Writing to Qi

We read data out of multiple performance counters under the same performance counter category and batch them before pushing into Qi. The use of timers generates an event every few milliseconds which reads data from all the performance counters under a category, batches them up and writes to Qi. A separate timer object is used for each performance counter category.

```csharp
     foreach (PerformanceCounter counter in performanceCounters)
     {
         events.Add(new PerformanceEvent()
         {
	          Counter = counter.CounterName,
	          Instance = counter.InstanceName,
	          Time = time,
	          Value = counter.NextValue()
          });
      }
              
      await _dataService.InsertValuesAsync(category.Key, events);
```
### Reading events from Qi
We read the recent events pushed to Qi for a specific performance counter using filter expressions. As discussed above a stream receives events from multiple performance counters under a performance category. Using filter expressions we read back all the events associated with a single performance counter. 

```csharp		
   IEnumerable<PerformanceEvent> recentEvents = recentEvents = await      _dataService.GetValuesAsync<PerformanceEvent>(stream.Id, filter);
```
