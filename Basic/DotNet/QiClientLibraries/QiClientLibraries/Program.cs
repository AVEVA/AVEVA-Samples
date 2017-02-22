using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using OSIsoft.Qi;
using OSIsoft.Qi.Http.Security;
using OSIsoft.Qi.Reflection;

namespace QiClientLibraries
{
    internal class Program
    {
        private static WaveData GetWave(int order, double range, double multiplier)
        {
            var radians = order / range * 2 * Math.PI;

            return new WaveData
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians)
            };
        }

        private static void UpdateWave(WaveData wave, double multiplier)
        {
            wave.Tau = wave.Radians / (2 * Math.PI);
            wave.Sin = multiplier * Math.Sin(wave.Radians);
            wave.Cos = multiplier * Math.Cos(wave.Radians);
            wave.Tan = multiplier * Math.Tan(wave.Radians);
            wave.Sinh = multiplier * Math.Sinh(wave.Radians);
            wave.Cosh = multiplier * Math.Cosh(wave.Radians);
            wave.Tanh = multiplier * Math.Tanh(wave.Radians);
        }

        private static void Main(string[] args)
        {
            // ==== Client constants ====
            var tenant = ConfigurationManager.AppSettings["Tenant"];
            var address = ConfigurationManager.AppSettings["Address"];
            var resource = ConfigurationManager.AppSettings["Resource"];
            var appId = ConfigurationManager.AppSettings["AppId"];
            var appKey = ConfigurationManager.AppSettings["AppKey"];

            var namespaceId = ConfigurationManager.AppSettings["Namespace"];

            // ==== Setup the namespace.  The namespace provides isolation within a Tenant. ====
            var admin = QiService.GetAdministrationService(new Uri(address), tenant, new QiSecurityHandler(resource, tenant, appId, appKey));

            var sampleNamespace = new QiNamespace(namespaceId);
            sampleNamespace = admin.GetOrCreateNamespaceAsync(sampleNamespace).GetAwaiter().GetResult();

            // ==== Setup the type and stream ====
            var config = QiService.GetMetadataService(new Uri(address), tenant, namespaceId, new QiSecurityHandler(resource, tenant, appId, appKey));

            QiType type = QiTypeBuilder.CreateQiType<WaveData>();
            type = config.GetOrCreateTypeAsync(type).GetAwaiter().GetResult();

            var stream = new QiStream
            {
                Id = Guid.NewGuid().ToString(),
                Name = "Wave Data Sample",
                TypeId = type.Id,
                Description = "This is a sample QiStream for storing WaveData type measurements"
            };
            stream = config.GetOrCreateStreamAsync(stream).GetAwaiter().GetResult();

            // ==== Perform a number of CRUD opreations ====
            var client = QiService.GetDataService(new Uri(address), tenant, namespaceId, new QiSecurityHandler(resource, tenant, appId, appKey));

            // Insert a single event into a stream
            var wave = GetWave(0, 200, 2);
            client.InsertValueAsync(stream.Id, wave).GetAwaiter().GetResult();

            // Update will add the event as well
            wave.Order += 1;
            client.UpdateValueAsync(stream.Id, wave).GetAwaiter().GetResult();

            // Inserting a collection of events into a stream (more efficient)
            var waves = new List<WaveData>();
            for (var i = 2; i <= 200; ++i)
            {
                waves.Add(GetWave(i, 200, 2));
            }

            client.InsertValuesAsync(stream.Id, waves).GetAwaiter().GetResult();

            // Retrieve events for a the range.  Indexes are expected in string format.  Order property is is the Key
            IEnumerable<WaveData> retrieved = client.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200").GetAwaiter().GetResult();
            Console.WriteLine("Retrieved {0} events", retrieved.Count());
            Console.WriteLine("\tfrom {0} {1}", retrieved.First().Order, retrieved.First().Sin);
            Console.WriteLine("\tto {0} {1}", retrieved.Last().Order, retrieved.Last().Sin);

            // Update some events
            UpdateWave(retrieved.First(), 4);
            client.UpdateValueAsync(stream.Id, retrieved.First()).GetAwaiter().GetResult();

            foreach (var value in waves)
            {
                UpdateWave(value, 4);
            }

            client.UpdateValuesAsync(stream.Id, waves.ToList()).GetAwaiter().GetResult();

            retrieved = client.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200").GetAwaiter().GetResult();
            Console.WriteLine("Updated {0} events", retrieved.Count());
            Console.WriteLine("\tfrom {0} {1}", retrieved.First().Order, retrieved.First().Sin);
            Console.WriteLine("\tto {0} {1}", retrieved.Last().Order, retrieved.Last().Sin);

            // Stream behaviors modify retrieval
            // Retrieve a range of three values using the default behavior.  The default behavior is Continuous,
            // so ExactOrCalculated should bring back interpolated values
            retrieved = client.GetRangeValuesAsync<WaveData>(stream.Id, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
            Console.WriteLine("Default behavior {0} events", retrieved.Count());
            foreach (var value in retrieved)
            {
                Console.WriteLine("\t{0} {1}", value.Order, value.Sin);
            }

            // Modify the stream behavior to StepwiseContinuousLeading
            var stepwiseContinuousLeading = new QiStreamBehavior
            {
                Id = Guid.NewGuid().ToString(),
                Mode = QiStreamMode.StepwiseContinuousLeading
            };
            stepwiseContinuousLeading = config.GetOrCreateBehaviorAsync(stepwiseContinuousLeading).GetAwaiter().GetResult();

            stream.BehaviorId = stepwiseContinuousLeading.Id;
            config.UpdateStreamAsync(stream.Id, stream).GetAwaiter().GetResult();

            retrieved = client.GetRangeValuesAsync<WaveData>(stream.Id, "1", 0, 3, false, QiBoundaryType.ExactOrCalculated).GetAwaiter().GetResult();
            Console.WriteLine("StepwiseContinuousLeading behavior {0} events", retrieved.Count());
            foreach (var value in retrieved)
            {
                Console.WriteLine("\t{0} {1}", value.Order, value.Sin);
            }

            // Delete the first event in the stream, the event at index zero
            client.RemoveValueAsync(stream.Id, 0).GetAwaiter().GetResult();

            // Delete the rest of the Events
            client.RemoveWindowValuesAsync(stream.Id, 1, 200).GetAwaiter().GetResult();

            retrieved = client.GetWindowValuesAsync<WaveData>(stream.Id, "0", "200").GetAwaiter().GetResult();
            Console.WriteLine("After delete {0} events remain", retrieved.Count());

            // Delete the stream and behavior
            config.DeleteStreamAsync(stream.Id).GetAwaiter().GetResult();
            config.DeleteBehaviorAsync(stepwiseContinuousLeading.Id).GetAwaiter().GetResult();

            // It is less common to remove the type and namespace
            config.DeleteTypeAsync(type.Id).GetAwaiter().GetResult();
            // admin.DeleteNamespaceAsync(sampleNamespace.Id).GetAwaiter().GetResult();
        }
    }
}