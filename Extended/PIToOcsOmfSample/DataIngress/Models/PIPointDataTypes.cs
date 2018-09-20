using System;

namespace PIToOcsOmfSample.DataIngress
{
    /// <summary>
    /// All data events retrieved from PI points will be indexed on time. All data events retrieved 
    /// from PI points will also have some description of data quality, represented here by the IsGood 
    /// flag.
    /// </summary>
    public abstract class PIData
    {
        public DateTime Time { get; set; }
    }

    public class NumberData : PIData
    {
        public double Value { get; set; }
    }

    public class IntegerData : PIData
    {
        public Int64 Value { get; set; }
    }

    public class StringData : PIData
    {
        public string Value { get; set; }
    }

    public class TimeData : PIData
    {
        public string Value { get; set; }
    }

    public class ByteArrayData : PIData
    {
        public byte[] Value { get; set; }
    }
}
