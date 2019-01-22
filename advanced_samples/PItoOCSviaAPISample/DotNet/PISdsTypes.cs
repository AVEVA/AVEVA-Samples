// <copyright file="PISdsTypes.cs" company="OSIsoft, LLC">
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
using System.Threading.Tasks;
using OSIsoft.AF.PI;
using OSIsoft.Data;
using OSIsoft.Data.Reflection;

namespace PItoOCSviaAPISample
{
    enum StreamDataType
    {
        Integer,
        Float,
        String,
        Blob,
        Time
    }

    /// <summary>
    /// This is a static class that encapsulates the definition and creation of Sds Stream Types
    /// that represent data from the various available PI Point types. The numerical types are
    /// reduced to integer (int64) and double (float64) in order to avoid having to distinguish
    /// between the storage sizes. 
    /// </summary>
    static class PISdsTypes
    {
        static PISdsTypes()
        {
            DoubleSdsType = SdsTypeBuilder.CreateSdsType<DoubleData>();
            DoubleSdsType.Id = "PIDoubleValueAndTimestamp";
            DoubleSdsType.Name = "PIDoubleValueAndTimestamp";
            DoubleSdsType.Description = "Represents simple time series data with a floating point value";

            IntegerSdsType = SdsTypeBuilder.CreateSdsType<IntegerData>();
            IntegerSdsType.Id = "PIIntegerValueAndTimestamp";
            IntegerSdsType.Name = "PIIntegerValueAndTimestamp";
            IntegerSdsType.Description = "Represents simple time series data with an integer value";

            StringSdsType = SdsTypeBuilder.CreateSdsType<StringData>();
            StringSdsType.Id = "PIStringValueAndTimestamp";
            StringSdsType.Name = "PIStringValueAndTimestamp";
            StringSdsType.Description = "Represents simple time series data with a string value";

            BlobSdsType = SdsTypeBuilder.CreateSdsType<BlobData>();
            BlobSdsType.Id = "PIBlobValueAndTimestamp";
            BlobSdsType.Name = "PIBlobValueAndTimestamp";
            BlobSdsType.Description = "Represents simple time series data with a blob(byte array) value";

            TimestampSdsType = SdsTypeBuilder.CreateSdsType<TimeData>();
            TimestampSdsType.Id = "PITimestampValueAndTimestamp";
            TimestampSdsType.Name = "PITimestampValueAndTimestamp";
            TimestampSdsType.Description = "Represents simple time series data with a Timestamp(DateTime) value";
        }

        public static SdsType DoubleSdsType { get; }
        public static SdsType IntegerSdsType { get; }
        public static SdsType StringSdsType { get; }
        public static SdsType BlobSdsType { get; }
        public static SdsType TimestampSdsType { get; }

        public class DoubleData
        {
            [SdsMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public double Value { get; set; }
        }

        public class IntegerData
        {
            [SdsMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public Int64 Value { get; set; }
        }

        public class StringData
        {
            [SdsMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public string Value { get; set; }
        }

        public class BlobData
        {
            [SdsMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public byte[] Value { get; set; }
        }

        public class TimeData
        {
            [SdsMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public DateTime Value { get; set; }
        }

        public static Task CreateOrUpdateTypesInOcsAsync(ISdsMetadataService metadataService)
        {
            var taskList = new Task[]
            {
                metadataService.CreateOrUpdateTypeAsync(DoubleSdsType),
                metadataService.CreateOrUpdateTypeAsync(IntegerSdsType),
                metadataService.CreateOrUpdateTypeAsync(StringSdsType),
                metadataService.CreateOrUpdateTypeAsync(BlobSdsType),
                metadataService.CreateOrUpdateTypeAsync(TimestampSdsType)
            };
            return Task.WhenAll(taskList);
        }

        public static string GetSdsTypeId(StreamDataType desiredType)
        {
            switch (desiredType)
            {
                case StreamDataType.Integer:
                    return IntegerSdsType.Id;
                case StreamDataType.Float:
                    return DoubleSdsType.Id;
                case StreamDataType.String:
                    return StringSdsType.Id;
                case StreamDataType.Blob:
                    return BlobSdsType.Id;
                case StreamDataType.Time:
                    return TimestampSdsType.Id;
                default:
                    throw new ArgumentOutOfRangeException(nameof(desiredType), desiredType, null);
            }
        }

        public static string GetSdsTypeId(PIPointType pointType)
        {
            return GetSdsTypeId(GetDataType(pointType));
        }

        public static StreamDataType GetDataType(PIPointType pointType)
        {
            switch (pointType)
            {
                case PIPointType.Int16:
                    return StreamDataType.Integer;
                case PIPointType.Int32:
                    return StreamDataType.Integer;
                case PIPointType.Float16:
                    return StreamDataType.Float;
                case PIPointType.Float32:
                    return StreamDataType.Float;
                case PIPointType.Float64:
                    return StreamDataType.Float;
                case PIPointType.Digital:
                    return StreamDataType.String;
                case PIPointType.Timestamp:
                    return StreamDataType.Time;
                case PIPointType.String:
                    return StreamDataType.String;
                case PIPointType.Blob:
                    return StreamDataType.Blob;
                default:
                    throw new ArgumentOutOfRangeException();
            }
        }
    }
}
