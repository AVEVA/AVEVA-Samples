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
using System.Collections.Generic;
using System.Linq;
using CommandLine;
using OSIsoft.AF.Asset;
using OSIsoft.AF.Data;
using OSIsoft.AF.PI;
using OSIsoft.Data;
using OSIsoft.Data.Http.Security;
using OSIsoft.AF.Time;
using System.Configuration;
using System.Net;
using System.Threading.Tasks;
using OSIsoft.Data.Http;

namespace PItoOCSviaAPISample
{
    class Program
    {
        private static CommandLineOptions _options; 

        static int Main(string[] args)
        {
            _options = new CommandLineOptions();
            var errors = new List<Error>();
            var result = Parser.Default.ParseArguments<CommandLineOptions>(args);
            result.WithParsed(opts => _options = opts).WithNotParsed(errs => errors = errs.ToList());
            if (errors.Any())
            {
                foreach (var error in errors)
                {
                    Console.WriteLine(error.Tag);
                }

                return 1;
            }
            
            MainAsync().Wait();
            return 0;
        }

        private static async Task MainAsync()
        {
            string accountId = ConfigurationManager.AppSettings["accountId"];
            string namespaceId = ConfigurationManager.AppSettings["namespaceId"];
            string address = ConfigurationManager.AppSettings["address"];
            string resource = ConfigurationManager.AppSettings["resource"];
            string clientId = ConfigurationManager.AppSettings["clientId"];
            string clientSecret = ConfigurationManager.AppSettings["clientSecret"];
            string piServerName = ConfigurationManager.AppSettings["PIDataArchive"];

            var qiService = new QiService(new Uri(address),
                new QiSecurityHandler(resource, accountId, clientId, clientSecret));

            var metadataService = qiService.GetMetadataService(accountId, namespaceId);
            var dataService = qiService.GetDataService(accountId, namespaceId);

            var piServer = new PIServers()[piServerName];
            piServer.Connect();

            PIPointQuery nameFilter = new PIPointQuery
            {
                AttributeName = PICommonPointAttributes.Tag,
                AttributeValue = _options.TagMask,
                Operator = OSIsoft.AF.Search.AFSearchOperator.Equal
            };

            IEnumerable<string> attributesToRetrieve = new[]
            {
                PICommonPointAttributes.Descriptor,
                PICommonPointAttributes.EngineeringUnits,
                PICommonPointAttributes.PointSource
            };

            var piPoints =
                (await PIPoint.FindPIPointsAsync(piServer, new[] {nameFilter}, attributesToRetrieve)).ToList();

            if (!piPoints.Any())
            {
                Console.WriteLine($"No points found matching the tagMask query!");
                return;
            }
            Console.WriteLine($"Found {piPoints.Count} points matching mask: {_options.TagMask}");

            //create types
            await PIQiTypes.CreateOrUpdateTypesInOcsAsync(metadataService);

            //delete existing streams if requested
            if (_options.Mode == CommandLineOptions.DataWriteModes.clearExistingData)
            {
                Parallel.ForEach(piPoints, piPoint => DeleteStreamBasedOnPIPointAsync(piPoint, metadataService).Wait());
            }

            Parallel.ForEach(piPoints, piPoint => CreateStreamBasedOnPIPointAsync(piPoint, attributesToRetrieve, metadataService).Wait());
            Console.WriteLine($"Created or updated {piPoints.Count()} streams.");

            //for each PIPoint, get the data of interest and write it to OCS
            Parallel.ForEach(piPoints, piPoint =>
            {
                //Indices must be unique in OCS so we get rid of duplicate values for a given timestamp
                var timeRange = new AFTimeRange(_options.StartTime, _options.EndTime);
                var afValues = piPoint.RecordedValues(timeRange, AFBoundaryType.Inside, null, true)
                    .GroupBy(value => value.Timestamp)
                    .Select(valuesAtTimestamp => valuesAtTimestamp.Last()) //last event for particular timestamp
                    .Where(val => val.IsGood) //System Digital States (e.g. Shutdown, IO Timeout, etc...) are ignored
                    .ToList();

                WriteDataToOcsAsync(piPoint, afValues, dataService).Wait();
            });
        }

        private static string GetStreamId(PIPoint point)
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
            var result = $"PI_{point.Server.Name}_{point.Name}";
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
        
