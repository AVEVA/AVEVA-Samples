
# OSIsoft.Qi.Http.Help


## Api

Class to produce the template output


### M:OSIsoft.Qi.Http.Help.TransformText

Create the template output


## ApiBase

Base class for this transformation


### M:OSIsoft.Qi.Http.Help.ClearIndent

Remove any indentation


### .CurrentIndent

Gets the current indent we use when adding lines to the output


### M:OSIsoft.Qi.Http.Help.Error(System.String)

Raise an error


### .Errors

The error collection for the generation process


### .GenerationEnvironment

The string builder that generation-time code is using to assemble generated output


### .indentLengths

A list of the lengths of each indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PopIndent

Remove the last indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PushIndent(System.String)

Increase the indent


### .Session

Current transformation session


### .ToStringHelper

Helper to produce culture-oriented representation of an object as a string


## ApiBase.ToStringInstanceHelper

Utility class to produce culture-oriented representation of an object as a string.


### .FormatProvider

Gets or sets format provider to be used by ToStringWithCulture method.


### M:OSIsoft.Qi.Http.Help.ToStringWithCulture(System.Object)

This is called from the compile/run appdomain to convert objects within an expression block to a string


### M:OSIsoft.Qi.Http.Help.ApiBase.Warning(System.String)

Raise a warning


### M:OSIsoft.Qi.Http.Help.ApiBase.Write(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.ApiBase.Write(System.String,System.Object[])

Write formatted text directly into the generated output


### M:OSIsoft.Qi.Http.Help.ApiBase.WriteLine(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.ApiBase.WriteLine(System.String,System.Object[])

Write formatted text directly into the generated output


### M:OSIsoft.Qi.Http.Help.ApiDescriptionExtensions.GetFriendlyId(description)

Generates an URI-friendly ID for the . E.g. "Get-Values-id_name" instead of "GetValues/{id}?name={name}"

| Name | Description |
| ---- | ----------- |
| description | *System.Web.Http.Description.ApiDescription*<br>The . |


#### Returns

The ID as a string.


## ApiModel

The model that represents an API displayed on the help page.


### M:OSIsoft.Qi.Http.Help.#ctor

Initializes a new instance of the class.


### .ApiDescription

Gets or sets the that describes the API.


### .ErrorMessages

Gets the error messages associated with this model.


### .SampleRequests

Gets the sample requests associated with the API.


### .SampleResponses

Gets the sample responses associated with the API.


## HelpPageSampleGenerator

This class will generate the samples for the help page.


### M:OSIsoft.Qi.Http.Help.#ctor

Initializes a new instance of the class.


### .ActionSamples

Gets the objects that are used directly as samples for certain actions.


### .ActualHttpMessageTypes

Gets CLR types that are used as the content of or .


### M:OSIsoft.Qi.Http.Help.GetActionSample(controllerName, actionName, parameterNames, type, formatter, mediaType, sampleDirection)

Search for samples that are provided directly through .

| Name | Description |
| ---- | ----------- |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.Collections.Generic.IEnumerable{System.String}*<br>The parameter names. |
| type | *System.Type*<br>The CLR type. |
| formatter | *System.Net.Http.Formatting.MediaTypeFormatter*<br>The formatter. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| sampleDirection | *OSIsoft.Qi.Http.Help.SampleDirection*<br>The value indicating whether the sample is for a request or for a response. |


#### Returns

The sample that matches the parameters.


### M:OSIsoft.Qi.Http.Help.GetSample(api, sampleDirection)

Gets the request or response body samples.

| Name | Description |
| ---- | ----------- |
| api | *System.Web.Http.Description.ApiDescription*<br>The . |
| sampleDirection | *OSIsoft.Qi.Http.Help.SampleDirection*<br>The value indicating whether the sample is for a request or for a response. |


#### Returns

The samples keyed by media type.


### M:OSIsoft.Qi.Http.Help.GetSampleObject(type)

Gets the sample object that will be serialized by the formatters. First, it will look at the . If no sample object is found, it will try to create one using .

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br>The type. |


#### Returns

The sample object.


### M:OSIsoft.Qi.Http.Help.GetSampleRequests(api)

Gets the request body samples for a given .

| Name | Description |
| ---- | ----------- |
| api | *System.Web.Http.Description.ApiDescription*<br>The . |


#### Returns

The samples keyed by media type.


### M:OSIsoft.Qi.Http.Help.GetSampleResponses(api)

Gets the response body samples for a given .

| Name | Description |
| ---- | ----------- |
| api | *System.Web.Http.Description.ApiDescription*<br>The . |


#### Returns

The samples keyed by media type.


### M:OSIsoft.Qi.Http.Help.ResolveType(api, controllerName, actionName, parameterNames, sampleDirection, formatters)

Resolves the type of the action parameter or return value when or is used.

