using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;

namespace SdsClientLibraries
{
    public class Program
    {
        public static Exception toThrow = null;
        public static bool success = true;

        public static void Main() => MainAsync().GetAwaiter().GetResult();

        public static async Task<bool> MainAsync(bool test = false)
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
            string streamIdSecondary = "SampleStream_Secondary";
            string streamIdCompound = "SampleStream_Compound";

            string typeId = "SampleType";
            string targetTypeId = "SampleType_Target";
            string targetIntTypeId = "SampleType_TargetInt";
            string autoStreamViewId = "SampleAutoStreamView";
            string manualStreamViewId = "SampleManualStreamView";
            string compoundTypeId = "SampleType_Compound";

            var uriResource = new Uri(resource);
            // Step 1 
            // Get Sds Services to communicate with server
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);

            SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
            var metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            var dataService = sdsService.GetDataService(tenantId, namespaceId);
            var tableService = sdsService.GetTableService(tenantId, namespaceId);


            Console.WriteLine(@"-------------------------------------------------------------");
            Console.WriteLine(@"  _________    .___           _______  ______________________");
            Console.WriteLine(@" /   _____/  __| _/______     \      \ \_   _____/\__    ___/");
            Console.WriteLine(@" \_____  \  / __ |/  ___/     /   |   \ |    __)_   |    |   ");
            Console.WriteLine(@" /        \/ /_/ |\___ \     /    |    \|        \  |    |   ");
            Console.WriteLine(@"/_______  /\____ /____  > /\ \____|__  /_______  /  |____|   ");
            Console.WriteLine(@"        \/      \/    \/  \/         \/        \/            ");
            Console.WriteLine(@"-------------------------------------------------------------");
            Console.WriteLine();
            Console.WriteLine($"SDS endpoint at {resource}");
            Console.WriteLine();

            try
            {
                // Step 2
                // create an SdsType
                Console.WriteLine("Creating an SdsType");
                SdsType type = SdsTypeBuilder.CreateSdsType<WaveData>();
                type.Id = typeId;
                type = await metadataService.GetOrCreateTypeAsync(type);

                // Step 3
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

                // Step 4
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

                // Step 5
                // get last event
                Console.WriteLine("Getting latest event");
                var latest = await dataService.GetLastValueAsync<WaveData>(streamId);
                Console.WriteLine(latest.ToString());
                Console.WriteLine();

                // get all events
                Console.WriteLine("Getting all events");
                var allEvents = (List<WaveData>)await dataService.GetWindowValuesAsync<WaveData>(streamId, "0", "180");
                Console.WriteLine($"Total events found: {allEvents.Count}");
                foreach (var evnt in allEvents)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Step 6
                //Step2 Getting all events in table format with headers.
                var tableEvents = await tableService.GetWindowValuesAsync(stream.Id, "0", "180");

                Console.WriteLine("Getting table events");
                foreach (var evnt in tableEvents.Rows)
                {
                    Console.WriteLine(String.Join(",", evnt.ToArray()));
                }
                Console.WriteLine();

                // Step 7
                // update events
                Console.WriteLine("Updating events");

                // update one event
                var updatedWave = UpdateWave(allEvents.First(), 4);
                await dataService.UpdateValueAsync(stream.Id, updatedWave);

                // update all events, adding ten more
                var updatedCollection = new List<WaveData>();
                for (int i = 2; i < 40; i = i + 2)
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

                // Step 8
                // replacing events
                Console.WriteLine("Replacing events");

                // replace one event
                var replaceEvent = UpdateWave(allEvents.First(), multiplier:5);

                await dataService.ReplaceValueAsync<WaveData>(streamId, replaceEvent);

                // replace all events
                for (int i = 1; i < allEvents.Count; i++)
                {
                    allEvents[i] = UpdateWave(allEvents[i], multiplier: 5);
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

                // Step 9
                // Property Overrides
                Console.WriteLine("SDS can interpolate or extrapolate data at an index location where data does not explicitly exist:");
                Console.WriteLine();

                // We will retrieve three events using the default behavior, Continuous
                var retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated);
                Console.WriteLine("Default (Continuous) requesting data starting at index location '1', where we have not entered data, SDS will interpolate a value for this property and then return entered values:");
                foreach (var value in retrieved)
                {
                    Console.WriteLine(value.ToString());
                }
                Console.WriteLine();

                var retrievedInterpolated = await dataService
                    .GetValuesAsync<WaveData>(stream.Id, "5", "32", 4);
                Console.WriteLine("SDS will interpolate a value for each index asked for (5,14,23,32):");
                foreach (var value in retrievedInterpolated)
                {
                    Console.WriteLine(value.ToString());
                }
                Console.WriteLine();

                // Step 10
                // We will retrieve events filtered to only get the ones where the radians are less than 50.  Note, this can be done on index properties too.

                var retrievedInterpolatedFiltered = (await dataService.GetWindowFilteredValuesAsync<WaveData>(stream.Id, "0", "180", SdsBoundaryType.ExactOrCalculated, "Radians lt 50"));
                Console.WriteLine("SDS will only return the values where the radians are less than 50:");
                foreach (var value in retrievedInterpolatedFiltered)
                {
                    Console.WriteLine(value.ToString());
                }
                Console.WriteLine();

                //Step 11
                //We will retrieve a sample of our data
                Console.WriteLine("SDS can return a sample of your data population to show trends.");
                Console.WriteLine("Getting Sampled Values:");
                var sampledValues = await dataService.GetSampledValuesAsync<WaveData>(stream.Id, "0",
                    "40", 4, new[] {nameof(WaveData.Sin)});
                foreach(var sample in sampledValues)
                {
                    Console.WriteLine(sample);
                }
                Console.WriteLine();

                // Step 12
                // create a Discrete stream PropertyOverride indicating that we do not want Sds to calculate a value for Radians and update our stream 
                var propertyOverride = new SdsStreamPropertyOverride()
                {
                    SdsTypePropertyId = "Radians",
                    InterpolationMode = SdsInterpolationMode.Discrete
                };
                var propertyOverrides = new List<SdsStreamPropertyOverride>() { propertyOverride };

                // update the stream
                stream.PropertyOverrides = propertyOverrides;
                await metadataService.CreateOrUpdateStreamAsync(stream);

                retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated);
                Console.WriteLine("We can override this behavior on a property by property basis, here we override the Radians property instructing Sds not to interpolate.");
                Console.WriteLine("SDS will now return the default value for the data type:");

