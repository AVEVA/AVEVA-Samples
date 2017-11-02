using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiViewMap
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

        public IList<QiViewProperty> Properties
        {
            get;
            set;
        }

    }
}
