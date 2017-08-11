using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiType
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

        public QiTypeCode QiTypeCode
        {
            get;
            set;
        }

        public IList<QiTypeProperty> Properties
        {
            get;
            set;
        }
    }
}
