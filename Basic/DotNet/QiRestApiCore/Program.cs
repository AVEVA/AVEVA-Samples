using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;

namespace QiRestApiCore
{
    class Program
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
            string tenantId = configuration["Tenant"];
            string namespaceId = configuration["Namespace"];
            string address = configuration["Address"];
            string resource = configuration["Resource"];
            string appId = configuration["AppId"];
            string appKey = configuration["AppKey"];
            string aadInstanceFormat = configuration["AADInstanceFormat"];
			
			// ==== Metadata IDs ====
			string StreamId = "WaveStreamId";
			string TypeId = "WaveDataTypeId";
			string BehaviorId = "WaveStreamBehaviorId";
			string TargetTypeId = "WaveDataTargetTypeId";
			string TargetIntTypeId = "WaveDataTargetIntTypeId";
			string AutoViewId = "WaveDataAutoViewId";
			string ManualViewId = "WaveDataManualViewId";

            QiSecurityHandler securityHandler =
                new QiSecurityHandler(resource, tenantId, aadInstanceFormat, appId, appKey);
            HttpClient httpClient = new HttpClient(securityHandler)
            {
                BaseAddress = new Uri(address)
            };

            Console.WriteLine(@"-------------------------------------------------------");
            Console.WriteLine(@"________  ._______________________ ____________________");
            Console.WriteLine(@"\_____  \ |__\______   \_   _____//   _____/\__    ___/");
            Console.WriteLine(@" /  / \  \|  ||       _/|    __)_ \_____  \   |    |   ");
            Console.WriteLine(@"/   \_/.  \  ||    |   \|        \/        \  |    |   ");
            Console.WriteLine(@"\_____\ \_/__||____|_  /_______  /_______  /  |____|   ");
            Console.WriteLine(@"       \__>          \/        \/        \/            ");
            Console.WriteLine(@"-------------------------------------------------------");
            Console.WriteLine();
            Console.WriteLine($"Qi endpoint at {address}");
            Console.WriteLine();

            try
            {
                // create a QiType
                Console.WriteLine("Creating a QiType");
                QiType waveType = BuildWaveDataType(TypeId);
                HttpResponseMessage response =
                    await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{waveType.Id}",
                        new StringContent(JsonConvert.SerializeObject(waveType)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // create a QiStream
                Console.WriteLine("Creating a QiStream");
                QiStream waveStream = new QiStream
                {
                    Id = StreamId,
                    Name = "WaveStream",
                    TypeId = waveType.Id
                };
                response = await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/InsertValue",
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/InsertValues",
                    new StringContent(JsonConvert.SerializeObject(waves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException();
                }

                // get last event
                Console.WriteLine("Getting latest event");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetLastValue");
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex=0&endIndex={waves[waves.Count - 1].Order}");
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/UpdateValue",
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/UpdateValues",
                    new StringContent(JsonConvert.SerializeObject(updateWaves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("Getting updated events");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/ReplaceValue",
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
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/ReplaceValues",
                new StringContent(JsonConvert.SerializeObject(replaceEvents)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("Getting replaced events");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex={updateWaves[0].Order}&endIndex={updateWaves[updateWaves.Count - 1].Order}");
                retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Total events found: {retrievedList.Count}");
                foreach (var evnt in retrievedList)
                {
                    Console.WriteLine(evnt.ToString());
                }
                Console.WriteLine();

                // Stream behaviors
                Console.WriteLine("QiStreamBehaviors determine whether Qi interpolates or extrapolates data at the requested index location");
                Console.WriteLine();

                // Stream behaviors modify retrieval.  We will retrieve three events using the default behavior, Continuous
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> rangeValuesContinuous =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine("Default (Continuous) stream behavior, requesting data starting at index location '1', Qi will interpolate this value:");
                foreach (var waveData in rangeValuesContinuous)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}");
                }
                Console.WriteLine();

                // create a Discrete stream behavior
                QiStreamBehavior waveStreamBehavior = new QiStreamBehavior
                {
                    Id = BehaviorId,
                    Mode = QiStreamMode.Discrete,
                    Name = "WaveStreamBehavior"
                };
                response = await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Behaviors/{BehaviorId}",
                    new StringContent(JsonConvert.SerializeObject(waveStreamBehavior)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // update the stream
                waveStream.BehaviorId = waveStreamBehavior.Id;
                response = await httpClient.PutAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                Console.WriteLine("Discrete stream behavior, Qi does not interpolate and returns the data starting at the next index location containing data:");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> rangeValuesDiscrete =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                foreach (var waveData in rangeValuesDiscrete)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}");
                }
                Console.WriteLine();

                // Stream views
                Console.WriteLine("QiViews");

                // create target types
                var targetType = BuildWaveDataTargetType(TargetTypeId);
                var targetIntType = BuildWaveDataTargetIntType(TargetIntTypeId);

                HttpResponseMessage targetTypeResponse =
                    await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetTypeId}",
                    new StringContent(JsonConvert.SerializeObject(targetType)));
                if (!targetTypeResponse.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                HttpResponseMessage targetIntTypeResponse =
                    await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetIntTypeId}",
                    new StringContent(JsonConvert.SerializeObject(targetIntType)));
                if (!targetIntTypeResponse.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // create views
                var autoView = new QiView()
                {
                    Id = AutoViewId,
                    SourceTypeId = TypeId,
                    TargetTypeId = TargetTypeId
                };

                // create explicit mappings 
                var vp1 = new QiViewProperty() { SourceId = "Order", TargetId = "OrderTarget" };
                var vp2 = new QiViewProperty() { SourceId = "Sin", TargetId = "SinInt" };
                var vp3 = new QiViewProperty() { SourceId = "Cos", TargetId = "CosInt" };
                var vp4 = new QiViewProperty() { SourceId = "Tan", TargetId = "TanInt" };

                var manualView = new QiView()
                {
                    Id = ManualViewId,
                    SourceTypeId = TypeId,
                    TargetTypeId = TargetIntTypeId,
                    Properties = new List<QiViewProperty>() { vp1, vp2, vp3, vp4 }
                };

                response =
                    await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{AutoViewId}",
                    new StringContent(JsonConvert.SerializeObject(autoView)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                response =
                     await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{ManualViewId}",
                     new StringContent(JsonConvert.SerializeObject(manualView)));
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

                // get data with autoview
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}&viewId={AutoViewId}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                List<WaveDataTarget> autoViewData =
                    JsonConvert.DeserializeObject<List<WaveDataTarget>>(await response.Content.ReadAsStringAsync());

