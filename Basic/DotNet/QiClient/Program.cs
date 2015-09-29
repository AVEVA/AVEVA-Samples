using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using OSIsoft.Qi;
using OSIsoft.Qi.Http;
using OSIsoft.Qi.Reflection;

namespace QiLibsSample
{
    class Program
    {
        // VERY IMPORTANT: edit the following values to reflect the authorization items you were given

        static string _resource = "PLACEHOLDER_REPLACE_WITH_RESOURCE";
        static string _authority = "PLACEHOLDER_REPLACE_WITH_AUTHORITY";
        static string _appId = "PLACEHOLDER_REPLACE_WITH_USER_ID";
        static string _appKey = "PLACEHOLDER_REPLACE_WITH_USER_SECRET";

        // Azure AD authentication related
        private static AuthenticationContext _authContext = null;

        static void Main(string[] args)
        {
            Console.WriteLine("Creating a .NET Qi Client...");

            string server = ConfigurationManager.AppSettings["QiServerUrl"];
            QiType evtType = null;

            ServicePointManager.ServerCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            QiHttpClientFactory<IQiServer> clientFactory = new QiHttpClientFactory<IQiServer>();
            clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);

            IQiServer qiclient = clientFactory.CreateChannel(new Uri(server));
            IQiClientProxy proxy = (IQiClientProxy)qiclient;
            proxy.OnBeforeInvoke((handler)=>{
                string token = AcquireAuthToken();
                if (proxy.Client.DefaultHeaders.Contains("Authorization"))
                {
                    proxy.Client.DefaultHeaders.Remove("Authorization");
                }
                    
                proxy.Client.DefaultHeaders.Add("Authorization", new AuthenticationHeaderValue("Bearer", token).ToString());

            });
            
            try
            {
                // Create a Qi Type -- the Qi Libraries let you do this via reflection
                // First, create a type builder, then pass it the name of the class you are using for events.
                // This greatly simplifies type creation

                Console.WriteLine("Creating a Qi type for WaveData instances");
                QiTypeBuilder typeBuilder = new QiTypeBuilder();
                evtType = typeBuilder.Create<WaveData>();
                evtType.Id = "WaveType";
                QiType tp = qiclient.GetOrCreateType(evtType);

                Console.WriteLine("Creating a stream in this tenant for simple event measurements");

                QiStream sampleStream = new QiStream();
                sampleStream.Name = "evtStream";
                sampleStream.Id = "evtStream";

                // set the TypeId property to the value of the Id property of the type you submitted
                // All events submitted to this stream must be of this type
                // Note there are Async versions of the client methods, too, using .NET TPL
                sampleStream.TypeId = tp.Id;
                sampleStream.Description = "This is a sample stream for storing WaveData type measurements";
                QiStream strm = qiclient.GetOrCreateStream(sampleStream);

                #region CRUD Operations

                #region Create Events (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                TimeSpan span = new TimeSpan(0, 1, 0);
                WaveData evt = WaveData.Next(span, 2.0, 0);

                qiclient.InsertValue("evtStream", evt);

                List<WaveData> events = new List<WaveData>();
                // how to insert an a collection of events
                for (int i = 2; i < 200; i+=2)
                {
                    WaveData newEvt = WaveData.Next(span, 2.0, i);
                    events.Add(newEvt);
                    Thread.Sleep(400);
                }

                qiclient.InsertValues<WaveData>("evtStream", events);
                Thread.Sleep(2000);

                #endregion


                #region Retrieve events for a time range

                // use the round trip formatting for time
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                IEnumerable<WaveData> foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "198");
                DumpEvents(foundEvts);
                #endregion

                #region Update an event

                Console.WriteLine();
                Console.WriteLine("Updating values");

                // take the first value inserted and update the value using a multiplier of 4, while retaining the order
                evt = foundEvts.First<WaveData>();
                evt = WaveData.Next(span, 4.0, evt.Order);

                qiclient.UpdateValue<WaveData>("evtStream", evt);

                // update the collection of events (same span, multiplier of 4, retain order)
                List<WaveData> newEvents = new List<WaveData>();
                foreach (WaveData evnt in events)
                {
                    WaveData newEvt = WaveData.Next(span, 4.0, evnt.Order);
                    newEvents.Add(newEvt);
                    Thread.Sleep(500);
                }

                qiclient.UpdateValues<WaveData>("evtStream", newEvents);
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
                foundEvts = qiclient.GetRangeValues<WaveData>("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
                DumpEvents(foundEvts);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                QiStreamBehavior behavior = new QiStreamBehavior();
                behavior.Id = "evtStreamStepLeading";
                behavior.Mode = QiStreamMode.StepwiseContinuousLeading;
                behavior = qiclient.GetOrCreateBehavior(behavior);

                // update the stream to include this behavior
                sampleStream.BehaviorId = behavior.Id;
                qiclient.UpdateStream("evtStream", sampleStream);

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                foundEvts = qiclient.GetRangeValues<WaveData>("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated);
                DumpEvents(foundEvts);

                #endregion

                #region Delete events

                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValue<int>("evtStream", 0);
                qiclient.RemoveWindowValues<int>("evtStream", 2, 198);
                Thread.Sleep(2000);
                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");
                foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "198");
                DumpEvents(foundEvts);
                #endregion
                #endregion

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
                    
                }
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


        static protected void DumpEvents(IEnumerable<WaveData> evnts)
        {
            Console.WriteLine(string.Format("Found {0} events, writing", evnts.Count<WaveData>()));
            foreach (WaveData evnt in evnts)
            {
                Console.WriteLine(evnt.ToString());
            }
        }
    }
}