                foreach (var value in retrieved)
                {
                    Console.WriteLine(value.ToString());
                }
                Console.WriteLine();

                // Step 13
                // StreamViews
                Console.WriteLine("SdsStreamViews");

                // create target types
                var targetType = SdsTypeBuilder.CreateSdsType<WaveDataTarget>();
                targetType.Id = targetTypeId;

                var targetIntType = SdsTypeBuilder.CreateSdsType<WaveDataInteger>();
                targetIntType.Id = targetIntTypeId;

                await metadataService.GetOrCreateTypeAsync(targetType);
                await metadataService.GetOrCreateTypeAsync(targetIntType);

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

                // get manualStreamView data
                Console.WriteLine("SdsStreamViews can also convert certain types of data, here we return integers where the original values were doubles:");
                var manualStreamViewData = await dataService.GetRangeValuesAsync<WaveDataInteger>(stream.Id, "1", 3, SdsBoundaryType.ExactOrCalculated, manualStreamViewId);

                foreach (var value in manualStreamViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get SdsStreamViewMap
                Console.WriteLine("We can query SDS to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:");
                var autoStreamViewMap = await metadataService.GetStreamViewMapAsync(autoStreamViewId);
                PrintStreamViewMapProperties(autoStreamViewMap);

                Console.WriteLine("Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                var manualStreamViewMap = await metadataService.GetStreamViewMapAsync(manualStreamViewId);
                PrintStreamViewMapProperties(manualStreamViewMap);

                // Step 14
                // Update Stream Type based on SdsStreamView
                Console.WriteLine("We will now update the stream type based on the streamview");

                var firstVal = await dataService.GetFirstValueAsync<WaveData>(stream.Id);

                await metadataService.UpdateStreamTypeAsync(stream.Id, autoStreamViewId);
                var newStream = await metadataService.GetStreamAsync(stream.Id);

                var firstValUpdated = await dataService.GetFirstValueAsync<WaveDataTarget>(stream.Id);

                Console.WriteLine($"The new type id {newStream.TypeId} compared to the original one {stream.TypeId}.");
                Console.WriteLine($"The new type value {firstValUpdated.ToString()} compared to the original one {firstVal.ToString()}.");
                Console.WriteLine();

                // Step 15
                // Show filtering on Type, works the same as filtering on Streams

                var types = await metadataService.GetTypesAsync();
                var typesFiltered = await metadataService.GetTypesAsync("Id:*Target*");

                Console.WriteLine($"The number of types returned without filtering: {types.Count()}.  With filtering {typesFiltered.Count()}.");
                Console.WriteLine();

                // Step 16
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

                // Step 17
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

                // Step 18
                // Adding a new stream with a secondary index.
                Console.WriteLine("Adding a stream with a secondary index.");

                SdsStreamIndex measurementIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = type.Properties.First(p => p.Id.Equals("Radians")).Id
                };

                SdsStream secondary = new SdsStream()
                {
                    Id = streamIdSecondary,
                    TypeId = type.Id,
                    Indexes = new List<SdsStreamIndex>()
                  {
                      measurementIndex
                  }
                };

                secondary = await metadataService.GetOrCreateStreamAsync(secondary);
                Console.WriteLine($"Secondary indexes on streams. {stream.Id}:{stream.Indexes?.Count()}. {secondary.Id}:{secondary.Indexes.Count()}. ");
                Console.WriteLine();

                // Modifying an existing stream with a secondary index.
                Console.WriteLine("Modifying a stream to have a secondary index.");

                stream = await metadataService.GetStreamAsync(stream.Id);
                type = await metadataService.GetTypeAsync(stream.TypeId);

                SdsStreamIndex measurementTargetIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = type.Properties.First(p => p.Id.Equals("RadiansTarget")).Id
                };
                stream.Indexes = new List<SdsStreamIndex>() { measurementTargetIndex };

