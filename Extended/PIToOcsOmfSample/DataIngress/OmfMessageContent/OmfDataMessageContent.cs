using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using OMFSample.DataIngress.OmfMessageContent;
namespace PIToOcsOmfSample.DataIngress.OmfMessageContent
{
    /// <summary>
    /// This class is serialized into part of an OMF data message. It groups information to be sent 
    /// in an OMF data message. The information translates to an event in an OSIsoft cloud services 
    /// QiStream.
    /// </summary>
    public class OmfDataMessageContent
    {
        // OMF data messages can specify a container Id once for a set of data values. This class facilitates that translation.
        private class CompactOmfData
        {
            public string ContainerId { get; set; }

            public IEnumerable<PIData> Values { get; set; }
        }

        private readonly CompactOmfData _compactOmfData;

        public OmfDataMessageContent(string containerId, IEnumerable<PIData> values)
        {
            _compactOmfData = new CompactOmfData()
            {
                ContainerId = containerId,
                Values = values
            };
        }

        public byte[] ToByteArray()
        {
            string json = $"[{JsonConvert.SerializeObject(_compactOmfData)}]";
            return Encoding.UTF8.GetBytes(json);
        }
    }
}
