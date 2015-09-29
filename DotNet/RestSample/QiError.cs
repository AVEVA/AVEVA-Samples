using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public class QiError: Exception
    {
        public HttpStatusCode Code
        {
            get;
            private set;
        }

        public String Message
        {
            get;
            private set;
        }

        public QiError(HttpStatusCode code, string msg)
        {
            Code = code;
            Message = msg;
        }
    }
}
