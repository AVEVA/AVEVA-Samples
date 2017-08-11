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
        private const string StreamId = "WaveStreamId";
        private const string TypeId = "WaveDataTypeId";
        private const string BehaviorId = "WaveStreamBehaviorId";

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

            string tenantId = configuration["Tenant"];
            string namespaceId = configuration["Namespace"];
            string address = configuration["Address"];
            string resource = configuration["Resource"];
            string appId = configuration["AppId"];
            string appKey = configuration["AppKey"];
            string aadInstanceFormat = configuration["AADInstanceFormat"];

            QiSecurityHandler securityHandler =
                new QiSecurityHandler(resource, tenantId, aadInstanceFormat, appId, appKey);
            HttpClient httpClient = new HttpClient(securityHandler)
            {
                BaseAddress = new Uri(address)
            };

            try
            {
                // to write data, we need a QiType and a QiStream
                QiType waveType = BuildWaveDataType(TypeId);
                HttpResponseMessage response =
                    await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types",
                        new StringContent(JsonConvert.SerializeObject(waveType)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                QiStream waveStream = new QiStream
                {
                    Id = StreamId,
                    Name = "WaveStream",
                    TypeId = waveType.Id
                };
                response = await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                if (response.StatusCode == HttpStatusCode.Found)
                {
                    response = await httpClient.GetAsync(
                        $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}");
                    waveStream = JsonConvert.DeserializeObject<QiStream>(await response.Content.ReadAsStringAsync());
                }
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // insert and read one value
                WaveData wave = GetWave(1, 1, 2.0);
                response = await httpClient.PostAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/InsertValue",
                    new StringContent(JsonConvert.SerializeObject(wave)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetValue?index={wave.Order}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                WaveData retrievedData =
                    JsonConvert.DeserializeObject<WaveData>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Read data back:{retrievedData}");

                // insert many data points at once
                List<WaveData> waves = new List<WaveData>();
                for (int i = 2; i < 200; i += 2)
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

                // read all of our data back at once
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetWindowValues?startIndex={waves[0].Order}&endIndex={waves[waves.Count - 1].Order}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> retrievedList =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                Console.WriteLine($"Retrieved {retrievedList.Count} events using GetWindowValues");

                // change the data slightly and then update
                foreach (var waveData in waves)
                {
                    waveData.Order += 2;
                }
                response = await httpClient.PutAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/UpdateValues",
                    new StringContent(JsonConvert.SerializeObject(waves)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // QiStreams use the "Continous" interpolation mode, so when we read at a nonexistent 
                // index, it should interpolate a value using the previous and next index values
                Console.WriteLine("Reading values with Continuous behavior:");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={5}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                List<WaveData> rangeValuesContinuous =
                    JsonConvert.DeserializeObject<List<WaveData>>(await response.Content.ReadAsStringAsync());
                foreach (var waveData in rangeValuesContinuous)
                {
                    Console.WriteLine($"Order: {waveData.Order}, Radians: {waveData.Radians}");
                }

                // behaviors allow users to dictate how Qi will interpolate or extrapolate when reading data from a stream
                // the discrete mode for this behavior will only allow values explicitly written to be read back
                QiStreamBehavior waveStreamBehavior = new QiStreamBehavior
                {
                    Id = BehaviorId,
                    Mode = QiStreamMode.Discrete,
                    Name = "WaveStreamBehavior"
                };
                response = await httpClient.PostAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Behaviors",
                    new StringContent(JsonConvert.SerializeObject(waveStreamBehavior)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
                if (response.StatusCode == HttpStatusCode.Found)
                {
                    response = await httpClient.GetAsync(
                        $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Behaviors/{waveStreamBehavior.Id}");
                    waveStreamBehavior =
                        JsonConvert.DeserializeObject<QiStreamBehavior>(await response.Content.ReadAsStringAsync());
                }

                // update stream to use behavior
                waveStream.BehaviorId = waveStreamBehavior.Id;
                response = await httpClient.PutAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}",
                    new StringContent(JsonConvert.SerializeObject(waveStream)));
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }

                // the Discrete behavior should only return values explicitly written
                Console.WriteLine("Reading values with Discrete behavior:");
                response = await httpClient.GetAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/GetRangeValues?startIndex={5}&count={3}&boundaryType={QiBoundaryType.ExactOrCalculated}");
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

                // delete a value (we delete the stream later, which also deletes the stream's data)
                response = await httpClient.DeleteAsync(
                    $"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{waveStream.Id}/Data/RemoveValue?index={waves[0].Order}");
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(response.ToString());
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.InnerException);
            }
            finally
            {
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Streams/{StreamId}");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Types/{TypeId}");
                await httpClient.DeleteAsync($"api/Tenants/{tenantId}/Namespaces/{namespaceId}/Behaviors/{BehaviorId}");
            }
            
            Console.ReadKey();
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
                QiTypeCode = QiTypeCode.Empty
            };

            return waveType;
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