using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public class QiError : Exception
    {
        public QiError(HttpStatusCode code, string msg)
            : base(msg)
        {
            Code = code;
        }

        public HttpStatusCode Code
        {
            get;
            private set;
        }
    }
}
