using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OMFSample.DataIngress.OmfMessageContent
{
    public class OmfContainer
    {
        public string Id { get; set; }
        public string TypeId { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public IDictionary<string, string> MetaData { get; set; }
    }
}
