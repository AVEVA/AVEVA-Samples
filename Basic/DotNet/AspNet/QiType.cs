using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
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

        public QiTypeProperty[] Properties
        {
            get;
            set;
        }
    }
}
