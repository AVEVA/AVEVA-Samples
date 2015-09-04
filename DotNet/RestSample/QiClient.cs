using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

using Newtonsoft.Json;

namespace RestSample
{
    public class QiClient
    {
        private HttpClient _httpClient;
        private string _baseUrl;

        // REST API url strings
        private string _tenantsBase = @"Qi/Tenants";
        private string _typesBase = @"Qi/Types";
        private string _streamsBase = @"Qi/Streams";
        private string _insertSingle = @"/Data/InsertValue";
        private string _insertMultiple = @"/Data/InsertValues";
        private string _getTemplate = @"/Data/GetWindowValues?startIndex={0}&endIndex={1}";

        // void error formats
        private string _createError = "Failed to create {0} with Id = {1}";

        public QiClient(string tenant, string baseUrl)
        {
            _httpClient = new HttpClient();
            _baseUrl = baseUrl;
            if (_baseUrl.Substring(_baseUrl.Length - 1).CompareTo(@"/") != 0)
                _baseUrl = _baseUrl + "/";

            _httpClient.BaseAddress = new Uri(_baseUrl); 
            _httpClient.Timeout = new TimeSpan(0, 0, 30);
            _httpClient.DefaultRequestHeaders.Add("QiTenant", tenant);
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }
        #region Metadata methods
        // TODO retract when provisioning is complete
        public async Task CreateTenant(string tenantId)
        {
            QiTenant tenant = new QiTenant(tenantId);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _tenantsBase),
                Method = HttpMethod.Post,
            };

            //msg.Headers.Authorization = "Bearer: x";
            
            string content = JsonConvert.SerializeObject(tenant);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Failed to create tenant with Id = " + tenantId);
            }
        }

        public async Task DeleteTenant(string tenantId)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _tenantsBase + @"/" + tenantId),
                Method = HttpMethod.Delete
            };

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Failed to create tenant with Id = " + tenantId);
            }
        }

        public async Task CreateStream(QiStream streamDef)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase),
                Method = HttpMethod.Post,
            };

            //msg.Headers.Authorization = "Bearer: x";

            string content = JsonConvert.SerializeObject(streamDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            await SendAndRespondVoid(msg, "stream", streamDef.Id);
        }

        public async Task DeleteStream(string streamId)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId),
                Method = HttpMethod.Delete,
            };

            await SendAndRespondVoid(msg, "stream", streamId);
        }

        public async Task CreateType(QiType typeDef)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _typesBase),
                Method = HttpMethod.Post,
            };

            //msg.Headers.Authorization = "Bearer: x";

            string content = JsonConvert.SerializeObject(typeDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            await SendAndRespondVoid(msg, "type", typeDef.Id);
        }

        public async Task DeleteType(string typeId)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _typesBase +@"/" + typeId),
                Method = HttpMethod.Delete,
            };

           await  SendAndRespondVoid(msg, "type", typeId);
        }
        #endregion

        #region Create Methods for Data (Insert)

        public async Task CreateEvent(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _insertSingle),
                Method = HttpMethod.Post
            };
            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, "data event", streamId);
        }

        public async Task CreateEvents(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _insertMultiple),
                Method = HttpMethod.Post
            };
            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, "data events", streamId);
        }

        #endregion

        #region Retrieve Methods for Data
        public async Task<string> GetWindowValues(string streamId, string startIndex, string endIndex)
        {   
            string getClause = string.Format(_getTemplate, startIndex, endIndex);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + streamId + getClause),
                Method = HttpMethod.Get
            };
            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (response.IsSuccessStatusCode)
            {
                string jsonResults = await response.Content.ReadAsStringAsync();
                return jsonResults;
            }
            else
            {
                throw new QiError(response.StatusCode, "Error getting windows values: " + response.ReasonPhrase);
            }
        }

        #endregion

        private async Task SendAndRespondVoid(HttpRequestMessage msg, string entity, string id)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(_createError, entity, id));
            }
        }
    }
}
