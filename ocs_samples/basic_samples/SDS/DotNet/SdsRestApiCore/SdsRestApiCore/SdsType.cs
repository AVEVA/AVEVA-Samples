// <copyright file="SdsType.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsType
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

        public SdsTypeCode SdsTypeCode
        {
            get;
            set;
        }

        public IList<SdsTypeProperty> Properties
        {
            get;
            set;
        }
    }
}
