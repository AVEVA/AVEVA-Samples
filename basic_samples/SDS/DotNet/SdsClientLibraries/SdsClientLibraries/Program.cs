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

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Data.Http.Security;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity; 
using Microsoft.IdentityModel.Clients.ActiveDirectory;

namespace SdsClientLibraries
{
    internal class Program
    {
        public static void Main() => MainAsync().GetAwaiter().GetResult();

        private static async Task MainAsync()
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("appsettings.test.json", optional: true);
            IConfiguration configuration = builder.Build();

            // ==== Client constants ====
            var tenantId = configuration["TenantId"];
            var namespaceId = configuration["NamespaceId"];
            var resource = configuration["Resource"];
            var clientId = configuration["ClientId"];
            var clientKey = configuration["ClientKey"];

            // ==== Metadata IDs ====
            string streamId = "SampleStream";
            string typeId = "SampleType";
            string targetTypeId = "SampleType_Target";
            string targetIntTypeId = "SampleType_TargetInt";
            string autoStreamViewId = "SampleAutoStreamView";
            string manualStreamViewId = "SampleManualStreamView";

            // Get Sds Services to communicate with server
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(resource, clientId, clientKey);

            SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
            var metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            var dataService = sdsService.GetDataService(tenantId, namespaceId);

            LoggerCallbackHandler.UseDefaultLogging = false;


            Console.WriteLine(@"-------------------------------------------------------------");
            Console.WriteLine(@"  _________    .___           _______  ______________________");
            Console.WriteLine(@" /   _____/  __| _/______     \      \ \_   _____/\__    ___/");
            Console.WriteLine(@" \_____  \  / __ |/  ___/     /   |   \ |    __)_   |    |   ");
            Console.WriteLine(@" /        \/ /_/ |\___ \     /    |    \|        \  |    |   ");
            Console.WriteLine(@"/_______  /\____ /____  > /\ \____|__  /_______  /  |____|   ");
            Console.WriteLine(@"        \/      \/    \/  \/         \/        \/            ");
            Console.WriteLine(@"-------------------------------------------------------------");
            Console.WriteLine();
            Console.WriteLine($"Sds endpoint at {resource}");
            Console.WriteLine();

