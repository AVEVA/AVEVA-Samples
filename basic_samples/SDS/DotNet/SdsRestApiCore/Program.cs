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
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;

namespace SdsRestApiCore
{
    class Program
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
            Console.WriteLine($"Sds endpoint at {resource}");
            Console.WriteLine();

            try
            {
                // create a SdsType
                Console.WriteLine("Creating a SdsType");
                SdsType waveType = BuildWaveDataType(TypeId);
                HttpResponseMessage response =
                    await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveType.Id}",
                        new StringContent(JsonConvert.SerializeObject(waveType)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

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
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // insert data
                Console.WriteLine("Inserting data");

                // insert a single event
                WaveData wave = GetWave(0, 1, 2.0);
                response = await httpClient.PostAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/InsertValue",
                    new StringContent(JsonConvert.SerializeObject(wave)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // insert a list of events
                List<WaveData> waves = new List<WaveData>();
                for (int i = 2; i < 20; i += 2)
                {
                    WaveData newEvent = GetWave(i, 2, 2.0);
                    waves.Add(newEvent);
                }
                response = await httpClient.PostAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/InsertValues",
                    new StringContent(JsonConvert.SerializeObject(waves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException();
                }

                // get last event
                Console.WriteLine("Getting latest event");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetLastValue");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                WaveData retrieved =
                    JsonConvert.DeserializeObject<WaveData>(await response.Content.ReadAsStringAsync());
                Console.WriteLine(retrieved.ToString());
                Console.WriteLine();

                // get all events
                Console.WriteLine("Getting all events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex=0&endIndex={waves[waves.Count - 1].Order}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // update events
                Console.WriteLine("Updating events");

                // update one event
                var updateEvent = retrieved;
                updateEvent.Sin = 1/2.0;
                updateEvent.Cos = Math.Sqrt(3)/2;
                updateEvent.Tan = 1;

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/UpdateValue",
                    new StringContent(JsonConvert.SerializeObject(updateEvent)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // update all events, adding ten more
                List<WaveData> updateWaves = new List<WaveData>();
                for (int i = 0; i < 40; i += 2)
                {
                    WaveData newEvent = GetWave(i, 4, 6.0);
                    updateWaves.Add(newEvent);
                }

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/UpdateValues",
                    new StringContent(JsonConvert.SerializeObject(updateWaves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("Getting updated events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
                retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // replacing events
                Console.WriteLine("Replacing events");

                // replace one event
                var replaceEvent = retrievedList[0];
                replaceEvent.Sin = 4*(Math.Sqrt(2)/2);
                replaceEvent.Cos = 4*(Math.Sqrt(2)/2);
                replaceEvent.Tan = 4;

                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/ReplaceValue",
                new StringContent(JsonConvert.SerializeObject(replaceEvent)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // replace all events
                var replaceEvents = retrievedList;
                foreach (var evnt in replaceEvents)
                {
                    evnt.Sin = 6 * (Math.Sqrt(2) / 2);
                    evnt.Cos = 6 * (Math.Sqrt(2) / 2);
                    evnt.Tan = 6;
                }
                response = await httpClient.PutAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/ReplaceValues",
                new StringContent(JsonConvert.SerializeObject(replaceEvents)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("Getting replaced events");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
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
                Console.WriteLine("Sds can interpolate or extrapolate data at an index location where data does not explicitly exist:");
                Console.WriteLine();

                // We will retrieve three events using the default behavior, Continuous
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> rangeValuesContinuous =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine("Default (Continuous) stream behavior, requesting data starting at index location '1', Sds will interpolate this value:");
                foreach (var waveData in rangeValuesContinuous)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}, Cos: {waveData.Cos}");
                }
                Console.WriteLine();

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
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("We can override this behavior on a property by property basis, here we override the Radians property instructing Sds not to interpolate.");
                Console.WriteLine("Sds will now return the default value for the data type:");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> rangeValuesDiscrete =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                foreach (var waveData in rangeValuesDiscrete)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}, Cos: {waveData.Cos}");
                }
                Console.WriteLine();

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
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                response =
                     await httpClient.PostAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}",
                     new StringContent(JsonConvert.SerializeObject(manualStreamView)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
            
                Console.WriteLine("Here is some of our data as it is stored on the server:");
                foreach (var evnt in rangeValuesDiscrete)
                {
                    Console.WriteLine($"Sin: {evnt.Sin}, Cos: {evnt.Cos}, Tan {evnt.Tan}");
                }
                Console.WriteLine();

                // get data with autoStreamView
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}&streamViewId={AutoStreamViewId}");

                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

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
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={SdsBoundaryType.ExactOrCalculated}&streamViewId={ManualStreamViewId}");

                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                List<WaveDataInteger> manualStreamViewData =
                    JsonConvert.DeserializeObject<List<WaveDataInteger>>(await response.Content.ReadAsStringAsync());

                foreach (var value in manualStreamViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get SdsStreamViewMap
                Console.WriteLine("We can query Sds to return the SdsStreamViewMap for our SdsStreamView, here is the one generated automatically:");

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}/Map");


                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                SdsStreamViewMap sdsStreamViewMap =
                    JsonConvert.DeserializeObject<SdsStreamViewMap>(await response.Content.ReadAsStringAsync());

                PrintStreamViewMapProperties(sdsStreamViewMap);

                Console.WriteLine("Here is our explicit mapping, note SdsStreamViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}/Map");

                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                sdsStreamViewMap = JsonConvert.DeserializeObject<SdsStreamViewMap>(await response.Content.ReadAsStringAsync());

                PrintStreamViewMapProperties(sdsStreamViewMap);

                // tags and metadata
                Console.WriteLine("Let's add some Tags and Metadata to our stream:");
                var tags = new List<string> { "waves", "periodic", "2018", "validated" };
                var metadata = new Dictionary<string, string>() { { "Region", "North America" }, { "Country", "Canada" }, { "Province", "Quebec" } };
                
                response =
                    await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Tags",
                    new StringContent(JsonConvert.SerializeObject(tags)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                response =
                    await httpClient.PutAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata",
                    new StringContent(JsonConvert.SerializeObject(metadata)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Tags");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

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
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                var region = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata/Country");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                var country = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                response = await httpClient.GetAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}/Metadata/Province");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                var province = JsonConvert.DeserializeObject<string>(await response.Content.ReadAsStringAsync());

                Console.WriteLine("Metadata key Region: " + region);
                Console.WriteLine("Metadata key Country: " + country);
                Console.WriteLine("Metadata key Province: " + province);

                Console.WriteLine();
              
                Console.WriteLine("Deleting values from the SdsStream");

                // delete one event
                response = await httpClient.DeleteAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/RemoveValue?index=0");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // delete all Events
                response = await httpClient.DeleteAsync(
                    $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/RemoveWindowValues?startIndex=0&endIndex=40");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                response = await httpClient.GetAsync(
                   $"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex=0&endIndex=40");
                retrievedList = JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                if (retrievedList.Count == 0)
                {
                    Console.WriteLine("All values deleted successfully!");
                }
                Console.WriteLine();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
            finally
            {
                Console.WriteLine("Cleaning up");
                // Delete the stream, types and streamViews
                Console.WriteLine("Deleteing stream");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}");
                Console.WriteLine("Deleteing streamViews");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{AutoStreamViewId}");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/StreamViews/{ManualStreamViewId}");
                Console.WriteLine("Deleteing types");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TypeId}");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetTypeId}");
                await httpClient.DeleteAsync($"api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetIntTypeId}");

                Console.WriteLine("done");
            }

            Console.ReadKey();
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

        private static WaveData GetWave(int order, int range, double multiplier)
        {
            Random random = new Random();
            var radians = ( random.Next(1,100)* 2 * Math.PI) % 2*Math.PI;

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
    }
}
