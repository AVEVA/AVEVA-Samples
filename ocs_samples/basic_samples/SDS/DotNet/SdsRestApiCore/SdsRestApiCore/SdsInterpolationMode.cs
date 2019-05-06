// <copyright file="SdsInterpolationMode.cs" company="OSIsoft, LLC">
//
// </copyright>

using System;
using System.Collections.Generic;
using System.Text;

namespace SdsRestApiCore
{
    public enum SdsInterpolationMode
    {
        Default = Continuous,
        Continuous = 0,
        StepwiseContinuousLeading = 1,
        StepwiseContinuousTrailing = 2,
        Discrete = 3
    }
}
