using OSIsoft.OmfIngress.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace OmfIngressClientLibraries
{
    public class OmfConnection
    {
        public string[] ClientIds { get; set; }
        public Topic Topic { get; set; }
        public Subscription Subscription { get; set; }
    }
}
