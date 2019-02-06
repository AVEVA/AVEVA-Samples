// <copyright file="CommandLineOptions.cs" company="OSIsoft, LLC">
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
