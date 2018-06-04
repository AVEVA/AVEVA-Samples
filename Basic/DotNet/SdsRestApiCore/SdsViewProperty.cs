using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsViewProperty
    {
        public string SourceId
        {
            get;
            set;
        }

        public string TargetId
        {
            get;
            set;
        }

        public SdsView SdsView
        {
            get;
            set;
        }
    }
}
