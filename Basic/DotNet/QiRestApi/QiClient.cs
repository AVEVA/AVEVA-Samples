using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

using Microsoft.IdentityModel.Clients.ActiveDirectory;
using Newtonsoft.Json;
using RestSample;

namespace QiRestApiSample
{
    public class QiClient
    {
        private HttpClient _httpClient;
        private HttpClientHandler _httpClientHandler;
        private string _baseUrl;

        // Azure AD authentication related
        private static AuthenticationContext _authenticationToken = null;

        public QiClient(string baseUrl)
        {
            _httpClientHandler = new HttpClientHandler
            {
                AllowAutoRedirect = false
            };

            _httpClient = new HttpClient(_httpClientHandler);
            _baseUrl = baseUrl;
            if (_baseUrl.Substring(_baseUrl.Length - 1).CompareTo(@"/") != 0)
            {
                _baseUrl = _baseUrl + "/";
            }

            _httpClient.BaseAddress = new Uri(_baseUrl);
            _httpClient.Timeout = new TimeSpan(0, 0, 30);
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }

        #region Metadata methods

        /// <summary>
        /// Create a namespace on the target Qi Service
        /// </summary>
        /// <param name="namespaceDef">QiNamespace object to be created</param>
        /// <returns></returns>
        public async Task<string> CreateNamespaceAsync(string tenantId, QiNamespace namespaceDef)
        {
            return await CreateQiObjectAsync<QiNamespace>(_baseUrl + string.Format(RestSampleStrings.NamespacesBaseUrl, Constants.TenantId), namespaceDef);
        }

        /// <summary>
        /// Delete a namespace on the target Qi Service
        /// </summary>
        /// <param name="namespaceId">The id of the QiNamespace</param>
        /// <returns></returns>
        public async Task DeleteNamespaceAsync(string tenantId, string namespaceId)
        {
            await DeleteQiObjectAsync(_baseUrl + string.Format(RestSampleStrings.NamespacesBaseUrl, tenantId) + @"/" + namespaceId);
        }

        /// <summary>
        /// Create a stream on the target Qi Service
        /// </summary>
        /// <param name="namespaceId">The Id of the QiNamespace to create the stream on</param>
        /// <param name="streamDef">QiStream object with name, Id, type</param>
        /// <returns>void</returns>
        public async Task<string> CreateStreamAsync(string tenantId, string namespaceId, QiStream streamDef)
        {
            return await CreateQiObjectAsync<QiStream>(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId), streamDef);
        }

        /// <summary>
        /// Updates a stream's definition
        /// </summary>
        /// <param name="namespaceId">The Id of the QiNamespace to update the stream on</param>
        /// <param name="streamDef">Updated definition</param>
        /// <returns>void</returns>
        public async Task UpdateStreamAsync(string tenantId, string namespaceId, QiStream streamDef)
        {
            await UpdateQiObject<QiStream>(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamDef.Id, streamDef);
        }

        /// <summary>
        /// Deletes the stream whose Id is passed
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace to delete the stream on</param>
        /// <param name="streamId">Id of the QiStream to be deleted</param>
        /// <returns>void</returns>
        public async Task DeleteStreamAsync(string tenantId, string namespaceId, string streamId)
        {
            await DeleteQiObjectAsync(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId);
        }

        /// <summary>
        /// Creates a QiType in the remote Qi Service.  QiTypes are required by QiStreams and cannot be deleted while so referenced.
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace to create the type on</param>
        /// <param name="typeDef">QiType object defining a user-defined type with properties</param>
        /// <returns>void</returns>
        public async Task<string> CreateTypeAsync(string tenantId, string namespaceId, QiType typeDef)
        {
            return await CreateQiObjectAsync<QiType>(_baseUrl + string.Format(RestSampleStrings.TypesBaseUrl, tenantId, namespaceId), typeDef);
        }

        /// <summary>
        /// Deletes a QiType in the remote Qi Service
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace to delete the type on</param>
        /// <param name="typeId">Id of the QiType to delete</param>
        /// <returns>void</returns>
        public async Task DeleteTypeAsync(string tenantId, string namespaceId, string typeId)
        {
            await DeleteQiObjectAsync(_baseUrl + string.Format(RestSampleStrings.TypesBaseUrl, tenantId, namespaceId) + @"/" + typeId);
        }

        /// <summary>
        /// Create a stream behavior on the target Qi Service
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace to create the behavior on</param>
        /// <param name="behavior">QiStreamBehavior object to be created</param>
        /// <returns>void</returns>
        public async Task<string> CreateBehaviorAsync(string tenantId, string namespaceId, QiStreamBehavior behavior)
        {
            return await CreateQiObjectAsync<QiStreamBehavior>(_baseUrl + string.Format(RestSampleStrings.BehaviorsBaseUrl, tenantId, namespaceId), behavior);
        }

