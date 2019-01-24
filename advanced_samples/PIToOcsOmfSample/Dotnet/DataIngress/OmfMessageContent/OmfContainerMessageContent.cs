// <copyright file="OmfContainerMessageContent.cs" company="OSIsoft, LLC">
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
    /// This class is serialized into part of an OMF container message. It groups information to be sent 
    /// in an OMF container message. The information translates to a SDSStream in OSIsoft cloud services.
    /// </summary>
    public class OmfContainerMessageContent
    {
        public IEnumerable<OmfContainer> Containers { get; set; }

        public byte[] ToByteArray()
        {
            string json = JsonConvert.SerializeObject(Containers);
            return Encoding.UTF8.GetBytes(json);
        }
    }
}
