using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;

namespace SdsRestApiCore
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
            string tenantId = configuration["TenantId"];
            string namespaceId = configuration["NamespaceId"];
            string resource = configuration["Resource"];
            string clientId = configuration["ClientId"];
            string clientKey = configuration["ClientKey"];
            string apiVersion = configuration["ApiVersion"];
			
			// ==== Metadata IDs ====
			string StreamId = "WaveStreamId";
			string TypeId = "WaveDataTypeId";
			string TargetTypeId = "WaveDataTargetTypeId";
			string TargetIntTypeId = "WaveDataTargetIntTypeId";
			string AutoStreamViewId = "WaveDataAutoStreamViewId";
			string ManualStreamViewId = "WaveDataManualStreamViewId";
            string compoundTypeId = "SampleType_Compound";
            string streamIdSecondary = "SampleStream_Secondary";
            string streamIdCompound = "SampleStream_Compound";

            // Step 1
            SdsSecurityHandler securityHandler = new SdsSecurityHandler(resource, clientId, clientKey);
            HttpClient httpClient = new HttpClient(securityHandler)
            {
                BaseAddress = new Uri(resource)
            };

            Console.WriteLine(@"-------------------------------------------------------");
            Console.WriteLine(@"  _________    .___     _____________________ ____________________");
            Console.WriteLine(@" /   _____/  __| _/_____\______   \_   _____//   _____/\__    ___/");
            Console.WriteLine(@" \_____  \  / __ |/  ___/|       _/|    __)_ \_____  \   |    |   ");
            Console.WriteLine(@" /        \/ /_/ |\___ \ |    |   \|        \/        \  |    |   ");
            Console.WriteLine(@"/_______  /\____ /____  >|____|_  /_______  /_______  /  |____|   ");
            Console.WriteLine(@"        \/      \/    \/        \/        \/        \/            ");
            Console.WriteLine(@"-------------------------------------------------------");
            Console.WriteLine();
            Console.WriteLine($"SDS endpoint at {resource}");
            Console.WriteLine();

            try
            {
                // Step 2
                // create a SdsType
                Console.WriteLine("Creating a SdsType");
                SdsType waveType = BuildWaveDataType(TypeId);
                HttpResponseMessage response =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveType.Id}",
                        new StringContent(JsonConvert.SerializeObject(waveType)));
                CheckIfResponseWasSuccessful(response);

                // Step 3
                // create a SdsStream
                Console.WriteLine("Creating a SdsStream");
                SdsStream waveStream = new SdsStream
                {
                    Id = StreamId,
                    Name = "WaveStream",
                    TypeId = waveType.Id
                };
                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                CheckIfResponseWasSuccessful(response);

                // Step 4
                // insert data
                Console.WriteLine("Inserting data");

                // insert a single event
                var singleWaveList = new List<WaveData>();
                WaveData wave = GetWave(0, 1, 2.0);
                singleWaveList.Add(wave);
                response = await httpClient.PostAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(singleWaveList)));
                CheckIfResponseWasSuccessful(response);

                // insert a list of events
                List<WaveData> waves = new List<WaveData>();
                for (int i = 2; i < 20; i += 2)
                {
                    WaveData newEvent = GetWave(i, 2, 2.0);
                    waves.Add(newEvent);
                }
                response = await httpClient.PostAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(waves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException();
                }

                // Step 5
                // get last event
                Console.WriteLine("Getting latest event");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Last");
                CheckIfResponseWasSuccessful(response);
                WaveData retrieved =
                    JsonConvert.DeserializeObject<WaveData>(await response.Content.ReadAsStringAsync());
                Console.WriteLine(retrieved.ToString());
                Console.WriteLine();

                // get all events
                Console.WriteLine("Getting all events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex={waves[waves.Count - 1].Order}");
                CheckIfResponseWasSuccessful(response);
                List<WaveData> retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Step 6
                // get all events in table header format
                Console.WriteLine("Getting all events in table header format");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex={waves[waves.Count - 1].Order}&form=tableh");
                CheckIfResponseWasSuccessful(response);
                string retrievedEventWithHeaders = (await response.Content.ReadAsStringAsync());
                Console.WriteLine(retrievedEventWithHeaders);
                Console.WriteLine();

                // Step 7
                // update events
                Console.WriteLine("Updating events");

                // update one event
                var updateEvent = retrieved;
                updateEvent.Sin = 1 / 2.0;
                updateEvent.Cos = Math.Sqrt(3) / 2;
                updateEvent.Tan = 1;
                List<WaveData> updateWave = new List<WaveData>();
                updateWave.Add(updateEvent);

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(updateWave)));
                CheckIfResponseWasSuccessful(response);

                // update all events, adding ten more
                List<WaveData> updateWaves = new List<WaveData>();
                for (int i = 0; i < 40; i += 2)
                {
                    WaveData newEvent = GetWave(i, 4, 4.0);
                    updateWaves.Add(newEvent);
                }

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data",
                    new StringContent(JsonConvert.SerializeObject(updateWaves)));
                CheckIfResponseWasSuccessful(response);

                Console.WriteLine("Getting updated events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
                retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Step 8
                // replacing events
                Console.WriteLine("Replacing events");

                // replace one event
                var replaceSingleWaveList = new List<WaveData>();
                var replaceEvent = GetWave(order: 0, range: 4, multiplier: 5.0);
                replaceSingleWaveList.Add(replaceEvent);

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?allowCreate=false",
                new StringContent(JsonConvert.SerializeObject(replaceSingleWaveList)));
                CheckIfResponseWasSuccessful(response);

                // replace all events
                var replaceEvents = retrievedList;
                for (int i = 1; i < replaceEvents.Count; i++)
                {
                    replaceEvents[i] = GetWave(order: i*2, range: 4, multiplier: 5.0);
                }
              
                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?allowCreate=false",
                new StringContent(JsonConvert.SerializeObject(replaceEvents)));
                CheckIfResponseWasSuccessful(response);

                // Step 9
                Console.WriteLine("Getting replaced events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
                retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Property Overrides
                Console.WriteLine("Property Overrides");
                Console.WriteLine("SDS can interpolate or extrapolate data at an index location where data does not explicitly exist:");
                Console.WriteLine();

                // We will retrieve three events using the default behavior, Continuous
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Transform?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}");
                CheckIfResponseWasSuccessful(response);
                List<WaveData> rangeValuesContinuous =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine("Default (Continuous) stream read behavior, requesting data starting at index location '1', SDS will interpolate this value:");
                foreach (var waveData in rangeValuesContinuous)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}, Cos: {waveData.Cos}");
                }
                Console.WriteLine();

                // Step 10
                // We will retrieve events filtered to only get the ones where the radians are less than 50.  Note, this can be done on index properties too.
                Console.WriteLine("Getting replaced events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}&filter=Radians lt 50");
                var retrievedFilteredList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedFilteredList.Count}");
                foreach (var evnt in retrievedFilteredList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                //Step 11
                //We will retrieve a sample of our data
                Console.WriteLine("SDS can return a sample of your data population to show trends.");
                Console.WriteLine("Getting Sampled Values:");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Sampled?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count-1].Order}&intervals={4}&sampleBy={nameof(WaveData.Sin)}");
                var retrievedSamples =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                foreach (var sample in retrievedSamples)
                {
                    Console.WriteLine(sample);
                }
                Console.WriteLine();

                // Step 12
                // Create a Discrete stream PropertyOverride indicating that we do not want Sds to calculate a value for Radians and update our stream
                SdsStreamPropertyOverride propertyOverride = new SdsStreamPropertyOverride
                {
                    SdsTypePropertyId = "Radians",
                    InterpolationMode = SdsInterpolationMode.Discrete
                };

                var propertyOverrides = new List<SdsStreamPropertyOverride>() { propertyOverride };

                // update the stream
                waveStream.PropertyOverrides = propertyOverrides;
                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                CheckIfResponseWasSuccessful(response);

                Console.WriteLine("We can override this read behavior on a property by property basis, here we override the Radians property instructing SDS not to interpolate.");
                Console.WriteLine("SDS will now return the default value for the data type:");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Transform?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}");
                CheckIfResponseWasSuccessful(response);
                List<WaveData> rangeValuesDiscrete =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                foreach (var waveData in rangeValuesDiscrete)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}, Cos: {waveData.Cos}");
                }
                Console.WriteLine();

                // Step 13
                // Stream views
                Console.WriteLine("SdsStreamViews");

                // create target types
                var targetType = BuildWaveDataTargetType(TargetTypeId);
                var targetIntType = BuildWaveDataTargetIntType(TargetIntTypeId);

                HttpResponseMessage targetTypeResponse =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetTypeId}",
                    new StringContent(JsonConvert.SerializeObject(targetType)));
                if (!targetTypeResponse.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                HttpResponseMessage targetIntTypeResponse =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetIntTypeId}",
                    new StringContent(JsonConvert.SerializeObject(targetIntType)));
                if (!targetIntTypeResponse.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // create StreamViews
                var autoStreamView = new SdsStreamView()
                {
                    Id = AutoStreamViewId,
                    SourceTypeId = TypeId,
                    TargetTypeId = TargetTypeId
                };

                // create explicit mappings 
                var vp1 = new SdsStreamViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
                var vp2 = new SdsStreamViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
                var vp3 = new SdsStreamViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
                var vp4 = new SdsStreamViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

                var manualStreamView = new SdsStreamView()
                {
                    Id = ManualStreamViewId,
                    SourceTypeId = TypeId,
                    TargetTypeId = TargetIntTypeId,
                    Properties = new List<SdsStreamViewProperty>() { vp1, vp2, vp3, vp4 }
                };

                response =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}",
                    new StringContent(JsonConvert.SerializeObject(autoStreamView)));
                CheckIfResponseWasSuccessful(response);

                response =
                     await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}",
                     new StringContent(JsonConvert.SerializeObject(manualStreamView)));
                CheckIfResponseWasSuccessful(response);

                Console.WriteLine("Here is some of our data as it is stored on the server:");
                foreach (var evnt in rangeValuesDiscrete)
                {
                    Console.WriteLine($"Sin: {evnt.Sin}, Cos: {evnt.Cos}, Tan {evnt.Tan}");
                }
                Console.WriteLine();

                // get data with autoStreamView
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Transform?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}&streamViewId={AutoStreamViewId}");

                CheckIfResponseWasSuccessful(response);

                List<WaveDataTarget> autoStreamViewData =
                    JsonConvert.DeserializeObject<List<WaveDataTarget>>(await response.Content.ReadAsStringAsync());

                Console.WriteLine("Specifying a StreamView with a SdsType of the same shape returns values that are automatically mapped to the target SdsType's properties:");

                foreach (var value in autoStreamViewData)
                {
                    Console.WriteLine($"SinTarget: {value.SinTarget} CosTarget: {value.CosTarget} TanTarget: {value.TanTarget}");
                }
                Console.WriteLine();

                Console.WriteLine("SdsStreamViews can also convert certain types of data, here we return integers where the original values were doubles:");

                // get data with manualStreamView
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Transform?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}&streamViewId={ManualStreamViewId}");

                CheckIfResponseWasSuccessful(response);

                List<WaveDataInteger> manualStreamViewData =
                    JsonConvert.DeserializeObject<List<WaveDataInteger>>(await response.Content.ReadAsStringAsync());

                foreach (var value in manualStreamViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get SdsStreamViewMap
                Console.WriteLine("We can query SDS to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:");

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}/Map");

                CheckIfResponseWasSuccessful(response);

                SdsStreamViewMap sdsStreamViewMap =
                    JsonConvert.DeserializeObject<SdsStreamViewMap>(await response.Content.ReadAsStringAsync());

                PrintStreamViewMapProperties(sdsStreamViewMap);

                Console.WriteLine("Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}/Map");

                CheckIfResponseWasSuccessful(response);

                sdsStreamViewMap = JsonConvert.DeserializeObject<SdsStreamViewMap>(await response.Content.ReadAsStringAsync());

                PrintStreamViewMapProperties(sdsStreamViewMap);

                // Step 14
                // Update Stream Type based on SdsStreamView
                Console.WriteLine("We will now update the stream type based on the streamview");
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/Last");
                CheckIfResponseWasSuccessful(response);
                WaveData lastData = JsonConvert.DeserializeObject<WaveData>(await response.Content.ReadAsStringAsync());

                response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Type?streamViewId={AutoStreamViewId}", null);
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}");
                CheckIfResponseWasSuccessful(response);

                SdsStream steamnew = JsonConvert.DeserializeObject<SdsStream>(await response.Content.ReadAsStringAsync());

                WaveDataTarget lastDataUpdated = JsonConvert.DeserializeObject<WaveDataTarget>(await response.Content.ReadAsStringAsync());

                Console.WriteLine($"The new type id {steamnew.TypeId} compared to the original one {waveStream.TypeId}.");
                Console.WriteLine();

                // Step 15
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types");
                CheckIfResponseWasSuccessful(response);
                List<SdsType> types = JsonConvert.DeserializeObject<List<SdsType>>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types?query=Id:*Target*");
                CheckIfResponseWasSuccessful(response);
                List<SdsType> typesFiltered = JsonConvert.DeserializeObject<List<SdsType>>(await response.Content.ReadAsStringAsync());

                Console.WriteLine($"The number of types returned without filtering: {types.Count}.  With filtering {typesFiltered.Count}.");
                Console.WriteLine();

                // Step 16
                // tags and metadata
                Console.WriteLine("Let's add some Tags and Metadata to our stream:");
                var tags = new List<string> { "waves", "periodic", "2018", "validated" };
                var metadata = new Dictionary<string, string>() { { "Region", "North America" }, { "Country", "Canada" }, { "Province", "Quebec" } };

                response =
                    await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Tags",
                    new StringContent(JsonConvert.SerializeObject(tags)));
                CheckIfResponseWasSuccessful(response);

                response =
                    await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata",
                    new StringContent(JsonConvert.SerializeObject(metadata)));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Tags");
                CheckIfResponseWasSuccessful(response);

                tags = JsonConvert.DeserializeObject<List<string>>(await response.Content.ReadAsStringAsync());

                Console.WriteLine();
                Console.WriteLine($"Tags now associated with {StreamId}:");
                foreach (var tag in tags)
                {
                    Console.WriteLine(tag);
                }
                Console.WriteLine();
                Console.WriteLine($"Metadata now associated with {StreamId}:");

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata/Region");
                CheckIfResponseWasSuccessful(response);

                var region = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata/Country");
                CheckIfResponseWasSuccessful(response);

                var country = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata/Province");
                CheckIfResponseWasSuccessful(response);

                var province = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                Console.WriteLine("Metadata key Region: " + region);
                Console.WriteLine("Metadata key Country: " + country);
                Console.WriteLine("Metadata key Province: " + province);
                Console.WriteLine();

                Console.WriteLine("Deleting values from the SdsStream");

                // Step 17
                // delete one event
                response = await httpClient.DeleteAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?index=0");
                CheckIfResponseWasSuccessful(response);

                // delete all Events
                response = await httpClient.DeleteAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex=40");
                CheckIfResponseWasSuccessful(response);
                response = await httpClient.GetAsync(
                   $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data?startIndex=0&endIndex=40");
                retrievedList = JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                if (retrievedList.Count == 0)
                {
                    Console.WriteLine("All values deleted successfully!");
                }
                Console.WriteLine();

                // Step 18
                Console.WriteLine("Creating a SdsStream with secondary index");

                SdsStreamIndex measurementIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = waveType.Properties.First(p => p.Id.Equals("Radians")).Id
                };

                SdsStream waveStreamSecond = new SdsStream
                {
                    Id = streamIdSecondary,
                    Name = "WaveStream_Secondary",
                    TypeId = waveType.Id,
                    Indexes = new List<SdsStreamIndex>()
                  {
                      measurementIndex
                  }

                };
                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStreamSecond.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStreamSecond)));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStreamSecond.Id}");
                CheckIfResponseWasSuccessful(response);

                waveStreamSecond = JsonConvert.DeserializeObject<SdsStream>(await response.Content.ReadAsStringAsync());

                Console.WriteLine($"Secondary indexes on streams. {waveStream.Id}:{waveStream.Indexes?.Count()}. {waveStreamSecond.Id}:{waveStreamSecond.Indexes.Count()}.");
                Console.WriteLine();

                Console.WriteLine("Modifying a stream to have a secondary index.");

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}");
                CheckIfResponseWasSuccessful(response);

                waveStream = JsonConvert.DeserializeObject<SdsStream>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveStream.TypeId}");
                CheckIfResponseWasSuccessful(response);

                waveType = JsonConvert.DeserializeObject<SdsType>(await response.Content.ReadAsStringAsync());

                measurementIndex = new SdsStreamIndex()
                {
                    SdsTypePropertyId = waveType.Properties.First(p => p.Id.Equals("RadiansTarget")).Id
                };

                waveStream.Indexes = new List<SdsStreamIndex>() { measurementIndex };

                response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                CheckIfResponseWasSuccessful(response);
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}");
                CheckIfResponseWasSuccessful(response);
                waveStream = JsonConvert.DeserializeObject<SdsStream>(await response.Content.ReadAsStringAsync());

                Console.WriteLine("Removing a secondary index from a stream.");

                waveStreamSecond.Indexes = null;

                response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStreamSecond.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStreamSecond)));
                CheckIfResponseWasSuccessful(response);
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStreamSecond.Id}");
                CheckIfResponseWasSuccessful(response);
                waveStreamSecond = JsonConvert.DeserializeObject<SdsStream>(await response.Content.ReadAsStringAsync());
                
                var count = 0;
                if (waveStream.Indexes != null)
                {
                    count = waveStream.Indexes.Count();
                }

                var count2 = 0;
                if (waveStreamSecond.Indexes != null)
                {
                    count2 = waveStreamSecond.Indexes.Count();
                }

                Console.WriteLine($"Secondary indexes on streams. {waveStream.Id}:{count}. {waveStreamSecond.Id}:{count2}.");
                Console.WriteLine();
                
                // Step 19
                Console.WriteLine("Creating a SdsType with a compound index");
                SdsType waveCompound = BuildWaveDataCompoundType(compoundTypeId);
                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveCompound.Id}",
                        new StringContent(JsonConvert.SerializeObject(waveCompound)));
                CheckIfResponseWasSuccessful(response);

                // create an SdsStream
                Console.WriteLine("Creating an SdsStream off of type with compound index");
                var streamCompound = new SdsStream
                {
                    Id = streamIdCompound,
                    Name = "Wave Data Sample",
                    TypeId = waveCompound.Id,
                    Description = "This is a sample SdsStream for storing WaveData type measurements"
                };

                response = await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}",
                    new StringContent(JsonConvert.SerializeObject(streamCompound)));
                CheckIfResponseWasSuccessful(response);

                // Step 20
                Console.WriteLine("Inserting data");

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(1, 10) })));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(2, 2) })));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(3, 2) })));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(10, 3) })));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(10, 8) })));
                CheckIfResponseWasSuccessful(response);

                response = await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data", new StringContent(JsonConvert.SerializeObject(new List<WaveDataCompound>() { GetWaveMultiplier(10, 10) })));
                CheckIfResponseWasSuccessful(response);
                
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data/Last");
                CheckIfResponseWasSuccessful(response);
                WaveDataCompound lastCompound = JsonConvert.DeserializeObject<WaveDataCompound>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data/First");
                CheckIfResponseWasSuccessful(response);
                WaveDataCompound firstCompound = JsonConvert.DeserializeObject<WaveDataCompound>(await response.Content.ReadAsStringAsync());

                var startIndex = "2|1";
                var endIndex = "10|8";
                response = await httpClient.GetAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamCompound.Id}/Data/Transform?startIndex={startIndex}&endIndex={endIndex}");
                CheckIfResponseWasSuccessful(response);
                List<WaveDataCompound> data = JsonConvert.DeserializeObject<List<WaveDataCompound>>(await response.Content.ReadAsStringAsync());                

                Console.WriteLine($"First data: {firstCompound.ToString()}.  Latest data: {lastCompound.ToString()}.");
                Console.WriteLine();

                Console.WriteLine("Window Data:");

                foreach (var evnt in data)
                {
                    Console.WriteLine(evnt.ToString());
                }
                
            }
            catch (Exception e)
            {
                success = false;
                Console.WriteLine(e.Message);
                toThrow = e;
            }
            finally
            {
                // Step 21
                Console.WriteLine();
                Console.WriteLine("Cleaning up");
                // Delete the stream, types and streamViews
                Console.WriteLine("Deleting stream");
                RunInTryCatch(httpClient.DeleteAsync, $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}");
                RunInTryCatch(httpClient.DeleteAsync, $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamIdSecondary}");
                RunInTryCatch(httpClient.DeleteAsync, $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{streamIdCompound}");
                Console.WriteLine("Deleting streamViews");
                RunInTryCatch(httpClient.DeleteAsync, ($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}"));
                RunInTryCatch(httpClient.DeleteAsync,($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}"));
                Console.WriteLine("Deleting types");
                RunInTryCatch(httpClient.DeleteAsync,($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TypeId}"));
                RunInTryCatch(httpClient.DeleteAsync, ($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{compoundTypeId}"));
                RunInTryCatch(httpClient.DeleteAsync,($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetTypeId}"));
                RunInTryCatch(httpClient.DeleteAsync,($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetIntTypeId}"));
                Console.WriteLine("done");
            }

            if (test && !success)
                throw toThrow;
            return success;
        }

        private static void CheckIfResponseWasSuccessful(HttpResponseMessage response)
        {
            //if support is needed please know the Operation-ID header information for support purposes (it is included in the exception below automatically too)
            //string operationId = response.Headers.GetValues("Operation-Id").First();

            if (!response.IsSuccessStatusCode)
            {
                throw new HttpRequestException(response.ToString());
            }
        }

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an error
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        private static void RunInTryCatch(Func<string, Task> methodToRun, string value)
        {
            try
            {
                methodToRun(value).Wait(10000);
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

        private static SdsType BuildWaveDataType(string id)
        {
            SdsType intSdsType = new SdsType
            {
                Id = "intSdsType",
                SdsTypeCode = SdsTypeCode.Int32
            };

            SdsType doubleSdsType = new SdsType
            {
                Id = "doubleSdsType",
                SdsTypeCode = SdsTypeCode.Double
            };

            SdsTypeProperty orderProperty = new SdsTypeProperty
            {
                Id = "Order",
                SdsType = intSdsType,
                IsKey = true
            };

            SdsTypeProperty tauProperty = new SdsTypeProperty
            {
                Id = "Tau",
                SdsType = doubleSdsType
            };

            SdsTypeProperty radiansProperty = new SdsTypeProperty
            {
                Id = "Radians",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinProperty = new SdsTypeProperty
            {
                Id = "Sin",
                SdsType = doubleSdsType
            };

            SdsTypeProperty cosProperty = new SdsTypeProperty
            {
                Id = "Cos",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanProperty = new SdsTypeProperty
            {
                Id = "Tan",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinhProperty = new SdsTypeProperty
            {
                Id = "Sinh",
                SdsType = doubleSdsType
            };

            SdsTypeProperty coshProperty = new SdsTypeProperty
            {
                Id = "Cosh",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanhProperty = new SdsTypeProperty
            {
                Id = "Tanh",
                SdsType = doubleSdsType
            };

            SdsType waveType = new SdsType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<SdsTypeProperty>
                {
                    orderProperty,
                    tauProperty,
                    radiansProperty,
                    sinProperty,
                    cosProperty,
                    tanProperty,
                    sinhProperty,
                    coshProperty,
                    tanhProperty
                },
                SdsTypeCode = SdsTypeCode.Object
            };

            return waveType;
        }

        private static SdsType BuildWaveDataTargetType(string id)
        {
            SdsType intSdsType = new SdsType
            {
                Id = "intSdsType",
                SdsTypeCode = SdsTypeCode.Int32
            };

            SdsType doubleSdsType = new SdsType
            {
                Id = "doubleSdsType",
                SdsTypeCode = SdsTypeCode.Double
            };

            SdsTypeProperty orderTargetProperty = new SdsTypeProperty
            {
                Id = "OrderTarget",
                SdsType = intSdsType,
                IsKey = true
            };

            SdsTypeProperty tauTargetProperty = new SdsTypeProperty
            {
                Id = "TauTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty radiansTargetProperty = new SdsTypeProperty
            {
                Id = "RadiansTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinTargetProperty = new SdsTypeProperty
            {
                Id = "SinTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty cosTargetProperty = new SdsTypeProperty
            {
                Id = "CosTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanTargetProperty = new SdsTypeProperty
            {
                Id = "TanTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinhTargetProperty = new SdsTypeProperty
            {
                Id = "SinhTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty coshTargetProperty = new SdsTypeProperty
            {
                Id = "CoshTarget",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanhTargetProperty = new SdsTypeProperty
            {
                Id = "TanhTarget",
                SdsType = doubleSdsType
            };

            SdsType waveType = new SdsType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<SdsTypeProperty>
                {
                    orderTargetProperty,
                    tauTargetProperty,
                    radiansTargetProperty,
                    sinTargetProperty,
                    cosTargetProperty,
                    tanTargetProperty,
                    sinhTargetProperty,
                    coshTargetProperty,
                    tanhTargetProperty
                },
                SdsTypeCode = SdsTypeCode.Object
            };

            return waveType;
        }

        private static SdsType BuildWaveDataTargetIntType(string id)
        {
            SdsType intSdsType = new SdsType
            {
                Id = "intSdsType",
                SdsTypeCode = SdsTypeCode.Int32
            };

            SdsTypeProperty orderTargetProperty = new SdsTypeProperty
            {
                Id = "OrderTarget",
                SdsType = intSdsType,
                IsKey = true
            };

            SdsTypeProperty sinIntProperty = new SdsTypeProperty
            {
                Id = "SinInt",
                SdsType = intSdsType
            };

            SdsTypeProperty cosIntProperty = new SdsTypeProperty
            {
                Id = "CosInt",
                SdsType = intSdsType
            };

            SdsTypeProperty tanIntProperty = new SdsTypeProperty
            {
                Id = "TanInt",
                SdsType = intSdsType
            };

            SdsType waveTargetIntType = new SdsType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<SdsTypeProperty>
                {
                    orderTargetProperty,
                    sinIntProperty,
                    cosIntProperty,
                    tanIntProperty,
                },
                SdsTypeCode = SdsTypeCode.Object
            };

            return waveTargetIntType;
        }

        private static SdsType BuildWaveDataCompoundType(string id)
        {
            SdsType intSdsType = new SdsType
            {
                Id = "intSdsType",
                SdsTypeCode = SdsTypeCode.Int32
            };

            SdsType doubleSdsType = new SdsType
            {
                Id = "doubleSdsType",
                SdsTypeCode = SdsTypeCode.Double
            };

            SdsTypeProperty orderProperty = new SdsTypeProperty
            {
                Id = "Order",
                SdsType = intSdsType,
                IsKey = true,
                Order = 0
            };

            SdsTypeProperty multiplierProperty = new SdsTypeProperty
            {
                Id = "Multiplier",
                SdsType = intSdsType,
                IsKey = true,
                Order = 1
            };

            SdsTypeProperty tauProperty = new SdsTypeProperty
            {
                Id = "Tau",
                SdsType = doubleSdsType
            };

            SdsTypeProperty radiansProperty = new SdsTypeProperty
            {
                Id = "Radians",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinProperty = new SdsTypeProperty
            {
                Id = "Sin",
                SdsType = doubleSdsType
            };

            SdsTypeProperty cosProperty = new SdsTypeProperty
            {
                Id = "Cos",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanProperty = new SdsTypeProperty
            {
                Id = "Tan",
                SdsType = doubleSdsType
            };

            SdsTypeProperty sinhProperty = new SdsTypeProperty
            {
                Id = "Sinh",
                SdsType = doubleSdsType
            };

            SdsTypeProperty coshProperty = new SdsTypeProperty
            {
                Id = "Cosh",
                SdsType = doubleSdsType
            };

            SdsTypeProperty tanhProperty = new SdsTypeProperty
            {
                Id = "Tanh",
                SdsType = doubleSdsType
            };

            SdsType waveType = new SdsType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<SdsTypeProperty>
                {
                    orderProperty,
                    multiplierProperty,
                    tauProperty,
                    radiansProperty,
                    sinProperty,
                    cosProperty,
                    tanProperty,
                    sinhProperty,
                    coshProperty,
                    tanhProperty
                },
                SdsTypeCode = SdsTypeCode.Object
            };

            return waveType;
        }

        private static WaveData GetWave(int order, int range, double multiplier)
        {
            var radians = order * (Math.PI / 32);

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
                Tanh = multiplier * Math.Tanh(radians),
            };
        }

        private static WaveDataCompound GetWaveMultiplier(int order, int multiplier)
        {
            Random random = new Random();
            var radians = (random.Next(1, 100) * 2 * Math.PI) % 2 * Math.PI;

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