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
    public class Program
    {
        public static void Main(string[] args)
        {
            // Instantiate the REST client
            Console.WriteLine("Creating a Qi REST API Client...");

            string server = ConfigurationManager.AppSettings["QiServerUrl"];
            QiClient qiclient = new QiClient(server);
            QiType evtType = null;

            try
            {
                // create types for int and double, then create properties for all the WaveData properties
                Console.WriteLine("Creating a Qi type for WaveData instances");
                QiType intType = new QiType();
                intType.Id = "intType";
                intType.QiTypeCode = QiTypeCode.Int32;

                QiType doubleType = new QiType();
                doubleType.Id = "doubleType";
                doubleType.QiTypeCode = QiTypeCode.Double;

                QiTypeProperty orderProperty = new QiTypeProperty();
                orderProperty.Id = "Order";
                orderProperty.QiType = intType;
                orderProperty.IsKey = true;

                QiTypeProperty tauProperty = new QiTypeProperty();
                tauProperty.Id = "Tau";
                tauProperty.QiType = doubleType;

                QiTypeProperty radiansProperty = new QiTypeProperty();
                radiansProperty.Id = "Radians";
                radiansProperty.QiType = doubleType;

                QiTypeProperty sinProperty = new QiTypeProperty();
                sinProperty.Id = "Sin";
                sinProperty.QiType = doubleType;

                QiTypeProperty cosProperty = new QiTypeProperty();
                cosProperty.Id = "Cos";
                cosProperty.QiType = doubleType;

                QiTypeProperty tanProperty = new QiTypeProperty();
                tanProperty.Id = "Tan";
                tanProperty.QiType = doubleType;

                QiTypeProperty sinhProperty = new QiTypeProperty();
                sinhProperty.Id = "Sinh";
                sinhProperty.QiType = doubleType;

                QiTypeProperty coshProperty = new QiTypeProperty();
                coshProperty.Id = "cosh";
                coshProperty.QiType = doubleType;

                QiTypeProperty tanhProperty = new QiTypeProperty();
                tanhProperty.Id = "Tanh";
                tanhProperty.QiType = doubleType;
                
                // Create a QiType for our WaveData class; the metadata proeprties are the ones we just created
                QiType type = new QiType();
                type.Name = "WaveData";
                type.Id = "WaveDataType";
                type.Description = "This is a sample stream for storing WaveData type events";
                QiTypeProperty[] props = { orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty }; 
                type.Properties = props;

                // create the type in the Qi Service
                string evtTypeString = qiclient.CreateTypeAsync(type).Result;
                evtType = JsonConvert.DeserializeObject<QiType>(evtTypeString);

                // create a stream named evtStream
                Console.WriteLine("Creating a stream in this tenant for simple event measurements");
                QiStream stream = new QiStream("evtStream", evtType.Id);
                string evtStreamString = qiclient.CreateStreamAsync(stream).Result;
                QiStream evtStream = JsonConvert.DeserializeObject<QiStream>(evtStreamString);

                #region CRUD operations
                #region Create (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                TimeSpan span = new TimeSpan(0, 1, 0);
                WaveData evt = WaveData.Next(span, 2.0, 0);

                qiclient.CreateEventAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();

                // how to insert an a collection of events
                List<WaveData> events = new List<WaveData>();
                for (int i = 2; i < 200; i += 2)
                {
                    evt = WaveData.Next(span, 2.0, i);
                    events.Add(evt);
                    Thread.Sleep(400);
                }

                qiclient.CreateEventsAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();
                Thread.Sleep(2000);

                #endregion

                #region Retrieve events
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                string jCollection = qiclient.GetWindowValuesAsync("evtStream", "0", "198").Result;
                WaveData[] foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                #endregion

                #region Update events
                Console.WriteLine();
                Console.WriteLine("Updating values");
                
                // take the first value inserted and update 
                evt = foundEvents.First<WaveData>();
                evt = WaveData.Next(span, 4.0, 0);
                qiclient.UpdateValueAsync("evtStream", JsonConvert.SerializeObject(evt)).Wait();

                // update the remaining events (same span, multiplier, order)
                List<WaveData> newEvents = new List<WaveData>();
                foreach (WaveData evnt in events)
                {
                    WaveData newEvt = WaveData.Next(span, 4.0, evnt.Order);
                    newEvents.Add(newEvt);
                    Thread.Sleep(500);
                }

                qiclient.UpdateValuesAsync("evtStream", JsonConvert.SerializeObject(events)).Wait();
                Thread.Sleep(2000);

                // check the results
                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                jCollection = qiclient.GetWindowValuesAsync("evtStream", "0", "198").Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                #endregion

                #region stream behavior

                // illustrate how stream behaviors modify retrieval
                // First, pull three items back with GetRangeValuesAsync for range values between events.
                // The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
                Console.WriteLine();
                Console.WriteLine(@"Retrieving three events without a stream behavior");
                jCollection = qiclient.GetRangeValuesAsync("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                QiStreamBehavior behavior = new QiStreamBehavior();
                behavior.Id = "evtStreamStepLeading";
                behavior.Mode = QiStreamMode.StepwiseContinuousLeading;
                string behaviorString = qiclient.CreateBehaviorAsync(behavior).Result;
                behavior = JsonConvert.DeserializeObject<QiStreamBehavior>(behaviorString);

                // update the stream to include this behavior
                evtStream.BehaviorId = behavior.Id;
                qiclient.UpdateStreamAsync(evtStream).Wait();

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                jCollection = qiclient.GetRangeValuesAsync("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                #endregion

                #region delete events

                // remove the first value -- index is the timestamp of the event
                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValueAsync("evtStream", "0").Wait();

                // remove the rest -- start and end time indices
                qiclient.RemoveWindowValuesAsync("evtStream", "1", "198").Wait();
                Thread.Sleep(2000);

                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");

                jCollection = qiclient.GetWindowValuesAsync("evtStream", "0", "198").Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
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
                    qiclient.DeleteStreamAsync("evtStream").Wait();
                    qiclient.DeleteBehaviorAsync("evtStreamStepLeading").Wait();
                    qiclient.DeleteTypeAsync(evtType.Id).Wait();
                }
                catch (Exception)
                {
                }
            }
        }

        protected static void DumpEvents(IEnumerable<WaveData> evnts)
        {
            Console.WriteLine(string.Format("Found {0} events, writing", evnts.Count<WaveData>()));
            foreach (WaveData evnt in evnts)
            {
                Console.WriteLine(evnt.ToString());
            }
        }
    }
}
