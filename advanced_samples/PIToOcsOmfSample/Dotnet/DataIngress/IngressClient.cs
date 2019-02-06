// <copyright file="IngressClient.cs" company="OSIsoft, LLC">
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

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using PIToOcsOmfSample.DataIngress.OmfMessageContent;

namespace PIToOcsOmfSample.DataIngress
{
    /// <summary>
    /// Client used to send OSIsoft Message Format messages to OSIsoft Cloud Services.
    /// </summary>
    public class IngressClient : IDisposable
    {
        public const string CurrentOmfVersion = "1.0";
        private readonly HttpClient _client;
        private readonly string _producerToken;

        /// <param name="serviceUrl">The OSIsoft Cloud Services HTTP endpoint for OMF message ingress.</param>
        /// <param name="producerToken">Security token used to authenticate with OSIsoft Cloud Services. Can be retrieved from the OCS web portal.</param>     
        public IngressClient(string serviceUrl, string producerToken)
        {
            _client = new HttpClient();
            _client.BaseAddress = new Uri(serviceUrl);
            _producerToken = producerToken;
        }

        public bool UseCompression { get; set; }

        public async Task SendMessageAsync(byte[] body, MessageType msgType, MessageAction action)
        {
            OmfMessage omfMessage = new OmfMessage();
            omfMessage.ProducerToken = _producerToken;
            omfMessage.MessageType = msgType;
            omfMessage.Action = action;
            omfMessage.MessageFormat = MessageFormat.JSON;
            omfMessage.Body = body;
            omfMessage.Version = CurrentOmfVersion;

            if (UseCompression)
                omfMessage.Compress(MessageCompression.GZip);

            HttpContent content = ToHttpContent(omfMessage);
            HttpResponseMessage response = await _client.PostAsync("" /* use the base URI */, content);
            response.EnsureSuccessStatusCode();
        }

        private HttpContent ToHttpContent(OmfMessage msg)
        {
            ByteArrayContent content = new ByteArrayContent(msg.Body);
            foreach(var header in msg.Headers)
            {
                content.Headers.Add(header.Key, header.Value);
            }
            return content;
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
