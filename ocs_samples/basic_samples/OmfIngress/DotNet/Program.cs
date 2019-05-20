// <copyright file="Program.cs" company="OSIsoft, LLC">
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.
// </copyright>

using Microsoft.Extensions.Configuration;
using System;
using System.IO;
using System.Threading.Tasks;

namespace OmfIngressClientLibraries
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
            string tenantId = configuration["TenantId"];
            string namespaceId = configuration["NamespaceId"];
            string address = configuration["Address"];
            string clientId = configuration["ClientId"];
            string clientSecret = configuration["ClientSecret"];
            string topicName = configuration["TopicName"];
            string streamId = configuration["StreamId"];
            string deviceClientId = configuration["DeviceClientId"];
            string deviceClientSecret = configuration["DeviceClientSecret"];

            //Get Ingress Services to communicate with server and handle ingress management
            OmfIngressClient omfIngressClient = new OmfIngressClient(address, tenantId, namespaceId, clientId, clientSecret);

            Console.WriteLine($"OCS endpoint at {address}");
            Console.WriteLine();

            OmfConnection omfConnection = null;
            Device omfDevice = new Device(address, tenantId, namespaceId, deviceClientId, deviceClientSecret);

            try
            {
                omfConnection = await omfIngressClient.CreateOmfConnectionAsync(deviceClientId, topicName, namespaceId);

                // At this point, we are ready to send OMF data to OCS.
                //create type
                await omfDevice.CreateDataPointTypeAsync();
                await omfDevice.CreateStreamAsyc(streamId);

                //send random data points
                Random rand = new Random();
                Console.WriteLine("Sending OMF Data Messages. Pres ESC key to stop sending.");
                do
                {
                    while (!Console.KeyAvailable)
                    {
                        DataPointType dataPoint = new DataPointType() { Timestamp = DateTime.UtcNow, Value = rand.NextDouble() };
                        await omfDevice.SendValueAsync(streamId, dataPoint);
                        await Task.Delay(1000);
                    }
                } while (Console.ReadKey(true).Key != ConsoleKey.Escape);
                Console.WriteLine();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.ReadLine();
            }
            finally
            {
                try
                {
                    // Delete the container and type
                    await omfDevice.DeleteStreamAsync(streamId);
                    await omfDevice.DeleteDataPointTypeAsync();

                    // Delete the Subscription                  
                    await omfIngressClient.DeleteOmfConnectionAsync(omfConnection);
                    
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    Console.ReadLine();
                }
            }
        }
    }
}
