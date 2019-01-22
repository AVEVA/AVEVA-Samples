// <copyright file="Program.cs" company="OSIsoft, LLC">
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
using System.Configuration;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using OSIsoft.AF.Data;
using OSIsoft.AF.PI;
using OSIsoft.AF.Time;
using CommandLine;
using OMFSample.DataIngress.OmfMessageContent;
using OSIsoft.AF.Asset;
using OSIsoft.Data.Http.Security;
using PIToOcsOmfSample.DataIngress;
using PIToOcsOmfSample.DataIngress.OmfMessageContent;
using PIToOcsOmfSample.IngressManagement;
namespace PIToOcsOmfSample
{
    public class Program
    {
        private const int MaxChunkSize = 256;

        class Options
        {
            [Option('t', "tagMask", Required = true,
                    HelpText = "Name mask used to select tags for transfer. Wild card characters such as '*' and '?' are allowed.")]
            public string TagMask { get; set; }

            [Option('s', "startTime", Required = true,
                HelpText = "Start of range for data retrieval. Supports only absolute times.")]
            public DateTime StartTime { get; set; }

            [Option('e', "endTime", Required = true,
                HelpText = "End of range for data retrieval. Supports only absolute times.")]
            public DateTime EndTime { get; set; }

            [Option('m', "dataWriteMode", Required = false,
                HelpText = "The write mode directs whether or not existing data in streams should be removed before the sample is run.", 
                Default = DataWriteMode.appendToExistingData)]
            public DataWriteMode WriteMode { get; set; }

            [Option('d', "deleteIngressObjects", Required = false,
                HelpText = "Include this option if you would like to delete the Publisher, Topic, and Subscription after running the sample.")]
            public bool DeleteIngressObjects { get; set; }

            public enum DataWriteMode
            {
                clearExistingData,
                appendToExistingData,
            }
        }

        internal enum OmfTypeCode
        {
            Number,
            Integer,
            String,
            Time,
            ByteArray
        }

