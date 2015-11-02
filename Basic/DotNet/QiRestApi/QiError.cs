using System;
using System.Net;

namespace QiRestApiSample
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
