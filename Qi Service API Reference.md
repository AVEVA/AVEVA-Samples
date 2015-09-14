#Overview

This reference is a complete guide to the client reference API of the Qi Service.  We provide both the .NET Qi Libraries methods and the REST API.  Please refer to the readme docs within the language-specific folders for examples.

Each participant was allocated a tenant to represent their organization prior to the start of testing.  Each tenant is a self-contained entity within the Qi Service and may define the following entities:

* Type -- user defined structure denoting a single measured event or object for storage
* Stream -- basic unit of storage consisting of an ordered series of objects conforming to a type definition
* Stream Beahvior -- defines whether interpolation occurs during event retrieval, and if so, how

# Type

Qi is capable of storing any data type you care to define.  A Qi Type consists of one or more properties.  Properties are either simple atomic types (e.g., integer) or previously-defined Qi Types.  The latter permits the construction of complex, nested types. The only requirement is that your data type have one or more properties that constitute an ordered key.  While a timestamp is a very common type of key, any ordered value is permitted. 

## Naming Rules for typeId
1.	Case sensitive
2.	Allows spaces

## Type Methods

*GetStreamType*
```c#
QiType GetStreamType(string streamId);
Task<QiType> GetStreamTypeAsync(string streamId);
```
*Parameters*

`streamId` -- id of the stream associated with a type

Returns the type definition associated with a stream


*GetType*
```c#
QiType GetType(string typeId);
Task<QiType> GetTypeAsync(string typeId);
```

*Parameters*
```typeId``` -- id of the type to retrieve

Returns type searched for by typeId

*GetTypes*
```c#
IEnumerable<QiType> GetTypes();
Task<IEnumerable<QiType>> GetTypesAsync();
```

Returns IEnumerable of all types for the tenant. 


*GetOrCreateType*
```c#
QiType GetOrCreateType(QiType entity);
Task<QiType> GetOrCreateTypeAsync(QiType entity);
```

*Parameters*
`entity` -- Qi Type object

Returns a Qi Type object. If entity already exists on the server by Id, that existing type is returned to the caller unchanged.  Otherwise, a new type definition is added to the Qi Service for use by that tenant.

*UpdateType*
```c#
void UpdateType(string typeId, QiType entity);
Task UpdateTypeAsync(string typeId, QiType entity);
```
This call is not allowed at this time.

*DeleteType*
```c#
void DeleteType(string typeId);
Task DeleteTypeAsync(string typeId);
```

*Parameters*
`typeId` -- string type id of the type to delete

Deletes type from server.. 


# Stream

Streams are the fundamental unit of storage in the Qi Service.  Each stream represents an ordered series of events or observations for a particular item of interest, e.g., the temperature of a given room.  Each stream must have a Qi Type associated with it, and each event sent to the stream must conform to this type or it will be rejected.  Streams may optionally have a Stream Behavior to control how data is returned.

## Qi Stream Object

```c#  
  string Id
  string Name
  string Description
  string TypeId
  string BehaviorId
```

A Qi Stream object must include:
•	an ‘Id’ field (unique)
•	a ‘TypeId’ field with the Id of an existing Type.

## Naming Rules for Stream Identifiers
1.	Case sensitive
2.	Allows spaces.

## Stream Methods
*GetStream*
```c#
QiStream GetStream(string streamId);
Task<QiStream> GetStreamAsync (string streamId);
```

*Parameters*
`streamId` -- string identifying the stream

Returns a QiStream object.

*GetStreams*
```c#
IEnumerable<QiStream> GetStreams ();
Task<IEnumerable<QiStream>> GetStreamsAsync ();
```

Returns IEnumerable of all streams for the tenant. 

*GetOrCreateStream*
```c#
QiStream GetOrCreateStream (QiStream entity);
Task<QiStream> GetOrCreateStreamAsync (QiStream entity);
```

*Parameters*

`entity` -- Qi Stream object
  
