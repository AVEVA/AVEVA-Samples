using System;
using System.Configuration;
using System.Threading.Tasks;

using OSIsoft.Data;
using OSIsoft.Data.Reflection;
using System.Collections.Generic;
using OSIsoft.Identity;
using Microsoft.Extensions.Configuration;
using System.IO;

namespace UomsSample
{
    public class Program
    {

        static bool success = true;
        static Exception toThrow = null;

        private static Random Random = new Random();

        static void Main(string[] args)
        {
            MainAsync().GetAwaiter().GetResult();
        }

        public static async Task<bool> MainAsync(bool test = false)
        {

            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddJsonFile("appsettings.test.json", optional: true);
            IConfiguration configuration = builder.Build();

            string tenantId = configuration["TenantId"];
            string namespaceId = configuration["NamespaceId"];
            string resource = configuration["Resource"];
            string clientId = configuration["ClientId"];
            string clientKey = configuration["ClientKey"];
            string apiVersion = configuration["ApiVersion"];

            string ResourcePrefix = "UomSample";
            string TypeId = $"{ResourcePrefix} Uom";
            string StreamWithPropertyOverriden = $"{ResourcePrefix} UomPropertyOverridden";
            string StreamWithoutPropertyOverriden = $"{ResourcePrefix} UomNoPropertyOverridden";

            AuthenticationHandler authenticationHandler = new AuthenticationHandler(new Uri(resource), clientId, clientKey);
            SdsService service = new SdsService(new Uri(resource), authenticationHandler);

            ISdsMetadataService MetadataService = service.GetMetadataService(tenantId, namespaceId);
            ISdsDataService DataService = service.GetDataService(tenantId, namespaceId);
            try
            {

                /*
                 * The following code provides an implementation for getting all the SdsUom ID's for each quantity.
                 * If you are not aware with which SdsUom ID to use, you can uncomment the below code and find out the
                 * uom id.
                 * 
                 * e.g. I am using degree_fahrenheit and  degree_celsius UOMS for temperature SdsQuantity.
                 * 
                 * 
                IEnumerable<SdsUomQuantity> sdsUomQuantities = await MetadataService.GetQuantitiesAsync();
                IEnumerable<SdsUom> sdsUoms = null;

                foreach (SdsUomQuantity sdsUomQuantity in sdsUomQuantities)
                {
                    sdsUoms = await MetadataService.GetQuantityUomsAsync(sdsUomQuantity.Id);

                    foreach (SdsUom sdsUom in sdsUoms)
                    {
                        Console.WriteLine(sdsUom.Id);
                    }
                }
                */

                // Creating a Sdstype
                SdsType sdsType = SdsTypeBuilder.CreateSdsType<Widget>();
                sdsType.Id = TypeId;

                sdsType = await MetadataService.GetOrCreateTypeAsync(sdsType);

                //Creating a Stream overriding the distance property.
                SdsStream sdsStreamOne = new SdsStream()
                {
                    Id = StreamWithPropertyOverriden,
                    TypeId = TypeId,
                    Name = "UomStreamSourceWithPropertyOverridden",
                    PropertyOverrides = new List<SdsStreamPropertyOverride>()
                };

                //Overriding the UOM of the distance property to be kilometer instead of mile.
                sdsStreamOne.PropertyOverrides.Add(new SdsStreamPropertyOverride()
                {
                    Uom = "kilometer",
                    SdsTypePropertyId = "Distance"
                });

                sdsStreamOne = await MetadataService.GetOrCreateStreamAsync(sdsStreamOne);

                //Creating a Stream without overriding properties.
                SdsStream sdsStreamTwo = new SdsStream()
                {
                    Id = StreamWithoutPropertyOverriden,
                    TypeId = TypeId,
                    Name = "UomStreamSourceWithNoPropertyOverridden",
                };

                sdsStreamTwo = await MetadataService.GetOrCreateStreamAsync(sdsStreamTwo);

                // Generating data
                IList<Widget> data = new List<Widget>();
                for (int i = 0; i < 10; i++)
                {
                    Widget widget = new Widget();
                    widget.Time = DateTime.UtcNow.AddSeconds(i);
                    widget.Temperature = Random.Next(1, 100);
                    widget.Distance = Random.Next(1, 100);
                    data.Add(widget);
                }

                /* In stream one, the temperature value will be inserted as Fahrenheit since we have defined the 
                 * default uom as Fahrenheit for Temperature in the Widget class. The distance value will be 
                 * inserted as kilometer, as we have overridden the Distance property in stream one, 
                 * regardless of the default uom for Distance in the Widget class.
                 */
                await DataService.InsertValuesAsync<Widget>(sdsStreamOne.Id, data);

                /* In stream two, the temperature value will be inserted as Fahrenheit and the distance will be inserted as mile.
                 *
                 */
                await DataService.InsertValuesAsync<Widget>(sdsStreamTwo.Id, data);

                /*
                 * The last value stored in stream one. 
                 */
                Widget widgetFromStreamOne = await DataService.GetLastValueAsync<Widget>(sdsStreamOne.Id);

                Console.WriteLine($"In stream one, the distance is {widgetFromStreamOne.Distance} kilometers and the temperature is {widgetFromStreamOne.Temperature} degrees fahrenheit");
                Console.WriteLine();
                /*
                 * The last value stored in stream two. 
                 */
                Widget widgetFromStreamTwo = await DataService.GetLastValueAsync<Widget>(sdsStreamTwo.Id);

                Console.WriteLine($"In stream two, the distance is {widgetFromStreamTwo.Distance} miles and the temperature is {widgetFromStreamTwo.Temperature} degrees fahrenheit");
                Console.WriteLine();

                /*
                 * If you want your data to be in specified uom, you can override your properties while making a call.
                 * In the following, I want the temperature to be in Celsius, and the distance to be in feet.
                 * 
                 * Then you can pass IList<SdsStreamPropertyOverride> to DataService while getting values.
                 * 
                 */
                IList<SdsStreamPropertyOverride> requestOverrides = new List<SdsStreamPropertyOverride>();

                requestOverrides.Add(new SdsStreamPropertyOverride()
                {
                    Uom = "degree celsius",
                    SdsTypePropertyId = "Temperature"
                });

                requestOverrides.Add(new SdsStreamPropertyOverride()
                {
                    Uom = "foot",
                    SdsTypePropertyId = "Distance"
                });

                /*
                 * In the following call, data will be converted from Fahrenheit to Celsius for the temperature property,
                 * and from kilometer to foot for the distance property.
                 * 
                 * Uoms in Stream one (Temperature : Fahrenheit, Distance : Kilometer)
                 * 
                 */
                widgetFromStreamOne = await DataService.GetLastValueAsync<Widget>(sdsStreamOne.Id, requestOverrides);

                Console.WriteLine($"In stream one, the distance is {widgetFromStreamOne.Distance} foot and the temperature is {widgetFromStreamOne.Temperature} degrees celsius");
                Console.WriteLine();

                /*
                 * In the following call, data will be converted from Fahrenheit to Celsius for the temperature property, 
                 * and from mile to foot for the distance property.
                 * 
                 * Uoms in Stream two (Temperature : Fahrenheit, Distance : Mile) 
                 * 
                 */
                widgetFromStreamTwo = await DataService.GetLastValueAsync<Widget>(sdsStreamTwo.Id, requestOverrides);

                Console.WriteLine($"In stream two, the distance is {widgetFromStreamTwo.Distance} foot and the temperature is {widgetFromStreamTwo.Temperature} degrees celsius");
                Console.WriteLine();


            }
            catch (Exception ex)
            {
                success = false;
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {

                Console.WriteLine("Deleting");
                RunInTryCatch(MetadataService.DeleteStreamAsync, StreamWithPropertyOverriden);
                RunInTryCatch(MetadataService.DeleteStreamAsync, StreamWithoutPropertyOverriden);
                RunInTryCatch(MetadataService.DeleteTypeAsync, TypeId);
                if (!test)
                    Console.ReadLine();

            }

            if (test && !success)
                throw toThrow;
            return success;
        }



        /// <summary>
        /// Use this to run a method that you don't want to stop the program if there is an error and you don't want to report the error
        /// </summary>
        /// <param name="methodToRun">The method to run.</param>
        /// <param name="value">The value to put into the method to run</param>
        private static void RunInTryCatch(Func<string, Task> methodToRun, string value)
        {
            try
            {
                methodToRun(value).Wait(100);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Got error in {methodToRun.Method.Name} with value {value} but continued on:" + ex.Message);
                success = false;
                if(toThrow == null)
                {
                    toThrow = ex;
                }
                    
            }
        }
    }
}
