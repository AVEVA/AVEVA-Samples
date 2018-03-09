using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using OSIsoft.Data;
using OSIsoft.Data.Http.Security;
using OSIsoft.Data.Reflection;
using Microsoft.IdentityModel.Clients.ActiveDirectory;

namespace QiClientLibraries
{
    internal class Program
    {
        public static void Main()
        {
            MainAsync().GetAwaiter().GetResult();
        }

        private static async Task MainAsync()
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            IConfiguration configuration = builder.Build();

            // ==== Client constants ====
            var tenantId = configuration["TenantId"];
            var namespaceId = configuration["NamespaceId"];
            var address = configuration["Address"];
            var resource = configuration["Resource"];
            var clientId = configuration["ClientId"];
            var clientKey = configuration["ClientKey"];

            // ==== Metadata IDs ====
            string streamId = "SampleStream";
            string typeId = "SampleType";
            string behaviorId = "SampleBehavior";
            string targetTypeId = "SampleType_Target";
            string targetIntTypeId = "SampleType_TargetInt";
            string autoViewId = "SampleAutoView";
            string manualViewId = "SampleManualView";

            // Get Qi Services to communicate with server
            QiSecurityHandler securityHandler = new QiSecurityHandler(resource, tenantId, clientId, clientKey);

            QiService qiService = new QiService(new Uri(address), securityHandler);
            var metadataService = qiService.GetMetadataService(tenantId, namespaceId);
            var dataService = qiService.GetDataService(tenantId, namespaceId);

            LoggerCallbackHandler.UseDefaultLogging = false;


            Console.WriteLine(@"---------------------------------------------------");
            Console.WriteLine(@"________  .__      _______  ______________________");
            Console.WriteLine(@"\_____  \ |__|     \      \ \_   _____/\__    ___/");
            Console.WriteLine(@" /  / \  \|  |     /   |   \ |    __)_   |    |   ");
            Console.WriteLine(@"/   \_/.  \  |    /    |    \|        \  |    |   ");
            Console.WriteLine(@"\_____\ \_/__| /\ \____|__  /_______  /  |____|   ");
            Console.WriteLine(@"       \__>    \/         \/        \/           ");
            Console.WriteLine(@"---------------------------------------------------");
            Console.WriteLine();
            Console.WriteLine($"Qi endpoint at {address}");
            Console.WriteLine();

