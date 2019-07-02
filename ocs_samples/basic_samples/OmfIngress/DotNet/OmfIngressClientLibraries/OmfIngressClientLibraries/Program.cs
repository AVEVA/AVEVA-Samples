using Microsoft.Extensions.Configuration;
using System;
using System.IO;
using System.Threading.Tasks;

namespace OmfIngressClientLibraries
{
    public class Program
    {
        private static bool success = true;
        private static Exception toThrow = null;
        public static OmfIngressClient _omfIngressClient;
        public static Device _omfDevice;

        public static string _tenantId;
        public static string _namespaceId;
        public static string _address;
        public static string _clientId;
        public static string _clientSecret;
        public static string _connectionName;
        public static string _streamId;
        public static string _deviceClientId;
        public static string _deviceClientSecret;

        public static void Main()
        {
            Setup();
            OmfConnection omfConnection = null;
            try
            {
                //Create the Connection, send OMF
                omfConnection = CreateOmfConnectionAsync().GetAwaiter().GetResult();
                SendTypeContainerAndDataAsync().GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                success = false;
                Console.WriteLine(ex.Message);
                toThrow = ex;
            }
            finally
            {
                //Delete the Type and Stream
                try
                {
                    DeleteTypeAndContainerAsync().GetAwaiter().GetResult();
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    if (toThrow == null)
                    {
                        success = false;
                        toThrow = ex;
                    }
                }

                //Delete the Connection
                try
                {
                    DeleteOmfConnectionAsync(omfConnection).GetAwaiter().GetResult();
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    if (toThrow == null)
                    {
                        success = false;
                        toThrow = ex;
                    }
                }
                Console.WriteLine("Done");
                Console.ReadKey();
            }
            if (!success)
            {
                throw toThrow;
            }
        }

        public static void Setup()
        {
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            IConfiguration configuration = builder.Build();

            // ==== Client constants ====
            _tenantId = configuration["TenantId"];
            _namespaceId = configuration["NamespaceId"];
            _address = configuration["Address"];
            _clientId = configuration["ClientId"];
            _clientSecret = configuration["ClientSecret"];
            _connectionName = configuration["ConnectionName"];
            _streamId = configuration["StreamId"];
            _deviceClientId = configuration["DeviceClientId"];
            _deviceClientSecret = configuration["DeviceClientSecret"];

            _omfDevice = new Device(_address, _tenantId, _namespaceId, _deviceClientId, _deviceClientSecret);

            //Get Ingress Services to communicate with server and handle ingress management
            _omfIngressClient = new OmfIngressClient(_address, _tenantId, _namespaceId, _clientId, _clientSecret);

            Console.WriteLine($"OCS endpoint at {_address}");
            Console.WriteLine();            
        }

        public static async Task<OmfConnection> CreateOmfConnectionAsync()
        {
            //Create the Connection
            OmfConnection omfConnection = await _omfIngressClient.CreateOmfConnectionAsync(_deviceClientId, _connectionName, _namespaceId);
            return omfConnection;
        }

        public static async Task SendTypeContainerAndDataAsync()
        {
            //Create the Type and Stream
            await _omfDevice.CreateDataPointTypeAsync();
            await _omfDevice.CreateStreamAsync(_streamId);

            //Send random data points
            Random rand = new Random();
            Console.WriteLine("Sending 5 OMF Data Messages.");
            for (int i = 0; i < 5; i++)
            {
                DataPointType dataPoint = new DataPointType() { Timestamp = DateTime.UtcNow, Value = rand.NextDouble() };
                await _omfDevice.SendValueAsync(_streamId, dataPoint);
                await Task.Delay(1000);
            }
        }

        public static async Task DeleteTypeAndContainerAsync()
        {
            // Delete the Type and Stream
            await _omfDevice.DeleteStreamAsync(_streamId);
            await _omfDevice.DeleteDataPointTypeAsync();
        }

        public static async Task DeleteOmfConnectionAsync(OmfConnection omfConnection)
        {
            // Delete the Connection           
            await _omfIngressClient.DeleteOmfConnectionAsync(omfConnection);
        }
    }
}
