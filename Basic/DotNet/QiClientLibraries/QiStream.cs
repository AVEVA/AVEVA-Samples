using System;
using System.Collections.Generic;
using System.Text;

namespace QiRestApiCore
{
    public class QiStream
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

        public string TypeId
        {
            get;
            set;
        }

        public string BehaviorId
        {
            get;
            set;
        }

        public IDictionary<string, string> Metadata
        {
            get;
            set;
        }

        public IList<string> Tags
        {
            get;
            set;
        }
    }
}
