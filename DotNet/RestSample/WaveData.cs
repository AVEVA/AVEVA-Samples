using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public class WaveData
    {
        public WaveData()
        {
        }

        public static WaveData Next(TimeSpan interval, double multiplier, int order)
        {
            DateTime now = DateTime.UtcNow;
            TimeSpan timeOfDay = now.TimeOfDay;

            double radians = ((timeOfDay.TotalSeconds % interval.TotalSeconds) / interval.TotalSeconds) * 2 * Math.PI;

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

        public override string ToString()
        {
            StringBuilder builder = new StringBuilder();
            builder.AppendLine(String.Format("Order = {0}", Order));
            builder.AppendLine(String.Format("Radians = {0}", Radians));
            builder.AppendLine(String.Format("Tau     = {0}", Tau));
            builder.AppendLine(String.Format("Sine    = {0}", Sin));
            builder.AppendLine(String.Format("Cosine  = {0}", Cos));
            builder.AppendLine(String.Format("Tangent = {0}", Tan));
            builder.AppendLine(String.Format("Sinh    = {0}", Sinh));
            builder.AppendLine(String.Format("Cosh    = {0}", Cosh));
            builder.AppendLine(String.Format("Tanh    = {0}", Tanh));
            return builder.ToString();
        }

    }
}
