using OSIsoft.Data.Http;
using OSIsoft.Identity;
using OSIsoft.Omf;
using OSIsoft.OmfIngress.Contracts;
using System;

namespace OmfIngressClientLibraries
{
    internal class Device
    {
        private IIngressService _deviceIngressService;

        public Device(string address, string tenantId, string namespaceId, string clientId, string clientSecret)
        {
            AuthenticationHandler deviceAuthenticationHandler = new AuthenticationHandler(new Uri(address), clientId, clientSecret);

            IngressService deviceBaseIngressService = new IngressService(new Uri(address), null, HttpCompressionMethod.None, deviceAuthenticationHandler);
            _deviceIngressService = deviceBaseIngressService.GetIngressService(tenantId, namespaceId);
        }

        public async void CreateDataPointTypeAsync()
        {
            Console.WriteLine($"Creating Type with Id {typeof(DataPointType).Name}");
            Console.WriteLine();

            OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));
            //await _deviceIngressService.SendOMFMessageAsync(typeMessage);
        }

        public async void CreateStreamAsyc(string streamId)
        {
            //create container
            Console.WriteLine($"Creating Container with Id {streamId}");
            Console.WriteLine();

            OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));
            //await _deviceIngressService.SendOMFMessageAsync(containerMessage);
        }

        public async void SendValueAsync(string streamId, DataPointType value)
        {
            OmfDataMessage dataMessage = OmfMessageCreator.CreateDataMessage(streamId, value);

            //await _deviceIngressService.SendOMFMessageAsync(dataMessage);
            Console.WriteLine($"Sent data point: Time: {value.Timestamp}, Value: {value.Value}");
        }

        public async void DeleteStreamAsync(string streamId)
        {
            //delete container
            Console.WriteLine($"Deleting Container with Id {streamId}");
            Console.WriteLine();
            OmfContainerMessage containerMessage = OmfMessageCreator.CreateContainerMessage(streamId, typeof(DataPointType));
            containerMessage.ActionType = ActionType.Delete;
            //await _deviceIngressService.SendOMFMessageAsync(containerMessage);  
        }

        public async void DeleteDataPointTypeAsync()
        {
            //delete type
            Console.WriteLine($"Deleting Type with Id {typeof(DataPointType).Name}");
            Console.WriteLine();
            OmfTypeMessage typeMessage = OmfMessageCreator.CreateTypeMessage(typeof(DataPointType));
            typeMessage.ActionType = ActionType.Delete;
            //await _deviceIngressService.SendOMFMessageAsync(typeMessage);   
        }
    }
}
