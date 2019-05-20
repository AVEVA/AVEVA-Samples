using OSIsoft.Omf.DefinitionAttributes;
using System;

namespace OmfIngressClientLibraries
{
    [OmfType(Id = "DataPointType")]
    public class DataPointType
    {
        [OmfProperty(IsIndex = true)]
        public DateTime Timestamp { get; set; }
        public double Value { get; set; }
    }
}