            try
            {
                // create a QiType
                Console.WriteLine("Creating a QiType");
                QiType type = QiTypeBuilder.CreateQiType<WaveData>();
                type.Id = typeId;
                type = await metadataService.GetOrCreateTypeAsync(type);

                // create a QiStream
                Console.WriteLine("Creating a QiStream");
                var stream = new QiStream
                {
                    Id = streamId,
                    Name = "Wave Data Sample",
                    TypeId = type.Id,
                    Description = "This is a sample QiStream for storing WaveData type measurements"
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

                // Stream behaviors
                Console.WriteLine("QiStreamBehaviors determine whether Qi interpolates or extrapolates data at the requested index location");
                Console.WriteLine();
                
                // Stream behaviors modify retrieval.  We will retrieve three events using the default behavior, Continuous
                var retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, QiBoundaryType.ExactOrCalculated);
                Console.WriteLine("Default (Continuous) stream behavior, requesting data starting at index location '1', Qi will interpolate this value:");
                foreach (var value in retrieved)
                {
                    Console.WriteLine($"Order: {value.Order}, Radians: {value.Radians}");
                }
                Console.WriteLine();

                // create a Discrete stream behavior
                var behavior = new QiStreamBehavior
                {
                    Id = behaviorId,
                    Mode = QiStreamMode.Discrete
                };
                behavior = await metadataService.GetOrCreateBehaviorAsync(behavior);

                // update the stream
                stream.BehaviorId = behavior.Id;
                await metadataService.CreateOrUpdateStreamAsync(stream);

                retrieved = await dataService
                    .GetRangeValuesAsync<WaveData>(stream.Id, "1", 3, QiBoundaryType.ExactOrCalculated);
                Console.WriteLine("Discrete stream behavior, Qi does not interpolate and returns the data starting at the next index location containing data:");
                foreach (var value in retrieved)
                {
                    Console.WriteLine($"Order: {value.Order}, Radians: {value.Radians}");
                }
                Console.WriteLine();

                // Stream views
                Console.WriteLine("QiViews");
                
                // create target types
                var targetType = QiTypeBuilder.CreateQiType<WaveDataTarget>();
                targetType.Id = targetTypeId;

                var targetIntType = QiTypeBuilder.CreateQiType<WaveDataInteger>();
                targetIntType.Id = targetIntTypeId;

                await metadataService.CreateOrUpdateTypeAsync(targetType);
                await metadataService.CreateOrUpdateTypeAsync(targetIntType);

                // create views
                var autoView = new QiView()
                {
                    Id = autoViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetTypeId
                };

                // create explicit mappings 
                var vp1 = new QiViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
                var vp2 = new QiViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
                var vp3 = new QiViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
                var vp4 = new QiViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

                var manualView = new QiView()
                {
                    Id = manualViewId,
                    SourceTypeId = typeId,
                    TargetTypeId = targetIntTypeId,
                    Properties = new List<QiViewProperty>() { vp1, vp2, vp3, vp4 }
                };

                await metadataService.CreateOrUpdateViewAsync(autoView);
                await metadataService.CreateOrUpdateViewAsync(manualView);

                Console.WriteLine("Here is some of our data as it is stored on the server:");
                foreach (var evnt in retrieved)
                {
                    Console.WriteLine($"Sin: {evnt.Sin}, Cos: {evnt.Cos}, Tan {evnt.Tan}");
                }
                Console.WriteLine();

                // get autoview data
                var autoViewData = await dataService.GetRangeValuesAsync<WaveDataTarget>(stream.Id, "1", 3, QiBoundaryType.ExactOrCalculated, autoViewId);

                Console.WriteLine("Specifying a view with a QiType of the same shape returns values that are automatically mapped to the target QiType's properties:");

                foreach (var value in autoViewData)
                {
                    Console.WriteLine($"SinTarget: {value.SinTarget} CosTarget: {value.CosTarget} TanTarget: {value.TanTarget}");
                }
                Console.WriteLine();

                // get manaulview data
                Console.WriteLine("QiViews can also convert certain types of data, here we return integers where the original values were doubles:");
                var manualViewData = await dataService.GetRangeValuesAsync<WaveDataInteger>(stream.Id, "1", 3, QiBoundaryType.ExactOrCalculated, manualViewId);

                foreach (var value in manualViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get QiViewMap
                Console.WriteLine("We can query Qi to return the QiViewMap for our QiView, here is the one generated automatically:");
                var autoViewMap = await metadataService.GetViewMapAsync(autoViewId);
                PrintViewMapProperties(autoViewMap);

                Console.WriteLine("Here is our explicit mapping, note QiViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                var manualViewMap = await metadataService.GetViewMapAsync(manualViewId);
                PrintViewMapProperties(manualViewMap);

                // tags, metadata and search
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
                Console.WriteLine("Pausing to allow for search indexing...");
                // allow time for search indexing
                await Task.Delay(15000);

                Console.WriteLine("We can also use our tags to search for streams, let's search for streams tagged with 'periodic':");

                var streams = await metadataService.GetStreamsAsync("periodic");

                foreach (var strm in streams)
                {
                    Console.WriteLine(strm.Id);
                }
                Console.WriteLine();

                // delete values
                Console.WriteLine("Deleting values from the QiStream");

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
                // Delete the stream, types, views and behavior
                Console.WriteLine("Deleteing stream");
                await metadataService.DeleteStreamAsync(streamId);
                Console.WriteLine("Deleteing types");
                await metadataService.DeleteTypeAsync(typeId);
                await metadataService.DeleteTypeAsync(targetTypeId);
                await metadataService.DeleteTypeAsync(targetIntTypeId);
                Console.WriteLine("Deleteing views");
                await metadataService.DeleteViewAsync(autoViewId);
                await metadataService.DeleteViewAsync(manualViewId);
                Console.WriteLine("Deleteing behavior");
                await metadataService.DeleteBehaviorAsync(behaviorId);
                Console.WriteLine("done");
                Console.ReadKey();
            }
        }

        private static void PrintViewMapProperties(QiViewMap qiViewMap)
        {
            foreach (var prop in qiViewMap.Properties)
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