        /// <summary>
        /// Deletes a QiStreamBehavior in the remote Qi Service
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace to delete the behavior on</param>
        /// <param name="behaviorId">Id of the QiStreamBehavior to delete</param>
        /// <returns>void</returns>
        public async Task DeleteBehaviorAsync(string tenantId, string namespaceId, string behaviorId)
        {
            await DeleteQiObjectAsync(_baseUrl + string.Format(RestSampleStrings.BehaviorsBaseUrl, tenantId, namespaceId) + @"/" + behaviorId);
        }

        #endregion

        #region Create Methods for Data (Insert)

        /// <summary>
        /// Insert single event into the identified Qi Stream
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace where the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="singleEvent">JSON serialization of the object to store</param>
        /// <returns></returns>
        public async Task CreateEventAsync(string tenantId, string namespaceId, string streamId, string singleEvent)
        {
            string requestUrl = _baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + RestSampleStrings.InsertSingleBaseUrl;
            await InsertEventDataIntoStreamAsync(tenantId, namespaceId, requestUrl, singleEvent);
        }

        /// <summary>
        /// Insert multiple events into the identified Qi Stream
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace where the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="events">JSON serialization of an array of events</param>
        /// <returns>void</returns>
        public async Task CreateEventsAsync(string tenantId, string namespaceId, string streamId, string events)
        {
            string requestUrl = _baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + RestSampleStrings.InsertMultipleBaseUrl;
            await InsertEventDataIntoStreamAsync(tenantId, namespaceId, requestUrl, events);
        }

        #endregion