| Name | Description |
| ---- | ----------- |
| api | *System.Web.Http.Description.ApiDescription*<br>The . |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.Collections.Generic.IEnumerable{System.String}*<br>The parameter names. |
| sampleDirection | *OSIsoft.Qi.Http.Help.SampleDirection*<br>The value indicating whether the sample is for a request or a response. |
| formatters | *System.Collections.ObjectModel.Collection{System.Net.Http.Formatting.MediaTypeFormatter}@*<br>The formatters. |

### .SampleObjects

Gets the objects that are serialized as samples by the supported formatters.


### M:OSIsoft.Qi.Http.Help.WriteSampleObjectUsingFormatter(formatter, value, type, mediaType)

Writes the sample object using formatter.

| Name | Description |
| ---- | ----------- |
| formatter | *System.Net.Http.Formatting.MediaTypeFormatter*<br>The formatter. |
| value | *System.Object*<br>The value. |
| type | *System.Type*<br>The type. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>Type of the media. |


#### Returns




## HelpPageSampleKey

This is used to identify the place where the sample should be applied.


### M:OSIsoft.Qi.Http.Help.#ctor(sampleDirection, controllerName, actionName, parameterNames)

Creates a new based on , controller name, action name and parameter names.

| Name | Description |
| ---- | ----------- |
| sampleDirection | *OSIsoft.Qi.Http.Help.SampleDirection*<br>The . |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.Collections.Generic.IEnumerable{System.String}*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.#ctor(mediaType, sampleDirection, controllerName, actionName, parameterNames)

Creates a new based on media type, , controller name, action name and parameter names.

| Name | Description |
| ---- | ----------- |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| sampleDirection | *OSIsoft.Qi.Http.Help.SampleDirection*<br>The . |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.Collections.Generic.IEnumerable{System.String}*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.#ctor(mediaType, type)

Creates a new based on media type and CLR type.

| Name | Description |
| ---- | ----------- |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| type | *System.Type*<br>The CLR type. |

### .ActionName

Gets the name of the action.


### .ControllerName

Gets the name of the controller.


### .MediaType

Gets the media type.


### .ParameterNames

Gets the parameter names.


### .SampleDirection

Gets the .


### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.GetHelpPageSampleGenerator(config)

Gets the help page sample generator.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |


#### Returns

The help page sample generator.


### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetActualRequestType(config, type, controllerName, actionName)

Specifies the actual type of passed to the in an action. The help page will use this information to produce more accurate request samples.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| type | *System.Type*<br>The type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetActualRequestType(config, type, controllerName, actionName, parameterNames)

Specifies the actual type of passed to the in an action. The help page will use this information to produce more accurate request samples.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| type | *System.Type*<br>The type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.String[]*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetActualResponseType(config, type, controllerName, actionName)

Specifies the actual type of returned as part of the in an action. The help page will use this information to produce more accurate response samples.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| type | *System.Type*<br>The type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetActualResponseType(config, type, controllerName, actionName, parameterNames)

Specifies the actual type of returned as part of the in an action. The help page will use this information to produce more accurate response samples.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| type | *System.Type*<br>The type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.String[]*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetHelpPageSampleGenerator(config, sampleGenerator)

Sets the help page sample generator.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sampleGenerator | *OSIsoft.Qi.Http.Help.HelpPageSampleGenerator*<br>The help page sample generator. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleForType(config, sample, mediaType, type)

Sets the sample directly for all actions with the specified type and media type.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sample | *System.Object*<br>The sample. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| type | *System.Type*<br>The parameter type or return type of an action. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleObjects(System.Web.Http.HttpConfiguration,System.Collections.Generic.IDictionary{System.Type,System.Object})

Sets the objects that will be used by the formatters to produce sample requests/responses.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sampleObjects | *Unknown type*<br>The sample objects. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleRequest(config, sample, mediaType, controllerName, actionName)

Sets the sample request directly for the specified media type and action.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sample | *System.Object*<br>The sample request. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleRequest(config, sample, mediaType, controllerName, actionName, parameterNames)

Sets the sample request directly for the specified media type and action with parameters.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sample | *System.Object*<br>The sample request. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.String[]*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleResponse(config, sample, mediaType, controllerName, actionName)

Sets the sample request directly for the specified media type of the action.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sample | *System.Object*<br>The sample response. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.SetSampleResponse(config, sample, mediaType, controllerName, actionName, parameterNames)

Sets the sample response directly for the specified media type of the action with specific parameters.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| sample | *System.Object*<br>The sample response. |
| mediaType | *System.Net.Http.Headers.MediaTypeHeaderValue*<br>The media type. |
| controllerName | *System.String*<br>Name of the controller. |
| actionName | *System.String*<br>Name of the action. |
| parameterNames | *System.String[]*<br>The parameter names. |

