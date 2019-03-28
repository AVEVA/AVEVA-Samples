// <copyright file="Widget.cs" company="OSIsoft, LLC">
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
using OSIsoft.Data;

namespace UomsSample
{
    class Widget
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        [SdsMember(Uom = "degree Fahrenheit")]
        public double Temperature { get; set; }

        [SdsMember(Uom = "mile")]
        public double Distance { get; set; }

    }
}
