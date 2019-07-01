using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using OSIsoft.Data;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace SDS_TS_DotNet
{
    public class Program
    {
        public static Exception toThrow = null;
        public static bool success = true;

        static void Main(
            string region = null,
            string session = null,
            string package = null,
            string project = null,
            string[] args = null)
        {
            MainAsync().GetAwaiter().GetResult();
        }


        public static async Task<bool> MainAsync(bool test = false)
        {
            success = true;
            ISdsMetadataService metadataService = null;


            #region settings
            var typeValueTimeName = "Value_Time";
            var typePressureTemperatureTimeName = "Pressure_Temp_Time";

            var streamPressureName = "Pressure_Tank1";
            var streamTempName = "Temperature_Tank1";
            var streamTank0 = "Vessel";
            var streamTank1 = "Tank1";
            var streamTank2 = "Tank2";
            #endregion

            try
            {

                #region configurationSettings
                IConfigurationBuilder builder = new ConfigurationBuilder()
                    .SetBasePath(Directory.GetCurrentDirectory())
                    .AddJsonFile("appsettings.json")
                    .AddJsonFile("appsettings.test.json", optional: true);
                IConfiguration configuration = builder.Build();

                var tenantId = configuration["TenantId"];
                var namespaceId = configuration["NamespaceId"];
                var resource = configuration["Resource"];
                var clientId = configuration["ClientId"];
                var clientKey = configuration["ClientKey"];
                #endregion

                var uriResource = new Uri(resource);



                // Step 1 
                // Get Sds Services to communicate with server
                #region step1
                AuthenticationHandler authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);

                SdsService sdsService = new SdsService(new Uri(resource), authenticationHandler);
                metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
                var dataService = sdsService.GetDataService(tenantId, namespaceId);
                var tableService = sdsService.GetTableService(tenantId, namespaceId);
                #endregion

                // Step 2
                #region step2b
                SdsType type = SdsTypeBuilder.CreateSdsType<TimeData>();
                type.Id = typeValueTimeName;
                type = await metadataService.GetOrCreateTypeAsync(type);
                #endregion

                // Step 3
                // create an SdsStream
                #region step3
                var pressure_stream = new SdsStream
                {
                    Id = streamPressureName,
                    TypeId = type.Id,
                    Description = "A stream for pressure data of tank1"
                };
                pressure_stream = await metadataService.GetOrCreateStreamAsync(pressure_stream);

                var temperature_stream = new SdsStream
                {
                    Id = streamTempName,
                    TypeId = type.Id,
                    Description = "A stream for temperature data of tank1"
                };
                temperature_stream = await metadataService.GetOrCreateStreamAsync(temperature_stream);
                #endregion

                // Step 4
                // insert simple data
                #region step4c
                await dataService.InsertValuesAsync(pressure_stream.Id, GetPressureData());
                await dataService.InsertValuesAsync(streamTempName, GetTemperatureData());
                #endregion
            
                // Step 5
                // create complex type
                #region step5b
                SdsType tankType = SdsTypeBuilder.CreateSdsType<PressureTemperatureData>();
                tankType.Id = typePressureTemperatureTimeName;
                tankType = await metadataService.GetOrCreateTypeAsync(tankType);
                #endregion

                // Step 6
                // create complex type stream
                #region step6
                var tankStream = new SdsStream
                {
                    Id = streamTank1,
                    TypeId = tankType.Id,
                    Description = "A stream for data of tank1"
                };
                tankStream = await metadataService.GetOrCreateStreamAsync(tankStream);
                #endregion

                // Step 7
                // insert complex data
                #region step7
                var data = GetData();
                await dataService.InsertValuesAsync(streamTank1, data);
                #endregion



                // Step 8 and Step 9
                //  view data
                // note: step 9 is not done in this example as the JSON conversion by the library takes care of it automatically for you
                #region step8
                var sortedData = data.OrderBy(entry => entry.Time).ToList();
                var firstTime = sortedData.First();
                var lastTime = sortedData.Last();

                var resultsPressure = (await dataService.GetWindowValuesAsync<TimeData>(streamPressureName, firstTime.Time.ToString("o"), lastTime.Time.ToString("o"))).ToList();

                Console.WriteLine("Values from Pressure of Tank1:");
                foreach (var evnt in resultsPressure)
                {
                    Console.WriteLine(JsonConvert.SerializeObject(evnt));
                }

                var resultsTank = (await dataService.GetWindowValuesAsync<PressureTemperatureData>(streamTank1, firstTime.Time.ToString("o"), lastTime.Time.ToString("o"))).ToList();

                Console.WriteLine("Values from Tank1:");
                foreach (var evnt in resultsTank)
                {
                    Console.WriteLine(JsonConvert.SerializeObject(evnt));
                }
                #endregion

                if (test)
                {
                    //testing to make sure we get back expected stuff
                    if (String.Compare(JsonConvert.SerializeObject(resultsPressure.First()),"{\"Time\":\"2017-01-11T22:21:23.43Z\",\"Value\":346.0}") !=0)
                        throw new Exception("Value retreived isn't expected value for pressure of Tank1");

                    if (String.Compare(JsonConvert.SerializeObject(resultsTank.First()), "{\"Time\":\"2017-01-11T22:21:23.43Z\",\"Pressure\":346.0,\"Temperature\":91.0}") != 0)
                        throw new Exception("Value retreived isn't expected value for Temeprature from Tank1");
                }

                // Step 10
                //  view summary data
                #region step10
                var resultsTankSummary = (await dataService.GetIntervalsAsync<PressureTemperatureData>(streamTank1, firstTime.Time.ToString("o"), lastTime.Time.ToString("o"), 1)).ToList();

                Console.WriteLine("Summaries from Tank1:");
                foreach (var evnt in resultsTankSummary)
                {
                    Console.WriteLine(JsonConvert.SerializeObject(evnt.Summaries));
                }
                #endregion


                // Step 11
                //  Bulk calls
                #region step11a
                var tankStream0 = new SdsStream
                {
                    Id = streamTank0,
                    TypeId = tankType.Id
                };
                tankStream = await metadataService.GetOrCreateStreamAsync(tankStream0);

                var tankStream2 = new SdsStream
                {
                    Id = streamTank2,
                    TypeId = tankType.Id,
                    Description = "A stream for data of tank2"
                };
                tankStream2 = await metadataService.GetOrCreateStreamAsync(tankStream2);

                var data2 = GetData2();
                var sortedData2 = data2.OrderBy(entry => entry.Time).ToList();
                var firstTime2 = sortedData2.First();
                var lastTime2 = sortedData2.Last();

                await dataService.InsertValuesAsync(tankStream2.Id, data2);
                await dataService.InsertValuesAsync(tankStream0.Id, GetData());

                #endregion

                Thread.Sleep(200); //slight rest here for consistency

                #region step11b
                var results2Tanks = await dataService.GetJoinValuesAsync<PressureTemperatureData>(new string[] { tankStream0.Id, tankStream2.Id }, SdsJoinType.Outer, firstTime2.Time.ToString("o"), lastTime2.Time.ToString("o"));

                Console.WriteLine();
                Console.WriteLine();
                Console.WriteLine($"Bulk Values:   {tankStream0.Id}  then {tankStream2.Id}: ");
                Console.WriteLine();
                foreach (var tankResult in results2Tanks)
                {
                    foreach (var dataEntry in tankResult)
                    {
                        Console.WriteLine(JsonConvert.SerializeObject(dataEntry));
                    }
                    Console.WriteLine();
                }

                #endregion
            }
            catch (Exception ex)
            {
                success = false;
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {
                if (metadataService != null)
                {
                    // Step 12
                    // delete everything
                    #region step12
                    await RunInTryCatch(metadataService.DeleteStreamAsync, streamPressureName);
                    await RunInTryCatch(metadataService.DeleteStreamAsync, streamTempName);
                    await RunInTryCatch(metadataService.DeleteStreamAsync, streamTank0);
                    await RunInTryCatch(metadataService.DeleteStreamAsync, streamTank1);
                    await RunInTryCatch(metadataService.DeleteStreamAsync, streamTank2);

                    await RunInTryCatch(metadataService.DeleteTypeAsync, typeValueTimeName);
                    await RunInTryCatch(metadataService.DeleteTypeAsync, typePressureTemperatureTimeName);
                    #endregion 

                    Thread.Sleep(10); //slight rest here for consistency

                    // Check deletes
                    await RunInTryCatchExpectException(metadataService.GetStreamAsync, streamPressureName);
                    await RunInTryCatchExpectException(metadataService.GetStreamAsync, streamTempName);
                    await RunInTryCatchExpectException(metadataService.GetStreamAsync, streamTank0);
                    await RunInTryCatchExpectException(metadataService.GetStreamAsync, streamTank1);
                    await RunInTryCatchExpectException(metadataService.GetStreamAsync, streamTank2);

                    await RunInTryCatchExpectException(metadataService.GetTypeAsync, typeValueTimeName);
                    await RunInTryCatchExpectException(metadataService.GetTypeAsync, typePressureTemperatureTimeName);
                }
            }


            if (test && !success)
                throw toThrow;
            
            return success;
        }

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an exception
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

        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an exception, and you expect an exception
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        private static async Task RunInTryCatchExpectException(Func<string, Task> methodToRun, string value)
        {
            try
            {
                await methodToRun(value);

                Console.WriteLine($"Got error.  Expected {methodToRun.Method.Name} with value {value} to throw an error but it did not:" );
            }
            catch 
            { 
            }
        }

        private static void DeleteThings()
        {
        }

        #region step4b
        static public List<TimeData> GetPressureData()
        {
            List<PressureTemperatureData> data = GetData();
            return data.Select(entry => new TimeData() {Time = entry.Time, Value = entry.Pressure}).ToList();
        }

        static public List<TimeData> GetTemperatureData()
        {
            List<PressureTemperatureData> data = GetData();
            return data.Select(entry => new TimeData() {Time = entry.Time, Value = entry.Temperature}).ToList();
        }
        #endregion



        #region step4a
        static public List<PressureTemperatureData> GetData()
        {
            List<PressureTemperatureData> values = new List<PressureTemperatureData>
            {
                new PressureTemperatureData() { Pressure = 346, Temperature = 91, Time = DateTime.Parse("2017-01-11T22:21:23.430Z") },
                new PressureTemperatureData() { Pressure = 0, Temperature = 0, Time = DateTime.Parse("2017-01-11T22:22:23.430Z") },
                new PressureTemperatureData() { Pressure = 386, Temperature = 93, Time = DateTime.Parse("2017-01-11T22:24:23.430Z") },
                new PressureTemperatureData() { Pressure = 385, Temperature = 92, Time = DateTime.Parse("2017-01-11T22:25:23.430Z") },
                new PressureTemperatureData() { Pressure = 385, Temperature = 0, Time = DateTime.Parse("2017-01-11T22:28:23.430Z") },
                new PressureTemperatureData() { Pressure = 384.2, Temperature = 92, Time = DateTime.Parse("2017-01-11T22:26:23.430Z") },
                new PressureTemperatureData() { Pressure = 384.2, Temperature = 92.2, Time = DateTime.Parse("2017-01-11T22:27:23.430Z") },
                new PressureTemperatureData() { Pressure = 396, Temperature = 0, Time = DateTime.Parse("2017-01-11T22:28:29.430Z") }
            };
            return values;
        }
        #endregion

        static public List<PressureTemperatureData> GetData2()
        {
            List<PressureTemperatureData> values = new List<PressureTemperatureData>
            {
                new PressureTemperatureData() { Pressure = 345, Temperature = 89, Time = DateTime.Parse("2017-01-11T22:20:23.430Z") },

                new PressureTemperatureData() { Pressure = 356, Temperature = 0, Time = DateTime.Parse("2017-01-11T22:21:23.430Z") },
                new PressureTemperatureData() { Pressure = 354, Temperature = 88, Time = DateTime.Parse("2017-01-11T22:22:23.430Z") },

                new PressureTemperatureData() { Pressure = 374, Temperature = 87, Time = DateTime.Parse("2017-01-11T22:28:23.430Z") },
                new PressureTemperatureData() { Pressure = 384.2, Temperature = 88, Time = DateTime.Parse("2017-01-11T22:26:23.430Z") },
                new PressureTemperatureData() { Pressure = 384.2, Temperature = 92.2, Time = DateTime.Parse("2017-01-11T22:27:23.430Z") },
                new PressureTemperatureData() { Pressure = 396, Temperature = 87, Time = DateTime.Parse("2017-01-11T22:28:29.430Z") }
            };
            return values;
        }
    }

    #region step2a
    public class TimeData
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        public double Value { get; set; }
    }
    #endregion

    #region step5a
    public class PressureTemperatureData
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        public double Pressure { get; set; }
        public double Temperature { get; set; }
    }
    #endregion
}
