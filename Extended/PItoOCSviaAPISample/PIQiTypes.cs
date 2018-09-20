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
    /// This is a static class that encapsulates the definition and creation of Qi Stream Types
    /// that represent data from the various available PI Point types. The numerical types are
    /// reduced to integer (int64) and double (float64) in order to avoid having to distinguish
    /// between the storage sizes. 
    /// </summary>
    static class PIQiTypes
    {
        static PIQiTypes()
        {
            DoubleQiType = QiTypeBuilder.CreateQiType<DoubleData>();
            DoubleQiType.Id = "PIDoubleValueAndTimestamp";
            DoubleQiType.Name = "PIDoubleValueAndTimestamp";
            DoubleQiType.Description = "Represents simple time series data with a floating point value";

            IntegerQiType = QiTypeBuilder.CreateQiType<IntegerData>();
            IntegerQiType.Id = "PIIntegerValueAndTimestamp";
            IntegerQiType.Name = "PIIntegerValueAndTimestamp";
            IntegerQiType.Description = "Represents simple time series data with an integer value";

            StringQiType = QiTypeBuilder.CreateQiType<StringData>();
            StringQiType.Id = "PIStringValueAndTimestamp";
            StringQiType.Name = "PIStringValueAndTimestamp";
            StringQiType.Description = "Represents simple time series data with a string value";

            BlobQiType = QiTypeBuilder.CreateQiType<BlobData>();
            BlobQiType.Id = "PIBlobValueAndTimestamp";
            BlobQiType.Name = "PIBlobValueAndTimestamp";
            BlobQiType.Description = "Represents simple time series data with a blob(byte array) value";

            TimestampQiType = QiTypeBuilder.CreateQiType<TimeData>();
            TimestampQiType.Id = "PITimestampValueAndTimestamp";
            TimestampQiType.Name = "PITimestampValueAndTimestamp";
            TimestampQiType.Description = "Represents simple time series data with a Timestamp(DateTime) value";
        }

        public static QiType DoubleQiType { get; }
        public static QiType IntegerQiType { get; }
        public static QiType StringQiType { get; }
        public static QiType BlobQiType { get; }
        public static QiType TimestampQiType { get; }

        public class DoubleData
        {
            [QiMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public double Value { get; set; }
        }

        public class IntegerData
        {
            [QiMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public Int64 Value { get; set; }
        }

        public class StringData
        {
            [QiMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public string Value { get; set; }
        }

        public class BlobData
        {
            [QiMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public byte[] Value { get; set; }
        }

        public class TimeData
        {
            [QiMember(IsKey = true, Order = 0)]
            public DateTime Timestamp { get; set; }
            public DateTime Value { get; set; }
        }

        public static Task CreateOrUpdateTypesInOcsAsync(IQiMetadataService metadataService)
        {
            var taskList = new Task[]
            {
                metadataService.CreateOrUpdateTypeAsync(DoubleQiType),
                metadataService.CreateOrUpdateTypeAsync(IntegerQiType),
                metadataService.CreateOrUpdateTypeAsync(StringQiType),
                metadataService.CreateOrUpdateTypeAsync(BlobQiType),
                metadataService.CreateOrUpdateTypeAsync(TimestampQiType)
            };
            return Task.WhenAll(taskList);
        }

        public static string GetQiTypeId(StreamDataType desiredType)
        {
            switch (desiredType)
            {
                case StreamDataType.Integer:
                    return IntegerQiType.Id;
                case StreamDataType.Float:
                    return DoubleQiType.Id;
                case StreamDataType.String:
                    return StringQiType.Id;
                case StreamDataType.Blob:
                    return BlobQiType.Id;
                case StreamDataType.Time:
                    return TimestampQiType.Id;
                default:
                    throw new ArgumentOutOfRangeException(nameof(desiredType), desiredType, null);
            }
        }

        public static string GetQiTypeId(PIPointType pointType)
        {
            return GetQiTypeId(GetDataType(pointType));
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
