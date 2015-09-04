using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public class SimpleEvent
    {
        public double Value
        {
            get;
            set;
        }
        public string Units
        {
            get;
            set;
        }

        public DateTime Timestamp
        {
            get;
            set;
        }

        public SimpleEvent()
        {

        }

        public SimpleEvent(double value, string units)
        {
            Value = value;
            Units = units;
            Timestamp = DateTime.UtcNow;
        }
    }
}
