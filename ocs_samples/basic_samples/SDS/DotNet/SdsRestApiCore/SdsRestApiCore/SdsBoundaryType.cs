// <copyright file="SdsBoundaryType.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public enum SdsBoundaryType
    {
        Exact = 0,
        Inside = 1,
        Outside = 2,
        ExactOrCalculated = 3
    }
}
