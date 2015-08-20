
# OSIsoft.Qi.Http.MetadataRepository


## T:OSIsoft.Qi.Http.Repository.BehaviorController

Data access methods for managing Qi stream behavior definitions


### M:OSIsoft.Qi.Http.Repository.BehaviorController.DeleteStreamBehavior(behaviorId)

Delete a Qi stream behavior definition

| Name | Description |
| ---- | ----------- |
| behaviorId | *System.String*<br>Qi stream behavior Id |


#### Returns




### M:OSIsoft.Qi.Http.Repository.BehaviorController.GetOrCreateStreamBehavior(definition)

Add a Qi stream behavior definition

| Name | Description |
| ---- | ----------- |
| definition | *OSIsoft.Qi.QiStreamBehavior*<br>Qi stream behavior definition |


#### Returns

Qi stream behavior definition


### M:OSIsoft.Qi.Http.Repository.BehaviorController.GetStreamBehavior(behaviorId)

Get a Qi stream behavior definition

| Name | Description |
| ---- | ----------- |
| behaviorId | *System.String*<br>Qi stream behavior Id |


#### Returns

Qi stream behavior definition


### M:OSIsoft.Qi.Http.Repository.BehaviorController.GetStreamBehaviors

Get all Qi stream behavior definitions


#### Returns

IEnumerable of Qi stream behavior definitions


### M:OSIsoft.Qi.Http.Repository.BehaviorController.UpdateStreamBehavior(behaviorId, definition)

Update a Qi Stream Behavior definition

| Name | Description |
| ---- | ----------- |
| behaviorId | *System.String*<br>Qi stream behavior Id |
| definition | *OSIsoft.Qi.QiStreamBehavior*<br>Qi stream behavior definition |


#### Returns




## T:OSIsoft.Qi.Http.Repository.StreamController

Data access methods for managing Qi streams definitions


### M:OSIsoft.Qi.Http.Repository.StreamController.DeleteStream(streamId)

Delete a Qi stream definition

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The Qi stream name |


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamController.GetOrCreateStream(definition)

Add a Qi stream definition

| Name | Description |
| ---- | ----------- |
| definition | *OSIsoft.Qi.QiStream*<br>Qi stream definition |


#### Returns

Qi stream definition


### M:OSIsoft.Qi.Http.Repository.StreamController.GetStream(streamId)

Get a Qi stream definition

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The Qi stream name |


#### Returns

Qi stream definition


### M:OSIsoft.Qi.Http.Repository.StreamController.GetStreams

Get all Qi stream definitions


#### Returns




### M:OSIsoft.Qi.Http.Repository.StreamController.UpdateStream(streamId, definition)

Update a Qi stream definition

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>The Qi stream name |
| definition | *OSIsoft.Qi.QiStream*<br>Qi stream definition |


#### Returns




### M:OSIsoft.Qi.Http.Repository.SubscriptionController.DeleteStreamSubscription(System.String,System.String)

Delete a Qi stream subscription definition

| Name | Description |
| ---- | ----------- |
| subscriptionId | *Unknown type*<br>Qi stream subscription Id |


#### Returns




### M:OSIsoft.Qi.Http.Repository.SubscriptionController.GetOrCreateStreamSubscription(System.String,OSIsoft.Qi.QiStreamSubscription)

Add a Qi stream subscriber definition

| Name | Description |
| ---- | ----------- |
| definition | *OSIsoft.Qi.QiStream*<br>Qi stream subscriber definition |


#### Returns

Qi stream subscriber definition


### M:OSIsoft.Qi.Http.Repository.SubscriptionController.GetStreamSubscription(System.String,System.String)

Get a Qi stream subscription definition

| Name | Description |
| ---- | ----------- |
| subscriptionId | *Unknown type*<br>Qi stream subscription Id |


#### Returns

Qi stream subscription definition


### M:OSIsoft.Qi.Http.Repository.SubscriptionController.GetStreamSubscriptions(System.String)

Get all Qi stream subscription definitions


#### Returns

IEnumerable of Qi stream subscription definitions


## T:OSIsoft.Qi.Http.Repository.TypeController

Data access methods for managing Qi type definitions


### M:OSIsoft.Qi.Http.Repository.TypeController.DeleteType(typeId)

Delete a Qi type definition

| Name | Description |
| ---- | ----------- |
| typeId | *System.String*<br>Qi type Id |


#### Returns




### M:OSIsoft.Qi.Http.Repository.TypeController.GetOrCreateType(definition)

Add a Qi type definition

| Name | Description |
| ---- | ----------- |
| definition | *OSIsoft.Qi.QiType*<br>Qi type definition |


#### Returns

Qi type definition


### M:OSIsoft.Qi.Http.Repository.TypeController.GetType(typeId)

Get a Qi type definition

| Name | Description |
| ---- | ----------- |
| typeId | *System.String*<br>Qi type Id |


#### Returns

Qi type definition


### M:OSIsoft.Qi.Http.Repository.TypeController.GetTypes

Get all Qi type definitions


#### Returns

INumerable of Qi type definitions


### M:OSIsoft.Qi.Http.Repository.TypeController.UpdateType(typeId, definition)

Update a Qi type definition

| Name | Description |
| ---- | ----------- |
| typeId | *System.String*<br>Qi type Id |
| definition | *OSIsoft.Qi.QiType*<br>Qi type definition |


#### Returns



