using System;
using System.Collections.Generic;
using System.Configuration;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using OSIsoft.Qi;
using OSIsoft.Qi.Reflection;

namespace QiRestApi
{
    internal class Program
    {
        private static WaveData GetWave(int order, int range, double multiplier)
        {
            var radians = order / range * 2 * Math.PI;

            return new WaveData()
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians),
            };
        }

        private static void Main(string[] args)
        {
            // ==== Create the client ====
            var tenant = ConfigurationManager.AppSettings["Tenant"];
            var address = ConfigurationManager.AppSettings["Address"];
            var aadFormat = ConfigurationManager.AppSettings["AADInstanceFormat"];
            var resource = ConfigurationManager.AppSettings["Resource"];
            var appId = ConfigurationManager.AppSettings["AppId"];
            var appKey = ConfigurationManager.AppSettings["AppKey"];

            // A formal client should be wrapped in a retry handler.
            HttpClient client = HttpClientFactory.Create(new WebRequestHandler(),
                new AuthenticationHandler(resource, tenant, aadFormat, appId, appKey));
            client.BaseAddress = new Uri(address);

            // ==== Get or create the namespace, type and stream(s) ====
            var space = new QiNamespace()
            {
                Id = ConfigurationManager.AppSettings["Namespace"]
            };
            HttpResponseMessage response = client.GetAsync($"Qi/{tenant}/Namespaces/{space.Id}").GetAwaiter().GetResult();
            if (response.StatusCode == HttpStatusCode.NotFound)
                response = client.PostAsJsonAsync($"Qi/{tenant}/Namespaces", space).GetAwaiter().GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            var type = QiTypeBuilder.CreateQiType<WaveData>();
            response = client.GetAsync($"Qi/{tenant}/{space.Id}/Types/{type.Id}").GetAwaiter().GetResult();
            if (response.StatusCode == HttpStatusCode.NotFound)
                response = client.PostAsJsonAsync($"Qi/{tenant}/{space.Id}/Types", type).GetAwaiter().GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            var stream = new QiStream()
            {
                Id = Guid.NewGuid().ToString(),
                Name = typeof(WaveData).Name,
                Description = "Sample",
                TypeId = type.Id
            };
            response = client.GetAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}").GetAwaiter().GetResult();
            if (response.StatusCode == HttpStatusCode.NotFound)
                response = client.PostAsJsonAsync($"Qi/{tenant}/{space.Id}/Streams", stream).GetAwaiter().GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            // ==== Perform basic CRUD optations ====

            // insert a single event
            var wave = GetWave(0, 200, 2);
            response =
                client.PutAsJsonAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/UpdateValue", wave)
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            // Insert another single event using a Post instead of a Put
            wave.Order += 1;
            response =
                client.PostAsJsonAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/InsertValue", wave)
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            // Insert a collection of events
            var events = new List<WaveData>();
            for (var i = 2; i <= 200; i += 2)
                events.Add(GetWave(i, 200, 2));

            response =
                client.PostAsJsonAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/InsertValues", events)
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            // retrieve the newly inserted events
            response =
                client.GetAsync(
                        $"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/GetValues?startIndex={0}&endIndex={200}&count={100}")
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);
            var retrievedEvents = response.Content.ReadAsAsync<WaveData[]>().GetAwaiter().GetResult();

            // Update the events
            Array.ForEach(retrievedEvents, w => GetWave(w.Order, 200, 3));
            response =
                client.PutAsJsonAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/UpdateValues", events)
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            // ==== Clean up ====

            // It's not necessary to delete the values if you're deleting the stream
            response =
                client.DeleteAsync(
                        $"Qi/{tenant}/{space.Id}/Streams/{stream.Id}/Data/RemoveWindowValues?startIndex={0}&endIndex={200}")
                    .GetAwaiter()
                    .GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);

            response = client.DeleteAsync($"Qi/{tenant}/{space.Id}/Streams/{stream.Id}").GetAwaiter().GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);
            response = client.DeleteAsync($"Qi/{tenant}/{space.Id}/Types/{type.Id}").GetAwaiter().GetResult();
            if (!response.IsSuccessStatusCode)
                throw new HttpResponseException(response);
        }
    }
}