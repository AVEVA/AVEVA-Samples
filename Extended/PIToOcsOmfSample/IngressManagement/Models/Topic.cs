using System;
using System.Collections.Generic;

namespace PIToOcsOmfSample.IngressManagement.Models
{
    class Topic
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string TenantId { get; set; }
        public string Description { get; set; }
        public DateTime CreatedDate { get; set; }
        public IEnumerable<string> MappedPublishers { get; set; }
    }
}