            try
            {
                // create an SdsType
                Console.WriteLine("Creating an SdsType");
                SdsType type = SdsTypeBuilder.CreateSdsType<WaveData>();
                type.Id = typeId;
                type = await metadataService.GetOrCreateTypeAsync(type);

                // create an SdsStream
                Console.WriteLine("Creating an SdsStream");
                var stream = new SdsStream
                {
                    Id = streamId,
                    Name = "Wave Data Sample",
                    TypeId = type.Id,
                    Description = "This is a sample SdsStream for storing WaveData type measurements"
                };
                stream = await metadataService.GetOrCreateStreamAsync(stream);

                // insert data
                Console.WriteLine("Inserting data");

                // insert a single event
                var wave = GetWave(0, 200, 2);
                await dataService.InsertValueAsync(stream.Id, wave);

                // insert a list of events
                var waves = new List<WaveData>();
                for (var i = 2; i <= 18; i += 2)
                {
                    waves.Add(GetWave(i, 200, 2));
                }
                await dataService.InsertValuesAsync(stream.Id, waves);

                // get last event
                Console.WriteLine("Getting latest event");
                var latest = await dataService.GetLastValueAsync<WaveData>(streamId);
                Console.WriteLine(latest.ToString());
                Console.WriteLine();

                // get all events
                Console.WriteLine("Getting all events");
                var allEvents = (List<WaveData>) await dataService.GetWindowValuesAsync<WaveData>(streamId, "0", "180");
                Console.WriteLine($"Total events found: {allEvents.Count}");
                foreach (var evnt in allEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // update events
                Console.WriteLine("Updating events");

                // update one event
                var updatedWave = UpdateWave(allEvents.First(), 4);
                await dataService.UpdateValueAsync(stream.Id, updatedWave);

                // update all events, adding ten more
                var updatedCollection = new List<WaveData>();
                for (int i = 2; i < 40; i = i+2)
                {
                    updatedCollection.Add(GetWave(i, 400, 4));
                }
                await dataService.UpdateValuesAsync(stream.Id, updatedCollection);

                allEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(stream.Id, "0", "180");

                Console.WriteLine("Getting updated events");
                Console.WriteLine($"Total events found: {allEvents.Count}");

                foreach (var evnt in allEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // replacing events
                Console.WriteLine("Replacing events");

                // replace one event
                var replaceEvent = allEvents.First();
                replaceEvent.Sin = 0.717;
                replaceEvent.Cos = 0.717;
                replaceEvent.Tan = Math.Sqrt(2 * (0.717 * 0.717));

                await dataService.ReplaceValueAsync<WaveData>(streamId, replaceEvent);

                // replace all events
                foreach (var evnt in allEvents)
                {
                    evnt.Sin = 5.0/2;
                    evnt.Cos = 5*Math.Sqrt(3)/2;
                    evnt.Tan = 5/Math.Sqrt(3);
                }

                await dataService.ReplaceValuesAsync<WaveData>(streamId, allEvents);

                Console.WriteLine("Getting replaced events");
                var replacedEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(streamId, "0", "180");
                Console.WriteLine($"Total events found: {replacedEvents.Count}");
                foreach (var evnt in replacedEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Property Overrides
                Console.WriteLine("Sds can interpolate or extrapolate data at an index location where data does not explicitly exist:");
                Console.WriteLine();

                // We will retrieve three events using the default behavior, Continuous
                var retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated);
                Console.WriteLine("Default (Continuous) requesting data starting at index location '1', where we have not entered data, Sds will interpolate a value for each property:");
                foreach (var value in retrieved)
                {
                    Console.WriteLine($"Order: {value.Order}, Radians: {value.Radians}, Cos: {value.Cos}");
                }
                Console.WriteLine();

                // create a Discrete stream PropertyOverride indicating that we do not want Sds to calculate a value for Radians and update our stream 
                var propertyOverride = new SdsStreamPropertyOverride()
                {
                    SdsTypePropertyId = "Radians",
                    InterpolationMode = SdsInterpolationMode.Discrete
                };
                var propertyOverrides = new List<SdsStreamPropertyOverride>() {propertyOverride};

                // update the stream
                stream.PropertyOverrides = propertyOverrides;
                await metadataService.CreateOrUpdateStreamAsync(stream);

                retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated);
                Console.WriteLine("We can override this behavior on a property by property basis, here we override the Radians property instructing Sds not to interpolate.");
                Console.WriteLine("Sds will now return the default value for the data type:");

                foreach (var value in retrieved)
                {
                    Console.WriteLine($"Order: {value.Order}, Radians: {value.Radians}, Cos: {value.Cos}");
                }
                Console.WriteLine();

                // StreamViews
                Console.WriteLine("SdsStreamViews");
                
                // create target types
                var targetType = SdsTypeBuilder.CreateSdsType<WaveDataTarget>();
                targetType.Id = targetTypeId;

                var targetIntType = SdsTypeBuilder.CreateSdsType<WaveDataInteger>();
                targetIntType.Id = targetIntTypeId;

                await metadataService.CreateOrUpdateTypeAsync(targetType);
                await metadataService.CreateOrUpdateTypeAsync(targetIntType);

                // create StreamViews
                var autoStreamView = new SdsStreamView()
                {
                    Id = autoStreamViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetTypeId
                };

                // create explicit mappings 
                var vp1 = new SdsStreamViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
                var vp2 = new SdsStreamViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
                var vp3 = new SdsStreamViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
                var vp4 = new SdsStreamViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

                var manualStreamView = new SdsStreamView()
                {
                    Id = manualStreamViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetIntTypeId,
                    Properties = new List<SdsStreamViewProperty>() { vp1, vp2, vp3, vp4 }
                };

                await metadataService.CreateOrUpdateStreamViewAsync(autoStreamView);
                await metadataService.CreateOrUpdateStreamViewAsync(manualStreamView);

                Console.WriteLine("Here is some of our data as it is stored on the server:");
                foreach (var evnt in retrieved)
                {
                    Console.WriteLine($"Sin: {evnt.Sin}, Cos: {evnt.Cos}, Tan {evnt.Tan}");
                }
                Console.WriteLine();

                // get autoStreamView data
                var autoStreamViewData = await dataService.GetRangeValuesAsync<WaveDataTarget>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, autoStreamViewId);

                Console.WriteLine("Specifying a StreamView with an SdsType of the same shape returns values that are automatically mapped to the target SdsType's properties:");

                foreach (var value in autoStreamViewData)
                {
                    Console.WriteLine($"SinTarget: {value.SinTarget} CosTarget: {value.CosTarget} TanTarget: {value.TanTarget}");
                }
                Console.WriteLine();

                // get manaulStreamView data
                Console.WriteLine("SdsStreamViews can also convert certain types of data, here we return integers where the original values were doubles:");
                var manualStreamViewData = await dataService.GetRangeValuesAsync<WaveDataInteger>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, manualStreamViewId);