        static int Main(string[] args)
        {
            var options = new Options();
            var errors = new List<Error>();
            var result = Parser.Default.ParseArguments<Options>(args);
            result.WithParsed(opts => options = opts).WithNotParsed(errs => errors = errs.ToList());
            if (errors.Any())
            {
                foreach (var error in errors)
                {
                    Console.WriteLine(error.Tag);
                }
                return 1;
            }

            NameValueCollection appSettings = ConfigurationManager.AppSettings;
            string accountId = appSettings["accountId"];
            string namespaceId = appSettings["namespaceId"];
            string clusterAddress = appSettings["address"];
            string ingressServiceUrl = clusterAddress + @"/api/omf";

            // Use a client secret, retrieved from the OSIsoft Cloud Services portal for your account, to 
            // create a SecurityHandler used to authenticate this app.
            string resource = appSettings["resource"];
            string clientId = appSettings["clientId"];
            string clientSecret = appSettings["clientSecret"];
            var securityHandler = new SdsSecurityHandler(resource, accountId, clientId, clientSecret);

            // Create a client to manage OSIsoft Cloud Services Ingress resources.
            using (var managementClient = new IngressManagementClient(clusterAddress, accountId, securityHandler))
            {
                // Connect to a PI server and select PI points for which to move data to OCS.
                var piServerName = appSettings["PIDataArchive"];
                var piServer = new PIServers()[piServerName];
                var points = PIPoint.FindPIPoints(piServer, options.TagMask).ToList();
                if (!points.Any())
                {
                    Console.WriteLine($"No PI points found matching the tagMask query!");
                    return 1;
                }

                // Create OCS data ingress objects.
                string publisherName = appSettings["publisherName"];
                string topicName = appSettings["topicName"];
                string subscriptionName = appSettings["subscriptionName"];
                Console.WriteLine("Setting up OSIsoft Cloud Services OMF ingress objects.");
                string publisherId = managementClient.GetOrCreatePublisherAsync(publisherName).GetAwaiter().GetResult();
                string producerToken = managementClient.GetOrCreateToken(publisherId).GetAwaiter().GetResult();
                string topicId = managementClient.GetOrCreateTopic(topicName, publisherId).GetAwaiter().GetResult();
                string subscriptionId = managementClient.GetOrCreateSubscription(subscriptionName, topicId, namespaceId).GetAwaiter().GetResult();

                // Each PI point type will be written to an OSIsoft Cloud Services(OCS) SDSStream.
                // The structure of each stream is defined by an OCS SDSType. We create this SDSType 
                // by posting an OSIsoft Message Format(OMF) type message to OCS.
                // PI point value types need to translate to OCS SDSTypes. We create a limited number
                // of SDSTypes in OCS and then map PI point value types to those SDSTypes. 
                // A mapping between PI point value types and the Ids of the SDSType that represents
                // them in OCS is shown below.
                Dictionary<OmfTypeCode, string> typeIdsByOmfType = new Dictionary<OmfTypeCode, string>();
                typeIdsByOmfType.Add(OmfTypeCode.Number, "numberValueAndTimestamp");
                typeIdsByOmfType.Add(OmfTypeCode.Integer, "integerValueAndTimestamp");
                typeIdsByOmfType.Add(OmfTypeCode.String, "stringValueAndTimestamp");
                typeIdsByOmfType.Add(OmfTypeCode.Time, "timeValueAndTimestamp");
                typeIdsByOmfType.Add(OmfTypeCode.ByteArray, "byteArrayValueAndTimestamp");

                using (var client = new IngressClient(ingressServiceUrl, producerToken) { UseCompression = true })
                {
                    // Create and send OMF Type messages.
                    Console.WriteLine("Creating basic types in OCS to represent the format of PI points.");
                    List<OmfType> types = GetOmfTypes(typeIdsByOmfType);
                    var omfTypeMessageContent = new OmfTypeMessageContent() { Types = types };
                    client.SendMessageAsync(omfTypeMessageContent.ToByteArray(), MessageType.Type, MessageAction.Create).GetAwaiter().GetResult();

                    // Generate containers for each of the point with the correct OMF message type.
                    List<OmfContainer> containers = GetOmfContainers(points, typeIdsByOmfType);
                    if (options.WriteMode == Options.DataWriteMode.clearExistingData)
                    {
                        // Deleting the OMF container deletes the underlying SDSStream and its data.
                        Console.WriteLine("Deleting OMF containers corresponding to the selected PI points that existed before the sample was run.");
                        var omfContainerMessageContent = new OmfContainerMessageContent() { Containers = containers };
                        client.SendMessageAsync(omfContainerMessageContent.ToByteArray(), MessageType.Container, MessageAction.Delete).GetAwaiter().GetResult();
                    }

                    Console.WriteLine("Creating corresponding containers for the PI points whose data will be written to OCS.");

                    // OSIsoft Cloud Services' OMF Ingress sets a size limit on the request accepted by its external endpoint. We may need to split, or chunk, 
                    // containers into multiple OMF messages sent to the endpoint.
                    for (int chunkStartIndex = 0; chunkStartIndex < containers.Count; chunkStartIndex += MaxChunkSize)
                    {
                        int numberOfContainersToSendInThisChunk = Math.Min(containers.Count - chunkStartIndex, MaxChunkSize);
                        var containersToSendInThisChunk = containers.GetRange(chunkStartIndex, numberOfContainersToSendInThisChunk).ToList();
                        var omfContainerMessageContent = new OmfContainerMessageContent() { Containers = containersToSendInThisChunk };
                        client.SendMessageAsync(omfContainerMessageContent.ToByteArray(), MessageType.Container, MessageAction.Create).GetAwaiter().GetResult();
                    }

                    // Write data from each PI point to a SDSStream.
                    foreach (PIPoint point in points)
                    {
                        Console.WriteLine($"Writing PI point data for point {point.Name} to OCS.");
                        string containerId = GetContainerId(point);
                        AFValues values = point.RecordedValues(new AFTimeRange(options.StartTime, options.EndTime), AFBoundaryType.Inside, null, true);

                        // OSIsoft Cloud Services' OMF Ingress sets a size limit on the request accepted by its external endpoint. We may need to split, or chunk, 
                        // events into multiple OMF messages sent to the endpoint.
                        for (int chunkStartIndex = 0; chunkStartIndex < values.Count; chunkStartIndex += MaxChunkSize)
                        {
                            int numberOfEventsToReadForThisChunk = Math.Min(values.Count - chunkStartIndex, MaxChunkSize);

                            // If there are multiple events at a single timestamp for the PI point, the most recently added event will be written to OCS.
                            List<AFValue> distinctValuesInChunk = values.GetRange(chunkStartIndex, numberOfEventsToReadForThisChunk).GroupBy(value => value.Timestamp).Select(valuesAtTimestamp => valuesAtTimestamp.Last()).ToList();
                            List<PIData> piDataEvents = GetPIData(distinctValuesInChunk, ToOmfTypeCode(point.PointType));

                            OmfDataMessageContent omfDataMessageContent = new OmfDataMessageContent(containerId, piDataEvents);

                            Console.WriteLine($"Sending PI point data from index {distinctValuesInChunk.First().Timestamp} to index {distinctValuesInChunk.Last().Timestamp} to OCS ({distinctValuesInChunk.Count} values).");
                            client.SendMessageAsync(omfDataMessageContent.ToByteArray(), MessageType.Data, MessageAction.Create).GetAwaiter().GetResult();
                        }
                    }
                }

                // Delete OCS data ingress objects.
                if (options.DeleteIngressObjects)
                {
                    Console.WriteLine($"Deleting subscription with Id {subscriptionId}.");
                    managementClient.DeleteSubscription(subscriptionId).GetAwaiter().GetResult();
                    Console.WriteLine($"Deleting topic with Id {topicId}.");
                    managementClient.DeleteTopicAsync(topicId).GetAwaiter().GetResult();
                    Console.WriteLine($"Deleting publisher with Id {publisherId}.");
                    managementClient.DeletePublisherAsync(publisherId).GetAwaiter().GetResult();
                }
            }

            return 0;
        }

