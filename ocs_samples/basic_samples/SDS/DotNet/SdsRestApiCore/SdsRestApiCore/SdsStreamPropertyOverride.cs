// <copyright file="SdsStreamPropertyOverride.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsStreamPropertyOverride
    {
        public string SdsTypePropertyId
        {
            get;
            set;
        }

        public string Uom
        {
            get;
            set;
        }

        public SdsInterpolationMode InterpolationMode
        {
            get;
            set;
        }
    }
}
