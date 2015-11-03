using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

using Microsoft.IdentityModel.Clients.ActiveDirectory;
using Newtonsoft.Json;

namespace QiRestApiSample
{
    public class QiClient
    {
        private HttpClient _httpClient;
        private HttpClientHandler _httpClientHandler;
        private string _baseUrl;

        // Azure AD authentication related
        private static AuthenticationContext _authContext = null;

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
        /// Create a stream on the target Qi Service
        /// </summary>
        /// <param name="streamDef">QiStream object with name, Id, type</param>
        /// <returns>void</returns>
        public async Task<string> CreateStreamAsync(QiStream streamDef)
        {
            return await CreateQiObjectAsync<QiStream>(_baseUrl + RestSampleStrings.StreamsBaseUrl, streamDef);
        }

        /// <summary>
        /// Updates a stream's definition
        /// </summary>
        /// <param name="streamDef">Updated definition</param>
        /// <returns>void</returns>
        public async Task UpdateStreamAsync(QiStream streamDef)
        {
            await UpdateQiObject<QiStream>(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamDef.Id, streamDef);
        }

        /// <summary>
        /// Deletes the stream whose Id is passed
        /// </summary>
        /// <param name="streamId">Id of the QiStream to be deleted</param>
        /// <returns>void</returns>
        public async Task DeleteStreamAsync(string streamId)
        {
            await DeleteQiObjectAsync(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId);
        }

        /// <summary>
        /// Creates a QiType in the remote Qi Service.  QiTypes are required by QiStreams and cannot be deleted while so referenced.
        /// </summary>
        /// <param name="typeDef">QiType object defining a user-defined type with properties</param>
        /// <returns>void</returns>
        public async Task<string> CreateTypeAsync(QiType typeDef)
        {
            return await CreateQiObjectAsync<QiType>(_baseUrl + RestSampleStrings.TypesBaseUrl, typeDef);
        }

        /// <summary>
        /// Deletes a QiType in the remote Qi Service
        /// </summary>
        /// <param name="typeId">Id of the QiType to delete</param>
        /// <returns>void</returns>
        public async Task DeleteTypeAsync(string typeId)
        {
            await DeleteQiObjectAsync(_baseUrl + RestSampleStrings.TypesBaseUrl + @"/" + typeId);
        }

        /// <summary>
        /// Create a stream behavior on the target Qi Service
        /// </summary>
        /// <param name="behavior">QiStreamBehavior object to be created</param>
        /// <returns>void</returns>
        public async Task<string> CreateBehaviorAsync(QiStreamBehavior behavior)
        {
            return await CreateQiObjectAsync<QiStreamBehavior>(_baseUrl + RestSampleStrings.BehaviorsBaseUrl, behavior);
        }

        /// <summary>
        /// Deletes a QiStreamBehavior in the remote Qi Service
        /// </summary>
        /// <param name="behaviorId">Id of the QiStreamBehavior to delete</param>
        /// <returns>void</returns>
        public async Task DeleteBehaviorAsync(string behaviorId)
        {
            await DeleteQiObjectAsync(_baseUrl + RestSampleStrings.BehaviorsBaseUrl + @"/" + behaviorId);
        }

        #endregion

        #region Create Methods for Data (Insert)

        /// <summary>
        /// Insert single event into the identified Qi Stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="singleEvent">JSON serialization of the object to store</param>
        /// <returns></returns>
        public async Task CreateEventAsync(string streamId, string singleEvent)
        {
            string requestUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.InsertSingleBaseUrl;
            await InsertEventDataIntoStreamAsync(requestUrl, singleEvent);
        }