                await metadataService.CreateOrUpdateStreamAsync(stream);
                stream = await metadataService.GetStreamAsync(stream.Id);


                // Modifying an existing stream to remove the secondary index
                Console.WriteLine("Removing a secondary index from a stream.");

                secondary.Indexes = null;
                await metadataService.CreateOrUpdateStreamAsync(secondary);
                secondary = await metadataService.GetStreamAsync(secondary.Id);
                Console.WriteLine($"Secondary indexes on streams. {stream.Id}:{stream.Indexes?.Count()}. {secondary.Id}:{secondary.Indexes?.Count()}. ");
                Console.WriteLine();

                // Step 19
                // Adding Compound Index Type
                Console.WriteLine("Creating an SdsType with a compound index");
                SdsType typeCompound = SdsTypeBuilder.CreateSdsType<WaveDataCompound>();
                typeCompound.Id = compoundTypeId;
                typeCompound = await metadataService.GetOrCreateTypeAsync(typeCompound);

                // create an SdsStream
                Console.WriteLine("Creating an SdsStream off of type with compound index");
                var streamCompound = new SdsStream
                {
                    Id = streamIdCompound,
                    Name = "Wave Data Sample",
                    TypeId = typeCompound.Id,
                    Description = "This is a sample SdsStream for storing WaveData type measurements"
                };
                streamCompound = await metadataService.GetOrCreateStreamAsync(streamCompound);

                // Step 20
                // insert compound data
                Console.WriteLine("Inserting data");
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(1, 10));
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(2, 2));
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(3, 1));
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 3));
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 8));
                await dataService.InsertValueAsync(streamCompound.Id, GetWaveMultiplier(10, 10));

                var latestCompound = await dataService.GetLastValueAsync<WaveDataCompound>(streamCompound.Id);
                var firstCompound = await dataService.GetFirstValueAsync<WaveDataCompound>(streamCompound.Id);

                var data = await dataService.GetWindowValuesAsync<WaveDataCompound, int, int>(streamCompound.Id, Tuple.Create(2, 1), Tuple.Create(10, 8));

                Console.WriteLine($"First data: {firstCompound.ToString()}.  Latest data: {latestCompound.ToString()}.");

                Console.WriteLine();

                Console.WriteLine("Window Data:");

                foreach (var evnt in data)
                {
                    Console.WriteLine(evnt.ToString());
                }
            }
            catch (Exception ex)
            {
                success = false;
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {
                //step 21
                Console.WriteLine();
                Console.WriteLine("Cleaning up");
                // Delete the stream, types and streamViews making sure
                Console.WriteLine("Deleting stream");
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamId);
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamIdSecondary);
                await RunInTryCatch(metadataService.DeleteStreamAsync, streamIdCompound);
                Console.WriteLine("Deleting streamViews");
                await RunInTryCatch(metadataService.DeleteStreamViewAsync, autoStreamViewId);
                await RunInTryCatch(metadataService.DeleteStreamViewAsync, manualStreamViewId);
                Console.WriteLine("Deleting types");
                await RunInTryCatch(metadataService.DeleteTypeAsync, typeId);
                await RunInTryCatch(metadataService.DeleteTypeAsync, compoundTypeId);
                await RunInTryCatch(metadataService.DeleteTypeAsync, targetTypeId);
                await RunInTryCatch(metadataService.DeleteTypeAsync, targetIntTypeId);

                Console.WriteLine("done");
                if (!test)
                    Console.ReadKey();
            }

            if (test && !success)
                throw toThrow;
            return success;
        }

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an error
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        private static async Task RunInTryCatch(Func<string, Task> methodToRun, string value)
        {
            try
            {
                await methodToRun(value);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Got error in {methodToRun.Method.Name} with value {value} but continued on:" + ex.Message);
                if (toThrow == null)
                {
                    success = false;
                    toThrow = ex;
                }
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
            var radians = order * (Math.PI/32);

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

        private static WaveDataCompound GetWaveMultiplier(int order, int multiplier)
        {
            var radians = order * (Math.PI/32);

            return new WaveDataCompound
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians),
                Multiplier = multiplier
            };
        }

    }
}