// <copyright file="IngressManagementClient.cs" company="OSIsoft, LLC">
//
// Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
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
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json;
using OSIsoft.Data.Http.Security;
using PIToOcsOmfSample.IngressManagement.Models;
namespace PIToOcsOmfSample.IngressManagement
{
    /// <summary>
    /// This class is responsible for provisioning of certain OSIsoft Cloud Services objects to enable OCS data ingress via OSIsoft Message Format.
    /// </summary>
    class IngressManagementClient : IDisposable
    {
        private readonly JsonSerializerSettings _ignoreNullValues = new JsonSerializerSettings
        {
            NullValueHandling = NullValueHandling.Ignore,
            DefaultValueHandling = DefaultValueHandling.IgnoreAndPopulate
        };

        private readonly HttpClient _client;
        private readonly string _accountId;

        /// <param name="baseAddress">The OSIsoft Cloud Services HTTP endpoint.</param>
        /// <param name="accountId">The Guid account Id.</param>
        public IngressManagementClient(string baseAddress, string accountId, QiSecurityHandler qiSecurityHandler)
        {
            _accountId = accountId;
            qiSecurityHandler.InnerHandler = new HttpClientHandler();
            _client = new HttpClient(qiSecurityHandler);
            _client.BaseAddress = new Uri(baseAddress);
        }

        public async Task<string> GetOrCreatePublisherAsync(string publisherName)
        {
            string publisherId;
            HttpRequestMessage getRequest = new HttpRequestMessage(HttpMethod.Get, $"api/tenants/{_accountId}/publishers");
            HttpResponseMessage getResponse = await _client.SendAsync(getRequest);
            List<Publisher> allPublishers = JsonConvert.DeserializeObject<List<Publisher>>(await getResponse.Content.ReadAsStringAsync());
            List<Publisher> publisherWithSameNames = allPublishers.Where(p => p.Name == publisherName).ToList();
            if (publisherWithSameNames.Count == 0)
            {
                var publisher = new Publisher()
                {
                    Name = publisherName,
                    TenantId = _accountId
                };

                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"api/tenants/{_accountId}/publisher/");
                request.Content = new StringContent(JsonConvert.SerializeObject(publisher, _ignoreNullValues));
                request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json");
                HttpResponseMessage response = await _client.SendAsync(request);
                publisher = JsonConvert.DeserializeObject<Publisher>(await response.Content.ReadAsStringAsync());
                publisherId = publisher.Id;
            }
            else if (publisherWithSameNames.Count == 1)
            {
                publisherId = publisherWithSameNames[0].Id;
            }
            else
            {
                throw new InvalidOperationException($"{publisherName} could not be created or there exists more than one {publisherName}.");
            }

            return publisherId;
        }

        public async Task DeletePublisherAsync(string publisherId)
        {
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Delete, $"api/tenants/{_accountId}/publishers/{publisherId}");
            await _client.SendAsync(request);
        }

        public async Task<string> GetOrCreateToken(string publisherId)
        {
            HttpRequestMessage getRequest = new HttpRequestMessage(HttpMethod.Get, $"api/tenants/{_accountId}/publishers/{publisherId}/tokens");
            HttpResponseMessage getResponse = await _client.SendAsync(getRequest);
            List<Token> allTokens = JsonConvert.DeserializeObject<List<Token>>(await getResponse.Content.ReadAsStringAsync());

            if (allTokens.Count > 0)
            {
                return allTokens[0].TokenString;
            }
            else
            {
                var token = new Token()
                {
                    PublisherId = publisherId,
                    CreationDate = DateTime.Now,
                    ExpirationDate = DateTime.Now.AddYears(2)
                };
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post,
                    $"api/tenants/{_accountId}/publishers/{publisherId}/tokens");
                request.Content = new StringContent(JsonConvert.SerializeObject(token, _ignoreNullValues));
                request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json");
                HttpResponseMessage response = await _client.SendAsync(request);
                token = JsonConvert.DeserializeObject<Token>(await response.Content.ReadAsStringAsync());
                return token.TokenString;
            }
        }

        public async Task<string> GetOrCreateTopic(string topicName, string mappedPublisherId)
        {
            string topicId;
            HttpRequestMessage getRequest = new HttpRequestMessage(HttpMethod.Get, $"api/tenants/{_accountId}/topics");
            HttpResponseMessage getResponse = await _client.SendAsync(getRequest);
            List<Topic> allTopics = JsonConvert.DeserializeObject<List<Topic>>(await getResponse.Content.ReadAsStringAsync());
            List<Topic> topicsWithSameNames = allTopics.Where(t => t.Name == topicName).ToList();
            if (topicsWithSameNames.Count == 0)
            {
                var topic = new Topic()
                {
                    Name = topicName,
                    MappedPublishers = new string[] { mappedPublisherId },
                    TenantId = _accountId
                };
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"api/tenants/{_accountId}/topic/");
                string serialized = JsonConvert.SerializeObject(topic, _ignoreNullValues);
                request.Content = new StringContent(serialized);
                request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json");
                HttpResponseMessage response = await _client.SendAsync(request);
                topic = JsonConvert.DeserializeObject<Topic>(await response.Content.ReadAsStringAsync());
                topicId = topic.Id;
            }
            else if (topicsWithSameNames.Count == 1)
            {
                topicId = topicsWithSameNames[0].Id;
            }
            else
            {
                throw new InvalidOperationException($"{topicName} could not be created or there exists more than one {topicName}.");
            }

            return topicId;
        }

        public async Task DeleteTopicAsync(string topicId)
        {
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Delete, $"api/tenants/{_accountId}/topics/{topicId}");
            await _client.SendAsync(request);
        }

        public async Task<string> GetOrCreateSubscription(string subscriptionName, string topicId, string namespaceId)
        {
            string subscriptionId;
            HttpRequestMessage getRequest = new HttpRequestMessage(HttpMethod.Get, $"api/tenants/{_accountId}/subscriptions");
            HttpResponseMessage getResponse = await _client.SendAsync(getRequest);
            List<Subscription> allTopics = JsonConvert.DeserializeObject<List<Subscription>>(await getResponse.Content.ReadAsStringAsync());
            List<Subscription> subscriptionsWithSameNames = allTopics.Where(s => s.Name == subscriptionName).ToList();
            if (subscriptionsWithSameNames.Count == 0)
            {
                var subscription = new Subscription()
                {
                    Name = subscriptionName,
                    SubscriptionTenantId = _accountId,
                    TopicId = topicId,
                    TopicTenantId = _accountId,
                    OCSNamespace = namespaceId,
                    Type = SubscriptionType.Qi
                };
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"api/tenants/{_accountId}/subscription/{namespaceId}");
                var serialized = JsonConvert.SerializeObject(subscription, _ignoreNullValues);
                request.Content = new StringContent(serialized);
                request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse("application/json");
                HttpResponseMessage response = await _client.SendAsync(request);
                var stringcontent = await response.Content.ReadAsStringAsync();
                subscription = JsonConvert.DeserializeObject<Subscription>(stringcontent);
                subscriptionId = subscription.Id;
            }
            else if (subscriptionsWithSameNames.Count == 1)
            {
                subscriptionId = subscriptionsWithSameNames[0].Id;
            }
            else
            {
                throw new InvalidOperationException($"{subscriptionName} could not be created or there exists more than one {subscriptionName}.");
            }

            return subscriptionId;
        }

        public async Task DeleteSubscription(string subscriptionId)
        {
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Delete, $"api/tenants/{_accountId}/subscriptions/{subscriptionId}");
            await _client.SendAsync(request);
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                _client?.Dispose();
            }
        }
    }
}
