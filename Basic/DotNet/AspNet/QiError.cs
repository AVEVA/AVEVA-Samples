using System;
using System.Net;

namespace RestSample
{
    public class QiError : Exception
    {
        #region Public Constructors

        public QiError(HttpStatusCode code, string msg)
        {
            Code = code;
            Message = msg;
        }

        #endregion Public Constructors

        #region Public Properties

        public HttpStatusCode Code { get; private set; }

        public new string Message { get; private set; }

        #endregion Public Properties
    }
}