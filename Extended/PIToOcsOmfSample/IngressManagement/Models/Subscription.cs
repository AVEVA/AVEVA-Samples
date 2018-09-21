// <copyright file="Subscription.cs" company="OSIsoft, LLC">
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

namespace PIToOcsOmfSample.IngressManagement.Models
{
    public enum SubscriptionType
    {
        NonQi,
        Qi
    }

    class Subscription
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string TopicId { get; set; }
        public string TopicTenantId { get; set; }
        public string SubscriptionTenantId { get; set; }
        public bool? IsRevoked { get; set; }
        public string Description { get; set; }
        public SubscriptionType Type { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool? Enabled { get; set; }
        public string OCSNamespace { get; set; }
    }
}
