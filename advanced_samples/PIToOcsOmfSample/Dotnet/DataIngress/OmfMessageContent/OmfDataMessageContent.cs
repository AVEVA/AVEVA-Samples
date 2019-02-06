// <copyright file="OmfDataMessageContent.cs" company="OSIsoft, LLC">
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

using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using OMFSample.DataIngress.OmfMessageContent;
namespace PIToOcsOmfSample.DataIngress.OmfMessageContent
{
    /// <summary>
    /// This class is serialized into part of an OMF data message. It groups information to be sent 
    /// in an OMF data message. The information translates to an event in an OSIsoft cloud services 
    /// SDSStream.
    /// </summary>
    public class OmfDataMessageContent
    {
        // OMF data messages can specify a container Id once for a set of data values. This class facilitates that translation.
        private class CompactOmfData
        {
            public string ContainerId { get; set; }

            public IEnumerable<PIData> Values { get; set; }
        }

        private readonly CompactOmfData _compactOmfData;

        public OmfDataMessageContent(string containerId, IEnumerable<PIData> values)
        {
            _compactOmfData = new CompactOmfData()
            {
                ContainerId = containerId,
                Values = values
            };
        }

        public byte[] ToByteArray()
        {
            string json = $"[{JsonConvert.SerializeObject(_compactOmfData)}]";
            return Encoding.UTF8.GetBytes(json);
        }
    }
}
