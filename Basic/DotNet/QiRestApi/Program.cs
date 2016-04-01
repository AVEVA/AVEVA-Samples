using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace QiRestApiSample
{
    public class Program
    {
        public static void Main(string[] args)
        {
            const string sampleNamespaceId = "WaveDataSampleNamespace";
            const string sampleTypeId = "WaveType";
            const string sampleStreamId = "evtStream";
            const string sampleBehaviorId = "evtStreamStepLeading";

            // Instantiate the REST client
            Console.WriteLine("Creating a Qi REST API Client...");
            string server = Constants.QiServerUrl;
            QiClient qiclient = new QiClient(server);

            try
            {
                // create a QiNamespace
                Console.WriteLine("Creating a Qi Namespace");
                QiNamespace sampleNamespace = new QiNamespace(sampleNamespaceId);
                string evtNamespaceString = qiclient.CreateNamespaceAsync(Constants.TenantId, sampleNamespace).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // create types for int and double, then create properties for all the WaveData properties
                Console.WriteLine("Creating a Qi type for WaveData instances");
                QiType sampleType = GetWaveDataTypeObject(sampleTypeId);
                
                // create the type in the Qi Service
                string evtTypeString = qiclient.CreateTypeAsync(Constants.TenantId, sampleNamespaceId, sampleType).GetAwaiter().GetResult();
                sampleType = JsonConvert.DeserializeObject<QiType>(evtTypeString);

                DelayForQiConsistency();

                // create a stream named evtStream
                Console.WriteLine("Creating a stream in this tenant for simple event measurements");
                QiStream sampleStream = new QiStream(sampleStreamId, sampleTypeId);
                string evtStreamString = qiclient.CreateStreamAsync(Constants.TenantId, sampleNamespaceId, sampleStream).GetAwaiter().GetResult();
                sampleStream = JsonConvert.DeserializeObject<QiStream>(evtStreamString);

                DelayForQiConsistency();

                #region CRUD operations

                #region Create (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // How to insert a single event
                TimeSpan span = new TimeSpan(0, 1, 0);
                WaveData evt = WaveData.Next(span, 2.0, 0);

                qiclient.CreateEventAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, JsonConvert.SerializeObject(evt)).GetAwaiter().GetResult();

                // how to insert an a collection of events
                List<WaveData> events = new List<WaveData>();
                for (int i = 2; i < 200; i += 2)
                {
                    evt = WaveData.Next(span, 2.0, i);
                    events.Add(evt);
                }

                qiclient.CreateEventsAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, JsonConvert.SerializeObject(events)).GetAwaiter().GetResult();

                DelayForQiConsistency();

                #endregion

                #region Retrieve events

                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                string jCollection = qiclient.GetWindowValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "0", "198").GetAwaiter().GetResult();
                WaveData[] foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                #endregion

                #region Update events
                Console.WriteLine();
                Console.WriteLine("Updating values");
                
                // take the first value inserted and update 
                evt = foundEvents.First<WaveData>();
                evt = WaveData.Next(span, 4.0, 0);
                qiclient.UpdateValueAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, JsonConvert.SerializeObject(evt)).GetAwaiter().GetResult();

                // update the remaining events (same span, multiplier, order)
                List<WaveData> newEvents = new List<WaveData>();
                foreach (WaveData evnt in events)
                {
                    WaveData newEvt = WaveData.Next(span, 4.0, evnt.Order);
                    newEvents.Add(newEvt);
                }

                qiclient.UpdateValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, JsonConvert.SerializeObject(events)).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // check the results
                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                jCollection = qiclient.GetWindowValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "0", "198").GetAwaiter().GetResult();
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                #endregion

                #region stream behavior

                // illustrate how stream behaviors modify retrieval
                // First, pull three items back with GetRangeValuesAsync for range values between events.
                // The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
                Console.WriteLine();
                Console.WriteLine(@"Retrieving three events without a stream behavior");
                jCollection = qiclient.GetRangeValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                QiStreamBehavior sampleBehavior = new QiStreamBehavior()
                {
                    Id = sampleBehaviorId,
                    Mode = QiStreamMode.StepwiseContinuousLeading
                };

                string behaviorString = qiclient.CreateBehaviorAsync(Constants.TenantId, sampleNamespaceId, sampleBehavior).GetAwaiter().GetResult();
                sampleBehavior = JsonConvert.DeserializeObject<QiStreamBehavior>(behaviorString);

                DelayForQiConsistency();

                // update the stream to include this behavior
                sampleStream.BehaviorId = sampleBehaviorId;
                qiclient.UpdateStreamAsync(Constants.TenantId, sampleNamespaceId, sampleStream).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                jCollection = qiclient.GetRangeValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                #endregion

                #region delete events

                // remove the first value -- index is the timestamp of the event
                Console.WriteLine();
                Console.WriteLine("Deleting events");
                qiclient.RemoveValueAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "0").GetAwaiter().GetResult();

                // remove the rest -- start and end time indices
                qiclient.RemoveWindowValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "1", "198").GetAwaiter().GetResult();

                DelayForQiConsistency();

                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");

                jCollection = qiclient.GetWindowValuesAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId, "0", "198").GetAwaiter().GetResult();
                foundEvents = JsonConvert.DeserializeObject<WaveData[]>(jCollection);
                DumpEvents(foundEvents);
                Console.WriteLine("Test ran successfully");
                Console.WriteLine("====================");
                Console.WriteLine("Press any button to shutdown");
                Console.ReadLine();

                #endregion

                #endregion
            }
            catch (QiError qerr)
            {
                PrintError("Error in Qi Service", qerr);
                Console.WriteLine("Press ENTER to terminate");
                Console.ReadLine();
            }
            catch (Exception e)
            {
                PrintError("Unexpected Error: ", e);
            }
            finally
            {
                Console.WriteLine("Deleting the stream out of the Qi Service");
                HandleQiCallAsync(async () => await qiclient.DeleteStreamAsync(Constants.TenantId, sampleNamespaceId, sampleStreamId)).GetAwaiter().GetResult();

                Console.WriteLine("Deleting the behavior out of the Qi Service");
                HandleQiCallAsync(async () => await qiclient.DeleteBehaviorAsync(Constants.TenantId, sampleNamespaceId, sampleBehaviorId)).GetAwaiter().GetResult();

                Console.WriteLine("Deleting the type out of the Qi Service");
                HandleQiCallAsync(async () => await qiclient.DeleteTypeAsync(Constants.TenantId, sampleNamespaceId, sampleTypeId)).GetAwaiter().GetResult();
            }
        }

        /// <summary>
        ///     Holds the code that forms the WaveData QiType
        /// </summary>
        /// <param name="sampleTypeId"></param>
        /// <returns></returns>
        protected static QiType GetWaveDataTypeObject(string sampleTypeId)
        {
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
            QiType sampleType = new QiType();
            sampleType.Name = "Wave Data Type";
            sampleType.Id = sampleTypeId;
            sampleType.Description = "This is a type for WaveData events";
            QiTypeProperty[] props = { orderProperty, tauProperty, radiansProperty, sinProperty, cosProperty, tanProperty, sinhProperty, coshProperty, tanhProperty };
            sampleType.Properties = props;

            return sampleType;
        }

        protected static void DumpEvents(IEnumerable<WaveData> evnts)
        {
            Console.WriteLine(string.Format("Found {0} events, writing", evnts.Count<WaveData>()));
            foreach (WaveData evnt in evnts)
            {
                Console.WriteLine(evnt.ToString());
            }
        }

        /// <summary>
        ///     Makes the asynchronous Qi call and handles any exceptions that may follow
        /// </summary>
        /// <param name="qiCallAsync">A function that returns an asychronous call to Qi</param>
        protected static async Task HandleQiCallAsync(Func<Task> qiCallAsync)
        {
            try
            {
                await qiCallAsync();
            }
            catch (QiError qerr)
            {
                PrintError("Error in Qi Service", qerr);
            }
            catch (Exception ex)
            {
                PrintError("Uknown Error", ex);
            }
        }

        /// <summary>
        ///     Prints out a formated error string
        /// </summary>
        /// <param name="exceptionDescription">A description of what may have caused the exception</param>
        /// <param name="exception">The exception itself</param>
        protected static void PrintError(string exceptionDescription, Exception exception)
        {
            Console.WriteLine("\n\n======= " + exceptionDescription + " =======");
            Console.WriteLine(exception.ToString());
            Console.WriteLine("======= End of " + exceptionDescription + " =======\n");
        }

        /// <summary>
        ///     Delays the program for an amount of time to allow the multiple servers on Qi to become consistent with recent calls.
        /// </summary>
        protected static void DelayForQiConsistency()
        {
            int millisecondsToWait = 5000;
            double seconds = millisecondsToWait / 1000.0;

            Console.WriteLine("Waiting for " + seconds + " seconds in order to allow the multiple servers on Qi to become consistent with recent calls...\n");
            Thread.Sleep(millisecondsToWait);
        }
    }
}
