// <copyright file="WaveData.cs" company="OSIsoft, LLC">
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

using OSIsoft.Data;
using System.Text;

namespace SdsClientLibraries
{
    public class WaveData
    {
        [SdsMember(IsKey = true)]
        public int Order { get; set; }

        public double Tau { get; set; }

        public double Radians { get; set; }

        public double Sin { get; set; }

        public double Cos { get; set; }

        public double Tan { get; set; }

        public double Sinh { get; set; }

        public double Cosh { get; set; }

        public double Tanh { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"Order: {Order}");
            builder.Append($", Radians: {Radians}");
            builder.Append($", Tau: {Tau}");
            builder.Append($", Sin: {Sin}");
            builder.Append($", Cos: {Cos}");
            builder.Append($", Tan: {Tan}");
            builder.Append($", Sinh: {Sinh}");
            builder.Append($", Cosh: {Cosh}");
            builder.Append($", Tanh: {Tanh}");
            return builder.ToString();
        }
    }

    public class WaveDataTarget
    {
        [SdsMember(IsKey = true)]
        public int OrderTarget { get; set; }

        public double TauTarget { get; set; }

        public double RadiansTarget { get; set; }

        public double SinTarget { get; set; }

        public double CosTarget { get; set; }

        public double TanTarget { get; set; }

        public double SinhTarget { get; set; }

        public double CoshTarget { get; set; }

        public double TanhTarget { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"OrderTarget: {OrderTarget}");
            builder.Append($", RadiansTarget: {RadiansTarget}");
            builder.Append($", TauTarget: {TauTarget}");
            builder.Append($", SinTarget: {SinTarget}");
            builder.Append($", CosTarget: {CosTarget}");
            builder.Append($", TanTarget: {TanTarget}");
            builder.Append($", SinhTarget: {SinhTarget}");
            builder.Append($", CoshTarget: {CoshTarget}");
            builder.Append($", TanhTarget: {TanhTarget}");
            return builder.ToString();
        }
    }

    public class WaveDataInteger
    {
        [SdsMember(IsKey = true)]
        public int OrderTarget { get; set; }

        public int SinInt { get; set; }

        public int CosInt { get; set; }

        public int TanInt { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"OrderTarget: {OrderTarget}");
            builder.Append($", SinInt: {SinInt}");
            builder.Append($", CosInt: {CosInt}");
            builder.Append($", TanInt: {TanInt}");
            return builder.ToString();
        }
    }
}
