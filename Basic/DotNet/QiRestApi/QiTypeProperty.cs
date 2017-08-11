using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiTypeProperty
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

        public int Order
        {
            get;
            set;
        }

        public QiType QiType
        {
            get;
            set;
        }

        public bool IsKey
        {
            get;
            set;
        }
    }
}
