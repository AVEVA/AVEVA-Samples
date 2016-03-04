using System;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace QiClientLibsSample
{
    public class WaveData
    {
        public WaveData()
        {
        }

        // The use of the KeyAttribute specifies that this data member is to be treated
        // as the key for data within streams that use this type
        [Key]
        public int Order
        {
            get;
            set;
        }

        public double Tau
        {
            get;
            set;
        }

        public double Radians
        {
            get;
            set;
        }

        public double Sin
        {
            get;
            set;
        }

        public double Cos
        {
            get;
            set;
        }

        public double Tan
        {
            get;
            set;
        }

        public double Sinh
        {
            get;
            set;
        }

        public double Cosh
        {
            get;
            set;
        }

        public double Tanh
        {
            get;
            set;
        }

        public static WaveData Next(TimeSpan interval, double multiplier, int order)
        {
            DateTime now = DateTime.UtcNow;
            TimeSpan timeOfDay = now.TimeOfDay;

            double radians = ((timeOfDay.TotalMilliseconds % interval.TotalMilliseconds) / interval.TotalMilliseconds) * 2 * Math.PI;

            return new WaveData()
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians),
            };
        }

        public override string ToString()
        {
            StringBuilder builder = new StringBuilder();
            builder.AppendLine(string.Format("Order = {0}", Order));
            builder.AppendLine(string.Format("Radians = {0}", Radians));
            builder.AppendLine(string.Format("Tau     = {0}", Tau));
            builder.AppendLine(string.Format("Sine    = {0}", Sin));
            builder.AppendLine(string.Format("Cosine  = {0}", Cos));
            builder.AppendLine(string.Format("Tangent = {0}", Tan));
            builder.AppendLine(string.Format("Sinh    = {0}", Sinh));
            builder.AppendLine(string.Format("Cosh    = {0}", Cosh));
            builder.AppendLine(string.Format("Tanh    = {0}", Tanh));
            return builder.ToString();
        }
    }
}