                Console.WriteLine("Specifying a view with a QiType of the same shape returns values that are automatically mapped to the target QiType's properties:");

                foreach (var value in autoViewData)
                {
                    Console.WriteLine($"SinTarget: {value.SinTarget} CosTarget: {value.CosTarget} TanTarget: {value.TanTarget}");
                }
                Console.WriteLine();

                Console.WriteLine("QiViews can also convert certain types of data, here we return integers where the original values were doubles:");

                // get data with manualview
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={1}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}&viewId={ManualViewId}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                List<WaveDataInteger> manualViewData =
                    JsonConvert.DeserializeObject<List<WaveDataInteger>>(await response.Content.ReadAsStringAsync());

                foreach (var value in manualViewData)
                {
                    Console.WriteLine($"SinInt: {value.SinInt} CosInt: {value.CosInt} TanInt: {value.TanInt}");
                }
                Console.WriteLine();

                // get QiViewMap
                Console.WriteLine("We can query Qi to return the QiViewMap for our QiView, here is the one generated automatically:");

                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{AutoViewId}/Map");

                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                QiViewMap qiViewMap =
                    JsonConvert.DeserializeObject<QiViewMap>(await response.Content.ReadAsStringAsync());

                PrintViewMapProperties(qiViewMap);

                Console.WriteLine("Here is our explicit mapping, note QiViewMap will return all properties of the Source Type, even those without a corresponding Target property:");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{ManualViewId}/Map");

                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                qiViewMap = JsonConvert.DeserializeObject<QiViewMap>(await response.Content.ReadAsStringAsync());

                PrintViewMapProperties(qiViewMap);

                Console.WriteLine("Deleting values from the QiStream");

                // delete one event
                response = await httpClient.DeleteAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/RemoveValue?index=0");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // delete all Events
                response = await httpClient.DeleteAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/RemoveWindowValues?startIndex=0&endIndex=40");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                response = await httpClient.GetAsync(
                   $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex=0&endIndex=40");
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
                // Delete the stream, types, views and behavior
                Console.WriteLine("Deleteing stream");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}");
                Console.WriteLine("Deleteing types");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TypeId}");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetTypeId}");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TargetIntTypeId}");
                Console.WriteLine("Deleteing views");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{AutoViewId}");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Views/{ManualViewId}");
                Console.WriteLine("Deleteing behavior");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Behaviors/{BehaviorId}");
                Console.WriteLine("done");
            }

            Console.ReadKey();
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

        private static QiType BuildWaveDataType(string id)
        {
            QiType intQiType = new QiType
            {
                Id = "intQiType",
                QiTypeCode = QiTypeCode.Int32
            };

            QiType doubleQiType = new QiType
            {
                Id = "doubleQiType",
                QiTypeCode = QiTypeCode.Double
            };

            QiTypeProperty orderProperty = new QiTypeProperty
            {
                Id = "Order",
                QiType = intQiType,
                IsKey = true
            };

            QiTypeProperty tauProperty = new QiTypeProperty
            {
                Id = "Tau",
                QiType = doubleQiType
            };

            QiTypeProperty radiansProperty = new QiTypeProperty
            {
                Id = "Radians",
                QiType = doubleQiType
            };

            QiTypeProperty sinProperty = new QiTypeProperty
            {
                Id = "Sin",
                QiType = doubleQiType
            };

            QiTypeProperty cosProperty = new QiTypeProperty
            {
                Id = "Cos",
                QiType = doubleQiType
            };

            QiTypeProperty tanProperty = new QiTypeProperty
            {
                Id = "Tan",
                QiType = doubleQiType
            };

            QiTypeProperty sinhProperty = new QiTypeProperty
            {
                Id = "Sinh",
                QiType = doubleQiType
            };

            QiTypeProperty coshProperty = new QiTypeProperty
            {
                Id = "Cosh",
                QiType = doubleQiType
            };

            QiTypeProperty tanhProperty = new QiTypeProperty
            {
                Id = "Tanh",
                QiType = doubleQiType
            };

            QiType waveType = new QiType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<QiTypeProperty>
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
                QiTypeCode = QiTypeCode.Object
            };

            return waveType;
        }

        private static QiType BuildWaveDataTargetType(string id)
        {
            QiType intQiType = new QiType
            {
                Id = "intQiType",
                QiTypeCode = QiTypeCode.Int32
            };

            QiType doubleQiType = new QiType
            {
                Id = "doubleQiType",
                QiTypeCode = QiTypeCode.Double
            };

            QiTypeProperty orderTargetProperty = new QiTypeProperty
            {
                Id = "OrderTarget",
                QiType = intQiType,
                IsKey = true
            };

            QiTypeProperty tauTargetProperty = new QiTypeProperty
            {
                Id = "TauTarget",
                QiType = doubleQiType
            };

            QiTypeProperty radiansTargetProperty = new QiTypeProperty
            {
                Id = "RadiansTarget",
                QiType = doubleQiType
            };

            QiTypeProperty sinTargetProperty = new QiTypeProperty
            {
                Id = "SinTarget",
                QiType = doubleQiType
            };

            QiTypeProperty cosTargetProperty = new QiTypeProperty
            {
                Id = "CosTarget",
                QiType = doubleQiType
            };

            QiTypeProperty tanTargetProperty = new QiTypeProperty
            {
                Id = "TanTarget",
                QiType = doubleQiType
            };

            QiTypeProperty sinhTargetProperty = new QiTypeProperty
            {
                Id = "SinhTarget",
                QiType = doubleQiType
            };

            QiTypeProperty coshTargetProperty = new QiTypeProperty
            {
                Id = "CoshTarget",
                QiType = doubleQiType
            };

            QiTypeProperty tanhTargetProperty = new QiTypeProperty
            {
                Id = "TanhTarget",
                QiType = doubleQiType
            };

            QiType waveType = new QiType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<QiTypeProperty>
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
                QiTypeCode = QiTypeCode.Object
            };

            return waveType;
        }

        private static QiType BuildWaveDataTargetIntType(string id)
        {
            QiType intQiType = new QiType
            {
                Id = "intQiType",
                QiTypeCode = QiTypeCode.Int32
            };

            QiTypeProperty orderTargetProperty = new QiTypeProperty
            {
                Id = "OrderTarget",
                QiType = intQiType,
                IsKey = true
            };

            QiTypeProperty sinIntProperty = new QiTypeProperty
            {
                Id = "SinInt",
                QiType = intQiType
            };

            QiTypeProperty cosIntProperty = new QiTypeProperty
            {
                Id = "CosInt",
                QiType = intQiType
            };

            QiTypeProperty tanIntProperty = new QiTypeProperty
            {
                Id = "TanInt",
                QiType = intQiType
            };

            QiType waveTargetIntType = new QiType
            {
                Id = id,
                Name = "WaveData",
                Properties = new List<QiTypeProperty>
                {
                    orderTargetProperty,
                    sinIntProperty,
                    cosIntProperty,
                    tanIntProperty,
                },
                QiTypeCode = QiTypeCode.Object
            };

            return waveTargetIntType;
        }

        private static WaveData GetWave(int order, int range, double multiplier)
        {
            var radians = order / range * 2 * Math.PI;

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