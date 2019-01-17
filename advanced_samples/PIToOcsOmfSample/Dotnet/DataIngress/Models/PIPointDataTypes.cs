// <copyright file="PIPointDataTypes.cs" company="OSIsoft, LLC">
//
// Copyright (C) 2018 OSIsoft, LLC. All rights reserved.
//
// THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
// OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
// THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.
//
// RESTRICTED RIGHTS LEGEND
// Use, duplication, or disclosure by the Government is subject to restrictions
// as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
// Computer Software clause at DFARS 252.227.7013
//
// OSIsoft, LLC
// 1600 Alvarado St, San Leandro, CA 94577
// </copyright>

using System;

namespace PIToOcsOmfSample.DataIngress
{
    /// <summary>
    /// All data events retrieved from PI points will be indexed on time. All data events retrieved 
    /// from PI points will also have some description of data quality, represented here by the IsGood 
    /// flag.
    /// </summary>
    public abstract class PIData
    {
        public DateTime Time { get; set; }
    }

    public class NumberData : PIData
    {
        public double Value { get; set; }
    }

    public class IntegerData : PIData
    {
        public Int64 Value { get; set; }
    }

    public class StringData : PIData
    {
        public string Value { get; set; }
    }

    public class TimeData : PIData
    {
        public string Value { get; set; }
    }

    public class ByteArrayData : PIData
    {
        public byte[] Value { get; set; }
    }
}
