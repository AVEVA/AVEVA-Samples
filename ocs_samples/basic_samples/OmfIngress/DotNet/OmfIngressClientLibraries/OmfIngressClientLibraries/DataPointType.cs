using OSIsoft.Omf;
using OSIsoft.Omf.DefinitionAttributes;
using System;

namespace OmfIngressClientLibraries
{
    [OmfType(Id = "DataPointType", ClassificationType = ClassificationType.Dynamic)]
    public class DataPointType
    {
        [OmfProperty(IsIndex = true)]
        public DateTime Timestamp { get; set; }
        public double Value { get; set; }
    }
}
