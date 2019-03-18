// <copyright file="SdsStream.cs" company="OSIsoft, LLC">
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
