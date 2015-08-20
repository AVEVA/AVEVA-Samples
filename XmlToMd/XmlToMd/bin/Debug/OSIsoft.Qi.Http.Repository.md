
# OSIsoft.Qi.Http.Repository


## T:OSIsoft.Qi.Http.ErrorStrings

A strongly-typed resource class, for looking up localized strings, etc.


### P:OSIsoft.Qi.Http.ErrorStrings.BadContent

Looks up a localized string similar to The message content could not be processed by the server.


### P:OSIsoft.Qi.Http.ErrorStrings.BadParameter

Looks up a localized string similar to Bad parameter, {0}.


### P:OSIsoft.Qi.Http.ErrorStrings.BadParameterFormat

Looks up a localized string similar to Unexpected input parameter format.


### P:OSIsoft.Qi.Http.ErrorStrings.BehaviorIdConflict

Looks up a localized string similar to The stream behavior cannot be updated as the stream behavior id presented, {0}, does not match the id in the stream behavior object, {1}..


### P:OSIsoft.Qi.Http.ErrorStrings.Culture

Overrides the current thread's CurrentUICulture property for all resource lookups using this strongly typed resource class.


### P:OSIsoft.Qi.Http.ErrorStrings.Found

Looks up a localized string similar to A resource already exists at the specified index.


### P:OSIsoft.Qi.Http.ErrorStrings.NotFound

Looks up a localized string similar to Resource not found.


### P:OSIsoft.Qi.Http.ErrorStrings.ResourceManager

Returns the cached ResourceManager instance used by this class.


### P:OSIsoft.Qi.Http.ErrorStrings.StreamUpdateIdConflict

Looks up a localized string similar to Cannot update stream {0} as the udpated id, {1}, does not match..


### P:OSIsoft.Qi.Http.ErrorStrings.TenantInvalid

Looks up a localized string similar to The tenant in the request was not found..


### P:OSIsoft.Qi.Http.ErrorStrings.TypeExists

Looks up a localized string similar to Type with id = {0} exists in storage.


### P:OSIsoft.Qi.Http.ErrorStrings.Unknown

Looks up a localized string similar to Unexpected error.


## T:OSIsoft.Qi.Http.IQiMetadataIndexRepository

Interface to storing metadata indexes


## T:OSIsoft.Qi.Http.IQiMetadataRepository

Interface for Qi repository service


### M:OSIsoft.Qi.Http.IQiMetadataRepository.GetStreamBehaviorRepository

Retrieve the QiStreamBehavior repository interface


#### Returns

IRepository of stream behaviors


### M:OSIsoft.Qi.Http.IQiMetadataRepository.GetStreamRepository

Retrieve the Stream repository interface


#### Returns

IRepository of streams


### M:OSIsoft.Qi.Http.IQiMetadataRepository.GetStreamSubscriptionRepository

Retrieve the QiStreamBehavior repository interface


#### Returns

IRepository of stream behaviors


### M:OSIsoft.Qi.Http.IQiMetadataRepository.GetTypeRepository

Retrieve the Type repository interface


#### Returns

IRepository of types


## T:OSIsoft.Qi.Http.IQiStreamRepository

Interface to stream respository


### M:OSIsoft.Qi.Http.IQiStreamRepository.GetStreamProxy(key, callContext, proxy)



| Name | Description |
| ---- | ----------- |
| key | *System.String*<br> |
| callContext | *OSIsoft.Qi.IQiCallContext*<br> |
| proxy | *OSIsoft.Qi.Http.Repository.IQiStreamProxy@*<br> |


#### Returns




### M:OSIsoft.Qi.Http.IQiStreamRepository.GetStreamViewProxy(key, selectExpression, callContext, proxy)



| Name | Description |
| ---- | ----------- |
| key | *System.String*<br> |
| selectExpression | *System.String*<br> |
| callContext | *OSIsoft.Qi.IQiCallContext*<br> |
| proxy | *OSIsoft.Qi.Http.Repository.IQiStreamProxy@*<br> |


#### Returns




### M:OSIsoft.Qi.Http.IQiStreamRepository.RemoveStreamProxy(key, callContext)



| Name | Description |
| ---- | ----------- |
| key | *System.String*<br> |
| callContext | *OSIsoft.Qi.IQiCallContext*<br> |

### M:OSIsoft.Qi.Http.IQiStreamRepository.TryGetStreamProxy(key, callContext, lease, proxy)



