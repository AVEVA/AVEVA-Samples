// <copyright file="SdsStreamViewProperty.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsStreamViewProperty
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

        public SdsStreamView SdsStreamView
        {
            get;
            set;
        }
    }
}
