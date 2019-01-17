// <copyright file="CommandLineOptions.cs" company="OSIsoft, LLC">
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
using CommandLine;

namespace PItoOCSviaAPISample
{
    class CommandLineOptions
    {
        [Option('t', "tagMask", Required = true,
            HelpText =
                "Name mask used to select tags for transfer. Wild card characters such as '*' and '?' are allowed.")]
        public string TagMask { get; set; }

        [Option('s', "startTime", Required = true,
            HelpText = "Start of range for data retrieval. Supports only absolute times.")]
        public DateTime StartTime { get; set; }

        [Option('e', "endTime", Required = true,
            HelpText = "End of range for data retrieval. Supports only absolute times.")]
        public DateTime EndTime { get; set; }

        public enum DataWriteModes
        {
            clearExistingData,
            appendToExistingData
        }

        [Option('m', "mode", Required = false, Default = DataWriteModes.appendToExistingData,
            HelpText =
                "[clearExistingData|appendToExistingData] will optionally clear previous data for streams by deleting and recreating them.")]
        public DataWriteModes Mode { get; set; }
    }
}
