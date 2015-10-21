using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Net;
using System.Net.Http.Headers;
using System.Threading;
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using OSIsoft.Qi;
using OSIsoft.Qi.Http;
using OSIsoft.Qi.Reflection;

namespace QiLibsSample
{
    internal class Program
    {
        // VERY IMPORTANT: edit the following values to reflect the authorization items you were given

        #region Private Fields

        private const string AppId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        private const string AppKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";
        private const string Authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        private const string Resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";

        // Azure AD authentication related
        private static AuthenticationContext _authContext;

        #endregion Private Fields

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

        protected static void DumpEvents(IEnumerable<WaveData> evnts)
        {
            var waveDatas = evnts as IList<WaveData> ?? evnts.ToList();
            Console.WriteLine("Found {0} events, writing", waveDatas.Count());
            foreach (var evnt in waveDatas)
            {
                Console.WriteLine(evnt.ToString());
            }
        }

        #endregion Protected Methods

        #region Private Methods

        private static void Main(string[] args)
        {
            Console.WriteLine("Creating a .NET Qi Client...");

            var server = ConfigurationManager.AppSettings["QiServerUrl"];
            QiType evtType = null;

            ServicePointManager.ServerCertificateValidationCallback =
                (sender, certificate, chain, sslPolicyErrors) => true;
            var clientFactory = new QiHttpClientFactory<IQiServer>();
            clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);

            var qiclient = clientFactory.CreateChannel(new Uri(server));
            var proxy = (IQiClientProxy)qiclient;
            proxy.OnBeforeInvoke(handler =>
            {
                var token = AcquireAuthToken();
                if (proxy.Client.DefaultHeaders.Contains("Authorization"))
                {
                    proxy.Client.DefaultHeaders.Remove("Authorization");
                }

                proxy.Client.DefaultHeaders.Add("Authorization",
                    new AuthenticationHeaderValue("Bearer", token).ToString());
            });

            try
            {
                // Create a Qi Type -- the Qi Libraries let you do this via reflection
                // First, create a type builder, then pass it the name of the class you are using for events.
                // This greatly simplifies type creation

                Console.WriteLine("Creating a Qi type for WaveData instances");
                var typeBuilder = new QiTypeBuilder();
                evtType = typeBuilder.Create<WaveData>();
                evtType.Id = "WaveType";
                var tp = qiclient.GetOrCreateType(evtType);

                Console.WriteLine("Creating a stream in this tenant for simple event measurements");

                var sampleStream = new QiStream();
                sampleStream.Name = "evtStream";
                sampleStream.Id = "evtStream";

                // set the TypeId property to the value of the Id property of the type you submitted
                // All events submitted to this stream must be of this type
                // Note there are Async versions of the client methods, too, using .NET TPL
                sampleStream.TypeId = tp.Id;
                sampleStream.Description = "This is a sample stream for storing WaveData type measurements";
                var strm = qiclient.GetOrCreateStream(sampleStream);

                #region CRUD Operations

                #region Create Events (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                var span = new TimeSpan(0, 1, 0);
                var evt = WaveData.Next(span, 2.0, 0);

                qiclient.InsertValue("evtStream", evt);

                var events = new List<WaveData>();
                // how to insert an a collection of events
                for (var i = 2; i < 200; i += 2)
                {
                    var newEvt = WaveData.Next(span, 2.0, i);
                    events.Add(newEvt);
                    Thread.Sleep(400);
                }

                qiclient.InsertValues("evtStream", events);
                Thread.Sleep(2000);

                #endregion Create Events (Insert)

                #region Retrieve events for a time range

                // use the round trip formatting for time
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                var foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "198");
                var waveDatas = foundEvts as IList<WaveData> ?? foundEvts.ToList();
                DumpEvents(waveDatas);

                #endregion Retrieve events for a time range

                #region Update an event

                Console.WriteLine();
                Console.WriteLine("Updating values");

                // take the first value inserted and update the value using a multiplier of 4, while retaining the order
                evt = waveDatas.First();
                evt = WaveData.Next(span, 4.0, evt.Order);

                qiclient.UpdateValue("evtStream", evt);

                // update the collection of events (same span, multiplier of 4, retain order)
                var newEvents = new List<WaveData>();
                foreach (var evnt in events)
                {
                    var newEvt = WaveData.Next(span, 4.0, evnt.Order);
                    newEvents.Add(newEvt);
                    Thread.Sleep(500);
                }

                qiclient.UpdateValues("evtStream", newEvents);
                Thread.Sleep(2000);

                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "198");
                DumpEvents(foundEvts);

                // illustrate how stream behaviors modify retrieval
                // First, pull three items back with GetRangeValues for range values between events.
                // The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
                Console.WriteLine();
                Console.WriteLine(@"Retrieving three events without a stream behavior");
                foundEvts = qiclient.GetRangeValues<WaveData>("evtStream", "1", 0, 3, false,
                    QiBoundaryType.ExactOrCalculated);
                DumpEvents(foundEvts);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                var behavior = new QiStreamBehavior();
                behavior.Id = "evtStreamStepLeading";
                behavior.Mode = QiStreamMode.StepwiseContinuousLeading;
                behavior = qiclient.GetOrCreateBehavior(behavior);

                // update the stream to include this behavior
                sampleStream.BehaviorId = behavior.Id;
                qiclient.UpdateStream("evtStream", sampleStream);

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine(
                    "Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                foundEvts = qiclient.GetRangeValues<WaveData>("evtStream", "1", 0, 3, false,
                    QiBoundaryType.ExactOrCalculated);
                DumpEvents(foundEvts);

                #endregion Update an event

                #region Delete events

                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValue("evtStream", 0);
                qiclient.RemoveWindowValues("evtStream", 2, 198);
                Thread.Sleep(2000);
                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");
                foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "198");
                DumpEvents(foundEvts);

                #endregion Delete events

                #endregion CRUD Operations
            }
            catch (QiHttpClientException qiex)
            {
                Console.WriteLine("Error in Qi Service Client: " + qiex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Other error: " + ex.Message);
            }
            finally
            {
                // clean up all created entities so you can run this again
                // all entities are reference counted, so you must delete the stream, then the type it uses
                try
                {
                    qiclient.DeleteStream("evtStream");
                    qiclient.DeleteBehavior("evtStreamStepLeading");
                    qiclient.DeleteType(evtType.Id);
                }
                catch (Exception)
                {
                    // ignored
                }
            }
        }

        #endregion Private Methods
    }
}