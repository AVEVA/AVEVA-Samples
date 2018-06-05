using System;

namespace PIToOcsOmfSample.IngressManagement.Models
{
    public enum SubscriptionType
    {
        NonQi,
        Qi
    }

    class Subscription
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string TopicId { get; set; }
        public string TopicTenantId { get; set; }
        public string SubscriptionTenantId { get; set; }
        public bool? IsRevoked { get; set; }
        public string Description { get; set; }
        public SubscriptionType Type { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool? Enabled { get; set; }
        public string OCSNamespace { get; set; }
    }
}
