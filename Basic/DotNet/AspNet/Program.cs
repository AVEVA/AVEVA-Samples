using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Threading;
using Newtonsoft.Json;

namespace RestSample
{
    internal class Program
    {
        #region Protected Methods

        protected static void DumpEvents(IEnumerable<WaveData> evnts)
        {
            var waveDatas = evnts as WaveData[] ?? evnts.ToArray();
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
            // Instantiate the REST client
            Console.WriteLine("Creating a Qi REST API Client...");

            var server = ConfigurationManager.AppSettings["QiServerUrl"];
            var qiclient = new QiClient(server);
            QiType evtType = null;

            try
            {
                // create types for int and double, then create properties for all the WaveData properties
                Console.WriteLine("Creating a Qi type for WaveData instances");
                var intType = new QiType
                {
                    Id = "intType",
                    QiTypeCode = QiTypeCode.Int32
                };

                var doubleType = new QiType
                {
                    Id = "doubleType",
                    QiTypeCode = QiTypeCode.Double
                };

                var orderProperty = new QiTypeProperty
                {
                    Id = "Order",
                    QiType = intType,
                    IsKey = true
                };

                var tauProperty = new QiTypeProperty
                {
                    Id = "Tau",
                    QiType = doubleType
                };

                var radiansProperty = new QiTypeProperty
                {
                    Id = "Radians",
                    QiType = doubleType
                };

                var sinProperty = new QiTypeProperty
                {
                    Id = "Sin",
                    QiType = doubleType
                };

                var cosProperty = new QiTypeProperty
                {
                    Id = "Cos",
                    QiType = doubleType
                };

                var tanProperty = new QiTypeProperty
                {
                    Id = "Tan",
                    QiType = doubleType
                };

                var sinhProperty = new QiTypeProperty
                {
                    Id = "Sinh",
                    QiType = doubleType
                };

                var coshProperty = new QiTypeProperty
                {
                    Id = "cosh",
                    QiType = doubleType
                };

                var tanhProperty = new QiTypeProperty
                {
                    Id = "Tanh",
                    QiType = doubleType
                };

                // Create a QiType for our WaveData class; the metadata proeprties are the ones we just created
                var type = new QiType
                {
                    Name = "WaveData",
                    Id = "WaveDataType",
                    Description = "This is a sample stream for storing WaveData type events"
                };
                QiTypeProperty[] props =
                {
                    orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty,
                    tanProperty, sinhProperty, coshProperty, tanhProperty
                };
                type.Properties = props;

                // create the type in the Qi Service
                var evtTypeString = qiclient.CreateType(type).Result;
                evtType = JsonConvert.DeserializeObject<QiType>(evtTypeString);

                // create a stream named evtStream
                Console.WriteLine("Creating a stream in this tenant for simple event measurements");
                var stream = new QiStream("evtStream", evtType.Id);
                var evtStreamString = qiclient.CreateStream(stream).Result;
                var evtStream = JsonConvert.DeserializeObject<QiStream>(evtStreamString);

                #region CRUD operations

                #region Create (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                var span = new TimeSpan(0, 1, 0);
                var evt = WaveData.Next(span, 2.0, 0);

                qiclient.CreateEvent("evtStream", JsonConvert.SerializeObject(evt)).Wait();

                var events = new List<WaveData>();
                // how to insert an a collection of events
                for (var i = 2; i < 200; i += 2)
                {
                    evt = WaveData.Next(span, 2.0, i);
                    events.Add(evt);
                    Thread.Sleep(400);
                }
                qiclient.CreateEvents("evtStream", JsonConvert.SerializeObject(events)).Wait();
                Thread.Sleep(2000);

                #endregion Create (Insert)

                #region Retrieve events

                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                var jCollection = qiclient.GetWindowValues("evtStream", "0", "198").Result;
                var foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                #endregion Retrieve events

                #region Update events

                Console.WriteLine();
                Console.WriteLine("Updating values");
                // take the first value inserted and update
                evt = foundEvents.First();
                evt = WaveData.Next(span, 4.0, 0);
                qiclient.UpdateValue("evtStream", JsonConvert.SerializeObject(evt)).Wait();

                // update the remaining events (same span, multiplier, order)
                var newEvents = new List<WaveData>();
                foreach (var newEvt in events.Select(evnt => WaveData.Next(span, 4.0, evnt.Order)))
                {
                    newEvents.Add(newEvt);
                    Thread.Sleep(500);
                }
                qiclient.UpdateValues("evtStream", JsonConvert.SerializeObject(events)).Wait();
                Thread.Sleep(2000);

                // check the results
                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                jCollection = qiclient.GetWindowValues("evtStream", "0", "198").Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                #endregion Update events

                #region stream behavior

                // illustrate how stream behaviors modify retrieval
                // First, pull three items back with GetRangeValues for range values between events.
                // The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
                Console.WriteLine();
                Console.WriteLine(@"Retrieving three events without a stream behavior");
                jCollection =
                    qiclient.GetRangeValues("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                var behavior = new QiStreamBehavior
                {
                    Id = "evtStreamStepLeading",
                    Mode = QiStreamMode.StepwiseContinuousLeading
                };
                var behaviorString = qiclient.CreateBehavior(behavior).Result;
                behavior = JsonConvert.DeserializeObject<QiStreamBehavior>(behaviorString);

                // update the stream to include this behavior
                evtStream.BehaviorId = behavior.Id;
                qiclient.UpdateStream("evtStream", evtStream).Wait();

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine(
                    "Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                jCollection =
                    qiclient.GetRangeValues("evtStream", "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                #endregion stream behavior

                #region delete events

                // remove the first value -- index is the timestamp of the event
                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValue("evtStream", "0").Wait();

                // remove the rest -- start and end time indices
                qiclient.RemoveWindowValues("evtStream", "1", "198").Wait();
                Thread.Sleep(2000);

                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");

                jCollection = qiclient.GetWindowValues("evtStream", "0", "198").Result;
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                #endregion delete events

                #endregion CRUD operations
            }
            catch (QiError qerr)
            {
                Console.WriteLine("Error, status code = " + qerr.Code + "; " + qerr.Message);
                Console.WriteLine("Press ENTER to terminate");
                Console.ReadLine();
            }
            finally
            {
                try
                {
                    qiclient.DeleteStream("evtStream").Wait();
                    qiclient.DeleteBehavior("evtStreamStepLeading").Wait();
                    qiclient.DeleteType(evtType.Id).Wait();
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