### M:OSIsoft.Qi.Http.Help.HttpConfigurationExtensions.UseDocumentation(System.Web.Http.HttpConfiguration,System.String,System.String)

Sets the documentation provider for help page.

| Name | Description |
| ---- | ----------- |
| config | *System.Web.Http.HttpConfiguration*<br>The . |
| documentationProvider | *Unknown type*<br>The documentation provider. |

## ImageSample

This represents an image sample on the help page. There's a display template named ImageSample associated with this class.


### M:OSIsoft.Qi.Http.Help.#ctor(src)

Initializes a new instance of the class.

| Name | Description |
| ---- | ----------- |
| src | *System.String*<br>The URL of an image. |

## Index

Class to produce the template output


### M:OSIsoft.Qi.Http.Help.TransformText

Create the template output


## IndexBase

Base class for this transformation


### M:OSIsoft.Qi.Http.Help.ClearIndent

Remove any indentation


### .CurrentIndent

Gets the current indent we use when adding lines to the output


### M:OSIsoft.Qi.Http.Help.Error(System.String)

Raise an error


### .Errors

The error collection for the generation process


### .GenerationEnvironment

The string builder that generation-time code is using to assemble generated output


### .indentLengths

A list of the lengths of each indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PopIndent

Remove the last indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PushIndent(System.String)

Increase the indent


### .Session

Current transformation session


### .ToStringHelper

Helper to produce culture-oriented representation of an object as a string


## IndexBase.ToStringInstanceHelper

Utility class to produce culture-oriented representation of an object as a string.


### .FormatProvider

Gets or sets format provider to be used by ToStringWithCulture method.


### M:OSIsoft.Qi.Http.Help.ToStringWithCulture(System.Object)

This is called from the compile/run appdomain to convert objects within an expression block to a string


### M:OSIsoft.Qi.Http.Help.IndexBase.Warning(System.String)

Raise a warning


### M:OSIsoft.Qi.Http.Help.IndexBase.Write(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.IndexBase.Write(System.String,System.Object[])

Write formatted text directly into the generated output


### M:OSIsoft.Qi.Http.Help.IndexBase.WriteLine(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.IndexBase.WriteLine(System.String,System.Object[])

Write formatted text directly into the generated output


## InvalidSample

This represents an invalid sample on the help page. There's a display template named InvalidSample associated with this class.


## ObjectGenerator

This class will create an object of a given type and populate it with sample data.


### M:OSIsoft.Qi.Http.Help.GenerateObject(type)

Generates an object for a given type. The type needs to be public, have a public default constructor and settable public properties/fields. Currently it supports the following types: Simple types: , , , , , etc. Complex types: POCO types. Nullables: . Arrays: arrays of simple types or complex types. Key value pairs: Tuples: , , etc Dictionaries: or anything deriving from . Collections: , , , , , or anything deriving from or . Queryables: , .

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br>The type. |


#### Returns

An object of the given type.


## SampleDirection

Indicates whether the sample is used for request or response


## TextSample

This represents a preformatted text sample on the help page. There's a display template named TextSample associated with this class.


## Wadl

Class to produce the template output


### M:OSIsoft.Qi.Http.Help.TransformText

Create the template output


## WadlBase

Base class for this transformation


### M:OSIsoft.Qi.Http.Help.ClearIndent

Remove any indentation


### .CurrentIndent

Gets the current indent we use when adding lines to the output


### M:OSIsoft.Qi.Http.Help.Error(System.String)

Raise an error


### .Errors

The error collection for the generation process


### .GenerationEnvironment

The string builder that generation-time code is using to assemble generated output


### .indentLengths

A list of the lengths of each indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PopIndent

Remove the last indent that was added with PushIndent


### M:OSIsoft.Qi.Http.Help.PushIndent(System.String)

Increase the indent


### .Session

Current transformation session


### .ToStringHelper

Helper to produce culture-oriented representation of an object as a string


## WadlBase.ToStringInstanceHelper

Utility class to produce culture-oriented representation of an object as a string.


### .FormatProvider

Gets or sets format provider to be used by ToStringWithCulture method.


### M:OSIsoft.Qi.Http.Help.ToStringWithCulture(System.Object)

This is called from the compile/run appdomain to convert objects within an expression block to a string


### M:OSIsoft.Qi.Http.Help.WadlBase.Warning(System.String)

Raise a warning


### M:OSIsoft.Qi.Http.Help.WadlBase.Write(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.WadlBase.Write(System.String,System.Object[])

Write formatted text directly into the generated output


### M:OSIsoft.Qi.Http.Help.WadlBase.WriteLine(System.String)

Write text directly into the generated output


### M:OSIsoft.Qi.Http.Help.WadlBase.WriteLine(System.String,System.Object[])

Write formatted text directly into the generated output


## XmlDocumentationProvider

A custom that reads the API documentation from an XML documentation file.

