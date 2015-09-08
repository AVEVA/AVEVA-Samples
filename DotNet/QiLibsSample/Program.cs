using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using OSIsoft.Qi;
using OSIsoft.Qi.Http;
using OSIsoft.Qi.Reflection;

namespace QiLibsSample
{
    class Program
    {
        // VERY IMPORTANT: edit the following values to reflect the tenant and authorization items you were given
        static string tenantId = "sampletenant";
        static string target = "change_to_auth_target";
        static string tenant = "change_to_auth_tenant";
        static string audience = "change_to_auth_audience";
        static string clientKey = "change_to_auth_client_key";
        static string appKey = "change_to_auth_app_key";

        static void Main(string[] args)
        {
            Console.WriteLine("Creating a .NET Qi Client...");

            string server = ConfigurationManager.AppSettings["QiServerUrl"];
            QiType evtType = null;

            // set up a client to the Qi Service -- it is essential that you set the QiTenant header

            QiHttpClientFactory<IQiServer> clientFactory = new QiHttpClientFactory<IQiServer>();
            clientFactory.ProxyTimeout = new TimeSpan(0, 1, 0);
            clientFactory.OnCreated((p) => p.DefaultHeaders.Add("QiTenant", "sampletenant"));
            IQiServer qiclient = clientFactory.CreateChannel(new Uri(server));
            
            try
            {
                // TODO -- remove tenant creation when provisioning is accomplished

                Console.WriteLine("Creating a tenant named " + tenantId);
                QiTenant tenant = new QiTenant(tenantId);

                // submit to Qi Service to create the tenant in storage

                qiclient.GetOrCreateTenant(tenant);

                // Create a Qi Type -- the Qi Libraries let you do this via reflection
                // First, create a type builder, then pass it the name of the class you are using for events.
                // This greatly simplifies type creation

                Console.WriteLine("Creating a Qi type for WaveData instances");
                QiTypeBuilder typeBuilder = new QiTypeBuilder();
                evtType = typeBuilder.Create<WaveData>();

                QiType tp = qiclient.GetOrCreateType(evtType);

                Console.WriteLine("Creating a stream in this tenant for simple event measurements");

                QiStream sampleStream = new QiStream();
                sampleStream.Name = "evtStream";
                sampleStream.Id = "evtStream";

                // set the TypeId property to the value of the Id property of the type you submitted
                // All events submitted to this stream must be of this type
                // Note there are Async versions of the client methods, too, using .NET TPL
                sampleStream.TypeId = evtType.Id;
                sampleStream.Description = "This is a sample stream for storing WaveData type measurements";
                QiStream strm = qiclient.GetOrCreateStream(sampleStream);

                #region CRUD Operations

                #region Create Events (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                TimeSpan span = new TimeSpan(0, 0, 1);
                WaveData evt = WaveData.Next(span, 2.0, 0);

                qiclient.InsertValue("evtStream", evt);

                List<WaveData> events = new List<WaveData>();
                // how to insert an a collection of events
                for (int i = 1; i < 100; i++)
                {
                    evt = WaveData.Next(span, 2.0, i);
                    events.Add(evt);
                }

                qiclient.InsertValues<WaveData>("evtStream", events);
                Thread.Sleep(2000);

                #endregion


                #region Retrieve events for a time range

                // use the round trip formatting for time
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                IEnumerable<WaveData> foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "99");
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
                }

                qiclient.UpdateValues<WaveData>("evtStream", newEvents);
                Thread.Sleep(2000);

                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "99");
                DumpEvents(foundEvts);

                #endregion

                #region Delete events

                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValue<int>("evtStream", 0);
                qiclient.RemoveWindowValues("evtStream", 1, 99);
                Thread.Sleep(2000);
                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");
                foundEvts = qiclient.GetWindowValues<WaveData>("evtStream", "0", "99");
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
                    qiclient.DeleteType(evtType.Id);
                    qiclient.DeleteTenant("sampletenant");
                }
                catch (Exception)
                {
                    
                }
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
