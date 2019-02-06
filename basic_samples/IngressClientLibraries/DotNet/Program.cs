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
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using OSIsoft.Contracts.Ingress;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.Models.Ingress;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using static OSIsoft.Models.Ingress.SubscriptionTypeEnum;

namespace IngressClientLibraries
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
            string publisherName = configuration["PublisherName"];
            string topicName = configuration["TopicName"];
            string subscriptionName = configuration["SubscriptionName"];

            //Get Ingress Services to communicate with server
            LoggerCallbackHandler.UseDefaultLogging = false;
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(address, clientId, clientSecret);

            IngressService baseIngressService = new IngressService(new Uri(address), null, HttpCompressionMethod.None, authenticationHandler);
            IIngressService ingressService = baseIngressService.GetIngressService(tenantId, namespaceId);

            Console.WriteLine($"OCS endpoint at {address}");
            Console.WriteLine();

            Publisher createdPublisher = null;
            Token createdToken = null;
            Topic createdTopic = null;
            Subscription createdSubscription = null;

            try
            {
                // Create a Publisher
                Console.WriteLine($"Creating a Publisher");
                Console.WriteLine();
                Publisher publisher = new Publisher()
                {
                    TenantId = tenantId,
                    Name = publisherName,
                    Description = "This is a sample Publisher for sending OMF data to OCS"
                };
                createdPublisher = await ingressService.CreateOrUpdatePublisherAsync(publisher);
                Console.WriteLine($"Created a Publisher with Id {createdPublisher.Id}");
                Console.WriteLine();

                // Create a Token
                Console.WriteLine($"Creating a Token for Publisher with Id {createdPublisher.Id}");
                Console.WriteLine();
                Token token = new Token()
                {
                    PublisherId = createdPublisher.Id,
                    ExpirationDate = DateTime.UtcNow.AddDays(7),
                    IsDeleted = false
                };
                createdToken = await ingressService.CreateOrUndeleteTokenAsync(token, createdPublisher.Id);
                Console.WriteLine($"Created a Token with tokenString {createdToken.TokenString}");
                Console.WriteLine();

                // Create a Topic
                Console.WriteLine($"Creating a Topic in Namespace {namespaceId} for Publisher with Id {createdPublisher.Id}");
                Console.WriteLine();
                Topic topic = new Topic()
                {
                    TenantId = tenantId,
                    NamespaceId = namespaceId,
                    Name = topicName,
                    Description = "This is a sample Topic",
                    Publishers = new List<string>() { createdPublisher.Id }
                };
                createdTopic = await ingressService.CreateOrUpdateTopicAsync(topic);
                Console.WriteLine($"Created a Topic with Id {createdTopic.Id}");
                Console.WriteLine();

                // Create a Subscription
                Console.WriteLine($"Creating an OCS Subscription in Namespace {namespaceId} for Topic with Id {createdTopic.Id}");
                Console.WriteLine();
                Subscription subscription = new Subscription()
                {
                    TenantId = tenantId,
                    NamespaceId = namespaceId,
                    Name = subscriptionName,
                    Description = "This is a sample OCS Data Store Subscription",
                    Type = SubscriptionType.Sds,
                    TopicId = createdTopic.Id,
                    TopicTenantId = createdTopic.TenantId,
                    TopicNamespaceId = createdTopic.NamespaceId
                };
                createdSubscription = await ingressService.CreateOrUpdateSubscriptionAsync(subscription);
                Console.WriteLine($"Created an OCS Subscription with Id {createdSubscription.Id}");
                Console.WriteLine();

                // At this point, we are ready to send OMF data to OCS.
                // Please visit https://github.com/osisoft/OMF-Samples/tree/master/Tutorials/CSharp_Sds to learn how to do this.
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
                    // Delete the Subscription
                    Console.WriteLine($"Deleting the OCS Subscription with Id {createdSubscription.Id}");
                    Console.WriteLine();
                    if (createdSubscription != null)
                    {
                        await ingressService.DeleteSubscriptionAsync(createdSubscription.Id);
                    }
                    Console.WriteLine($"Deleted the OCS Subscription with Id {createdSubscription.Id}");
                    Console.WriteLine();

                    // Delete the Topic
                    Console.WriteLine($"Deleting the Topic with Id {createdTopic.Id}");
                    Console.WriteLine();
                    if (createdTopic != null)
                    {
                        await ingressService.DeleteTopicAsync(createdTopic.Id);
                    }
                    Console.WriteLine($"Deleted the Topic with Id {createdTopic.Id}");
                    Console.WriteLine();

                    // Delete the Token
                    Console.WriteLine($"Deleting the Token with Id {createdTopic.Id}");
                    Console.WriteLine();
                    if (createdToken != null)
                    {
                        await ingressService.DeleteTokenAsync(createdPublisher.Id, createdToken.Id);
                    }
                    Console.WriteLine($"Deleted the Token with Id {createdToken.Id}");
                    Console.WriteLine();

                    // Delete the Publisher
                    Console.WriteLine($"Deleting the Publisher with Id {createdPublisher.Id}");
                    Console.WriteLine();
                    if (createdPublisher != null)
                    {
                        await ingressService.DeletePublisherAsync(createdPublisher.Id);
                    }
                    Console.WriteLine($"Deleted the Publisher with Id {createdPublisher.Id}");
                    Console.WriteLine();
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
