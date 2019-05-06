// <copyright file="SdsExtrapolationMode.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public enum SdsExtrapolationMode : int
    {
        All = 0,
        None = 1,
        Forward = 2,
        Backward = 3
    }
}
