// <copyright file="OmfDataMessageContent.cs" company="OSIsoft, LLC">
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

using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using OMFSample.DataIngress.OmfMessageContent;
namespace PIToOcsOmfSample.DataIngress.OmfMessageContent
{
    /// <summary>
    /// This class is serialized into part of an OMF data message. It groups information to be sent 
    /// in an OMF data message. The information translates to an event in an OSIsoft cloud services 
    /// QiStream.
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