If BehaviorId is not specified, the stream will have the default behavior of Mode=‘Continuous’ and Extrapolation=‘All’. If entity already exists on the server by Id, that existing stream is returned to the caller unchanged.

*UpdateStream*
```c#
void UpdateStream(string streamId, QiStream entity);
Task UpdateStreamAsync(string streamId, QiStream entity);
```

*Parameters*

`streamId` -- identifier of the stream to modify
`entity` -- updated stream object

Permitted changes:
•	Name
•	BehaviorId
•	Description

Throws exception on unpermitted change attempt (and stream is left unchanged).
UpdateStream method will apply the entire entity. Optional fields left out of the entity will remove the field from the Stream if they had been set previously in the stream. 

*DeleteStream*
```c#
void DeleteStream(string streamId);
Task DeleteStreamAsync(string streamId);
```

*Parameters*

`streamId` -- identifier of the stream to delete

Delete stream using its stream id.

# Stream Behavior 

The Stream Behavior is applied to a stream and effects how certain data read operations will be performed. The Stream Behavior must first be defined and then can be applied to the stream when it is created (GetOrCreateStream method) or updated (UpdateStream method). Stream Behavior is always referenced with its Id.

The Stream Behavior can be changed between reads to change how the read acts. The Stream could also be set to use a different Stream Behavior.

The default behavior for a stream (when a defined Stream Behavior is not applied to the stream) is Mode = ‘Continuous’ and Extrapolation = ‘All’. 

## Stream Behavior Object

Stream Behavior Object
        QiStreamExtrapolation ExtrapolationMode
        string Id
        QiStreamMode Mode { get; set; }
        string Name
        IList<QiStreamBehaviorOverride> Overrides 
Id -- unique identifier used to reference this behavior
Name -- Optional descriptor.
Mode -- behavior setting to be applied to all ‘value’ parameters in the Type of Stream to which this is applied

`QiStreamMode` is an enumeration whose permissible values are:
1.	Continuous			
2.	StepwiseContinuousLeading
3.	StepwiseContinuousTrailing
4.	Discrete

`QiStreamBehaviorOverride` object
QiStreamMode Mode
string QiTypePropertyId

## Naming Rules for Behavior Identifiers
1.	Case sensitive
2.	Allows spaces.
   
## Stream Behavior Methods

*DeleteBehavior*
```c#
void DeleteBehavior(string behaviorId);
Task DeleteBehaviorAsync(string behaviorId);
```
*Parameters*
`behaviorId` -- id of the behavior to delete; the behavior must not be associated with any streams

Deletes behavior from server.

*GetBehavior*
```c#
QiStreamBehavior GetBehavior(string behaviorId);
Task<QiStreamBehavior> GetBehaviorAsync(string behaviorId);
```

*Parameters*
`behaviorId` -- id of the behavior definition to retrieve

Gets a behavior object from server.

*GetBehaviors*
```c#
IEnumerable<QiStreamBehavior> GetBehaviors();
Task<IEnumerable<QiStreamBehavior>> GetBehaviorsAsync();
```

Returns IEnumerable of all behaviors for the tenant.

*GetOrCreateBehavior*
```c#
QiStreamBehavior GetOrCreateBehavior(QiStreamBehavior entity);
Task<QiStreamBehavior> GetOrCreateBehaviorAsync(QiStreamBehavior entity);
```
*Parameters*
`entity` -- a QiStream object to add to the Qi Service for the current tenant.  
Creates a StreamBehavior (or returns it if it already exists). 

If `entity` already exists on the server by `Id`, that existing behavior is returned to the caller unchanged.

*UpdateBehavior*
```c#
void UpdateBehavior(string behaviorId, QiStreamBehavior entity);
Task UpdateBehaviorAsync(string behaviorId, QiStreamBehavior entity);
```

*Parameters*

`behaviorId` -- identifier of the stream behavior to update
`entity` -- updated stream behavior 

Permitted changes: 
•	Override list
•	BehaviorMode
•	ExtrapolationMode
•	Name