        private static async Task DeleteStreamBasedOnPIPointAsync(PIPoint piPoint, IQiMetadataService metadata)
        {
            var id = GetStreamId(piPoint);
            try
            {
                await metadata.GetStreamAsync(id);
            }
            catch (QiHttpClientException ex)
            {
                if (ex.StatusCode == HttpStatusCode.NotFound)
                {
                    Console.WriteLine($"Stream to be deleted not found: {id}.");
                    return;
                }

                throw;
            }

            await metadata.DeleteStreamAsync(id);
            Console.WriteLine($"Deleted stream {id}");
        }
        
        private static async Task CreateStreamBasedOnPIPointAsync(PIPoint piPoint,
            IEnumerable<string> pointAttributes, IQiMetadataService metadata)
        {
            var otherAttributes = pointAttributes.Where(s => s != PICommonPointAttributes.Descriptor)
                .ToDictionary(s => s, s => piPoint.GetAttribute(s).ToString());

            var id = GetStreamId(piPoint);
            var dataType = PIQiTypes.GetDataType(piPoint.PointType);

            await metadata.CreateOrUpdateStreamAsync(new QiStream()
            {
                Id = id,
                Name = piPoint.Name,
                TypeId = PIQiTypes.GetQiTypeId(dataType),
                Description = piPoint.GetAttribute(PICommonPointAttributes.Descriptor).ToString()
            });

            //write stream metadata from PIPoint attributes
            await metadata.UpdateStreamMetadataAsync(id, otherAttributes);
        }

        private static async Task WriteDataToOcsAsync(PIPoint piPoint, List<AFValue> afValues, IQiDataService data)
        {
            var streamId = GetStreamId(piPoint);

            switch (PIQiTypes.GetDataType(piPoint.PointType))
            {
                case StreamDataType.Integer:
                    await WriteDataForIntegerStreamAsync(data, afValues, streamId);
                    break;
                case StreamDataType.Float:
                    await WriteDataForFloatStreamAsync(data, afValues, streamId);
                    break;
                case StreamDataType.String:
                    await WriteDataForStringStreamAsync(data, afValues, streamId);
                    break;
                case StreamDataType.Blob:
                    await WriteDataForBlobStreamAsync(data, afValues, streamId);
                    break;
                case StreamDataType.Time:
                    await WriteDataForTimeStreamAsync(data, afValues, streamId);
                    break;
                default:
                    throw new ArgumentOutOfRangeException();
            }

            Console.WriteLine(
                $"Writing data for point: {piPoint.Name} to stream {streamId} ({afValues.Count} values written.)");
        }

        private static async Task WriteDataForIntegerStreamAsync(IQiDataService data, List<AFValue> afValues, string streamId)
        {
            var dataList = new List<PIQiTypes.IntegerData>();
            dataList.AddRange(afValues.Select(val => new PIQiTypes.IntegerData()
            {
                Timestamp = val.Timestamp,
                Value = val.ValueAsInt32()
            }));
            await data.UpdateValuesAsync(streamId, dataList);
        }

        private static async Task WriteDataForFloatStreamAsync(IQiDataService data, List<AFValue> afValues, string streamId)
        {
            var dataList = afValues.Select(val => new PIQiTypes.DoubleData()
            {
                Timestamp = val.Timestamp,
                Value = val.ValueAsDouble()
            }).ToList();
            await data.UpdateValuesAsync(streamId, dataList);
        }

        private static async Task WriteDataForStringStreamAsync(IQiDataService data, List<AFValue> afValues, string streamId)
        {
            var dataList = afValues.Select(val => new PIQiTypes.StringData()
            {
                Timestamp = val.Timestamp,
                Value = val.Value.ToString()
            }).ToList();
            await data.UpdateValuesAsync(streamId, dataList);
        }

        private static async Task WriteDataForBlobStreamAsync(IQiDataService data, List<AFValue> afValues, string streamId)
        {
            var dataList = afValues.Select(val => new PIQiTypes.BlobData()
            {
                Timestamp = val.Timestamp,
                Value = (byte[]) val.Value
            }).ToList();
            await data.UpdateValuesAsync(streamId, dataList);
        }

        private static async Task WriteDataForTimeStreamAsync(IQiDataService data, List<AFValue> afValues, string streamId)
        {
            var dataList = afValues.Select(val => new PIQiTypes.TimeData()
            {
                Timestamp = val.Timestamp,
                Value = (DateTime) val.Value
            }).ToList();
            await data.UpdateValuesAsync(streamId, dataList);
        }
    }
}