        private static List<OmfType> GetOmfTypes(Dictionary<OmfTypeCode, string> typeIdsByOmfType)
        {
            var messageContents = new List<OmfType>();
            messageContents.Add(new OmfType()
            {
                Id = typeIdsByOmfType[OmfTypeCode.Number],
                ValueType = "number",
                Format = "float64",
                Name = "doubleValueAndTimestamp",
                Description = "Represents simple time series data with a floating point value"
            });
            messageContents.Add(new OmfType()
            {
                Id = typeIdsByOmfType[OmfTypeCode.Integer],
                ValueType = "integer",
                Format = "int64",
                Name = "integerValueAndTimestamp",
                Description = "Represents simple time series data with an integer value"
            });
            messageContents.Add(new OmfType()
            {
                Id = typeIdsByOmfType[OmfTypeCode.String],
                ValueType = "string",
                Name = "stringValueAndTimestamp",
                Description = "Represents simple time series data with a string value or timestamp value"
            });
            messageContents.Add(new OmfType()
            {
                Id = typeIdsByOmfType[OmfTypeCode.ByteArray],
                ValueType = "array",
                Name = "blobValueAndTimestamp",
                Description = "Represents simple time series data with a blob(byte array) value"
            });
            messageContents.Add(new OmfType()
            {
                Id = typeIdsByOmfType[OmfTypeCode.Time],
                ValueType = "string",
                Format = "date-time",
                Name = "timeValueAndTimestamp",
                Description = "Represents simple time series data with a Timestamp(DateTime) value"
            });
            return messageContents;
        }

        /// <summary>
        /// Creates the content of OMF container messages that will be sent to OSIsoft Cloud Services.
        /// </summary>
        /// <param name="points">Each PI point will correspond to a single SDSStream in OCS.</param>
        /// <param name="typeIdsByOmfType">The container that is generated for each PI point will be associated with the type indicated by a typeId defined in this dictionary.</param>
        /// <returns></returns>
        private static List<OmfContainer> GetOmfContainers(IEnumerable<PIPoint> points, Dictionary<OmfTypeCode, string> typeIdsByOmfType)
        {
            var containers = new List<OmfContainer>();
            foreach (var point in points)
            {
                //get description and other attributes. 
                var attributesOfInterest = new string[]
                {
                    PICommonPointAttributes.Descriptor, PICommonPointAttributes.EngineeringUnits,
                    PICommonPointAttributes.PointSource
                };

                point.LoadAttributes(attributesOfInterest);
                var descriptor = point.GetAttribute(PICommonPointAttributes.Descriptor).ToString();
                var otherAttributes = new Dictionary<string, string>();
                foreach (var s in attributesOfInterest)
                {
                    if (s == PICommonPointAttributes.Descriptor)
                    {
                        continue;
                    }
                    if (!point.IsAttributeLoaded(s))
                    {
                        continue;
                    }
                    otherAttributes.Add(s, point.GetAttribute(s).ToString());
                }

                var id = GetContainerId(point);
                var dataType = ToOmfTypeCode(point.PointType);

                containers.Add(new OmfContainer()
                {
                    Id = id,
                    TypeId = typeIdsByOmfType[dataType],
                    Name = id,
                    Description = descriptor,
                    MetaData = otherAttributes
                });
            }

            return containers;
        }