| Name | Description |
| ---- | ----------- |
| key | *System.String*<br> |
| callContext | *OSIsoft.Qi.IQiCallContext*<br> |
| lease | *System.IDisposable@*<br> |
| proxy | *OSIsoft.Qi.Http.Repository.IQiStreamProxy@*<br> |


#### Returns




### M:OSIsoft.Qi.Http.IQiStreamRepository.TryGetStreamViewProxy(key, selectExpression, callContext, lease, proxy)



| Name | Description |
| ---- | ----------- |
| key | *System.String*<br> |
| selectExpression | *System.String*<br> |
| callContext | *OSIsoft.Qi.IQiCallContext*<br> |
| lease | *System.IDisposable@*<br> |
| proxy | *OSIsoft.Qi.Http.Repository.IQiStreamProxy@*<br> |


#### Returns




## T:OSIsoft.Qi.Http.QiDependencyResolver

Dependency resolver for Qi repositories


### M:OSIsoft.Qi.Http.QiDependencyResolver.#ctor(context, configuration)

Constructor

| Name | Description |
| ---- | ----------- |
| context | *OSIsoft.Qi.QiContext*<br> |
| configuration | *System.Web.Http.HttpConfiguration*<br> |

### M:OSIsoft.Qi.Http.QiDependencyResolver.BeginScope

Begin resolver scopt


#### Returns




### M:OSIsoft.Qi.Http.QiDependencyResolver.Dispose

Dispose the dependency resolver


### M:OSIsoft.Qi.Http.QiDependencyResolver.GetService(serviceType)

Get a resovled service

| Name | Description |
| ---- | ----------- |
| serviceType | *System.Type*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiDependencyResolver.GetServices(serviceType)

Get a collection of services

| Name | Description |
| ---- | ----------- |
| serviceType | *System.Type*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiDependencyResolver.LoadHelp

Load help controller


### M:OSIsoft.Qi.Http.QiDependencyResolver.RegisterController(System.Type,System.Func{OSIsoft.Qi.QiContext,System.Object})

Register a controller with the system

| Name | Description |
| ---- | ----------- |
| controllerType | *Unknown type*<br> |
| activator | *Unknown type*<br> |

## T:OSIsoft.Qi.Http.QiHttpMessageHandler

Http message handler for Qi repository services


### M:OSIsoft.Qi.Http.QiHttpMessageHandler.#ctor(context)

QiHttpMessageHandler constructor

| Name | Description |
| ---- | ----------- |
| context | *OSIsoft.Qi.QiContext*<br> |

### M:OSIsoft.Qi.Http.QiHttpMessageHandler.SendAsync(request, cancellationToken)

Implementation of the SendAsync method of DelegatingHandler class

| Name | Description |
| ---- | ----------- |
| request | *System.Net.Http.HttpRequestMessage*<br>Incoming Http request |
| cancellationToken | *System.Threading.CancellationToken*<br>Cancellation token for incoming call |


#### Returns




## T:OSIsoft.Qi.Http.QiTenantService

Repository for Qi tenants


### M:OSIsoft.Qi.Http.QiTenantService.#ctor(System.Collections.Generic.IDictionary{System.String,System.Object},OSIsoft.Qi.QiContext)

Constructor

| Name | Description |
| ---- | ----------- |
| settings | *Unknown type*<br> |
| context | *OSIsoft.Qi.QiContext*<br> |

### M:OSIsoft.Qi.Http.QiTenantService.Clear

Clears knowledge of all tenants and releases repositories


### M:OSIsoft.Qi.Http.QiTenantService.ContainsTenant(id)

Determines if a specific tenant definition exists

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>Tenant id |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.Dispose

Dispose


### M:OSIsoft.Qi.Http.QiTenantService.Dispose(disposing)

Dispose

| Name | Description |
| ---- | ----------- |
| disposing | *System.Boolean*<br> |

### M:OSIsoft.Qi.Http.QiTenantService.GetTenant(id)

Retreieve a specific Qi Tenant definition

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>The Qi Tenant id |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.GetTenantContext(id)

Retrieves a tenant's context

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>Tenant id |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.GetTenants

Retrieve all QiTenant definitions


#### Returns

IEnumberable of QiTenant objects


### M:OSIsoft.Qi.Http.QiTenantService.GetTenantService``1(id)

