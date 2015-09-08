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

                // submit to PI Cloud Historian to create the tenant in storage

                qiclient.GetOrCreateTenant(tenant);

                // Create a Qi Type -- the Qi Libraries let you do this via reflection
                // First, create a type builder, then pass it the name of the class you are using for events.
                // This greatly simplifies type creation

                Console.WriteLine("Creating a Qi type for SimpleEvents instances");
                QiTypeBuilder typeBuilder = new QiTypeBuilder();
                QiType evtType = typeBuilder.Create<SimpleEvent>();
                evtType.Name = "SimpleEvent";
                evtType.Id = "SimpleEvent";

                QiType tp = qiclient.GetOrCreateType(evtType);

                Console.WriteLine("Creating a stream in this tenant for simple event measurements");

                QiStream sampleStream = new QiStream();
                sampleStream.Name = "evtStream";
                sampleStream.Id = "evtStream";

                // set the TypeId property to the value of the Id property of the type you submitted
                // All events submitted to this stream must be of this type
                // Note there are Async versions of the client methods, too, using .NET TPL
                sampleStream.TypeId = "SimpleEvent";
                sampleStream.Description = "This is a sample stream for storing SimpleEvent type measurements";
                QiStream strm = qiclient.GetOrCreateStream(sampleStream);

                #region CRUD Operations

                #region Create Events (Insert)

                Console.WriteLine("Artificially generating 100 events at one second intervals and inserting them into the Qi Service");
                Random rnd = new Random();

                // How to insert a single event
                SimpleEvent evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");

                // for our contrived purposes, let's manually set the timestamp to 100 seconds in the past
                DateTime start = DateTime.UtcNow.AddSeconds(-100.0);
                evt.Timestamp = start;
                qiclient.InsertValue("evtStream", evt);

                List<SimpleEvent> events = new List<SimpleEvent>();
                // how to insert an a collection of events
                for (int i = 1; i < 100; i++)
                {
                    evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");
                    evt.Timestamp = start.AddSeconds((double)i);
                    events.Add(evt);
                }

                qiclient.InsertValues<SimpleEvent>("evtStream", events);
                Thread.Sleep(2000);

                #endregion


                #region Retrieve events for a time range

                // use the round trip formatting for time
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                IEnumerable<SimpleEvent> foundEvts = qiclient.GetWindowValues<SimpleEvent>("evtStream", start.ToString("o"), DateTime.UtcNow.ToString("o"));
                DumpEvents(foundEvts);
                #endregion

                #region Update an event

                Console.WriteLine();
                Console.WriteLine("Updating values");

                // take the first value inserted and update the value and UOM
                evt = foundEvts.First<SimpleEvent>();
                evt.Units = "deg F";
                evt.Value = 212.0;
                qiclient.UpdateValue<SimpleEvent>("evtStream", evt);

                // update the collection of events (convert to deg F)
                foreach (SimpleEvent evnt in events)
                {
                    evnt.Units = "deg F";
                    evnt.Value = evnt.Value * 9 / 5 + 32.0;
                }

                qiclient.UpdateValues<SimpleEvent>("evtStream", events);
                Thread.Sleep(2000);

                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                foundEvts = qiclient.GetWindowValues<SimpleEvent>("evtStream", start.ToString("o"), DateTime.UtcNow.ToString("o"));
                DumpEvents(foundEvts);

                #endregion

                #region Delete events

                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValue<DateTime>("evtStream", evt.Timestamp);
                qiclient.RemoveWindowValues("evtStream", foundEvts.First<SimpleEvent>().Timestamp.ToString("o"), foundEvts.Last<SimpleEvent>().Timestamp.ToString("o"));
                Thread.Sleep(2000);
                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");
                foundEvts = qiclient.GetWindowValues<SimpleEvent>("evtStream", start.ToString("o"), DateTime.UtcNow.ToString("o"));
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
                }
                catch (Exception exStrm)
                {
                    Console.WriteLine("Error deleting stream, type is left: " + exStrm.Message);
                }
                try
                {

                    qiclient.DeleteType("SimpleEvent");
                }
                catch (Exception exTyp)
                {
                    Console.WriteLine("Error deleting stream: " + exTyp.Message);
                }
                try
                {
                    qiclient.DeleteTenant("sampletenant");
                }
                catch (Exception exTnt)
                {
                    Console.WriteLine("Error deleting tenant: " + exTnt.Message);
                }
            }

        }

        static protected void DumpEvents(IEnumerable<SimpleEvent> evnts)
        {
            Console.WriteLine(string.Format("Found {0} events, writing", evnts.Count<SimpleEvent>()));
            foreach (SimpleEvent evnt in evnts)
            {
                Console.WriteLine(string.Format("Event: Value: {0}, UOM: {1}, Timestamp: {2}", evnt.Value.ToString("F2"), evnt.Units, evnt.Timestamp.ToString("yyyy-MM-dd'T'HH:mm:ssZ")));
            }
        }
    }
}