        private static List<PIData> GetPIData(IEnumerable<AFValue> afValues, OmfTypeCode omfTypeCode)
        {
            var piDataList = new List<PIData>();
            switch (omfTypeCode)
            {
                case OmfTypeCode.Integer:
                    piDataList.AddRange(GetPIPointIntegerData(afValues));
                    break;
                case OmfTypeCode.Number:
                    piDataList.AddRange(GetPIPointNumberData(afValues));
                    break;
                case OmfTypeCode.String:
                    piDataList.AddRange(GetPIPointStringData(afValues));
                    break;
                case OmfTypeCode.Time:
                    piDataList.AddRange(GetPIPointTimeData(afValues));
                    break;
                case OmfTypeCode.ByteArray:
                    piDataList.AddRange(GetPIPointBlobData(afValues));
                    break;
                default:
                    throw new ArgumentOutOfRangeException();
            }

            return piDataList;
        }

        private static List<PIData> GetPIPointIntegerData(IEnumerable<AFValue> afValues)
        {
            var dataList = new List<PIData>();
            foreach (AFValue afValue in afValues)
            {
                if (afValue.IsGood)
                {
                    dataList.Add(new IntegerData() { Time = afValue.Timestamp, Value = afValue.ValueAsInt32() });
                }
            }
            return dataList;
        }

        private static List<PIData> GetPIPointNumberData(IEnumerable<AFValue> afValues)
        {
            var dataList = new List<PIData>();
            foreach (AFValue afValue in afValues)
            {
                if (afValue.IsGood)
                {
                    dataList.Add(new NumberData() { Time = afValue.Timestamp, Value = afValue.ValueAsDouble() });
                }
            }
            return dataList;
        }

        private static List<PIData> GetPIPointStringData(IEnumerable<AFValue> afValues)
        {
            var dataList = new List<PIData>();
            foreach (AFValue afValue in afValues)
            {
                if (afValue.IsGood)
                {
                    dataList.Add(new StringData() { Time = afValue.Timestamp, Value = afValue.Value.ToString() });
                }
            }
            return dataList;
        }

        private static List<PIData> GetPIPointTimeData(IEnumerable<AFValue> afValues)
        {
            var dataList = new List<PIData>();
            foreach (AFValue afValue in afValues)
            {
                if (afValue.IsGood)
                {
                    dataList.Add(new TimeData() { Time = afValue.Timestamp, Value = afValue.Value.ToString() });
                }
            }
            return dataList;
        }

        private static List<PIData> GetPIPointBlobData(IEnumerable<AFValue> afValues)
        {
            var dataList = new List<PIData>();
            foreach (AFValue afValue in afValues)
            {
                if (afValue.IsGood)
                {
                    dataList.Add(new ByteArrayData() { Time = afValue.Timestamp, Value = (byte[])afValue.Value });
                }
            }
            return dataList;
        }
        
        private static string GetContainerId(PIPoint point)
        {
            /*Enforcing the rules for Stream ID
               Is not case sensitive.
               Can contain spaces.
               Cannot start with two underscores (“__”).
               Can contain a maximum of 260 characters.
               Cannot use the following characters: ( / : ? # [ ] @ ! $ & ‘ ( ) \* + , ; = %)
               Cannot start or end with a period.
               Cannot contain consecutive periods.
               Cannot consist of only periods.
             */
            var result = $"PI_{point.Server.Name}_{point}";
            if (result.Length > 260)
            {
                result = result.Substring(0, 260);
            }

            const string forbiddenChars = @"/:?#[]@!$&‘()\*+,;=%";
            if (result.EndsWith(@"."))
            {
                result = result.TrimEnd('.');
            }

            if (result.Contains(".."))
            {
                result = result.Replace("..", "_");
            }

            foreach (var forbiddenChar in forbiddenChars)
            {
                if (result.Contains(forbiddenChar))
                {
                    result = result.Replace(forbiddenChar, '_');
                }
            }

            return result;
        }

        private static OmfTypeCode ToOmfTypeCode(PIPointType pointType)
        {
            switch (pointType)
            {
                case PIPointType.Int16:
                    return OmfTypeCode.Integer;
                case PIPointType.Int32:
                    return OmfTypeCode.Integer;
                case PIPointType.Float16:
                    return OmfTypeCode.Number;
                case PIPointType.Float32:
                    return OmfTypeCode.Number;
                case PIPointType.Float64:
                    return OmfTypeCode.Number;
                case PIPointType.Digital:
                    return OmfTypeCode.String;
                case PIPointType.Timestamp:
                    return OmfTypeCode.Time;
                case PIPointType.String:
                    return OmfTypeCode.String;
                case PIPointType.Blob:
                    return OmfTypeCode.ByteArray;
                default:
                    throw new ArgumentOutOfRangeException();
            }
        }
    }
}
