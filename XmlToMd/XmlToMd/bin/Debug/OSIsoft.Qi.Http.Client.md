System.Collections.Generic.KeyNotFoundException: The given key was not present in the dictionary.
   at System.Collections.Generic.Dictionary`2.get_Item(TKey key)
   at GithubWikiDoc.XmlToMarkdown.ToMarkDown(XNode e) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 109
   at GithubWikiDoc.XmlToMarkdown.<>c.<ToMarkDown>b__1_0(String current, XNode x) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 130
   at System.Linq.Enumerable.Aggregate[TSource,TAccumulate](IEnumerable`1 source, TAccumulate seed, Func`3 func)
   at GithubWikiDoc.XmlToMarkdown.ToMarkDown(IEnumerable`1 es) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 130
   at GithubWikiDoc.XmlToMarkdown.<>c.<ToMarkDown>b__0_0(String att, XElement node) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 60
   at GithubWikiDoc.XmlToMarkdown.<>c__DisplayClass0_0.<ToMarkDown>b__5(XElement x) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 74
   at GithubWikiDoc.XmlToMarkdown.ToMarkDown(XNode e) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 109
   at GithubWikiDoc.XmlToMarkdown.<>c.<ToMarkDown>b__1_0(String current, XNode x) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 130
   at System.Linq.Enumerable.Aggregate[TSource,TAccumulate](IEnumerable`1 source, TAccumulate seed, Func`3 func)
   at GithubWikiDoc.XmlToMarkdown.ToMarkDown(IEnumerable`1 es) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 130
   at GithubWikiDoc.XmlToMarkdown.<>c.<ToMarkDown>b__0_1(XElement x) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 67
   at GithubWikiDoc.XmlToMarkdown.ToMarkDown(XNode e) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 109
   at GithubWikiDoc.Program.<>c.<Main>b__0_0(String file) in C:\dev\Qi-docs-md\XmlToMd\XmlToMd\Program.cs:line 25
<?xml version="1.0"?>
<doc>
    <assembly>
        <name>OSIsoft.Qi.Http.Client</name>
    </assembly>
    <members>
        <member name="T:OSIsoft.Qi.Http.QiMediaTypeFormatter">
            <summary>
            Media Formatter
            </summary>
        </member>
        <member name="M:OSIsoft.Qi.Http.QiMediaTypeFormatter.#ctor(OSIsoft.Qi.QiContext)">
            <summary>
            Constructor
            </summary>
        </member>
        <member name="M:OSIsoft.Qi.Http.QiMediaTypeFormatter.CanReadType(System.Type)">
            <summary>
            Can the type be read
            </summary>
            <param name="type"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.QiMediaTypeFormatter.CanWriteType(System.Type)">
            <summary>
             Can the type be written
            </summary>
            <param name="type"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.QiMediaTypeFormatter.ReadFromStreamAsync(System.Type,System.IO.Stream,System.Net.Http.HttpContent,System.Net.Http.Formatting.IFormatterLogger)">
            <summary>
            Create the type from the stream
            </summary>
            <param name="type"></param>
            <param name="readStream"></param>
            <param name="content"></param>
            <param name="formatterLogger"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.QiMediaTypeFormatter.WriteToStreamAsync(System.Type,System.Object,System.IO.Stream,System.Net.Http.HttpContent,System.Net.TransportContext)">
            <summary>
            Write a typed instance to a stream
            </summary>
            <param name="type"></param>
            <param name="value"></param>
            <param name="writeStream"></param>
            <param name="content"></param>
            <param name="transportContext"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.Client.QiEnumerableProviderBase.CreateQuery``1(System.Linq.Expressions.Expression)">
            <summary>
            Queryable's collection-returning standard query operators call this method.
            </summary>
            <typeparam name="TResult"></typeparam>
            <param name="expression"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.Client.QiEnumerableProviderBase.Execute``1(System.Linq.Expressions.Expression)">
            <summary>
            Queryable's "single value" standard query operators call this method.
            It is also called from TauQueryable.GetEnumerator().
            </summary>
            <typeparam name="TResult"></typeparam>
            <param name="expression"></param>
            <returns></returns>
        </member>
        <member name="M:OSIsoft.Qi.Http.Client.QiEnumerable`1.#ctor(OSIsoft.Qi.Http.Client.QiEnumerableProviderBase)">
            <summary>
            This constructor is called by the client to create the data source.
            </summary>
        </member>
        <member name="M:OSIsoft.Qi.Http.Client.QiEnumerable`1.#ctor(OSIsoft.Qi.Http.Client.QiEnumerableProviderBase,System.Linq.Expressions.Expression)">
            <summary>
            This constructor is called by Provider.CreateQuery().
            </summary>
            <param name="expression"></param>
        </member>
    </members>
</doc>
