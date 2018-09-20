using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using OMFSample.DataIngress.OmfMessageContent;
namespace PIToOcsOmfSample.DataIngress.OmfMessageContent
{
    /// <summary>
    /// This class is serialized into part of an OMF container message. It groups information to be sent 
    /// in an OMF container message. The information translates to a QiStream in OSIsoft cloud services.
    /// </summary>
    public class OmfContainerMessageContent
    {
        public IEnumerable<OmfContainer> Containers { get; set; }

        public byte[] ToByteArray()
        {
            string json = JsonConvert.SerializeObject(Containers);
            return Encoding.UTF8.GetBytes(json);
        }
    }
}
