
# OSIsoft.Qi.Http.StreamRepository


## T:OSIsoft.Qi.Http.Repository.StreamDataController

Data access method for Qi data streams


### M:OSIsoft.Qi.Http.Repository.StreamDataController.CreateGetValuesRequest(streamId, index)

Select a set of values from a Qi data stream.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| index | *System.String[]*<br>An array of indexes to return a value for |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.CreateRemoveValuesRequest(streamId, index)

Removes a set of values in a qi data stream. If a value doesn't exist at a specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| index | *System.String[]*<br>An array of indexes to remove |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.FindDistinctValue(streamId, index, mode)

Find a single discrete value in a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The id of Qi stream |
| index | *System.String*<br>The index of the value to return |
| mode | *OSIsoft.Qi.QiSearchMode*<br>The search mode |


#### Returns

Return value


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetDistinctValue(streamId, index)

Returns a single discrete value from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The id of Qi stream |
| index | *System.String*<br>The index of the value to return |


#### Returns

Return value


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetFirstValue(streamId)

Get the first value in a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The id of Qi stream |


#### Returns

Return value


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetIntervals(streamId, startIndex, endIndex, count)

Select a set of values from a Qi data stream. A value will be returned for the start and end index and (count - 2) other values at evenly spaces intervals between the start and end.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| count | *System.Int32*<br>The number of values to return |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetIntervals(streamId, startIndex, endIndex, count, count)

Select a set of values from a Qi data stream. A value will be returned for the start and end index and (count - 2) other values at evenly spaces intervals between the start and end.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| count | *System.String*<br>The number of values to return |
| count | *System.String*<br>A filter to apply to stream before creating aggregates |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetLastValue(streamId)

Get the last value in a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The id of Qi stream |


#### Returns

Return value


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetRangeValues(streamId, startIndex, count)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| count | *System.Int32*<br>The maximum number of values to return |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetRangeValues(streamId, startIndex, count, boundaryType)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| count | *System.Int32*<br>The maximum number of values to return |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>boundary condition for the start index |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetRangeValues(streamId, startIndex, count, reversed)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| count | *System.Int32*<br>The maximum number of values to return |
| reversed | *System.Boolean*<br>true to reverse the order of retrieval |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetRangeValues(streamId, startIndex, skip, count, reversed, boundaryType)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| skip | *System.Int32*<br>The number of events to skip before returning values |
| count | *System.Int32*<br>The maximum number of values to return |
| reversed | *System.Boolean*<br>true to reverse the order of retrieval |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>boundary condition for the start index |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetRangeValues(streamId, startIndex, skip, count, reversed, boundaryType, filterExpression)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| skip | *System.Int32*<br>The number of events to skip before returning values |
| count | *System.Int32*<br>The maximum number of values to return |
| reversed | *System.Boolean*<br>true to reverse the order of retrieval |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>boundary condition for the start index |
| filterExpression | *System.String*<br>Filter expression |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetType(streamId)

Get a type for a Qi stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns

Qi type definition


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetValue(streamId, index)

Returns a single value from a Qi data stream according to the configured stream behavior

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The id of the Qi stream |
| index | *System.String*<br>The index of the value to return |


#### Returns

Return value


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetValues(streamId, filterExpression)

Select a set of values from a Qi data stream.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| filterExpression | *System.String*<br>An array of indexes to return a value for |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetValues(streamId, startIndex, endIndex, count)

Select a set of values from a Qi data stream. A value will be returned for the start and end index and (count - 2) other values at evenly spaces intervals between the start and end.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| count | *System.Int32*<br>The number of values to return |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetValues(streamId, index)

Select a set of values from a Qi data stream.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| index | *System.String[]*<br>An array of indexes to return a value for |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, startBoundaryType, endIndex, endBoundaryType, filterExpression)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| startBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Start boundary condition for range |
| endIndex | *System.String*<br>Qi data stream value index end value |
| endBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>End boundary condition for range |
| filterExpression | *System.String*<br>Filter expression |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, startBoundaryType, endIndex, endBoundaryType, filterExpression, count, continuationToken)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| startBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Start boundary condition for range |
| endIndex | *System.String*<br>Qi data stream value index end value |
| endBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>End boundary condition for range |
| filterExpression | *System.String*<br>Filter expression |
| count | *System.Int32*<br>Boundary condition for range |
| continuationToken | *System.String*<br>Boundary condition for range |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, startBoundaryType, endIndex, endBoundaryType, filterExpression, selectExpression)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| startBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Start boundary condition for range |
| endIndex | *System.String*<br>Qi data stream value index end value |
| endBoundaryType | *OSIsoft.Qi.QiBoundaryType*<br>End boundary condition for range |
| filterExpression | *System.String*<br>Filter expression |
| selectExpression | *System.String*<br>Filter expression |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, endIndex)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, endIndex, boundaryType)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Boundary condition for range |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, endIndex, boundaryType, count, continuationToken)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Boundary condition for range |
| count | *System.Int32*<br>Boundary condition for range |
| continuationToken | *System.String*<br>Boundary condition for range |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, endIndex, boundaryType, filterExpression)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Boundary condition for range |
| filterExpression | *System.String*<br>Filter expression |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.GetWindowValues(streamId, startIndex, endIndex, boundaryType, filterExpression, count, continuationToken)

Select multiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |
| boundaryType | *OSIsoft.Qi.QiBoundaryType*<br>Boundary condition for range |
| filterExpression | *System.String*<br>Filter expression |
| count | *System.Int32*<br>Boundary condition for range |
| continuationToken | *System.String*<br>Boundary condition for range |


#### Returns

data values


### M:OSIsoft.Qi.Http.Repository.StreamDataController.InsertValue(streamId)

Add a value to a qi data stream. If the a value already exists at the specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.InsertValues

Adds a set of values to a set of qi data streams. If the a value already exists at a specified index an error is returned.


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.InsertValues(streamId)

Adds a set of values to a qi data stream. If the a value already exists at a specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.PatchValue(System.String,System.String)

Update a value in a qi data stream. If a value doesn't exist at the specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.PatchValues(System.String,System.String)

Update a set of values in a qi data stream. If a value doesn't exist at a specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.RemoveValue(streamId, index)

Remove a single value from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| index | *System.String*<br>Qi data stream index value |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.RemoveValues(streamId, index)

Removes a set of values in a qi data stream. If a value doesn't exist at a specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| index | *System.String[]*<br>An array of indexes to remove |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.RemoveWindowValues(streamId, startIndex, endIndex)

Remove mutiple values from a Qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |
| startIndex | *System.String*<br>Qi data stream value index start value |
| endIndex | *System.String*<br>Qi data stream value index end value |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.ReplaceValue(streamId)

Update a value in a qi data stream. If a value doesn't exist at the specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.ReplaceValues

Update a set of values in a set of qi data streams. If a value doesn't exist at a specified index an error is returned.


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.ReplaceValues(streamId)

Update a set of values in a qi data stream. If a value doesn't exist at a specified index an error is returned.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.UpdateValue(streamId)

Add or update a value in a qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.UpdateValues

Add or update multiple values in a set of qi data streams.


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamDataController.UpdateValues(streamId)

Add or update multiple values in a qi data stream

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns



