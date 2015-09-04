using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using Newtonsoft.Json;

namespace RestSample
{
    class Program
    {
        static void Main(string[] args)
        {
            // Instantiate the REST client
            string server = ConfigurationManager.AppSettings["QiServerUrl"];

            QiClient qiclient = new QiClient("sampletenant", server);

            try
            {
                // TODO retract when provisioning is complete
                Console.WriteLine("Creating a tenant named sampletenant");
                qiclient.CreateTenant("sampletenant").Wait();

                // create properties for double Value, DateTime Timstamp, string Units
                Console.WriteLine("Creating a Qi type for SimpleEvents instances");
                QiType doubleType = new QiType();
                doubleType.Id = "doubleType";
                doubleType.QiTypeCode = QiTypeCode.Double;
                QiTypeProperty doubleProperty = new QiTypeProperty();
                doubleProperty.Id = "Value";
                doubleProperty.QiType = doubleType;

                QiType stringType = new QiType();
                stringType.Id = "stringType";
                stringType.QiTypeCode = QiTypeCode.String;
                QiTypeProperty stringProperty = new QiTypeProperty();
                stringProperty.Id = "Units";
                stringProperty.QiType = stringType;

                QiType dateTimeType = new QiType();
                dateTimeType.Id = "dateTimeType";
                dateTimeType.QiTypeCode = QiTypeCode.DateTime;
                QiTypeProperty dateTimeProperty = new QiTypeProperty();
                dateTimeProperty.Id = "TimeStamp";
                dateTimeProperty.QiType = dateTimeType;
                dateTimeProperty.IsKey = true;

                // Create a QiType for our SimpleEvent class; the metadata proeprties are the three we just created
                QiType type = new QiType();
                type.Name = "SimpleEvent";
                type.Id = "SimpleEvent";
                type.Description = "This is a sample stream for storing SimpleEvent type measurements";
                QiTypeProperty[] props = {doubleProperty, stringProperty, dateTimeProperty}; 
                type.Properties = props;

                // create the type in the Qi Service
                qiclient.CreateType(type).Wait();

                // create a stream named evtStream
                Console.WriteLine("Creating a stream in this tenant for simple event measurements");
                QiStream stream = new QiStream("evtStream", "SimpleEvent");
                qiclient.CreateStream(stream).Wait();

                #region CRUD operations
                #region Create (Insert)

                Console.WriteLine("Artificially generating 100 events at one second intervals and inserting them into the Qi Service");
                Random rnd = new Random();

                // How to insert a single event
                SimpleEvent evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");

                // for our contrived purposes, let's manually set the timestamp to 100 seconds in the past
                DateTime start = DateTime.UtcNow.AddSeconds(-100.0);
                evt.Timestamp = start;
                qiclient.CreateEvent("evtStream", JsonConvert.SerializeObject(evt)).Wait();

                List<SimpleEvent> events = new List<SimpleEvent>();
                // how to insert an a collection of events
                for (int i = 1; i < 100; i++)
                {
                    evt = new SimpleEvent(rnd.NextDouble() * 100, "deg C");
                    evt.Timestamp = start.AddSeconds((double)i);
                    events.Add(evt);
                }
                qiclient.CreateEvents("evtStream", JsonConvert.SerializeObject(events)).Wait();
                Thread.Sleep(2000);


                #endregion

                #region Retrieve events
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                string jCollection = qiclient.GetWindowValues("evtStream", start.ToString("o"), DateTime.UtcNow.ToString("o")).Result;
                SimpleEvent[] evts = JsonConvert.DeserializeObject<SimpleEvent[]>(jCollection);
                DumpEvents(evts);
                #endregion
                #endregion


            }
            catch (QiError qerr)
            {
                Console.WriteLine("Error, status code = " + qerr.Code.ToString() + "; " + qerr.Message);
                Console.WriteLine("Press ENTER to terminate");
                Console.ReadLine();
            }
            finally
            {
                try
                {
                    qiclient.DeleteStream("evtStream").Wait();
                    qiclient.DeleteType("SimpleEvent").Wait();
                    qiclient.DeleteTenant("sampletenant").Wait();
                }
                catch (Exception)
                {
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