An override list can be added to add, remove or change the override Mode on parameters within the type. 
UpdateBehavior replaces the stream’s existing behavior with entity.  If certain aspects of the existing behavior are meant to remain, they must be included in entity.

This is a list of parameters from the `Type` (`QiTypePropertyId`) that are to be given different behaviors (`Mode`).  Each parameter.

The overrides list is used in cases where the user desires the stream to have different behaviors for different values in the stream events. 

`Extrapolation`
QiStreamExtrapolation can have one of 4 values.
1.	All
2.	None
3.	Forward
4.	Backward
This indicates whether indexes that are read before or after all data should attempt to return an event or not.

# Data Retrieval Methods

*FindDistinctValue*
```c#
T FindDistinctValue<T>(string streamId, string index, QiSearchMode mode);
Task<T> FindDistinctValueAsync<T>(string streamId, string index, QiSearchMode mode);
```

*Parameters*
`streamId` -- stream against which to perform retrieval
`index` -- value of the index at which to retrieve a value (e.g., a DateTime if the stream's Type is indexed by a DateTime property)
`mode` -- search mode enumeration indicating how to find the event

Search modes
1.	Exact 
2.	ExactOrNext 
3.	ExactOrPrevious 
4.	Next 
5.	Previous

This method is used in situations where the client software needs to query a stream without getting any exceptions when the indexes queried do not have data.

Returns null values for calls that do not find a value (e.g. Search of ‘Next’ from an index after all existing data.)

*GetDistinctValue* 
```c#
T GetDistinctValue<T>(string streamId, string index);
Task<T> GetDistinctValueAsync<T>(string streamId, string index);
```
*Parameters*
`streamId` -- id of the stream to search
`index` -- index value on which to search


This method is used by a client when data is specifically expected to reside at the index used. 
Returns event from the specified stream at the specified index. Throws exception if no event exists at index, or if the stream has no data.

*GetFirstValue* 
```c#
T GetFirstValue<T>(string streamId);
Task<T> GetFirstValueAsync<T>(string streamId);
```

*Parameters*
`streamId` -- identifier of the stream to search

Gets the first data event in the stream. If the stream has no data – a ‘null’ is returned (no exception thrown)

*GetLastValue* 
```c#
T GetLastValue<T>(string streamId);
Task<T> GetLastValueAsync<T>(string streamId);
```

*Parameters*
`streamId` -- stream identifier

Gets the last data event in the stream. If the stream has no data – a ‘null’ is returned (no exception thrown)

*GetIntervals*
```c#
IEnumerable<QiInterval<T>> GetIntervals<T>(string streamId, string startIndex, string endIndex, int count);
Task<IEnumerable<QiInterval<T>>> GetIntervalsAsync<T>(string streamId, string startIndex, string endIndex, int count);
```

*Parameters*
`streamId` -- identifier of the stream to search
`startIndex` -- string representation of the index starting value
`endIndex` -- string representation of the index ending value
`count` -- number of intervals

The call accepts a start and end value and the count of intervals. Intervals are created by dividing the time range into equal parts. The start and end index values will use an ‘ExactOrCalculated’ search so every intervals will typically have 2 (or more) values with which to work.

A QiInterval is made up of a start and end event and a List of Summaries.
IDictionary<string, IDictionary<QiSummaryType, object>> Summaries
T End
T Start

A Summaries object corresponds to the fields within the the type for which calculations were made. For example, if a Type was created with a DateTime TimeId property as an index, and two double values and a string value, then a GetIntervals call would include 2 Summaries (one for each of the double elements).

Summaries are made up of the following list of calculations:
Facets show the following 13 calculations for the field for the Interval.
1.	Minimum		(also shows Index where the first instance if this occurred)	
2.	Maximum		(also shows Index where this first instance if this occurred)
3.	Range
4.	Total
5.	Mean
6.	StandardDeviation
7.	PopulationStandardDeviation
8.	Skewness
9.	Kurtosis
10.	WeightedMean
11.	WeightedStandardDeviation
12.	WeightedPopulationStandardDeviation
13.	Integral

*GetRangeValues*
```c#
IEnumerable<T> GetRangeValues<T>(string streamId, string startIndex, int count);
IEnumerable<T> GetRangeValues<T>(string streamId, string startIndex, int count, bool reversed);
IEnumerable<T> GetRangeValues<T>(string streamId, string startIndex, int count, QiBoundaryType boundaryType);
IEnumerable<T> GetRangeValues<T>(string streamId, string startIndex, int skip, int count, bool reversed, 
IEnumerable<T> GetRangeValuesAsync<T>(string streamId, string startIndex, int skip, int count, bool reversed, QiBoundaryType boundaryType, string filterExpression);
Task<IEnumerable<T>> GetRangeValuesAsync<T>(string streamId, string startIndex, int count);
Task<IEnumerable<T>> GetRangeValuesAsync<T>(string streamId, string startIndex, int count, bool reversed);
Task<IEnumerable<T>> GetRangeValuesAsync<T>(string streamId, string startIndex, int count, QiBoundaryType boundaryType);
Task<IEnumerable<T>> GetRangeValuesAsync<T>(string streamId, string startIndex, int skip, int count, bool reversed, QiBoundaryType boundaryType);
Task<IEnumerable<T>> GetRangeValuesAsync<T>(string streamId, string startIndex, int skip, int count, bool reversed, QiBoundaryType boundaryType, string filterExpression);

*Parameters*
`streamId` -- identifier of the stream to search
`startIndex` -- string representation of the start value of the stream's index property
`count` -- number of events to return
`reversed` -- true to return events in reverse order
`skip` -- **clarification needed**
`boundaryType` -- enumeration indicating how to handle events on the boundaries
`filterExpression` -- string containing an ODATA filter expression (see below)

This call is used to obtain events from a stream where a start point is provided and the number of events desired. The many overloads allow the client to indicate where to start, which direction to search, whether to skip any values and also allows a special filter to be applied to the events found.

*QiBoundaryType Behavior*
For FORWARD (default) calls:
*Exact will find the first event at or after the index  
8ExactOrCalculated if the index is on an event, that event is used. Otherwise the Behavior and Extrapolation mode determine whether a value is ‘calculated’ for the index used. The result will either be no event or an event with the index used in the call and the value of the next event in the stream. 
*Inside will find the first event after the index  
*Outside will find the first event before the index  

For REVERSE calls.
*Exact will find the first event at or before the index  
*ExactOrCalculated if the index is on an event, that event is used. Otherwise the Behavior and Extrapolation mode determine whether a value is ‘calculated’ for the index used. The result will either be no event or an event with the index used in the call and the value of the previous event in the stream. 
*Inside will find the first event before the index  
*Outside will find the first event after the index  

Once the ‘start’ event is determined, then any filter is applied to determine possible values (in the direction requested) that could be returned. Next the Skip is applied and finally the number of events (up to count) is returned.
Filter uses OData query language. Most of the query language is supported.
	
*GetValue* and *GetValues*
```c#
T GetValue<T>(string streamId, string index);
Task<T> GetValueAsync<T>(string streamId, string index);

IEnumerable<T> GetValues<T>(string streamId, IEnumerable<string> index);
IEnumerable<T> GetValues<T>(string streamId, string startIndex, string endIndex, int count);
Task<IEnumerable<T>> GetValuesAsync<T>(string streamId, IEnumerable<string> index);
```

*Parameters*
`streamId` -- id denoting the stream to search
`index` -- value of an index into the stream type's index property.
`startIndex` -- start index value
`endIndex` -- end index value
`count` -- number of events to return

If the specified index is before any events, the value returned is determined by stream Behavior Mode and Extrapolation setting. By default (‘Continuous’ Mode and ‘Both’ Extrapolation), the first event value is returned with the index of the call.

If the specified index is after all events, the value returned is determined by stream Behavior Mode and Extrapolation setting. By default (Continous Mode and Both Extrapolation), the last event value is returned with the index of the call. 

If the specified index is between events, the value returned is determined by stream Behavior Mode (and any overrides).

If no data in stream – returns NULL (regardless of stream behavior setting)

GetValues can generally be thought of as multiple GetValue calls.
If no data in stream – returns array of NULLs (one for each member in requested list).

*GetWindowValues*
```c#
IEnumerable<T> GetWindowValues<T>(string streamId, string startIndex, string endIndex);
IEnumerable<T> GetWindowValues<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType);
IEnumerable<T> GetWindowValues<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, string filterExpression);
IEnumerable<T> GetWindowValues<T>(string streamId, string startIndex, QiBoundaryType startBoundaryType, string endIndex, QiBoundaryType endBoundaryType, string filterExpression);
QiResultPage<T> GetWindowValues<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, int count, string continuationToken);
IEnumerable<T> GetWindowValues<T>(string streamId, string startIndex, QiBoundaryType startBoundaryType, string endIndex, QiBoundaryType endBoundaryType, string filterExpression, string selectExpression);
QiResultPage<T> GetWindowValues<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, string filterExpression, int count, string continuationToken);
Task<IEnumerable<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, string endIndex);
Task<IEnumerable<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType);
Task<IEnumerable<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, string filterExpression);
Task<IEnumerable<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, QiBoundaryType startBoundaryType, string endIndex, QiBoundaryType endBoundaryType, string filterExpression);
Task<QiResultPage<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, int count, string continuationToken);
Task<IEnumerable<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, QiBoundaryType startBoundaryType, string endIndex, QiBoundaryType endBoundaryType, string filterExpression, string selectExpression);
Task<QiResultPage<T>> GetWindowValuesAsync<T>(string streamId, string startIndex, string endIndex, QiBoundaryType boundaryType, string filterExpression, int count, string continuationToken);
```

*Parameters*
`streamId` -- id of stream to search
`startIndex` -- string representation of the start index value of the range
`endIndex` -- string representation of the end index value of the range
`boundaryType` -- enumeration describing how to handle events near boundaries
`filterExpression` -- ODATA filter expression
`count` -- number of events to return
`continuationToken` -- continuation token for handling multiple return data sets
`startBoundaryType` -- how to handle events near the start of the range
`endBoundaryType` -- how to handle events near the end of the range
`selectExpression` -- **needs clarification**

These methods are used to obtain data between 2 indices.

Start index must be less than end index.
BoundaryCondition is ‘Exact’ unless otherwise set 

BoundaryConditions:
Exact: return values exactly on the start or end index value
Inside: any value inside the range but not including the boundaries
Outside: includes 1 value outside the boundary on both sides and any values at or inside the range
ExactOrCalculated: Will create values for the endpoints given if value at Exact index not found. Behavior for given value is used in calculation (Continuous is default)

Calls against an empty stream will always return a single null regardless of boundary type used. 

Filter uses OData queries. Please see the section on Filter Text at the end of this document.

Select Expression **clarification needed**

*InsertValue*
```c#
void InsertValue<T>(string streamId, T item);
Task InsertValueAsync<T>(string streamId, T item);
```

*Parameters*
`streamId` -- identifier of the stream into which to insert a value
`item` -- event to insert, where T is the type of the event and the stream
Inserts an item into the specified stream. Will throw an exception if the index of item already has an event. 

*InsertValues*
```c#
void InsertValues<T>(string streamId, IList<T> items);
Task InsertValuesAsync<T>(string streamId, IList<T> items);
```

*Parameters*
`streamId` -- identifier of the stream into which to insert values
`items` -- list of items of type T

Inserts items into the specified stream. Will throw an exception if any index in items already has an event. If any individual index has a problem, the entire list of events is rolled back and no inserts at all are done. The index that caused the issue can be determined in the error response.

*PatchValue*
```c#
void PatchValue(string streamId, string selectExpression, T item);
Task PatchValueAsync(string streamId, string selectExpression, T item);
```

*Parameters*
`streamId` -- identifier of the stream to update
`selectExpression` -- expression selecting events for patching
`item` -- object of the same type, T, as the property to patch

Patches a value at the index noted by T item using the value denoted by selectExpression and T item from the specified stream, e.g. 
```c#
var obj = new { TimeId = DateTime.UtcNow(), Value = 10 };
PatchValue(“someStreamId”, “Value”, obj);
```

*PatchValues* 
```c#
void PatchValues(string streamId, string selectExpression, IList<T> items);
Task PatchValuesAsync(string streamId, string selectExpression, IList<T> items);
```

*Parameters*

`streamId` -- identifier of the stream on which to operate
`selectExpression` -- ODATA expression for selecting values to patch
`items` -- list of properties to patch

Patches the values at the indexes denoted by the list of T items using the value denoted by selectExpression and the item from the specified stream. Rolls back all patches back to their original state if any of them fail.
**needs clarification**

*RemoveValue*
```c#
void RemoveValue(string streamId, string index);
Task RemoveValueAsync(string streamId, string index);
```

*Parameters*
`streamId` -- identifier of the stream on which to operate
`index` -- index of the value to remove

Removes the value at index from the specified stream. Precision can matter when finding a value. If index is a DateTime, use the round-trip format given by `.ToString(“o”)`.

*RemoveValues*
```c#
void RemoveValues(string streamId, IEnumerable<string> index);
Task RemoveValuesAsync(string streamId, IEnumerable<string> index);
```

*Parameters*
`streamId` -- identifier of the stream from which to remove values
`index` -- list of indices at which to remove values

Removes the value at each index from the specified stream. If any individual index has a problem, the enter list of attempted RemoveValues is rolled back and no removes are done.  The index that caused the issue can be determined in the error response.

*RemoveWindowValues*
```c#
void RemoveWindowValues(string streamId, string startIndex, string endIndex);
Task RemoveWindowValuesAsync(string streamId, string startIndex, string endIndex);
```

*Parameters*

`streamId` -- identifier of the stream from which to remove values
`startIndex` -- string representation of the starting index of the range
`endIndex` -- string representation of the ending index of the range

Removes a range of values at and between the indices given.

*ReplaceValue* 
```c#
void ReplaceValue<T>(string streamId, T item);
Task ReplaceValueAsync<T>(string streamId, T item);
```

*Parameters*

`streamId` -- identifier of the stream in which to replace value
`item` -- item to replace existing value

Writes an item over an existing value in the specified stream. Throws an exception if the stream does not have an event at the index to be replaced.

*ReplaceValues*
```c#
void ReplaceValues<T>(string streamId, IList<T> items);
Task ReplaceValuesAsync<T>(string streamId, IList<T> items);
```

*Parameters*
`streamId` -- identifier of the stream in which to replace values
`items` -- list of new items to replace existing items in the stream

Writes items over existing values in the specified stream. Throws an exception if any index does not have a value to be replaced.

If any individual index has a problem doing replace, the enter list of attempted replacements is rolled back and no replaces at all are done. The index that caused the issue can be determined in the error response.

*UpdateValue* 
```c#
void UpdateValue<T>(string streamId, T item);
Task UpdateValueAsync<T>(string streamId, T item);
```

*Parameters*
`streamId` -- identifier of the stream in which to update a value
`item` -- new value to replace an existing value

Writes item to specified stream.  Will insert at any index that does not have a value and will replace if the index already has a value. 

*UpdateValues*
```c#
void UpdateValues<T>(string streamId, IList<T> items);
Task UpdateValuesAsync<T>(string streamId, IList<T> items);
```

*Parameters*

`streamId` -- identifier of the stream in which to perform updates
`items` -- list of new items to replace existing items

Writes items to specified stream.   Will insert or replace. If any individual index has a problem, the enter set of attempted UpdateValues is rolled back (no updates at all are done). The index that caused the issue can also be determined in the error response.

#
