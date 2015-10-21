using System;
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
        // VERY IMPORTANT: edit the following values to reflect the authorization items you were given

        #region Private Fields

        private const string AppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        private const string AppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
        private const string Authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        private const string BehaviorsBase = @"Qi/Behaviors";

        // void error formats
        private const string CreateError = "Failed to create {0} with Id = {1}";

        private const string DeleteError = "Failed to delete event from stream {0} with index = {1}";
        private const string DeleteMultipleError = "Failed to delete events from stream {0} with indices {1}";

        private const string GetRangeTemplate =
            @"/Data/GetRangeValues?startIndex={0}&skip={1}&count={2}&reversed={3}&boundaryType={4}";

        private const string GetTemplate = @"/Data/GetWindowValues?startIndex={0}&endIndex={1}";
        private const string InsertMultiple = @"/Data/InsertValues";
        private const string InsertSingle = @"/Data/InsertValue";
        private const string RemoveMultipleTemplate = @"/{0}/Data/RemoveWindowValues?startIndex={1}&endIndex={2}";
        private const string RemoveSingleTemplate = @"/{0}/Data/RemoveValue?index={1}";
        private const string Resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        private const string StreamsBase = @"Qi/Streams";

        // REST API url strings
        private const string TypesBase = @"Qi/Types";

        private const string UpdateError = "Failed to update {0} with Id = {1}";
        private const string UpdateMultiple = @"/Data/UpdateValues";
        private const string UpdateSingle = @"/Data/UpdateValue";

        // Azure AD authentication related
        private static AuthenticationContext _authContext;

        private readonly string _baseUrl;
        private readonly HttpClient _httpClient;

        #endregion Private Fields

        #region Public Constructors

        public QiClient(string baseUrl)
        {
            _httpClient = new HttpClient();
            _baseUrl = baseUrl;
            if (string.Compare(_baseUrl.Substring(_baseUrl.Length - 1), @"/", StringComparison.Ordinal) != 0)
                _baseUrl = _baseUrl + "/";

            _httpClient.BaseAddress = new Uri(_baseUrl);
            _httpClient.Timeout = new TimeSpan(0, 0, 30);
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }

        #endregion Public Constructors

        #region Public Methods

        /// <summary>
        ///     removes a single value from the stream if the index is found
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="index">value of the key of the event to be deleted (for DateTime, ISO 8601 string)</param>
        /// <returns>void</returns>
        public async Task RemoveValue(string streamId, string index)
        {
            var uri = _baseUrl + StreamsBase + string.Format(RemoveSingleTemplate, streamId, index);
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(uri),
                Method = HttpMethod.Delete
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, DeleteError, streamId, index);
        }

        /// <summary>
        ///     Removes all events within a range in a stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">start key value for the range</param>
        /// <param name="endIndex">end key value for the range</param>
        /// <returns>void</returns>
        public async Task RemoveWindowValues(string streamId, string startIndex, string endIndex)
        {
            var uri = _baseUrl + StreamsBase + string.Format(RemoveMultipleTemplate, streamId, startIndex, endIndex);
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(uri),
                Method = HttpMethod.Delete
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, DeleteMultipleError, streamId, startIndex + ", " + endIndex);
        }

        #endregion Public Methods

        #region Protected Methods

        protected static string AcquireAuthToken()
        {
            if (_authContext == null)
            {
                _authContext = new AuthenticationContext(Authority);
            }

            // tokens expire after a certain period of time
            // You can check this with the ExpiresOn property of AuthenticationResult, but it is not necessary.
            // ADAL maintains an in-memory cache of tokens and transparently refreshes them as needed
            try
            {
                var userCred = new ClientCredential(AppId, AppKey);
                var authResult = _authContext.AcquireToken(Resource, userCred);
                return authResult.AccessToken;
            }
            catch (AdalException)
            {
                return string.Empty;
            }
        }

        #endregion Protected Methods

        #region Private Methods

        private async Task SendAndRespondVoid(HttpRequestMessage msg, string template, string entity, string id)
        {
            var response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, string.Format(template, entity, id));
            }
        }

        #endregion Private Methods

        #region Metadata methods

        public async Task<string> CreateBehavior(QiStreamBehavior behavior)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + BehaviorsBase),
                Method = HttpMethod.Post
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var content = JsonConvert.SerializeObject(behavior);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            var response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Error creating Type with id " + behavior.Id);
            }
            return await response.Content.ReadAsStringAsync();
        }

        /// <summary>
        ///     Create a stream on the target Qi Service
        /// </summary>
        /// <param name="streamDef">QiStream object with name, Id, type</param>
        /// <returns>void</returns>
        public async Task<string> CreateStream(QiStream streamDef)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase),
                Method = HttpMethod.Post
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var content = JsonConvert.SerializeObject(streamDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            var response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Error creating Stream with id " + streamDef.Id);
            }
            return await response.Content.ReadAsStringAsync();
        }

        /// <summary>
        ///     Creates a QiType in the remote Qi Service.  QiTypes are required by QiStreams and cannot be deleted while so
        ///     referenced.
        /// </summary>
        /// <param name="typeDef">QiType object defining a user-defined type with properties</param>
        /// <returns>void</returns>
        public async Task<string> CreateType(QiType typeDef)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + TypesBase),
                Method = HttpMethod.Post
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var content = JsonConvert.SerializeObject(typeDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            var response = await _httpClient.SendAsync(msg);
            if (!response.IsSuccessStatusCode)
            {
                throw new QiError(response.StatusCode, "Error creating Type with id " + typeDef.Id);
            }
            return await response.Content.ReadAsStringAsync();
        }

        public async Task DeleteBehavior(string behaviorId)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + BehaviorsBase + @"/" + behaviorId),
                Method = HttpMethod.Delete
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, DeleteError, "type", behaviorId);
        }

        /// <summary>
        ///     Deletes the stream whose Id is passed
        /// </summary>
        /// <param name="streamId">Id of the QiStream to be deleted</param>
        /// <returns>void</returns>
        public async Task DeleteStream(string streamId)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId),
                Method = HttpMethod.Delete
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, CreateError, "stream", streamId);
        }

        /// <summary>
        ///     Deletes a QiType in the remote Qi Service
        /// </summary>
        /// <param name="typeId">Id of the QiType to delete</param>
        /// <returns>void</returns>
        public async Task DeleteType(string typeId)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + TypesBase + @"/" + typeId),
                Method = HttpMethod.Delete
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            await SendAndRespondVoid(msg, DeleteError, "type", typeId);
        }

        public async Task UpdateStream(string streamId, QiStream streamDef)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId),
                Method = HttpMethod.Put
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var content = JsonConvert.SerializeObject(streamDef);
            msg.Content = new StringContent(content, Encoding.UTF8, "application/json");

            await SendAndRespondVoid(msg, UpdateError, "stream", streamId);
        }

        #endregion Metadata methods

        #region Create Methods for Data (Insert)

        /// <summary>
        ///     Creates a single instance of a measured event in the named Qi Stream provided the object conforms to the type of
        ///     the stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the object to store</param>
        /// <returns></returns>
        public async Task CreateEvent(string streamId, string evt)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + InsertSingle),
                Method = HttpMethod.Post
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, CreateError, "data event", streamId);
        }

        /// <summary>
        ///     Creates multiple events in the identified Qi Stream
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of an array of events</param>
        /// <returns>void</returns>
        public async Task CreateEvents(string streamId, string evt)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + InsertMultiple),
                Method = HttpMethod.Post
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, CreateError, "data events", streamId);
        }

        #endregion Create Methods for Data (Insert)

        #region Retrieve Methods for Data

        public async Task<string> GetRangeValues(string streamId, string startIndex, int skip, int count, bool reverse,
                    QiBoundaryType boundaryType)
        {
            var getClause = string.Format(GetRangeTemplate, startIndex, skip, count, reverse, boundaryType);
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.SendAsync(msg);
            if (response.IsSuccessStatusCode)
            {
                var jsonResults = await response.Content.ReadAsStringAsync();
                return jsonResults;
            }
            throw new QiError(response.StatusCode, "Error getting range values: " + response.ReasonPhrase);
        }

        /// <summary>
        ///     Gets all values in the range identified by the start and end indices
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="startIndex">
        ///     string representation of a value related to the streams key; for a DateTime key, an ISO 8601
        ///     time reference
        /// </param>
        /// <param name="endIndex">
        ///     string representaion of a value related to the stream's key denoting the end of the desired
        ///     range
        /// </param>
        /// <returns>JSON serialized array of events</returns>
        public async Task<string> GetWindowValues(string streamId, string startIndex, string endIndex)
        {
            var getClause = string.Format(GetTemplate, startIndex, endIndex);
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + getClause),
                Method = HttpMethod.Get
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.SendAsync(msg);
            if (response.IsSuccessStatusCode)
            {
                var jsonResults = await response.Content.ReadAsStringAsync();
                return jsonResults;
            }
            throw new QiError(response.StatusCode, "Error getting windows values: " + response.ReasonPhrase);
        }

        #endregion Retrieve Methods for Data

        #region Update Methods for Data

        /// <summary>
        ///     Updates a single event if found
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evt">JSON serialization of the updated event</param>
        /// <returns></returns>
        public async Task UpdateValue(string streamId, string evt)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + UpdateSingle),
                Method = HttpMethod.Put
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evt, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, UpdateError, "data event", evt);
        }

        /// <summary>
        ///     Updates an array of events in a stream (replaces an event with the same key value)
        /// </summary>
        /// <param name="streamId">stream identifier</param>
        /// <param name="evts">JSON serialization of an array of updated events</param>
        /// <returns>void</returns>
        public async Task UpdateValues(string streamId, string evts)
        {
            var msg = new HttpRequestMessage
            {
                RequestUri = new Uri(_baseUrl + StreamsBase + @"/" + streamId + UpdateMultiple),
                Method = HttpMethod.Put
            };

            var token = AcquireAuthToken();
            msg.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

            msg.Content = new StringContent(evts, Encoding.UTF8, "application/json");
            await SendAndRespondVoid(msg, UpdateError, "data events", streamId);
        }

        #endregion Update Methods for Data
    }
}