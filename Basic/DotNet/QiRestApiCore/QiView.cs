using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiView
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

        public IList<QiViewProperty> Properties
        {
            get;
            set;
        }
    }
}
