using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsView
    {
        public string Id
        {
            get;
            set;
        }

        public string Name
        {
            get;
            set;
        }

        public string Description
        {
            get;
            set;
        }

        public string SourceTypeId
        {
            get;
            set;
        }

        public string TargetTypeId
        {
            get;
            set;
        }

        public IList<SdsViewProperty> Properties
        {
            get;
            set;
        }
    }
}