Return a tenant specific platform service

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.IsValidTenantId(id)

Determine if a given tenant id is valid

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>String representing tenant id |


#### Returns

True if the string is a valid tenant id


### M:OSIsoft.Qi.Http.QiTenantService.OnTenantCreated(callback)

Signup for tenant creation

| Name | Description |
| ---- | ----------- |
| callback | *System.Action{OSIsoft.Qi.Platform}*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.RemoveTenant(id)

Removes a tenant's definition given it's id

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>Tenant's id |

### M:OSIsoft.Qi.Http.QiTenantService.ResolveUnknownTenant(id)

Resolve an unknown tenant id

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiTenantService.UpdateTenant(id, tenant)

Updates a Qi tenant's definition

| Name | Description |
| ---- | ----------- |
| id | *System.String*<br>Tenant's id |
| tenant | *OSIsoft.Qi.QiTenant*<br>Tenant's definition |

## SystemInstrumentationController

Instrumentation controller


### M:OSIsoft.Qi.Http.Repository.GetCounts

Get count of metrics in groups


#### Returns

IEnumerable of container counts


### M:OSIsoft.Qi.Http.Repository.GetGroups

Get all metric container Ids


#### Returns

IEnumerable of container Ids


### M:OSIsoft.Qi.Http.Repository.GetValues(System.String)

Get count of metrics in groups


#### Returns

IEnumerable of container counts


### M:OSIsoft.Qi.Http.Repository.Ping

Get all metric container Ids


#### Returns

IEnumerable of container Ids


## TenantController

Data access methods for managing Qi tenant definitions


### M:OSIsoft.Qi.Http.Repository.DeleteTenant(tenantId)

Delete a Qi tenant definition

| Name | Description |
| ---- | ----------- |
| tenantId | *System.String*<br>Qi tenant Id |


#### Returns




### M:OSIsoft.Qi.Http.Repository.GetOrCreateTenant(definition)

Add a Qi Tenant definition

| Name | Description |
| ---- | ----------- |
| definition | *OSIsoft.Qi.QiTenant*<br>Qi Tenant definition |


#### Returns

Qi Tenant definition


### M:OSIsoft.Qi.Http.Repository.GetTenant(tenantId)

Get a Qi tenant definition

| Name | Description |
| ---- | ----------- |
| tenantId | *System.String*<br>Qi tenant Id |


#### Returns

Qi Tenant definition


### M:OSIsoft.Qi.Http.Repository.GetTenants

Get all Qi tenant definitions


#### Returns

INumerable of Qi tenant definitions


### M:OSIsoft.Qi.Http.Repository.UpdateTenant(tenantId, definition)

Update a Qi Tenant definition

| Name | Description |
| ---- | ----------- |
| tenantId | *System.String*<br>Qi Tenant Id |
| definition | *OSIsoft.Qi.QiTenant*<br>Qi Tenant definition |


#### Returns




## TenantDiagnosticsController

Diagnostics endpoint for Qi server


### M:OSIsoft.Qi.Http.Repository.GetState(streamId)

Select a set of values from a Qi data stream.

| Name | Description |
| ---- | ----------- |
| streamId | *System.String*<br>Qi stream name |


#### Returns

data values


## TenantInstrumentationController

Instrumentation controller


### M:OSIsoft.Qi.Http.Repository.GetCounts

Get count of metrics in groups


#### Returns

IEnumerable of container counts


### M:OSIsoft.Qi.Http.Repository.GetGroups

Get all metric container Ids


#### Returns

IEnumerable of container Ids


### M:OSIsoft.Qi.Http.Repository.GetValues(System.String)

Get count of metrics in groups


#### Returns

IEnumerable of container counts


### M:OSIsoft.Qi.Http.Repository.Ping

Get all metric container Ids


#### Returns

IEnumerable of container Ids


## T:OSIsoft.Qi.HttpConfigurationExtensions

Http Configuration extensions


### M:OSIsoft.Qi.HttpConfigurationExtensions.EnableDocumentation(config)

Enable the help system

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br> |

## T:OSIsoft.Qi.PlatformExtensions

Qi Platform extension methods


### M:OSIsoft.Qi.PlatformExtensions.RegisterQiTenantService(platform)

Register in-memory system repository

| Name | Description |
| ---- | ----------- |
| platform | *OSIsoft.Qi.Platform*<br> |
