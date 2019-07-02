using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.OmfIngress;
using OSIsoft.OmfIngress.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using static OSIsoft.OmfIngress.Models.SubscriptionTypeEnum;

namespace OmfIngressClientLibraries
{
    public class OmfIngressClient
    {
        private readonly IOmfIngressService _omfIngressService;
        private readonly string _tenantId;
        private readonly string _namespaceId;

        public OmfIngressClient(string address, string tenantId, string namespaceId, string clientId, string clientSecret)
        {
            //Get Ingress Services to communicate with server and handle ingress management
            AuthenticationHandler authenticationHandler = new AuthenticationHandler(new Uri(address), clientId, clientSecret);
            _tenantId = tenantId;
            _namespaceId = namespaceId;
            OmfIngressService baseOmfIngressService = new OmfIngressService(new Uri(address), null, HttpCompressionMethod.None, authenticationHandler);
            _omfIngressService = baseOmfIngressService.GetOmfIngressService(tenantId, namespaceId);
        }

        public async Task<OmfConnection> CreateOmfConnectionAsync(string deviceClientId, string connectionName, string destinationNamespaceId)
        {
            // Create a Topic
            Console.WriteLine($"Creating a Topic in Namespace {_namespaceId} for Client with Id {deviceClientId}");
            Console.WriteLine();
            Topic topic = new Topic()
            {
                Name = connectionName,
                Description = "This is a sample Topic",
                ClientIds = new List<string>() { deviceClientId }
            };
            Topic createdTopic = await _omfIngressService.CreateTopicAsync(topic);
            Console.WriteLine($"Created a Topic with Id {createdTopic.Id}");
            Console.WriteLine();

            // Create a Subscription
            Console.WriteLine($"Creating a Subscription in Namespace {destinationNamespaceId} for Topic with Id {createdTopic.Id}");
            Console.WriteLine();
            Subscription subscription = new Subscription()
            {
                TenantId = _tenantId,
                NamespaceId = destinationNamespaceId,
                Name = $"{connectionName}-{destinationNamespaceId}",
                Description = "This is a sample Subscription",
                Type = SubscriptionType.Sds,
                TopicId = createdTopic.Id,
                TopicTenantId = _tenantId,
                TopicNamespaceId = _namespaceId
            };
            Subscription createdSubscription = await _omfIngressService.CreateSubscriptionAsync(subscription);
            Console.WriteLine($"Created a Subscription with Id {createdSubscription.Id}");
            Console.WriteLine();
            OmfConnection omfConnection = new OmfConnection()
            {
                ClientIds = new string[] { deviceClientId },
                Topic = createdTopic,
                Subscription = createdSubscription
            };
            return omfConnection;
        }

        public async Task DeleteOmfConnectionAsync(OmfConnection omfConnection)
        {
            // Delete the Topic and Subscription
            Console.WriteLine($"Deleting the Subscription with Id {omfConnection.Subscription.Id}");
            Console.WriteLine();

            await _omfIngressService.DeleteSubscriptionAsync(omfConnection.Subscription.Id);

            Console.WriteLine($"Deleted the Subscription with Id {omfConnection.Subscription.Id}");
            Console.WriteLine();

            // Delete the Topic
            Console.WriteLine($"Deleting the Topic with Id {omfConnection.Topic.Id}");
            Console.WriteLine();

            await _omfIngressService.DeleteTopicAsync(omfConnection.Topic.Id);

            Console.WriteLine($"Deleted the Topic with Id {omfConnection.Topic.Id}");
            Console.WriteLine();
        }
    }
}
