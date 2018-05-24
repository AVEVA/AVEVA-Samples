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