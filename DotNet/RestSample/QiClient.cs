using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

using Microsoft.IdentityModel.Clients.ActiveDirectory;
using Newtonsoft.Json;

namespace RestSample
{
    public class QiClient
    {
        private HttpClient _httpClient;
        private string _baseUrl;

        // VERY IMPORTANT: edit the following values to reflect the authorization items you were given

        static string _resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        static string _authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        static string _appId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        static string _appKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";

        // Azure AD authentication related
        private static AuthenticationContext _authContext = null;

        // REST API url strings
        private string _tenantsBase = @"Qi/Tenants";
        private string _typesBase = @"Qi/Types";
        private string _streamsBase = @"Qi/Streams";
        private string _insertSingle = @"/Data/InsertValue";
        private string _insertMultiple = @"/Data/InsertValues";
        private string _getTemplate = @"/Data/GetWindowValues?startIndex={0}&endIndex={1}";
        private string _updateSingle = @"/Data/UpdateValue";
        private string _updateMultiple = @"/Data/UpdateValues";
        private string _removeSingleTemplate = @"/{0}/Data/RemoveValue?index={1}";
        private string _removeMultipleTemplate = @"/{0}/Data/RemoveWindowValues?startIndex={1}&endIndex={2}";

        // void error formats
        private string _createError = "Failed to create {0} with Id = {1}";
        private string _updateError = "Failed to update {0} with Id = {1}";
        private string _deleteError = "Failed to delete event from stream {0} with index = {1}";
        private string _deleteMultipleError = "Failed to delete events from stream {0} with indices {1}";

        public QiClient(string baseUrl)
        {
            _httpClient = new HttpClient();
            _baseUrl = baseUrl;
            if (_baseUrl.Substring(_baseUrl.Length - 1).CompareTo(@"/") != 0)
                _baseUrl = _baseUrl + "/";

            _httpClient.BaseAddress = new Uri(_baseUrl); 
            _httpClient.Timeout = new TimeSpan(0, 0, 30);
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

        /// <summary>
        /// Create a stream on the target Qi Service
        /// </summary>
        /// <param name="streamDef">QiStream object with name, Id, type</param>
        /// <returns>void</returns>
        public async Task<string> CreateStream(QiStream streamDef)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase),
                Method = HttpMethod.Post,
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            string content = JsonConvert.SerializeObject(streamDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Error creating Stream with id " + streamDef.Id);
            }
            else
            {
                return await response.Content.ReadAsStringAsync();
            }
        }

        /// <summary>
        /// Deletes the stream whose Id is passed
        /// </summary>
        /// <param name="streamId">Id of the QiStream to be deleted</param>
        /// <returns>void</returns>
        public async Task DeleteStream(string streamId)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId),
                Method = HttpMethod.Delete,
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, _createError, "stream", streamId);
        }

        /// <summary>
        /// Creates a QiType in the remote Qi Service.  QiTypes are required by QiStreams and cannot be deleted while so referenced.
        /// </summary>
        /// <param name="typeDef">QiType object defining a user-defined type with properties</param>
        /// <returns>void</returns>
        public async Task<string> CreateType(QiType typeDef)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _typesBase),
                Method = HttpMethod.Post,
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            string content = JsonConvert.SerializeObject(typeDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Error creating Type with id " + typeDef.Id);
            }
            else
            {
                return await response.Content.ReadAsStringAsync();
            }
        }

        /// <summary>
        /// Deletes a QiType in the remote Qi Service
        /// </summary>
        /// <param name="typeId">Id of the QiType to delete</param>
        /// <returns>void</returns>
        public async Task DeleteType(string typeId)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _typesBase +@"/" + typeId),
                Method = HttpMethod.Delete,
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

           await  SendAndRespondVoid(msg, _deleteError, "type", typeId);
        }
        #endregion

        #region Create Methods for Data (Insert)

        /// <summary>
        /// Creates a single instance of a measured event in the named Qi Stream provided the object conforms to the type of the stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the object to store</param>
        /// <returns></returns>
        public async Task CreateEvent(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _insertSingle),
                Method = HttpMethod.Post
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, _createError, "data event", streamId);
        }

        /// <summary>
        /// Creates multiple events in the identified Qi Stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of an array of events</param>
        /// <returns>void</returns>
        public async Task CreateEvents(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _insertMultiple),
                Method = HttpMethod.Post
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, _createError, "data events", streamId);
        }

        #endregion

        #region Retrieve Methods for Data
        /// <summary>
        /// Gets all values in the range identified by the start and end indices
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">string representation of a value related to the streams key; for a DateTime key, an ISO 8601 time reference</param>
        /// <param name="endIndex">string representaion of a value related to the stream's key denoting the end of the desired range</param>
        /// <returns>JSON serialized array of events</returns>
        public async Task<string> GetWindowValues(string streamId, string startIndex, string endIndex)
        {   
            string getClause = string.Format(_getTemplate, startIndex, endIndex);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

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

        #region Update Methods for Data
        /// <summary>
        /// Updates a single event if found
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the updated event</param>
        /// <returns></returns>
        public async Task UpdateValue(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _updateSingle),
                Method = HttpMethod.Put
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, _updateError, "data event", evt);
        }

        /// <summary>
        /// Updates an array of events in a stream (replaces an event with the same key value)
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evts">JSON serialization of an array of updated events</param>
        /// <returns>void</returns>
        public async Task UpdateValues(string streamId, string evts)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + _streamsBase + @"/" + streamId + _updateMultiple),
                Method = HttpMethod.Put
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evts, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, _updateError, "data events", streamId);
        }

        #endregion

        /// <summary>
        /// removes a single value from the stream if the index is found
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="index">value of the key of the event to be deleted (for DateTime, ISO 8601 string)</param>
        /// <returns>void</returns>
        public async Task RemoveValue(string streamId, string index)
        {
            string uri = _baseUrl + _streamsBase + string.Format(_removeSingleTemplate, streamId, index);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(uri),
                Method = HttpMethod.Delete
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, _deleteError, streamId, index);
        }

        /// <summary>
        /// Removes all events within a range in a stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">start key value for the range</param>
        /// <param name="endIndex">end key value for the range</param>
        /// <returns>void</returns>
        public async Task RemoveWindowValues(string streamId, string startIndex, string endIndex)
        {
            string uri = _baseUrl + _streamsBase + string.Format(_removeMultipleTemplate, streamId, startIndex, endIndex);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(uri),
                Method = HttpMethod.Delete
            };

            string token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, _deleteMultipleError, streamId, startIndex + ", " + endIndex);
        }

        private async Task SendAndRespondVoid(HttpRequestMessage msg, string template, string entity, string id)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(template, entity, id));
            }

        }

        static protected string AcquireAuthToken()
        {
            if (_authContext == null)
            {
                _authContext = new AuthenticationContext(_authority);
            }

            // tokens expire after a certain period of time
            // You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
            // ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed
            try
            {
                ClientCredential userCred = new ClientCredential(_appId, _appKey);
                AuthenticationResult authResult = _authContext.AcquireToken(_resource, userCred);
                return authResult.AccessToken;
            }
            catch (AdalException)
            {
                return string.Empty;
            }


        }

    }
}
