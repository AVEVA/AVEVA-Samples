using System;

namespace PIToOcsOmfSample.IngressManagement.Models
{
    class Token
    {
        public string Id { get; set; }
        public string PublisherId { get; set; }
        public string TokenString { get; set; }
        public DateTime CreationDate { get; set; }
        public DateTime ExpirationDate { get; set; }
        public bool IsDeleted { get; set; }
    }
}
