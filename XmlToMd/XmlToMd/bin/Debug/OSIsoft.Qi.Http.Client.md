
# OSIsoft.Qi.Http.Client


### M:OSIsoft.Qi.Http.Client.QiEnumerable`1.#ctor(OSIsoft.Qi.Http.Client.QiEnumerableProviderBase)

This constructor is called by the client to create the data source.


### M:OSIsoft.Qi.Http.Client.QiEnumerable`1.#ctor(OSIsoft.Qi.Http.Client.QiEnumerableProviderBase,System.Linq.Expressions.Expression)

This constructor is called by Provider.CreateQuery().

| Name | Description |
| ---- | ----------- |
| expression | *Unknown type*<br> |

### M:OSIsoft.Qi.Http.Client.QiEnumerableProviderBase.CreateQuery``1(expression)

Queryable's collection-returning standard query operators call this method.

| Name | Description |
| ---- | ----------- |
| expression | *System.Linq.Expressions.Expression*<br> |


#### Returns




### M:OSIsoft.Qi.Http.Client.QiEnumerableProviderBase.Execute``1(expression)

Queryable's "single value" standard query operators call this method. It is also called from TauQueryable.GetEnumerator().

| Name | Description |
| ---- | ----------- |
| expression | *System.Linq.Expressions.Expression*<br> |


#### Returns




## T:OSIsoft.Qi.Http.QiMediaTypeFormatter

Media Formatter


### M:OSIsoft.Qi.Http.QiMediaTypeFormatter.#ctor(OSIsoft.Qi.QiContext)

Constructor


### M:OSIsoft.Qi.Http.QiMediaTypeFormatter.CanReadType(type)

Can the type be read

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiMediaTypeFormatter.CanWriteType(type)

Can the type be written

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiMediaTypeFormatter.ReadFromStreamAsync(type, readStream, content, formatterLogger)

Create the type from the stream

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br> |
| readStream | *System.IO.Stream*<br> |
| content | *System.Net.Http.HttpContent*<br> |
| formatterLogger | *System.Net.Http.Formatting.IFormatterLogger*<br> |


#### Returns




### M:OSIsoft.Qi.Http.QiMediaTypeFormatter.WriteToStreamAsync(type, value, writeStream, content, transportContext)

Write a typed instance to a stream

| Name | Description |
| ---- | ----------- |
| type | *System.Type*<br> |
| value | *System.Object*<br> |
| writeStream | *System.IO.Stream*<br> |
| content | *System.Net.Http.HttpContent*<br> |
| transportContext | *System.Net.TransportContext*<br> |


#### Returns



