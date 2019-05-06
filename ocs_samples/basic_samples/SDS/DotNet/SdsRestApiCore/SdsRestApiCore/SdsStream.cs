// <copyright file="SdsStream.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public class SdsStream
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

        public IList<SdsStreamIndex> Indexes
        {
            get;
            set;
        }


        public SdsInterpolationMode? InterpolationMode
        {
            get;
            set;
        }

        public SdsExtrapolationMode? ExtrapolationMode
        {
            get;
            set;
        }

        public IList<SdsStreamPropertyOverride> PropertyOverrides
        {
            get;
            set;
        }
    }
}