        /// <summary>
        /// Insert multiple events into the identified Qi Stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="events">JSON serialization of an array of events</param>
        /// <returns>void</returns>
        public async Task CreateEventsAsync(string streamId, string events)
        {
            string requestUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.InsertMultipleBaseUrl;
            await InsertEventDataIntoStreamAsync(requestUrl, events);
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
        public async Task<string> GetWindowValuesAsync(string streamId, string startIndex, string endIndex)
        {
            string getClause = string.Format(RestSampleStrings.GetWindowValuesUrlTemplate, startIndex, endIndex);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());

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

        public async Task<string> GetRangeValuesAsync(string streamId, string startIndex, int skip, int count, bool reverse, QiBoundaryType boundaryType)
        {
            string getClause = string.Format(RestSampleStrings.GetRangeValuesUrlTemplate, startIndex, skip, count, reverse, boundaryType);
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());

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
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the updated event</param>
        /// <returns></returns>
        public async Task UpdateValueAsync(string streamId, string evt)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.UpdateSingleBaseUrl),
                Method = HttpMethod.Put
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());
            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.UpdateErrorTemplate, "data event", evt);
        }

        /// <summary>
        /// Updates an array of events in a stream (replaces an event with the same key value)
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evts">JSON serialization of an array of updated events</param>
        /// <returns>void</returns>
        public async Task UpdateValuesAsync(string streamId, string evts)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/" + streamId + RestSampleStrings.UpdateMultipleBaseUrl),
                Method = HttpMethod.Put
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());
            msg.Content = new StringContent(evts, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.UpdateErrorTemplate, "data events", streamId);
        }

        #endregion

        /// <summary>
        /// removes a single value from the stream if the index is found
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="index">value of the key of the event to be deleted (for DateTime, ISO 8601 string)</param>
        /// <returns>void</returns>
        public async Task RemoveValueAsync(string streamId, string index)
        {
            string valueUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + string.Format(RestSampleStrings.RemoveSingleUrlTemplate, streamId, index);
            await DeleteQiObjectAsync(valueUrl);
        }

        /// <summary>
        /// Removes all events within a range in a stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">start key value for the range</param>
        /// <param name="endIndex">end key value for the range</param>
        /// <returns>void</returns>
        public async Task RemoveWindowValuesAsync(string streamId, string startIndex, string endIndex)
        {
            string valuesUrl = _baseUrl + RestSampleStrings.StreamsBaseUrl + string.Format(RestSampleStrings.RemoveMultipleUrlTemplate, streamId, startIndex, endIndex);
            await DeleteQiObjectAsync(valuesUrl);
        }

        protected static string AcquireAuthToken()
        {
            if (_authContext == null)
            {
                _authContext = new AuthenticationContext(Constants.SecurityAuthority);
            }

            // tokens expire after a certain period of time
            // You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
            // ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed
            try
            {
                ClientCredential userCred = new ClientCredential(Constants.SecurityAppId, Constants.SecurityAppKey);
                AuthenticationResult authResult = _authContext.AcquireToken(Constants.SecurityResource, userCred);
                return authResult.AccessToken;
            }
            catch (AdalException)
            {
                return string.Empty;
            }
        }

        private async Task SendAndRespondVoidAsync(HttpRequestMessage msg, string errorTemplate, string entityType, string id)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if((int)response.StatusCode == 409)
            {
                Console.WriteLine("{0} already contains the event",id);
            }
            else if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(errorTemplate, entityType, id));
            }
        }

        private async Task SendAndRespondVoidAsync(HttpRequestMessage msg, string errorTemplate, string objectUrl)
        {
            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if ((int)response.StatusCode == 409)
            {
                Console.WriteLine("The Qi Object already exists");
            }
            else if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(errorTemplate, objectUrl));
            }
        }

        private async Task<string> CreateQiObjectAsync<T>(string objectUrl, T objectDefinition)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(objectUrl),
                Method = HttpMethod.Post
            };

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());

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

                    msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());
                    response = await _httpClient.SendAsync(msg);
                }
            }
            catch(Exception)
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

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());

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

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());

            HttpResponseMessage response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(RestSampleStrings.DeleteObjectErrorTemplate, objectUrl));
            }
        }

        private async Task InsertEventDataIntoStreamAsync(string requestUrl, string eventData)
        {
            HttpRequestMessage msg = new HttpRequestMessage
            {
                RequestUri = new Uri(requestUrl),
                Method = HttpMethod.Post
            };

            var streamId = requestUrl.Replace(_baseUrl + RestSampleStrings.StreamsBaseUrl + @"/", string.Empty);
            streamId = streamId.Split('/')[0];

            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", AcquireAuthToken());
            msg.Content = new StringContent(eventData, Encoding.UTF8, "application/json");
            await SendAndRespondVoidAsync(msg, RestSampleStrings.CreateErrorTemplate, "event data", streamId);
        }
    }
}
