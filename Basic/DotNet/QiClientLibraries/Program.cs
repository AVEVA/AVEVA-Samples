using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using OSIsoft.Qi;
using OSIsoft.Qi.Http;
using OSIsoft.Qi.Http.Security;
using OSIsoft.Qi.Reflection;

namespace QiClientLibsSample
{
    public class Program
    {
        public static void Main(string[] args)
        {
            string sampleNamespaceId = "WaveDataSampleNamespace";
            string sampleTypeId = "WaveType";
            string sampleStreamId = "evtStream";
            string sampleBehaviorId = "evtStreamStepLeading";

            Console.WriteLine("Creating a .NET Qi Administration Service...");
            IQiAdministrationService qiAdministrationService = GetQiAdministrationService();

            Console.WriteLine("Creating a .NET Qi Metadata Service...");
            IQiMetadataService qiMetadataService = GetQiMetadataService(sampleNamespaceId);

            Console.WriteLine("Creating a .NET Qi Data Service...");
            IQiDataService qiDataService = GetQiDataService(sampleNamespaceId);

            try
            {
                // Create a QiNamespace to hold the streams, types, and behaviors
                Console.WriteLine("Creating a QiNamespace to hold the streams, types, and behaviors");
                QiNamespace sampleNamespace = new QiNamespace(sampleNamespaceId);
                sampleNamespace = qiAdministrationService.GetOrCreateNamespaceAsync(sampleNamespace).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // Create a Qi Type to reflect the event data being stored in Qi.
                // The Qi Client Libraries provide QiTypeBuilder which constructs a QiType object 
                // based upon a class you define in your code.  
                Console.WriteLine("Creating a Qi type for WaveData instances");
                QiTypeBuilder typeBuilder = new QiTypeBuilder();
                QiType sampleType = typeBuilder.Create<WaveData>();
                sampleType.Id = sampleTypeId;
                sampleType = qiMetadataService.GetOrCreateTypeAsync(sampleType).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // now let's create the stream to contain the events
                // specify the type id of the QiType created above in the TypeId property of the QiStream object
                // All events submitted to this stream must be of this type
                Console.WriteLine("Creating a stream for simple event measurements");
                QiStream sampleStream = new QiStream()
                {
                    Name = "Wave Data Sample Stream",
                    Id = sampleStreamId,
                    TypeId = sampleTypeId,
                    Description = "This is a sample QiStream for storing WaveData type measurements"
                };

                sampleStream = qiMetadataService.GetOrCreateStreamAsync(sampleStream).GetAwaiter().GetResult();

                DelayForQiConsistency();

                #region CRUD Operations

                #region Create Events (Insert)

                Console.WriteLine("Artificially generating 100 events and inserting them into the Qi Service");

                // Insert a single event into a stream
                TimeSpan span = new TimeSpan(0, 1, 0);
                WaveData waveDataEvent = WaveData.Next(span, 2.0, 0);

                Console.WriteLine("Inserting the first event");
                qiDataService.InsertValueAsync(sampleStreamId, waveDataEvent).GetAwaiter().GetResult();

                // Inserting a collection of events into a stream
                List<WaveData> waveDataEvents = new List<WaveData>();
                for (int i = 2; i < 200; i += 2)
                {
                    waveDataEvent = WaveData.Next(span, 2.0, i);
                    waveDataEvents.Add(waveDataEvent);
                }

                Console.WriteLine("Inserting the rest of the events");
                qiDataService.InsertValuesAsync(sampleStreamId, waveDataEvents).GetAwaiter().GetResult();

                DelayForQiConsistency();

                #endregion

                #region Retrieve events for a time range

                // use the round trip formatting for time
                Console.WriteLine("Retrieving the inserted events");
                Console.WriteLine("==============================");
                IEnumerable<WaveData> foundEvents = qiDataService.GetWindowValuesAsync<WaveData>(sampleStreamId, "0", "198").GetAwaiter().GetResult();
                DumpEvents(foundEvents);
                #endregion

                #region Update an event

                Console.WriteLine();
                Console.WriteLine("Updating the first event");

                // take the first value inserted and update the value using a multiplier of 4, while retaining the order
                waveDataEvent = foundEvents.First();
                waveDataEvent = WaveData.Next(span, 4.0, waveDataEvent.Order);
                qiDataService.UpdateValueAsync(sampleStreamId, waveDataEvent).GetAwaiter().GetResult();

                // update the collection of events (same span, multiplier of 4, retain order)
                waveDataEvents = new List<WaveData>();
                foreach (WaveData evnt in waveDataEvents)
                {
                    waveDataEvent = WaveData.Next(span, 4.0, evnt.Order);
                    waveDataEvents.Add(waveDataEvent);
                }

                Console.WriteLine("Updating the rest of the events");
                qiDataService.UpdateValuesAsync(sampleStreamId, waveDataEvents).GetAwaiter().GetResult();

                DelayForQiConsistency();

                Console.WriteLine("Retrieving the updated values");
                Console.WriteLine("=============================");
                foundEvents = qiDataService.GetWindowValuesAsync<WaveData>(sampleStreamId, "0", "198").GetAwaiter().GetResult();
                DumpEvents(foundEvents);

                // illustrate how stream behaviors modify retrieval
                // First, pull three items back with GetRangeValues for range values between events.
                // The default behavior is continuous, so ExactOrCalculated should bring back interpolated values
                Console.WriteLine();
                Console.WriteLine(@"Retrieving three events without a stream behavior");
                foundEvents = qiDataService.GetRangeValuesAsync<WaveData>(sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
                DumpEvents(foundEvents);

                // now, create a stream behavior with Discrete and attach it to the existing stream
                Console.WriteLine("Creating a QiStreamBehavior");
                QiStreamBehavior sampleBehavior = new QiStreamBehavior()
                {
                    Id = sampleBehaviorId,
                    Mode = QiStreamMode.StepwiseContinuousLeading
                };
                sampleBehavior = qiMetadataService.GetOrCreateBehaviorAsync(sampleBehavior).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // update the stream to include this behavior
                Console.WriteLine("Updating the QiStream with the new QiStreamBehaivor");
                sampleStream.BehaviorId = sampleBehaviorId;
                qiMetadataService.UpdateStreamAsync(sampleStreamId, sampleStream).GetAwaiter().GetResult();

                DelayForQiConsistency();

                // repeat the retrieval
                Console.WriteLine();
                Console.WriteLine("Retrieving three events with a stepwise stream behavior in effect -- compare to last retrieval");
                foundEvents = qiDataService.GetRangeValuesAsync<WaveData>(sampleStreamId, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
                DumpEvents(foundEvents);

                #endregion

                #region Delete events

                Console.WriteLine();
                Console.WriteLine("Deleting first event");
                qiDataService.RemoveValueAsync(sampleStreamId, 0).GetAwaiter().GetResult();
                Console.WriteLine("Deleting the rest of the events");
                qiDataService.RemoveWindowValuesAsync(sampleStreamId, 2, 198).GetAwaiter().GetResult();

                DelayForQiConsistency();

                Console.WriteLine("Checking for events");
                Console.WriteLine("===================");
                foundEvents = qiDataService.GetWindowValuesAsync<WaveData>(sampleStreamId, "0", "198").GetAwaiter().GetResult();
                DumpEvents(foundEvents);
                Console.WriteLine("Test ran successfully");
                Console.WriteLine("====================");
                Console.WriteLine("Press any button to shutdown");
                Console.ReadLine();

                #endregion
                
                #endregion
            }
            catch (QiHttpClientException qerr)
            {
                PrintError("Error in Qi Service", qerr);
            }
            catch (Exception ex)
            {
                PrintError("Unknown Error", ex);
            }
            finally
            {
                // clean up all created entities so you can run this again
                // all entities are reference counted, so you must delete the stream, then the type it uses
                Console.WriteLine("Deleting the stream...");
                HandleQiCallAsync(async () => await qiMetadataService.DeleteStreamAsync(sampleStreamId)).GetAwaiter().GetResult();

                Console.WriteLine("Deleting the behavior...");
                HandleQiCallAsync(async () => await qiMetadataService.DeleteBehaviorAsync(sampleBehaviorId)).GetAwaiter().GetResult();

                Console.WriteLine("Deleting the type...");
                HandleQiCallAsync(async () => await qiMetadataService.DeleteTypeAsync(sampleTypeId)).GetAwaiter().GetResult();
            }
        }

        /// <summary>
        ///     Returns a service which makes calls taht manage namespaces
        /// </summary>
        /// <returns></returns>
        protected static IQiAdministrationService GetQiAdministrationService()
        {
            QiSecurityHandler qiSecurityHandler = GetQiSecurityHandler();
            Uri qiServerUri = new Uri(Constants.QiServerUrl);
            IQiAdministrationService qiAdministrationService = QiService.GetAdministrationService(qiServerUri, Constants.TenantId, qiSecurityHandler);

            return qiAdministrationService;
        }

        /// <summary>
        ///     Returns a service which makes calls that manage streams, types, and behaviors
        /// </summary>
        /// <param name="namespaceId">The id of the namespace that the service will interface with</param>
        /// <returns></returns>
        protected static IQiMetadataService GetQiMetadataService(string namespaceId)
        {
            QiSecurityHandler qiSecurityHandler = GetQiSecurityHandler();
            Uri qiServerUri = new Uri(Constants.QiServerUrl);
            IQiMetadataService qiMetadataService = QiService.GetMetadataService(qiServerUri, Constants.TenantId, namespaceId, qiSecurityHandler);

            return qiMetadataService;
        }

        /// <summary>
        ///     Returns a service which makes calls taht manage data held in streams
        /// </summary>
        /// <param name="namespaceId"></param>
        /// <returns></returns>
        protected static IQiDataService GetQiDataService(string namespaceId)
        {
            QiSecurityHandler qiSecurityHandler = GetQiSecurityHandler();
            Uri qiServerUri = new Uri(Constants.QiServerUrl);
            IQiDataService qiDataService = QiService.GetDataService(qiServerUri, Constants.TenantId, namespaceId, qiSecurityHandler);

            return qiDataService;
        }

        /// <summary>
        ///     This will return a QiSecurityHandler using the values held in Constants
        /// </summary>
        /// <returns></returns>
        protected static QiSecurityHandler GetQiSecurityHandler()
        {
            QiSecurityHandler qiSecurityHandler = new QiSecurityHandler(Constants.SecurityResource, Constants.TenantId, Constants.SecurityAppId, Constants.SecurityAppKey);

            return qiSecurityHandler;
        }

        /// <summary>
        ///     Prints out each event in the list of events given
        /// </summary>
        /// <param name="evnts"></param>
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
            catch (QiHttpClientException qerr)
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
