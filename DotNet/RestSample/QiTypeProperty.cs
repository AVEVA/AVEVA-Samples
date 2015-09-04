using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
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
