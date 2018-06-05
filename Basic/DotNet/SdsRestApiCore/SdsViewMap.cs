using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsViewMap
    {
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