                foreach (var value in manualStreamViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get SdsStreamViewMap
                Console.WriteLine("We can query Sds to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:");
                var autoStreamViewMap = await metadataService.GetStreamViewMapAsync(autoStreamViewId);
                PrintStreamViewMapProperties(autoStreamViewMap);

                Console.WriteLine("Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                var manualStreamViewMap = await metadataService.GetStreamViewMapAsync(manualStreamViewId);
                PrintStreamViewMapProperties(manualStreamViewMap);
                
                // tags and metadata
                Console.WriteLine("Let's add some Tags and Metadata to our stream:");
                var tags = new List<string> { "waves", "periodic", "2018", "validated" };
                var metadata = new Dictionary<string, string>() { { "Region", "North America" }, { "Country", "Canada" }, { "Province", "Quebec" } };
                                
                await metadataService.UpdateStreamTagsAsync(streamId, tags);
                await metadataService.UpdateStreamMetadataAsync(streamId, metadata);

                tags = (List<string>)await metadataService.GetStreamTagsAsync(streamId);

                Console.WriteLine();
                Console.WriteLine($"Tags now associated with {streamId}:");
                foreach (var tag in tags)
                {
                    Console.WriteLine(tag);
                }
                Console.WriteLine();
                Console.WriteLine($"Metadata now associated with {streamId}:");
                Console.WriteLine("Metadata key Region: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Region"));
                Console.WriteLine("Metadata key Country: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Country"));
                Console.WriteLine("Metadata key Province: " + await metadataService.GetStreamMetadataValueAsync(streamId, "Province"));

                Console.WriteLine();

                // delete values
                Console.WriteLine("Deleting values from the SdsStream");

                // delete one event
                await dataService.RemoveValueAsync(stream.Id, 0);

                // delete all events
                await dataService.RemoveWindowValuesAsync(stream.Id, 1, 200);

                retrieved = await dataService.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200");
                if (retrieved.ToList<WaveData>().Count == 0)
                {
                    Console.WriteLine("All values deleted successfully!");
                }
                Console.WriteLine();

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                Console.WriteLine("Cleaning up");
                // Delete the stream, types and streamViews
                Console.WriteLine("Deleteing stream");
                await metadataService.DeleteStreamAsync(streamId);
                Console.WriteLine("Deleteing streamViews");
                await metadataService.DeleteStreamViewAsync(autoStreamViewId);
                await metadataService.DeleteStreamViewAsync(manualStreamViewId);
                Console.WriteLine("Deleteing types");
                await metadataService.DeleteTypeAsync(typeId);
                await metadataService.DeleteTypeAsync(targetTypeId);
                await metadataService.DeleteTypeAsync(targetIntTypeId);


                Console.WriteLine("done");
                Console.ReadKey();
            }
        }

        private static void PrintStreamViewMapProperties(SdsStreamViewMap sdsStreamViewMap)
        {
            foreach (var prop in sdsStreamViewMap.Properties)
            {
                if (prop.TargetId != null)
                {
                    Console.WriteLine($"{prop.SourceId} => {prop.TargetId}");
                }
                else
                {
                    Console.WriteLine($"{prop.SourceId} => Not Mapped");

                }
            }
            Console.WriteLine();
        }

        private static WaveData GetWave(int order, double range, double multiplier)
        {
            var radians = order * 2 * Math.PI;

            return new WaveData
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians)
            };
        }

        private static WaveData UpdateWave(WaveData wave, double multiplier)
        {
            wave.Tau = wave.Radians / (2 * Math.PI);
            wave.Sin = multiplier * Math.Sin(wave.Radians);
            wave.Cos = multiplier * Math.Cos(wave.Radians);
            wave.Tan = multiplier * Math.Tan(wave.Radians);
            wave.Sinh = multiplier * Math.Sinh(wave.Radians);
            wave.Cosh = multiplier * Math.Cosh(wave.Radians);
            wave.Tanh = multiplier * Math.Tanh(wave.Radians);

            return wave;
        }
    }
}
