// <copyright file="PIPointDataTypes.cs" company="OSIsoft, LLC">
//
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.
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
