// <copyright file="OmfTypeMessageContent.cs" company="OSIsoft, LLC">
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
using System.Collections.Generic;
using System.Text;
using OMFSample.DataIngress.OmfMessageContent;
namespace PIToOcsOmfSample.DataIngress.OmfMessageContent
{
    /// <summary>
    /// This class is serialized into part of an OMF type message. It groups information to be sent 
    /// in an OMF type message. The information translates to a SDSType in OSIsoft cloud services.
    /// </summary>
    public class OmfTypeMessageContent
    {
        public IEnumerable<OmfType> Types { get; set; }

        public byte[] ToByteArray()
        {
            var serializedTypes = new List<string>();
            foreach (OmfType typeContent in Types)
            {
                serializedTypes.Add(SerializeToJson(typeContent));
            }

            string json = $"[{string.Join(",", serializedTypes)}]";
            return Encoding.UTF8.GetBytes(json);
        }

        /// <summary>
        /// This client does not use the default Newtonsoft.Json serialization to create OSIsoft Message Format type messages.
        /// Instead, custom formatting is done within the client. Types that are sent as part of this sample will all have 
        /// common structure and some common properties. This is included in this method rather than in the representation of the
        /// OMF type message content.
        /// </summary>
        private string SerializeToJson(OmfType omfType)
        {
            var serializedValue = @"""Value"": { ""type"": """ + omfType.ValueType + @""", ""format"": """ + omfType.Format + @""" }";

            if (omfType.ValueType == "array")
            {
                serializedValue = @"""Value"": {
                    ""type"": """ + omfType.ValueType + @""",
                    ""items"": {
                        ""type"": ""integer""
                        }
                    }";
            }

            return @"{
                        ""id"": """ + omfType.Id + @""",
                        ""type"": ""object"",
                        ""classification"": ""dynamic"",
                        ""properties"": {
                            ""Time"": { ""type"": ""string"", ""format"": ""date-time"", ""isindex"": true },"
                            + serializedValue +
                        @"}
                    }";
        }
    }
}
