using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace QiLibsSample
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
        [Key]
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
