// <copyright file="SdsStreamViewMap.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsStreamViewMap
    {
        public string SourceTypeId
        {
            get;
            set;
        }

        public string TargetTypeId
        {
            get;
            set;
        }

        public IList<SdsStreamViewProperty> Properties
        {
            get;
            set;
        }

    }
}
