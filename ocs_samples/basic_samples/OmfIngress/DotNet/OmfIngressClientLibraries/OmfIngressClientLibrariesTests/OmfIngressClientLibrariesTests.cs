using OmfIngressClientLibraries;
using OSIsoft.Data;
using OSIsoft.Data.Http;
using OSIsoft.Identity;
using System;
using System.Diagnostics;
using System.Net;
using System.Threading.Tasks;
using Xunit;

namespace OmfIngressClientLibrariesTests
{
    public class OmfIngressClientLibrariesTests
    {
        [Fact]
        public async Task EndToEndTestAsync()
        {
            //Setting things up
            Program.Setup();

            //Initializing Sds Service
            ISdsMetadataService sdsMetadataService = SdsService.GetMetadataService(new Uri(Program._address), Program._tenantId, Program._namespaceId,
                new AuthenticationHandler(new Uri(Program._address), Program._clientId, Program._clientSecret));
            ISdsDataService sdsDataService = SdsService.GetDataService(new Uri(Program._address), Program._tenantId, Program._namespaceId,
                new AuthenticationHandler(new Uri(Program._address), Program._clientId, Program._clientSecret));

            OmfConnection omfConnection = null;

            try
            {
                //Create the Connection, send OMF
                omfConnection = await Program.CreateOmfConnectionAsync();
                await Program.SendTypeContainerAndDataAsync();

                //Check if Data was successfully stored in Sds
                DataPointType firstValueForStream = null;
                await PollUntilTrueAsync(async () =>
                {
                    try
                    {
                        firstValueForStream = await sdsDataService.GetFirstValueAsync<DataPointType>(Program._streamId);
                        return true;
                    }
                    catch
                    {
                        return false;
                    }
                }, TimeSpan.FromSeconds(180), TimeSpan.FromSeconds(1));
                Assert.NotNull(firstValueForStream);
            }
            finally
            {
                //Delete the Type and Stream
                await Program.DeleteTypeAndContainerAsync();

                //Verify the Type was successfully deleted in Sds
                bool deleted = await PollUntilTrueAsync(async () =>
                {
                    try
                    {
                        SdsType sdsType = await sdsMetadataService.GetTypeAsync("DataPointType");
                        return false;
                    }
                    catch (Exception ex) when (ex is SdsHttpClientException sdsHttpClientException
                        && sdsHttpClientException.StatusCode == HttpStatusCode.NotFound)
                    {
                        return true;
                    }
                    catch
                    {
                        return false;
                    }
                }, TimeSpan.FromSeconds(180), TimeSpan.FromSeconds(1));
                Assert.True(deleted);

                await Program.DeleteOmfConnectionAsync(omfConnection);
            }
        }

        private static async Task<bool> PollUntilTrueAsync(Func<Task<bool>> condition, TimeSpan timeout, TimeSpan waitBetweenPolls)
        {
            Stopwatch sw = Stopwatch.StartNew();

            while (sw.Elapsed < timeout)
            {
                if (await condition.Invoke())
                {
                    return true;
                }
                await Task.Delay(waitBetweenPolls);
            }

            return false;
        }
    }
}
