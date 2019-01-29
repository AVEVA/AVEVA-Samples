// <copyright file="Program.cs" company="OSIsoft, LLC">
//
// Copyright (C) 2018-2019 OSIsoft, LLC. All rights reserved.
//
// THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
// OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
// THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
//
// RESTRICTED RIGHTS LEGEND
// Use, duplication, or disclosure by the Government is subject to restrictions
// as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
// Computer Software clause at DFARS 252.227.7013
//
// OSIsoft, LLC
// 1600 Alvarado St, San Leandro, CA 94577
// </copyright>

using Newtonsoft.Json;
using OSIsoft.Data;
using OSIsoft.Identity;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace PerfmonSample
{
    public class Program
    {
        static readonly string[] Categories = { "Processor", "Memory", "IPv6" };

        public static void Main(string[] args)
        {
            MainAsync().GetAwaiter().GetResult();
        }

        static async Task MainAsync()
        {
            string resourcePrefix = ConfigurationManager.AppSettings["ResourcePrefix"];
            string tenantId = ConfigurationManager.AppSettings["Tenant"];
            string namespaceId = ConfigurationManager.AppSettings["Namespace"];
            string resource = ConfigurationManager.AppSettings["Resource"];
            string clientId = ConfigurationManager.AppSettings["ClientId"];
            string clientKey = ConfigurationManager.AppSettings["ClientSecret"];

            // Acquire OSIsoft provided SDS clients w/ appropriate security delegating handler
            AuthenticationHandler ocsAuthenticationHandler = new AuthenticationHandler(resource, clientId, clientKey);
            SdsService service = new SdsService(new Uri(resource), ocsAuthenticationHandler);
            

            ISdsMetadataService config = service.GetMetadataService(tenantId, namespaceId);

            // Acquire an HTTP Client, including the Azure Active Directory client credential authentication handler 
            // and associated pipeline.
            //
            // The authentication Handler performs the same function as the SDS Security Handler above.  It acquires 
            // a token from the token service and attaches it as a header to every request sent out of the client.
            //
            // An HttpClient pipeline has to end with a handler that can send requests to appropriate endpoints.  
            // HttpClientHandler is that appropriate handler; it is the end of the client pipeline.  Note that we 
            // do not allow auto - reidrects.We do so because the HttpClientHandler, like many clients, strips security 
            // related headers on redirect.  This results in 401 - unauthorized status indicating that the request 
            // failed to authenticate.  We will manage redirects manually.
            //
            // We take some shortcuts with disposable objects.  Because the program ends quickly, we don't bother 
            // cleaning up disposables.
            ApplicationAuthenticationHandler authenticationHandler = new ApplicationAuthenticationHandler(resource, clientId, clientKey);
            HttpClient httpClient = new HttpClient(authenticationHandler)
            {
                BaseAddress = new Uri(resource)
            };

            try
            {
                // As we encounter performance counter categories, we will create a bunch of funcs to update individual events
                // If we were concerned aobut performance, we would cache events and update in bulk
                List<Func<Task>> updates = new List<Func<Task>>();

                foreach (string categoryName in Categories)
                {
                    PerformanceCounterCategory category = PerformanceCounterCategory.GetCategories()
                        .First(cat => cat.CategoryName == categoryName);

                    // Interrogate the category and create an SdsType based on the counters.  This 
                    // strategy will not work for categories with instances that have different 
                    // performance counters, like Process.  For those we would need a different strategy.
                    SdsType type = new SdsType()
                    {
                        Id = $"{resourcePrefix}{category.CategoryName}",
                        Name = $"{category.CategoryName}",
                        SdsTypeCode = SdsTypeCode.Object,
                        Properties = new List<SdsTypeProperty>()
                    };
                    type.Properties.Add(new SdsTypeProperty()
                    {
                        Id = "Time",
                        Name = "Time",
                        IsKey = true,
                        SdsType = new SdsType()
                        {
                            SdsTypeCode = SdsTypeCode.DateTime
                        }
                    });

                    PerformanceCounter[] counters;
                    switch (category.CategoryType)
                    {
                        case PerformanceCounterCategoryType.MultiInstance:
                            counters = category.GetCounters(category.GetInstanceNames().First());
                            break;
                        case PerformanceCounterCategoryType.SingleInstance:
                            counters = category.GetCounters();
                            break;
                        default:
                            throw new InvalidOperationException($"Invalid counter category type, {category.CategoryName}");
                    }

                    foreach (PerformanceCounter counter in counters)
                    {
                        // Note that the identifier name is cleaned.  Counters often use characters incompatible with SDS identifiers.
                        type.Properties.Add(new SdsTypeProperty()
                        {
                            Id = CleanIdentifier(counter.CounterName),
                            Name = counter.CounterName,
                            SdsType = new SdsType()
                            {
                                SdsTypeCode = SdsTypeCode.Int64
                            }
                        });
                    }

                    type = await config.GetOrCreateTypeAsync(type);

                    // Create a stream and an update func for each instance in the category
                    switch (category.CategoryType)
                    {
                        case PerformanceCounterCategoryType.MultiInstance:
                            foreach (string instanceName in category.GetInstanceNames())
                            {
                                SdsStream stream = new SdsStream()
                                {
                                    Id = $"{resourcePrefix}{category.CategoryName}-{instanceName}",
                                    Name = $"{category.CategoryName} {instanceName}",
                                    TypeId = type.Id
                                };
                                stream = await config.GetOrCreateStreamAsync(stream);

                                counters = category.GetCounters(instanceName);

                                updates.Add(GetUpdate(httpClient, counters, stream));
                            }
                            break;

                        case PerformanceCounterCategoryType.SingleInstance:
                            {
                                SdsStream stream = new SdsStream()
                                {
                                    Id = $"{category.CategoryName}",
                                    Name = $"{category.CategoryName}",
                                    TypeId = type.Id
                                };
                                stream = await config.GetOrCreateStreamAsync(stream);

                                counters = category.GetCounters();

                                updates.Add(GetUpdate(httpClient, counters, stream));
                            }
                            break;
                    }
                }

                DateTime start = DateTime.UtcNow;

                for (int i = 0; i < 10; i++)
                {
                    await Task.Delay(TimeSpan.FromSeconds(10));

                    List<Task> tasks = new List<Task>();
                    foreach (Func<Task> update in updates)
                        tasks.Add(update());
                    await Task.WhenAll(tasks);
                }

                DateTime end = DateTime.UtcNow;

                Console.WriteLine();

                foreach (string categoryName in Categories)
                {
                    PerformanceCounterCategory category = PerformanceCounterCategory.GetCategories()
                        .FirstOrDefault(cat => cat.CategoryName == categoryName);

                    foreach (string instanceName in category.GetInstanceNames())
                    {
                        string streamId = $"{category.CategoryName}-{instanceName}";

                        HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get,
                            $"Streams/{streamId}/Data/GetWindowValues?startIndex={start.ToString("o")}&endIndex={end.ToString("o")}");

                        HttpResponseMessage response = await httpClient.SendAsync(request);

                        if (response.IsSuccessStatusCode)
                        {
                            Console.WriteLine();
                            Console.WriteLine();
                            Console.WriteLine(streamId);
                            string json = await response.Content.ReadAsStringAsync();
                            Dictionary<string, string>[] values = JsonConvert.DeserializeObject<Dictionary<string, string>[]>(json);
                            foreach (Dictionary<string, string> value in values)
                            {
                                Console.Write("\t");
                                foreach (KeyValuePair<string, string> property in value)
                                    Console.Write($"{property.Key}:{property.Value}, ");
                                Console.WriteLine();
                            }
                        }
                        else
                        {
                            Console.WriteLine($"Failed retrieving data from {streamId}, {response.ReasonPhrase}:{response.StatusCode}");
                            if (response.Content != null && response.Content.Headers.ContentLength > 0)
                                Console.WriteLine(await response.Content.ReadAsStringAsync());
                        }
                    }
                }

                Console.WriteLine();
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
            finally
            {
                //TODO can we search for types
                IEnumerable<string> typeIds = from t in (await config.GetTypesAsync())
                                              where Categories.Any(cat => t.Id.StartsWith(cat))
                                              select t.Id;
                foreach (string typeId in typeIds)
                {
                    int offset = 0;

                    //TODO actually search for streams w/ the matching type
                    IEnumerable<SdsStream> streams = await config.GetStreamsAsync(skip: offset, count: 10000);
                    while (streams.Count() > 0)
                    {
                        offset += streams.Count();

                        try
                        {
                            IEnumerable<string> streamIds = from s in streams
                                                            where s.TypeId.Equals(typeId, StringComparison.InvariantCultureIgnoreCase)
                                                            select s.Id;
                            foreach (string streamId in streamIds)
                            {
                                await config.DeleteStreamAsync(streamId);
                                --offset;
                            }
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine(e);
                        }

                        streams = await config.GetStreamsAsync(skip: offset, count: 100);
                    }

                    try
                    {
                        await config.DeleteTypeAsync(typeId);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e);
                    }
                }
            }
        }

        /// <summary>
        /// Less than efficient way to mangle identifier names to mostly compliy with documentation specification
        /// </summary>
        /// <param name="id">Identifier to be cleaned up.</param>
        /// <returns></returns>
        private static string CleanIdentifier(string id)
        {
            return id.Replace(' ', '-')
                .Replace("__", "_")
                .Replace("/", " per ")
                .Replace("..", ".");
        }

        /// <summary>
        /// Read values from a collection of counters, create an event and add the event to the stream.
        /// 
        /// Note the use of an HttpClient and raw JSON in place of the <see cref="ISdsDataService"/>.  We do
        /// this so that we do not have to define a formal CLR type to represent the performance counter category 
        /// instance.
        /// </summary>
        /// <param name="httpClient">HttpClient instance</param>
        /// <param name="counters">Collection of counters to be read and added to an event</param>
        /// <param name="stream">The stream to write the event to</param>
        /// <returns></returns>
        private static Func<Task> GetUpdate(HttpClient httpClient, PerformanceCounter[] counters, SdsStream stream)
        {
            return async () =>
            {
                // Build the event as a JSON string
                StringBuilder json = new StringBuilder();
                json.AppendLine("{");
                json.Append($"   \"Time\":\"{DateTime.UtcNow.ToString("o")}\"");
                foreach (PerformanceCounter counter in counters)
                {
                    json.AppendLine($",");
                    json.Append($"   \"{counter.CounterName}\":\"{counter.RawValue}\"");
                }
                json.AppendLine("}");

                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"Streams/{stream.Id}/Data/InsertValue")
                {
                    Content = new StringContent(json.ToString())
                };
                HttpResponseMessage response = await httpClient.SendAsync(request);
                if (!response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"Failed updating {stream.Name}, {response.ReasonPhrase}:{response.StatusCode}");
                    if (response.Content != null && response.Content.Headers.ContentLength > 0)
                        Console.WriteLine(await response.Content.ReadAsStringAsync());
                }
            };
        }
    }
}