        #region Retrieve Methods for Data
        /// <summary>
        /// Gets all values in the range identified by the start and end indices
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace where the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">string representation of a value related to the streams key; for a DateTime key, an ISO 8601 time reference</param>
        /// <param name="endIndex">string representaion of a value related to the stream's key denoting the end of the desired range</param>
        /// <returns>JSON serialized array of events</returns>
        public async Task<string> GetWindowValuesAsync(string tenantId, string namespaceId, string streamId, string startIndex, string endIndex)
        {
            string getClause = string.Format(RestSampleStrings.GetWindowValuesUrlTemplate, startIndex, endIndex);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                throw new QiError(response.StatusCode, "Error getting windows values: " + response.ReasonPhrase);
            }
        }

        /// <summary>
        /// Gets all values in the range identified by the start and end indices except for the items that are skipped.  Can also be reversed
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace from which the stream is located</param>
        /// <param name="streamId">Id of the QiStream from which the data is located</param>
        /// <param name="startIndex">The start index of the range of data</param>
        /// <param name="skip">The number of items to skip in the range</param>
        /// <param name="count">The number of items to return</param>
        /// <param name="reverse">Determines whethere the list is reversed or not</param>
        /// <param name="boundaryType">Determines if extrapolated values should be counted</param>
        /// <returns></returns>
        public async Task<string> GetRangeValuesAsync(string tenantId, string namespaceId, string streamId, string startIndex, int skip, int count, bool reverse, QiBoundaryType boundaryType)
        {
            string getClause = string.Format(RestSampleStrings.GetRangeValuesUrlTemplate, startIndex, skip, count, reverse, boundaryType);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                throw new QiError(response.StatusCode, "Error getting range values: " + response.ReasonPhrase);
            }
        }

        #endregion

        #region Update Methods for Data

        /// <summary>
        /// Updates a single event if found
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace from which the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the updated event</param>
        /// <returns></returns>
        public async Task UpdateValueAsync(string tenantId, string namespaceId, string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + RestSampleStrings.UpdateSingleBaseUrl),
                Method = HttpMethod.Put
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());
            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.UpdateErrorTemplate, "data event", evt);
        }

        /// <summary>
        /// Updates an array of events in a stream (replaces an event with the same key value)
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace from which the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evts">JSON serialization of an array of updated events</param>
        /// <returns>void</returns>
        public async Task UpdateValuesAsync(string tenantId, string namespaceId, string streamId, string evts)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/" + streamId + RestSampleStrings.UpdateMultipleBaseUrl),
                Method = HttpMethod.Put
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());
            msg.Content = new StringContent(evts, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.UpdateErrorTemplate, "data events", streamId);
        }

        #endregion

        /// <summary>
        /// removes a single value from the stream if the index is found
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace from which the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="index">value of the key of the event to be deleted (for DateTime, ISO 8601 string)</param>
        /// <returns>void</returns>
        public async Task RemoveValueAsync(string tenantId, string namespaceId, string streamId, string index)
        {
            string valueUrl = _baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + string.Format(RestSampleStrings.RemoveSingleUrlTemplate, streamId, index);
            await DeleteQiObjectAsync(valueUrl);
        }

        /// <summary>
        /// Removes all events within a range in a stream
        /// </summary>
        /// <param name="namespaceId">Id of the QiNamespace from which the stream is located</param>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">start key value for the range</param>
        /// <param name="endIndex">end key value for the range</param>
        /// <returns>void</returns>
        public async Task RemoveWindowValuesAsync(string tenantId, string namespaceId, string streamId, string startIndex, string endIndex)
        {
            string valuesUrl = _baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + string.Format(RestSampleStrings.RemoveMultipleUrlTemplate, streamId, startIndex, endIndex);
            await DeleteQiObjectAsync(valuesUrl);
        }

        /// <summary>
        ///     Acquires Authentication tokens to place in the header of the HTTP requests
        /// </summary>
        /// <returns></returns>
        protected static string AcquireAuthenticationToken()
        {
            if (_authenticationToken == null)
            {
                _authenticationToken = new AuthenticationContext(Constants.SecurityAuthority);
            }

            // tokens expire after a certain period of time
            // You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
            // ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed
            try
            {
                ClientCredential userCredential = new ClientCredential(Constants.SecurityAppId, Constants.SecurityAppKey);
                AuthenticationResult authenticationResult = _authenticationToken.AcquireToken(Constants.SecurityResource, userCredential);
                return authenticationResult.AccessToken;
            }
            catch (AdalException)
            {
                return string.Empty;
            }
        }

        /// <summary>
        ///     Used to make void data requests
        /// </summary>
        /// <param name="message">The HttpRequestMessage to be sent to Qi</param>
        /// <param name="errorTemplate">The template for an exception string</param>
        /// <param name="entityType">a description of the entity type</param>
        /// <param name="id">the id of the container of the event</param>
        /// <exception cref="QiError">Throws when the response does not indicate success</exception>
        /// <returns></returns>
        private async Task SendAndRespondVoidAsync(HttpRequestMessage message, string errorTemplate, string entityType, string id)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(message);
            if((int)response.StatusCode == 409)
            {
                Console.WriteLine("{0} already contains the event", id);
            }
            else if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(errorTemplate, entityType, id));
            }
        }

        /// <summary>
        ///     Used to make void Namespace, Streams, Types, and Behavior requests
        /// </summary>
        /// <param name="message"></param>
        /// <param name="errorTemplate"></param>
        /// <param name="objectUrl"></param>
        /// <exception cref="QiError">Throws when the response does not indicate success</exception>
        /// <returns></returns>
        private async Task SendAndRespondVoidAsync(HttpRequestMessage message, string errorTemplate, string objectUrl)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(message);
            if ((int)response.StatusCode == 409)
            {
                Console.WriteLine("The Qi Object already exists");
            }
            else if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(errorTemplate, objectUrl));
            }
        }

        /// <summary>
        ///     Used to make POST namespace, stream, type, or behavior requests
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="objectUrl"></param>
        /// <param name="objectDefinition"></param>
        /// <returns></returns>
        private async Task<string> CreateQiObjectAsync<T>(string objectUrl, T objectDefinition)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(objectUrl),
                Method = HttpMethod.Post
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());

            string content = JsonConvert.SerializeObject(objectDefinition);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");
            HttpResponseMessage response = null;
            try
            {
                response = await _httpClient.SendAsync(msg);
                if ((int) response.StatusCode == 302)
                {
                    Console.WriteLine("The Qi Object already exists under the tenant. Fetching the object...");
                    msg = new HttpRequestMessage
                    {
                        RequestUri = response.Headers.Location,
                        Method = HttpMethod.Get
                    };

                    msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());
                    response = await _httpClient.SendAsync(msg);
                }
            }
            catch(Exception ex)
            {
                throw;
            }

            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(RestSampleStrings.CreateObjectErrorTemplate, objectUrl));
            }
            else
            {
                return await response.Content.ReadAsStringAsync();
            }
        }

        private async Task UpdateQiObject<T>(string objectUrl, T objectDefinition)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(objectUrl),
                Method = HttpMethod.Put,
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());

            string content = JsonConvert.SerializeObject(objectDefinition);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(RestSampleStrings.UpdateObjectErrorTemplate, objectUrl));
            }
        }

        private async Task DeleteQiObjectAsync(string objectUrl)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(objectUrl),
                Method = HttpMethod.Delete,
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(RestSampleStrings.DeleteObjectErrorTemplate, objectUrl));
            }
        }

        private async Task InsertEventDataIntoStreamAsync(string tenantId, string namespaceId, string requestUrl, string eventData)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(requestUrl),
                Method = HttpMethod.Post
            };

            var streamId = requestUrl.Replace(_baseUrl + string.Format(RestSampleStrings.StreamsBaseUrl, tenantId, namespaceId) + @"/", string.Empty);
            streamId = streamId.Split('/')[0];

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthenticationToken());
            msg.Content = new StringContent(eventData, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.CreateErrorTemplate, "event data", streamId);
        }
    }
}
