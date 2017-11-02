using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiViewProperty
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

        public QiView QiView
        {
            get;
            set;
        }
    }
}
